"""Verify that the packaging command accepts the package and rejects known failures."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        workspace = self.enterContext(tempfile.TemporaryDirectory())
        self.repo = Path(workspace) / "repo"
        shutil.copytree(ROOT, self.repo, ignore=shutil.ignore_patterns(".git", ".venv", "__pycache__"))

    def validate(self):
        return subprocess.run(
            [sys.executable, "scripts/validate.py"], cwd=self.repo, capture_output=True, text=True,
        )

    def assert_rejected(self, error):
        result = self.validate()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(error, result.stderr)

    def test_accepts_current_package(self):
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_rejects_malformed_skill_frontmatter(self):
        entry = self.repo / "skills/frontend/SKILL.md"
        entry.write_text('---\nname: frontend\ndescription: Design interfaces: UI and APIs\n---\nBuild UI.\n')
        self.assert_rejected("skills/frontend/SKILL.md: invalid YAML frontmatter")

    def test_rejects_schema_invalid_manifest(self):
        path = self.repo / "plugin.json"
        manifest = json.loads(path.read_text())
        manifest["keywords"] = ["engineering", 42]
        path.write_text(json.dumps(manifest))
        self.assert_rejected("plugin.json: manifest schema violation at $.keywords[1]")

    def test_rejects_missing_skill(self):
        shutil.rmtree(self.repo / "skills/backend")
        self.assert_rejected("missing: backend")


if __name__ == "__main__":
    unittest.main()
