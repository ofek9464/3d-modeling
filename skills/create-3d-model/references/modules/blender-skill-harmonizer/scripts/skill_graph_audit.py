#!/usr/bin/env python3
"""Validate portable reference bundles and legacy manifest paths."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote

def audit_bundle(root: Path) -> dict:
    root = root.resolve()
    errors = []
    index_path = root / "module-index.json"
    modern = index_path.is_file()
    if not modern:
        index_path = root / "manifest.json"
    try:
        index = json.loads(index_path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        return {"schema": "blender_skill_graph_audit.v2", "passed": False,
                "errors": [f"Cannot read bundle index: {exc}"], "modules": []}
    if not isinstance(index, dict):
        return {"schema": "blender_skill_graph_audit.v2", "passed": False,
                "errors": ["Bundle index must be an object."], "modules": []}
    entries = index.get("modules" if modern else "skills", [])
    if not isinstance(entries, list) or not entries:
        errors.append("Index must list at least one module.")
        entries = []
    names, paths, modules = set(), set(), []
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("name"), str) or not isinstance(entry.get("path"), str):
            errors.append("Each module needs a string name and path.")
            continue
        name, relative = entry["name"], entry["path"]
        path = (root / relative).resolve()
        if name in names or relative in paths:
            errors.append(f"Duplicate module name or path: {name}")
        names.add(name); paths.add(relative)
        contained = path.is_relative_to(root)
        exists = contained and path.is_file()
        if not contained:
            errors.append(f"Module escapes bundle root: {relative}")
        elif not exists:
            errors.append(f"Missing module: {relative}")
        elif modern and path.name != "guide.md":
            errors.append(f"Internal module must be guide.md: {relative}")
        modules.append({"name": name, "path": relative, "exists": exists})
    if modern:
        actual = {p.relative_to(root).as_posix() for p in (root / "references/modules").glob("*/guide.md")}
        if actual != paths:
            errors.append(f"Guide/index mismatch: {sorted(actual.symmetric_difference(paths))}")
        entrypoints = sorted(p.relative_to(root).as_posix() for p in root.rglob("SKILL.md"))
        if entrypoints != ["SKILL.md"]:
            errors.append(f"Expected one root SKILL.md; found {entrypoints}")
        if index.get("entrypoint", "SKILL.md") != "SKILL.md":
            errors.append("Index entrypoint must be SKILL.md.")
        root_skill = root / "SKILL.md"
        if root_skill.is_file():
            text = root_skill.read_text(encoding="utf-8-sig")
            if not re.match(r"---\s*\nname: .+\ndescription: .+\n---", text):
                errors.append("Root SKILL.md requires name and description frontmatter.")
        for doc in root.rglob("*.md"):
            text = doc.read_text(encoding="utf-8-sig")
            text = re.sub(r"```.*?```", "", text, flags=re.S)
            for target in re.findall(r"\]\(([^)]+)\)", text):
                target = target.strip().split(' "', 1)[0].strip("<>")
                if not target or target.startswith(("#", "http:", "https:", "mailto:", "data:")):
                    continue
                path_text = unquote(target.split("#", 1)[0])
                if path_text and not (doc.parent / path_text).exists():
                    errors.append(f"Broken link: {doc.relative_to(root)} -> {target}")
    return {"schema": "blender_skill_graph_audit.v2", "version": index.get("version"),
            "modules": modules, "errors": errors, "passed": not errors}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plugin-root", default=".")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    report = audit_bundle(Path(args.plugin_root))
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"modules": len(report["modules"]), "errors": report["errors"], "passed": report["passed"]}, indent=2))
    raise SystemExit(0 if report["passed"] else 2)

if __name__ == "__main__":
    main()
