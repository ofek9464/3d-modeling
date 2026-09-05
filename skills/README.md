# Modeling skills

[`create-3d-model`](create-3d-model/SKILL.md) is a snapshot of the installed community Blender skill, copied on 2026-09-05. It includes the top-level skill, its referenced modules, helper scripts, and both upstream license notices. The snapshot is recorded in [snapshot.json](snapshot.json).

Source: [CheshireJCat/create-3d-model-skill](https://github.com/CheshireJCat/create-3d-model-skill), adapted from [RobLe3/cc-blender-skill](https://github.com/RobLe3/cc-blender-skill).

The modules used for these projects include reference analysis, contour modeling, mesh modeling, workflow coordination, rendering, and export. The PEQ color partitioning and manifold checks also use repository Python scripts; the skill alone does not validate printer settings or rail fit.

## Install for Codex

Copy the entire `create-3d-model` directory into your personal Codex skills directory, normally `~/.codex/skills/`. Preserve its `references` directory. If you already have a copy, compare or back it up before replacing it. Start a new turn or restart Codex if the skill does not appear.

Use `$create-3d-model` for modeling requests. Its interactive Blender workflow also needs [BlenderMCP](../mcp/). The repository's build and rendering scripts can run directly through Python and Blender's command line.

These are community instructions and examples. Read the relevant module before running its helpers. Some recipes target particular Blender versions; the model scripts here were exercised with Blender 5.2.1 LTS.
