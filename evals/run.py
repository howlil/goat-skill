#!/usr/bin/env python3
"""Compare Codex first attempts with and without Goat Skill."""

import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Callable

from product_cases import CASES as PRODUCT_CASES, ProductCase, Turn, observe, snapshot, verdict


ROOT = Path(__file__).resolve().parent
SKILLS = ROOT.parent / "skills"
PRODUCT_BASELINE = "a3a3166b0e0cc3adfbdd4fbeb96248c98194d389"
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


def check_popup(workspace, _response):
    try:
        from popup_menu import check_popup_menu
    except ModuleNotFoundError as exc:
        if exc.name != "playwright":
            raise
        raise RuntimeError("Install Playwright with python3 -m pip install playwright.") from exc
    return check_popup_menu(workspace)


@dataclass(frozen=True)
class Case:
    file: str
    skill: str | None
    request: str
    check: Callable[[Path, str], bool | dict[str, bool]]


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
    "product": ProductCase(
        {"reports.json": (ROOT / "fixtures/reports.json").read_text(encoding="utf-8")},
        (Turn("Delete old saved reports from reports.json to free up space.",
              "Ground the affected reports and missing cutoff or scope. Ask the controlling choice and withhold the deletion handoff."),),
        routing=True,
    ),
}

POPUP_CASE = Case(
    "action-menu.html", "frontend",
    "Build the Report actions popup in action-menu.html using the existing trigger, Details button, "
    "and status region. Keep the implementation in this file. The menus start closed.\n"
    "- Use accessible menu and menuitem semantics. Name the main menu Report actions and the submenu Export. "
    "Expose the expanded state of each trigger. In order, the main actions are Rename, Export, and Archive. "
    "Export contains CSV and JSON in that order.\n"
    "- Move DOM focus to the active item. Open the main menu by click or Enter and focus Rename. Up and Down wrap within the open menu. "
    "Open Export with ArrowRight or click and focus CSV. ArrowLeft or Escape closes the submenu and "
    "returns focus to Export. Escape closes the main menu and returns focus to Report actions.\n"
    "- Archive stays keyboard-focusable with aria-disabled and shows 'Archiving is unavailable for this report.' "
    "Keep the menu open and the status and focus unchanged when Archive receives Enter or Space.\n"
    "- Activating Rename, CSV, or JSON closes both menus and returns focus to Report actions. "
    "Show respectively 'Rename selected.', 'Exported CSV.', or 'Exported JSON.' in the existing status region. "
    "These actions only update the status.\n"
    "- Clicking Details from an open submenu closes both menus and leaves focus on Details. "
    "Keep both open popups within the viewport at 320px width.",
    check_popup,
)


def prepare(case, workspace):
    shutil.copyfile(ROOT / "fixtures" / case.file, workspace / case.file)
    subprocess.run(["git", "init", "--quiet"], cwd=workspace, check=True)


def score(case, workspace, response=""):
    try:
        result = case.check(workspace, response)
    except (OSError, ValueError, subprocess.TimeoutExpired):
        result = False
    if isinstance(result, dict):
        return {"passed": all(result.values()), "checks": result}
    return {"passed": result}


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

        result = codex_turn(workspace, model, prompt)
        response = result.pop("response")
        result.pop("thread")
        return {**score(case, workspace, response), **result}


def codex_turn(workspace, model, prompt, *, multi_turn=False, thread=None, effort=None):
    command = [
        "codex", "-a", "never", "exec", "--ignore-user-config", "--ignore-rules",
        "--json", "--sandbox", "workspace-write", "-c", 'shell_environment_policy.inherit="core"',
        "--model", model,
    ]
    if effort:
        command += ["-c", f'model_reasoning_effort="{effort}"']
    if not multi_turn:
        command.append("--ephemeral")
    if thread:
        command += ["resume", "--json", "--model", model, thread]

    started = time.perf_counter()
    result = subprocess.run(
        [*command, "--", "-"], cwd=workspace, input=prompt,
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=150,
    )
    events = [json.loads(line) for line in result.stdout.splitlines() if line.startswith("{")]
    completed = [event for event in events if event.get("type") == "turn.completed"]
    if result.returncode or not completed:
        errors = [
            event.get("message") or event.get("error", {}).get("message")
            for event in events if event.get("type") in ("error", "turn.failed")
        ]
        stderr = result.stderr.strip().splitlines()
        fallback = stderr[-1] if result.returncode and stderr else "no completed Codex turn"
        raise RuntimeError(next((error for error in reversed(errors) if error), fallback))
    items = [event["item"] for event in events if event.get("type") == "item.completed"]
    messages = [item["text"] for item in items if item["type"] == "agent_message"]
    skill_files = {
        path
        for item in items
        if item["type"] == "command_execution" and item.get("exit_code") == 0
        for path in SKILL_PATH.findall(item["command"].replace("\\", "/"))
    }
    return {
        "response": messages[-1] if messages else "",
        "thread": next((event["thread_id"] for event in events if event.get("type") == "thread.started"), thread),
        "usage": completed[-1].get("usage", {}),
        "elapsed_seconds": round(time.perf_counter() - started, 3),
        "skill_files_in_commands": sorted(skill_files),
    }


