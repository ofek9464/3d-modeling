# Modeling skills

[`create-3d-model`](create-3d-model/SKILL.md) is the maintained Blender skill bundle. It exposes one SKILL.md entrypoint and keeps 29 internal guide.md modules, optional recipe references, and helper scripts. The file inventory and provenance are recorded in [snapshot.json](snapshot.json).

Source: [CheshireJCat/create-3d-model-skill](https://github.com/CheshireJCat/create-3d-model-skill), adapted from [RobLe3/cc-blender-skill](https://github.com/RobLe3/cc-blender-skill).

The modules used for these projects include reference analysis, contour modeling, mesh modeling, workflow coordination, rendering, and export. The PEQ color partitioning and manifold checks also use repository Python scripts; the skill alone does not validate printer settings or rail fit.

## Install for Codex

Copy the entire `create-3d-model` directory into your personal Codex skills directory, normally `~/.codex/skills/`. Preserve its `references` directory. If you already have a copy, compare or back it up before replacing it. Start a fresh session after installation so the host rebuilds its skill catalog. Only create-3d-model should be discovered; guide.md files are internal references.

Use `$create-3d-model` for modeling requests. Its interactive Blender workflow also needs [BlenderMCP](../mcp/). The repository's build and rendering scripts can run directly through Python and Blender's command line.

These are community instructions and examples. Read the relevant module before running its helpers. Some recipes target particular Blender versions; the model scripts here were exercised with Blender 5.2.1 LTS.

For Codex or Claude, a directory link to this repository's create-3d-model folder keeps the installed skill current. Remove or archive an old copy only after comparing it and preserving local changes. Agent Kit does not install this bundle.
