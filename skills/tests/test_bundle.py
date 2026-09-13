"""Behavioral regression checks for reference bundle packaging and repair planning."""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest

BUNDLE = Path(__file__).resolve().parents[1] / "create-3d-model"
AUDITOR = BUNDLE / "references/modules/blender-skill-harmonizer/scripts/skill_graph_audit.py"
PLANNER = BUNDLE / "references/modules/quality-refinement-autoloop/scripts/ralph_autoloop_plan.py"

class BundleTests(unittest.TestCase):
    def test_repair_does_not_require_skill_maintenance(self):
        p = subprocess.run([sys.executable, str(PLANNER), "--feedback", "The texture is stretched"],
                           capture_output=True, text=True, check=True)
        plan = json.loads(p.stdout)
        self.assertIn("uv_texture", plan["failure_dimensions"])
        self.assertIn("repair_product", plan["phases"])
        self.assertFalse(any("patch_skill" in x or "validate_skill" in x for x in plan["phases"]))

    def test_release_readiness_checks_requested_version(self):
        checker = BUNDLE / "references/modules/quality-refinement-autoloop/scripts/release_readiness_check.py"
        for version, expected in [("1.1.0", 0), ("missing-version", 2)]:
            with self.subTest(version=version):
                p = subprocess.run([sys.executable, "-B", str(checker), "--repo-root", str(BUNDLE),
                                    "--expected-version", version], capture_output=True, text=True)
                self.assertEqual(expected, p.returncode, p.stdout + p.stderr)
                self.assertEqual(expected == 0, json.loads(p.stdout)["passed"])

    def test_reference_bundle_and_broken_packages(self):
        spec = importlib.util.spec_from_file_location("bundle_auditor", AUDITOR)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertTrue(module.audit_bundle(BUNDLE)["passed"])
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "SKILL.md").write_text("---\nname: sample\ndescription: Sample\n---\n", encoding="utf-8")
            (root / "module-index.json").write_text(json.dumps({
                "version": "1", "modules": [{"name": "a", "path": "references/modules/a/guide.md"}]
            }), encoding="utf-8")
            self.assertFalse(module.audit_bundle(root)["passed"], "Missing guides must fail")
            guide = root / "references/modules/a/guide.md"
            guide.parent.mkdir(parents=True)
            guide.write_text("# A\n", encoding="utf-8")
            self.assertTrue(module.audit_bundle(root)["passed"])
            (guide.parent / "SKILL.md").write_text("# Accidental entrypoint\n", encoding="utf-8")
            self.assertFalse(module.audit_bundle(root)["passed"], "Nested entrypoints must fail")
            (guide.parent / "SKILL.md").unlink()
            guide.write_text("# A\n[missing](missing.md)\n", encoding="utf-8")
            self.assertFalse(module.audit_bundle(root)["passed"], "Broken relative links must fail")
            guide.write_text("# A\n", encoding="utf-8")
            (root / "module-index.json").write_text(json.dumps({
                "version": "1", "modules": [{"name": "escape", "path": "../outside.md"}]
            }), encoding="utf-8")
            self.assertFalse(module.audit_bundle(root)["passed"], "Outside-root module paths must fail")
            (root / "module-index.json").write_text("[]", encoding="utf-8")
            self.assertFalse(module.audit_bundle(root)["passed"], "Non-object index must fail")

if __name__ == "__main__":
    unittest.main()
