#!/usr/bin/env python3
"""Compare Codex first attempts with and without Goat Skill."""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parent
SKILLS = ROOT.parent / "skills"
SKILL_PATH = re.compile(r"skills/((?:product|frontend|backend)/(?:SKILL\.md|references/[\w.-]+\.md))")


class EmailForm(HTMLParser):
    def __init__(self):
        super().__init__()
        self.field = {}
        self.label = None
        self.labels = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "label":
            self.label = {"attrs": attrs, "text": "", "wraps_email": False}
        if tag == "input" and attrs.get("name") == "email":
            self.field = attrs
            if self.label is not None and "for" not in self.label["attrs"]:
                self.label["wraps_email"] = True

    def handle_data(self, data):
        if self.label is not None:
            self.label["text"] += data

    def handle_endtag(self, tag):
        if tag == "label" and self.label is not None:
            self.labels.append(self.label)
            self.label = None


def check_ui(workspace, _response):
    form = EmailForm()
    form.feed((workspace / "settings.html").read_text(encoding="utf-8"))
    if form.field.get("type") != "email" or "required" not in form.field:
        return False
    return any(
        " ".join(label["text"].split()).casefold() == "email address"
        and "hidden" not in label["attrs"]
        and label["attrs"].get("aria-hidden") != "true"
        and (
            label["wraps_email"]
            or (form.field.get("id") and label["attrs"].get("for") == form.field["id"])
        )
        for label in form.labels
    )


def run_python(workspace, *args):
    return subprocess.run(
        [sys.executable, "-I", *args], cwd=workspace, text=True, capture_output=True,
        env={"PATH": os.defpath}, stdin=subprocess.DEVNULL, timeout=15,
    )


def check_cli(workspace, _response):
    with tempfile.TemporaryDirectory(prefix="goat-cli-inputs-") as directory:
        inputs = Path(directory)
        (inputs / "example.json").write_text('[{}, {}, {}]', encoding="utf-8")
        (inputs / "invalid.json").write_text('not JSON', encoding="utf-8")
        good = run_python(workspace, "report.py", str(inputs / "example.json"))
        if good.returncode or good.stderr or json.loads(good.stdout) != {"count": 3}:
            return False
        for name in ("missing.json", "invalid.json"):
            bad = run_python(workspace, "report.py", str(inputs / name))
            if bad.returncode != 2 or bad.stdout or not bad.stderr.strip():
                return False
    return True


def check_retry(workspace, _response):
    with tempfile.TemporaryDirectory(prefix="goat-retry-data-") as directory:
        result = run_python(workspace, "-c", """
import runpy
import sqlite3
import sys
from contextlib import closing

delivery = runpy.run_path("delivery.py")
with closing(sqlite3.connect(sys.argv[1])) as db:
    delivery["initialize"](db)
    delivery["apply_delivery"](db, "a", 4)
    assert db.execute("SELECT quantity FROM inventory").fetchone() == (4,)
with closing(sqlite3.connect(sys.argv[1])) as db:
    delivery["apply_delivery"](db, "a", 9)
    assert db.execute("SELECT quantity FROM inventory").fetchone() == (4,)
    delivery["apply_delivery"](db, "b", 3)
    assert db.execute("SELECT quantity FROM inventory").fetchone() == (7,)
    assert db.execute("SELECT message_id FROM receipts ORDER BY message_id").fetchall() == [("a",), ("b",)]
""", str(Path(directory) / "inventory.db"))
    return result.returncode == 0


def check_clear_edit(workspace, _response):
    expected = (ROOT / "fixtures/notice.txt").read_bytes().replace(b"every Tuesday", b"every Thursday")
    return (workspace / "notice.txt").read_bytes() == expected


def check_product(workspace, response):
    if (workspace / "reports.json").read_bytes() != (ROOT / "fixtures/reports.json").read_bytes():
        return False
    return any(
        re.search(r"\?|\b(?:clarify|confirm|specify|tell me)\b", sentence, re.I)
        and re.search(r"\b(?:which reports|old|older|cutoff|retention|retain|keep|date|days|months|years|age)\b", sentence, re.I)
        for sentence in re.split(r"(?<=[.!?])\s+|\n", response)
    )


@dataclass(frozen=True)
class Case:
    file: str
    skill: str | None
    request: str
    check: Callable[[Path, str], bool]


