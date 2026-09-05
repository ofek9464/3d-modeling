# Codex integration

## Contents

1. Runtime layout
2. Blender tool discovery
3. Module loading
4. Scene-safety overrides
5. Image handling
6. Deliverable contract
7. Artifact handoff
8. Helper scripts
9. MCP operation

## Runtime layout

Codex discovers this directory as one Agent Skill:

```text
skills/create-3d-model/
├── SKILL.md
├── agents/openai.yaml
└── references/
    ├── core/
    └── modules/<29 routed modules>/
```

The original upstream plugin registered every module as a separate Claude Code skill. This adaptation registers only `create-3d-model`; the other modules are reference documents loaded on demand. This keeps automatic discovery concise while retaining the upstream recipes, decision trees, domain references, and helper scripts.

## Blender tool discovery

Codex MCP tool namespaces can vary by host and version. Discover these capabilities semantically:

| Capability | Common semantic suffix |
| --- | --- |
| Inspect scene | `get_scene_info` |
| Inspect object | `get_object_info` |
| Capture viewport | `get_viewport_screenshot` |
| Execute reviewed `bpy` | `execute_blender_code` |

Do not fail solely because the server prefix differs. Do not claim modeling completed when these capabilities are absent.

BlenderMCP connects to the Blender add-on on `127.0.0.1:9876`. Blender must be open, the add-on must be enabled, and its connection must be started before the first tool call.

External asset tools can appear in upstream recipes. Treat them as unavailable by default. Use one only after the user explicitly authorizes the network service, license implications, data transmission, and possible cost.

## Module loading

When a module says to load or chain-load another skill, read:

```text
references/modules/<name>/SKILL.md
```

Resolve a module-relative path such as `references/overview.md` or `scripts/template_analyzer.py` from that module's directory. Use an absolute path derived from the installed `create-3d-model` skill when executing a helper; do not rely on Claude-specific environment variables.

Vendored module frontmatter can still list `Read`, `Bash`, `Glob`, `Grep`, or fixed Blender tool names. It is retained as source provenance inside a reference document, not as Codex runtime metadata or permission. Use the tools actually available in the current Codex task.

## Scene-safety overrides

These rules override looser upstream examples:

- Do not reset the world for every task. Reset only for a fresh or skill-owned scene, or after the user authorizes replacement.
- Do not treat a default-named cube as disposable. Delete startup content only after verifying an unchanged startup scene and a request to start fresh.
- Do not clear all objects, materials, actions, images, collections, or worlds as a convenient baseline.
- Do not overwrite the open `.blend`; save a versioned checkpoint and result.
- Do not replay a failed monolithic script. Retry the smallest failed stage.
- Do not let a routed module modify this skill, documentation, version files, Git state, or remotes unless the user explicitly requests skill development or publishing.

## Image handling

Inspect every user-supplied image before modeling. If an image is available as a local file, use Codex's local image-viewing capability instead of inferring its contents from a filename. For Blender viewport screenshots returned directly by MCP, inspect the image content rather than treating tool success as visual validation.

For durable renders:

- write to an absolute path under the active workspace or another approved directory;
- avoid `/tmp`, `/var/folders`, `file://` URLs, and transient BlenderMCP screenshot locations;
- verify existence, non-zero size, expected dimensions, and format;
- inspect the saved image through Codex before accepting it;
- embed a useful final preview with an absolute Markdown image target when the Codex client supports local rendering.

For animation, inspect representative frames or create a contact sheet with `animation-quality-gate/scripts/animation_contact_sheet.py`.

## Deliverable contract

Model creation is the normal product; Blender is the production backend.

- If the user names a target format or runtime, deliver that as the primary artifact.
- If no target is named, export a `.glb` as the portable primary model and save a versioned `.blend` as the editable engineering source.
- For 3D printing, prefer the requested printable format, usually STL. For engine and DCC pipelines, follow the relevant FBX, glTF/GLB, OBJ, or USD contract.
- Do not substitute a render, screenshot, or `.blend` file for an explicitly requested portable model.
- Validate the export itself. When practical, re-import it into a clean collection or inspect it with a target-compatible viewer and check geometry, materials, textures, axes, scale, and animation.
- For render-only, animation-only, or existing `.blend` editing tasks, the user's explicit output request overrides the default model-plus-source pair.

## Artifact handoff

After verifying all exports, end the completed response with one artifact per line. Use descriptive labels and absolute local Markdown targets so Codex clients can present quick-open file references:

```markdown
## Artifacts

- Primary model: [model.glb](/absolute/workspace/path/model.glb)
- Blender source: [model_v001.blend](/absolute/workspace/path/model_v001.blend)
- Output directory: [model-output](/absolute/workspace/path/model-output/)

![Validated model preview](/absolute/workspace/path/model_preview.png)
```

Requirements:

- use literal absolute filesystem targets, not `file://` URLs or link-only basenames;
- order the primary portable model first and the editable `.blend` source second;
- list each artifact once;
- link only files that exist, are non-empty, and passed applicable validation;
- keep durable artifacts under the active workspace or another user-approved location;
- use the requested 3D format, with `.glb`, `.gltf`, `.fbx`, `.obj`, `.usd`, `.usdz`, `.stl`, `.ply`, `.dae`, `.3mf`, and `.blend` all supported by the workflow.

Local directory links depend on the Codex client. Include the durable parent directory when useful, but always provide direct file links as the reliable handoff.

## Helper scripts

Twenty-six upstream Python helpers are retained beside their modules. They cover contour extraction, atlas detection, segmentation, reference manifests, overlays, view registration, fit reports, landmark checks, look calibration, texture transitions, contact sheets, and repair planning.

They require subsets of:

```text
opencv-python>=4.8
numpy>=1.24
scipy>=1.10
Pillow>=10
```

Prefer an existing project environment. Otherwise use ephemeral `uv run --with ...` dependencies rather than changing the user's global Python. Inspect a script and its CLI before execution. Keep generated reports and masks with the task artifacts.

`quality-refinement-autoloop` contains release-oriented helpers. They are retained for upstream capability parity but are not part of ordinary Blender artifact work.

## MCP operation

Register `ahujasid/blender-mcp` with Codex using the repository's installation instructions. Keep the Blender host on `127.0.0.1`, disable telemetry when required, and restart Codex after changing MCP registration so new tasks receive the tool inventory.