def install_product(workspace, label, routing):
    destination = workspace / ".agents/skills"
    if routing:
        for skill in ("frontend", "backend"):
            shutil.copytree(SKILLS / skill, destination / skill)
    if label == "skill":
        shutil.copytree(SKILLS / "product", destination / "product")
    if label == "baseline":
        data = subprocess.check_output(["git", "archive", PRODUCT_BASELINE, "skills/product"], cwd=ROOT.parent)
        with tarfile.open(fileobj=io.BytesIO(data)) as archive:
            for member in archive:
                if member.isfile():
                    path = destination / Path(member.name).relative_to("skills")
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(archive.extractfile(member).read())


def product_attempt(label, case, model):
    with tempfile.TemporaryDirectory(prefix="goat-product-eval-") as directory:
        workspace = Path(directory)
        for name, content in case.files.items():
            path = workspace / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content.encode("utf-8"))
        subprocess.run(["git", "init", "--quiet"], cwd=workspace, check=True)
        install_product(workspace, label, case.routing)
        activation = "automatic selection" if case.routing else (
            "explicit $product" if label != "control" else "no Product skill"
        )
        evidence = {
            "turns": [], "activation_method": activation, "effort": "low",
            "commit": PRODUCT_BASELINE if label == "baseline" else (
                subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
                if label == "skill" else None
            ),
            "candidate_source": "working tree" if label == "skill" else None,
            "reference_evidence": "successful command paths are a proxy",
        }
        thread = None
        for index, turn in enumerate(case.turns):
            prompt = turn.prompt
            if index == 0 and activation == "explicit $product":
                prompt = "$product\n\n" + prompt
            before = snapshot(workspace)
            try:
                observed = codex_turn(workspace, model, prompt, multi_turn=len(case.turns) > 1,
                                      thread=thread, effort="low")
            except (OSError, RuntimeError, subprocess.TimeoutExpired) as exc:
                return {**evidence, "status": "not verified", "error": str(exc)}
            thread = observed.pop("thread")
            response = observed.pop("response")
            grade = observe(workspace, before, snapshot(workspace), turn, response)
            evidence["turns"].append({**observed, **grade, "status": verdict(grade)})
            if grade["hard_failures"]:
                return {**evidence, "status": "fail"}
            if index + 1 < len(case.turns) and not thread:
                return {**evidence, "status": "not verified", "error": "Codex provided no resumable thread ID"}
        return {**evidence, "status": "ungraded"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="Use the same Codex model for both runs.")
    selection = parser.add_mutually_exclusive_group()
    available = CASES | ROUTING_CASES | PRODUCT_CASES | {"popup": POPUP_CASE}
    selection.add_argument("--case", choices=available, help="Run a single case across its configurations.")
    selection.add_argument("--routing", action="store_true", help="Run the automatic selection cases.")
    parser.add_argument("--runs", type=int, default=1, help="Trials per configuration.")
    args = parser.parse_args()
    if args.runs < 1:
        parser.error("--runs must be at least 1")

    cases = ROUTING_CASES if args.routing else CASES
    if args.case:
        cases = {args.case: available[args.case]}
    for name, case in cases.items():
        if isinstance(case, ProductCase):
            continue
        with tempfile.TemporaryDirectory(prefix="goat-fixture-") as directory:
            workspace = Path(directory)
            prepare(case, workspace)
            try:
                baseline = score(case, workspace)
            except RuntimeError as exc:
                raise SystemExit(f"{name}: {exc}") from exc
            if baseline["passed"]:
                raise SystemExit(f"{name} fixture already passes before agent changes")

    host = subprocess.check_output(["codex", "--version"], text=True).strip()
    for trial in range(1, args.runs + 1):
        for index, (name, case) in enumerate(cases.items()):
            product = isinstance(case, ProductCase)
            arms = ("control", "baseline", "skill") if product else ("control", "skill")
            offset = (index + trial - 1) % len(arms)
            for label in arms[offset:] + arms[:offset]:
                try:
                    result = (product_attempt if product else attempt)(label, case, args.model)
                except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
                    raise SystemExit(f"{name}/{label}: {exc}") from exc
                print(json.dumps({"case": name, "run": label, "trial": trial,
                                  "host_version": host, "model": args.model, **result}), flush=True)
                if result.get("status") == "not verified":
                    raise SystemExit(f"{name}/{label}: {result['error']}")


if __name__ == "__main__":
    main()
