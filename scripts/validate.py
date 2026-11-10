#!/usr/bin/env python3
"""Dependency-free structural and packaging checks for goat-skill."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORTABLE_MANIFEST = "plugin.json"
CODEX_COMPAT_MANIFEST = ".codex-plugin/plugin.json"
MANIFESTS = [
    PORTABLE_MANIFEST,
    CODEX_COMPAT_MANIFEST,
    ".claude-plugin/plugin.json",
    ".antigravity-plugin/plugin.json",
]
PLUGIN_NAME = "gs"
PLUGIN_REPOSITORY = "https://github.com/howlil/goat-skill"
PORTABLE_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
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


def require_text(value: object, label: str, max_length=None) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label}: expected non-empty string")
    value = value.strip()
    if max_length is not None and len(value) > max_length:
        fail(f"{label}: must be at most {max_length} characters")
    return value


def check_openai_interface(interface: object, label: str) -> dict:
    if not isinstance(interface, dict):
        fail(f"{label}: expected object")

    require_text(interface.get("displayName"), f"{label}.displayName", 30)
    require_text(interface.get("shortDescription"), f"{label}.shortDescription", 30)
    require_text(interface.get("longDescription"), f"{label}.longDescription", 4000)
    require_text(interface.get("developerName"), f"{label}.developerName", 80)

    category = require_text(interface.get("category"), f"{label}.category")
    if category not in CODEX_CATEGORIES:
        fail(f"{label}.category: unsupported category {category!r}")

    capabilities = interface.get("capabilities")
    if not isinstance(capabilities, list) or not 1 <= len(capabilities) <= 20:
        fail(f"{label}.capabilities: expected 1–20 items")
    for index, item in enumerate(capabilities):
        require_text(item, f"{label}.capabilities[{index}]", 120)

    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        fail(f"{label}.defaultPrompt: expected 1–3 items")
    normalized = set()
    for index, prompt in enumerate(prompts):
        text = require_text(prompt, f"{label}.defaultPrompt[{index}]", 128)
        if "\n" in text or "\r" in text:
            fail(f"{label}.defaultPrompt[{index}]: must be one line")
        key = " ".join(text.split()).casefold()
        if key in normalized:
            fail(f"{label}.defaultPrompt: duplicate prompt")
        normalized.add(key)

    return interface


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
        target = skill_dir / relative
        if not target.is_file():
            fail(f"{entry.relative_to(ROOT)}: missing referenced file {relative}")


def main() -> None:
    manifest_data = {path: load_json(path) for path in MANIFESTS}

    portable = manifest_data[PORTABLE_MANIFEST]
    canonical_name = require_text(portable.get("name"), "plugin.json name", 64)
    if canonical_name != PLUGIN_NAME or not NAME_RE.fullmatch(canonical_name):
        fail(f"plugin.json: expected plugin name {PLUGIN_NAME!r}")
    canonical_version = require_text(portable.get("version"), "plugin.json version", 64)
    canonical_description = require_text(
        portable.get("description"),
        "plugin.json description",
        4000,
    )

    for path, manifest in manifest_data.items():
        if manifest.get("name") != canonical_name:
            fail(f"{path}: name must match plugin.json")
        if manifest.get("version") != canonical_version:
            fail(f"{path}: version must match plugin.json")
        if manifest.get("description") != canonical_description:
            fail(f"{path}: description must match plugin.json")

    if portable.get("$schema") != PORTABLE_SCHEMA:
        fail("plugin.json: portable Agent Plugins schema is missing or inconsistent")
    if portable.get("repository") != PLUGIN_REPOSITORY:
        fail("plugin.json: repository is missing or inconsistent")
    author = portable.get("author")
    if not isinstance(author, dict) or author.get("name") != "howlil":
        fail("plugin.json: author.name is missing or inconsistent")

    extensions = portable.get("extensions")
    if not isinstance(extensions, dict):
        fail("plugin.json: extensions object is missing")
    openai = extensions.get("com.openai")
    if not isinstance(openai, dict):
        fail("plugin.json: extensions.com.openai is missing")
    portable_interface = check_openai_interface(
        openai.get("interface"),
        "plugin.json extensions.com.openai.interface",
    )

    compat = manifest_data[CODEX_COMPAT_MANIFEST]
    if compat.get("skills") != "./skills/":
        fail(f"{CODEX_COMPAT_MANIFEST}: skills must point to ./skills/")
    if compat.get("repository") != portable.get("repository"):
        fail(f"{CODEX_COMPAT_MANIFEST}: repository must match plugin.json")
    if compat.get("author") != portable.get("author"):
        fail(f"{CODEX_COMPAT_MANIFEST}: author must match plugin.json")
    compat_interface = check_openai_interface(
        compat.get("interface"),
        f"{CODEX_COMPAT_MANIFEST} interface",
    )
    if compat_interface != portable_interface:
        fail(f"{CODEX_COMPAT_MANIFEST}: interface must match plugin.json OpenAI metadata")

    claude = load_json(".claude-plugin/marketplace.json")
    if not any(
        entry.get("name") == canonical_name
        and entry.get("source") == {"source": "github", "repo": "howlil/goat-skill"}
        for entry in claude.get("plugins", [])
    ):
        fail("Claude marketplace source is missing or inconsistent")

    codex = load_json(".agents/plugins/marketplace.json")
    codex_entries = [
        entry
        for entry in codex.get("plugins", [])
        if entry.get("name") == canonical_name
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
    if codex_entry.get("category") != portable_interface["category"]:
        fail("Codex marketplace category must match plugin OpenAI metadata")

    marketplace_interface = codex_entry.get("interface")
    if (
        not isinstance(marketplace_interface, dict)
        or marketplace_interface.get("displayName") != portable_interface["displayName"]
    ):
        fail("Codex marketplace displayName must match plugin OpenAI metadata")

    skills = ROOT / "skills"
    if not skills.is_dir():
        fail("skills/ directory missing")

    entries = sorted(path for path in skills.iterdir() if path.is_dir())
    for item in entries:
        check_skill(item)

    if not entries:
        fail("at least one canonical skill is required")

    print(
        "OK: portable + Codex compatibility manifests consistent; "
        f"{len(entries)} skill layout(s) valid"
    )
    print("Note: native host discovery and model-behavior evaluation remain separate.")


if __name__ == "__main__":
    main()