CASES = {
    "ui": Case(
        "settings.html", "frontend",
        "In settings.html, show a visible Email address label associated with the email field. "
        "Keep the field name and its required email validation.",
        check_ui,
    ),
    "cli": Case(
        "report.py", "frontend",
        "Make report.py exit with status 2 and write the diagnostic to stderr for missing files "
        "and malformed JSON. Keep stdout empty on failure and preserve successful JSON output.",
        check_cli,
    ),
    "retry": Case(
        "delivery.py", "backend",
        "Fix apply_delivery so a repeated message ID never increments inventory again, even "
        "after reopening the database. Preserve the function signature and credits for new IDs.",
        check_retry,
    ),
}

ROUTING_CASES = {
    "clear-edit": Case(
        "notice.txt", None,
        "In notice.txt, change 'every Tuesday' to 'every Thursday'. Keep the rest of the file as is.",
        check_clear_edit,
    ),
    "product": Case(
        "reports.json", None,
        "Delete old saved reports from reports.json to free up space.",
        check_product,
    ),
}


def prepare(case, workspace):
    shutil.copyfile(ROOT / "fixtures" / case.file, workspace / case.file)
    subprocess.run(["git", "init", "--quiet"], cwd=workspace, check=True)


def score(case, workspace, response=""):
    try:
        return case.check(workspace, response)
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False


def attempt(label, case, model):
    with tempfile.TemporaryDirectory(prefix="goat-eval-") as directory:
        workspace = Path(directory)
        prepare(case, workspace)
        prompt = case.request
        if label == "skill":
            destination = workspace / ".agents/skills"
            if case.skill is None:
                shutil.copytree(SKILLS, destination)
            else:
                shutil.copytree(SKILLS / case.skill, destination / case.skill)
                prompt = f"${case.skill}\n\n{prompt}"

        started = time.perf_counter()
        result = subprocess.run(
            [
                "codex", "-a", "never", "exec", "--ignore-user-config", "--ignore-rules",
                "--ephemeral", "--json", "--sandbox", "workspace-write",
                "-c", 'shell_environment_policy.inherit="core"',
                "--model", model, "--", prompt,
            ],
            cwd=workspace, stdin=subprocess.DEVNULL, capture_output=True, text=True,
            timeout=150,
        )
        elapsed = time.perf_counter() - started
        events = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
        completed = [event for event in events if event.get("type") == "turn.completed"]
        if result.returncode or not completed:
            errors = [
                event.get("message") or event.get("error", {}).get("message")
                for event in events if event.get("type") in ("error", "turn.failed")
            ]
            message = next((error for error in reversed(errors) if error), "no completed Codex turn")
            raise RuntimeError(message)
        items = [event["item"] for event in events if event.get("type") == "item.completed"]
        messages = [item["text"] for item in items if item["type"] == "agent_message"]
        skill_files = {
            path
            for item in items
            if item["type"] == "command_execution" and item.get("exit_code") == 0
            for path in SKILL_PATH.findall(item["command"])
        }
        return {
            "passed": score(case, workspace, messages[-1] if messages else ""),
            "usage": completed[-1].get("usage", {}),
            "elapsed_seconds": round(elapsed, 3),
            "skill_files_in_commands": sorted(skill_files),
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Use the same Codex model for both runs.")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--case", choices=(*CASES, *ROUTING_CASES), help="Run a single pair.")
    selection.add_argument("--routing", action="store_true", help="Run the automatic selection cases.")
    args = parser.parse_args()

    cases = ROUTING_CASES if args.routing else CASES
    if args.case:
        cases = {args.case: (CASES | ROUTING_CASES)[args.case]}
    for name, case in cases.items():
        with tempfile.TemporaryDirectory(prefix="goat-fixture-") as directory:
            workspace = Path(directory)
            prepare(case, workspace)
            if score(case, workspace):
                raise SystemExit(f"{name} fixture already passes before agent changes")

    for index, (name, case) in enumerate(cases.items()):
        order = ("control", "skill") if index % 2 == 0 else ("skill", "control")
        for label in order:
            try:
                result = attempt(label, case, args.model)
            except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
                raise SystemExit(f"{name}/{label}: {exc}") from exc
            print(json.dumps({"case": name, "run": label, "model": args.model, **result}), flush=True)


if __name__ == "__main__":
    main()
