#!/usr/bin/env python3
"""Dependency-free structural checks for goat-skill (not a full host validator)."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFESTS = [
    "plugin.json",
    ".claude-plugin/plugin.json",
    ".antigravity-plugin/plugin.json",
]
NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
CODEX_CATEGORIES = {
    "Productivity",
    "Creativity",
    "Developer Tools",
    "Business & Operations",
    "Data & Analytics",
    "Communication",
    "Education & Research",
    "Security",
    "Finance",
    "Healthcare",
    "Travel",
    "Entertainment",
    "Other",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(relative: str) -> dict:
    try:
        data = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{relative}: {exc}")
    if not isinstance(data, dict):
        fail(f"{relative}: expected JSON object")
    return data


def check_skill(skill_dir: Path) -> None:
    entry = skill_dir / "SKILL.md"
    if not entry.is_file():
        fail(f"{skill_dir.relative_to(ROOT)}: missing SKILL.md")
    source = entry.read_text(encoding="utf-8").replace("\r\n", "\n")
    frontmatter = re.match(r"\A---\n(.*?)\n---\n", source, re.DOTALL)
    if not frontmatter:
        fail(f"{entry.relative_to(ROOT)}: missing YAML frontmatter")
    lines = frontmatter.group(1).splitlines()
    fields = {}
    for line in lines:
        if line and not line[0].isspace() and ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip("'\"")
    name = fields.get("name", "")
    if name != skill_dir.name or not NAME_RE.fullmatch(name) or len(name) > 64:
        fail(f"{entry.relative_to(ROOT)}: name must match its valid folder name")
    description = fields.get("description", "")
    if description in (">", ">-", "|", "|-", ">+", "|+"):
        description = " ".join(
            line.strip()
            for line in lines
            if line.startswith((" ", "\t")) and line.strip()
        )
    if not description or len(description) > 1024:
        fail(f"{entry.relative_to(ROOT)}: description must be 1–1024 characters")
    if not source[frontmatter.end():].strip():
        fail(f"{entry.relative_to(ROOT)}: instructions must not be empty")
    for relative in set(re.findall(r"references/[a-zA-Z0-9_.-]+\.md", source)):
        if not (skill_dir / relative).is_file():
            fail(f"{entry.relative_to(ROOT)}: missing referenced file {relative}")


def main() -> None:
    manifest_data = [load_json(path) for path in MANIFESTS]
    names = {item.get("name") for item in manifest_data}
    versions = {item.get("version") for item in manifest_data}
    if names != {"gs"} or len(versions) != 1 or not all(
        isinstance(v, str) and v for v in versions
    ):
        fail("plugin manifests have mismatched name or version")

    claude = load_json(".claude-plugin/marketplace.json")
    if not any(
        entry.get("name") == "gs"
        and entry.get("source") == {"source": "github", "repo": "howlil/goat-skill"}
        for entry in claude.get("plugins", [])
    ):
        fail("Claude marketplace source is missing or inconsistent")

    codex = load_json(".agents/plugins/marketplace.json")
    codex_entries = [
        entry
        for entry in codex.get("plugins", [])
        if entry.get("name") == "gs"
        and entry.get("source") == {"source": "local", "path": "./"}
    ]
    if len(codex_entries) != 1:
        fail("Codex local marketplace source is missing or inconsistent")
    codex_entry = codex_entries[0]
    if codex_entry.get("policy") != {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    }:
        fail("Codex marketplace policy is missing or inconsistent")
    if codex_entry.get("category") not in CODEX_CATEGORIES:
        fail("Codex marketplace category is missing or unsupported")

    skills = ROOT / "skills"
    if not skills.is_dir():
        fail("skills/ directory missing")
    entries = sorted(path for path in skills.iterdir() if path.is_dir())
    for item in entries:
        check_skill(item)
    if not entries:
        print("OK: scaffold manifests consistent; no skills authored yet")
    else:
        print(f"OK: manifests consistent; {len(entries)} basic skill layouts valid")
    print("Note: native host validation and behavior tests are separate.")


if __name__ == "__main__":
    main()
