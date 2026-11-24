#!/usr/bin/env python3
"""Compare Codex first attempts with and without one Goat Skill."""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parent
SKILLS = ROOT.parent / "skills"


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


def check_ui(workspace):
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


def check_cli(workspace):
    (workspace / "example.json").write_text('[{}, {}, {}]', encoding="utf-8")
    (workspace / "invalid.json").write_text('not JSON', encoding="utf-8")
    good = run_python(workspace, "report.py", "example.json")
    if good.returncode or good.stderr or json.loads(good.stdout) != {"count": 3}:
        return False
    for name in ("missing.json", "invalid.json"):
        bad = run_python(workspace, "report.py", name)
        if bad.returncode != 2 or bad.stdout or not bad.stderr.strip():
            return False
    return True


def check_retry(workspace):
    result = run_python(workspace, "-c", """
import runpy
import sqlite3
from contextlib import closing

delivery = runpy.run_path("delivery.py")
with closing(sqlite3.connect("inventory.db")) as db:
    delivery["initialize"](db)
    delivery["apply_delivery"](db, "a", 4)
    assert db.execute("SELECT quantity FROM inventory").fetchone() == (4,)
with closing(sqlite3.connect("inventory.db")) as db:
    delivery["apply_delivery"](db, "a", 9)
    assert db.execute("SELECT quantity FROM inventory").fetchone() == (4,)
    delivery["apply_delivery"](db, "b", 3)
    assert db.execute("SELECT quantity FROM inventory").fetchone() == (7,)
    assert db.execute("SELECT message_id FROM receipts ORDER BY message_id").fetchall() == [("a",), ("b",)]
""")
    return result.returncode == 0


@dataclass(frozen=True)
class Case:
    file: str
    skill: str
    request: str
    check: Callable[[Path], bool]


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


def prepare(case, workspace):
    shutil.copyfile(ROOT / "fixtures" / case.file, workspace / case.file)
    subprocess.run(["git", "init", "--quiet"], cwd=workspace, check=True)


def score(case, workspace):
    try:
        return case.check(workspace)
    except (OSError, ValueError, subprocess.TimeoutExpired):
        return False


def attempt(label, case, model):
    with tempfile.TemporaryDirectory(prefix="goat-eval-") as directory:
        workspace = Path(directory)
        prepare(case, workspace)
        prompt = case.request
        if label == "skill":
            shutil.copytree(SKILLS / case.skill, workspace / ".agents" / "skills" / case.skill)
            prompt = f"${case.skill}\n\n{prompt}"

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
        events = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
        completed = [event for event in events if event.get("type") == "turn.completed"]
        if result.returncode or not completed:
            errors = [
                event.get("message") or event.get("error", {}).get("message")
                for event in events if event.get("type") in ("error", "turn.failed")
            ]
            message = next((error for error in reversed(errors) if error), "no completed Codex turn")
            raise RuntimeError(message)
        return {
            "passed": score(case, workspace),
            "usage": completed[-1].get("usage", {}),
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Use the same Codex model for both runs.")
    parser.add_argument("--case", choices=CASES, help="Run a single pair.")
    args = parser.parse_args()

    names = (args.case,) if args.case else tuple(CASES)
    for name in names:
        case = CASES[name]
        with tempfile.TemporaryDirectory(prefix="goat-fixture-") as directory:
            workspace = Path(directory)
            prepare(case, workspace)
            if score(case, workspace):
                raise SystemExit(f"{name} fixture already passes before agent changes")

    for index, name in enumerate(names):
        case = CASES[name]
        order = ("control", "skill") if index % 2 == 0 else ("skill", "control")
        for label in order:
            try:
                result = attempt(label, case, args.model)
            except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
                raise SystemExit(f"{name}/{label}: {exc}") from exc
            print(json.dumps({"case": name, "run": label, "model": args.model, **result}), flush=True)


if __name__ == "__main__":
    main()
