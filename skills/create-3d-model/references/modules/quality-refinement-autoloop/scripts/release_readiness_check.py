#!/usr/bin/env python3
"""Check the reference bundle without requiring a separately installed connector."""
import argparse
import importlib.util
import json
from pathlib import Path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--expected-version")
    ap.add_argument("--out")
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    if (root / "skills/create-3d-model").is_dir():
        root = root / "skills/create-3d-model"
    checker = root / "references/modules/blender-skill-harmonizer/scripts/skill_graph_audit.py"
    if not checker.is_file():
        raise SystemExit(f"Bundle auditor not found: {checker}")
    spec = importlib.util.spec_from_file_location("bundle_auditor", checker)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    audit = module.audit_bundle(root)
    checks = [{"name": "bundle_structure", "ok": audit["passed"], "detail": audit.get("errors", [])}]
    if args.expected_version is not None:
        checks.append({"name": "version", "ok": audit.get("version") == args.expected_version,
                       "detail": audit.get("version")})
    for required in ["SKILL.md", "module-index.json", "LICENSE", "UPSTREAM_LICENSE",
                     "agents/openai.yaml", "references/upstream.md", "references/capability-map.md"]:
        checks.append({"name": required, "ok": (root / required).is_file()})
    report = {"schema": "blender_skill_release_readiness.v3", "checks": checks,
              "passed": all(c["ok"] for c in checks)}
    text = json.dumps(report, indent=2)
    if args.out:
        out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True); out.write_text(text, encoding="utf-8")
    print(text)
    raise SystemExit(0 if report["passed"] else 2)

if __name__ == "__main__":
    main()
