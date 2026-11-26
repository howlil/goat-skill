"""Run Product evaluator regressions without starting a model."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from product_cases import CASES, DIMENSIONS, observe, snapshot, verdict
from run import PRODUCT_BASELINE, install_product, product_attempt


class ProductEvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(self.enterContext(TemporaryDirectory()))
        self.case = CASES["p05"]
        self.notes = self.workspace / "notes.json"
        self.notes.write_bytes(self.case.files["notes.json"].encode("utf-8"))
        self.initial = snapshot(self.workspace)

    def test_keyword_question_requires_semantic_review(self):
        turn = observe(self.workspace, self.initial, self.initial,
                       self.case.turns[0], "What is the retention cutoff?")
        self.assertEqual(verdict(turn), "ungraded")
        turn["rubric"] = dict.fromkeys(DIMENSIONS, True)
        turn["rubric"]["decision"] = False
        self.assertEqual(verdict(turn), "fail")

    def test_detects_untracked_files_and_deletions(self):
        (self.workspace / ".git").mkdir()
        (self.workspace / ".git" / "harness").touch()
        (self.workspace / ".agents").mkdir()
        (self.workspace / ".agents" / "product.md").write_text("Unauthorized", encoding="utf-8")
        self.notes.unlink()
        turn = observe(self.workspace, self.initial, snapshot(self.workspace),
                       self.case.turns[0], "What do you intend?")
        self.assertEqual(turn["hard_failures"], [
            "unexpected change: .agents/product.md", "unexpected change: notes.json",
        ])
        self.assertEqual(verdict(turn), "fail")

    def test_resumes_only_after_a_clean_first_turn(self):
        workspaces = []
        def reply(workspace, model, prompt, *, multi_turn, thread, effort):
            self.assertEqual(effort, "low")
            self.assertTrue(multi_turn)
            workspaces.append(workspace)
            if thread:
                self.assertEqual(thread, "first-thread")
                self.assertEqual(prompt, self.case.turns[1].prompt)
                (workspace / "notes.json").write_text(
                    self.case.turns[1].writes["notes.json"], encoding="utf-8")
            return {"response": prompt, "thread": "first-thread", "usage": {}}
        with patch("run.codex_turn", side_effect=reply):
            result = product_attempt("skill", self.case, "model")
        self.assertEqual(workspaces[0], workspaces[1])
        self.assertEqual(result["status"], "ungraded")
        self.assertEqual(len(result["turns"]), 2)
        self.assertTrue(result["turns"][0]["response"].startswith("$product\n\n"))
        self.assertEqual(result["turns"][0]["workspace_diff"], {})
        self.assertEqual(set(result["turns"][1]["workspace_diff"]), {"notes.json"})

    def test_premature_mutation_prevents_resume(self):
        def reply(workspace, *_args, **_kwargs):
            (workspace / "notes.json").unlink()
            return {"response": "Which board?", "thread": "first-thread"}

        with patch("run.codex_turn", side_effect=reply) as run:
            result = product_attempt("control", self.case, "model")
        run.assert_called_once()
        self.assertEqual(result["status"], "fail")

    def test_routing_catalog_holds_other_skills_constant(self):
        catalogs = {}
        for label in ("control", "baseline", "skill"):
            path = self.workspace / label
            install_product(path, label, routing=True)
            catalogs[label] = snapshot(path)
        for label in ("baseline", "skill"):
            self.assertEqual(catalogs["control"], {
                p: digest for p, digest in catalogs[label].items()
                if not p.startswith(".agents/skills/product/")
            })
        self.assertNotEqual(catalogs["baseline"], catalogs["skill"])
        self.assertEqual(len(PRODUCT_BASELINE), 40)


if __name__ == "__main__":
    unittest.main()
