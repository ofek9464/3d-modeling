# Blender integration

Read before the first Blender call; reuse this guidance for the task. Source, target, and completion decisions belong to the [shared contract](workflow-contract.md).

## Tools and execution

Discover available tools by capability: scene inspection, object inspection, viewport screenshot, and reviewed Python execution. Typical suffixes are get_scene_info, get_object_info, get_viewport_screenshot, and execute_blender_code; namespaces vary.

Inspect the scene and relevant objects before writing. If BlenderMCP is absent or unreachable, report the missing connection and continue independent preparation. The usual add-on listener is localhost:9876. Do not expose it beyond localhost.

Treat code-execution calls as fresh Python namespaces. Re-import modules, retrieve persistent bpy data by stable names, and use purposeful retryable chunks. Inspect state after a timeout before retrying. Prefer the data API or bmesh; operators need explicit selection, active object, mode, and context.

## Scene and environment ownership

Preserve unrelated objects, materials, collections, worlds, actions, cameras, preferences, and files. Use a task-owned collection. Clear startup objects only after a request for a fresh scene and evidence that they are unchanged startup data. Save a versioned checkpoint before broad or destructive edits; do not overwrite the original source without authorization.

Run examples only after selecting the actual objects, units, version, and paths. Read helper source or --help before execution. Prefer an existing dependency environment or an ephemeral one; setup and package installation remain subject to host permissions. Use network assets or generation services only when requested and authorized; never infer permission to upload user assets or incur charges.

## Module and artifact layout

Only the root SKILL.md is an entrypoint. Internal guides live at references/modules/<name>/guide.md, with optional recipes.md, references/, and scripts/ alongside. They have no runtime skill frontmatter. Resolve relative paths from the current document or script directory. module-index.json is the complete inventory used by validation helpers.

Write outputs to absolute paths under the active workspace or another authorized durable directory. Replace legacy /tmp example paths. Keep checkpoints and final files distinct. Verify non-empty files and inspect actual images for visual claims.

Link the requested primary artifact first, the editable source when part of the contract, and useful previews. Use descriptive labels with absolute filesystem targets, one link per artifact. Read [visual validation](visual-validation.md) when appearance changes.

The inspection and execution rules apply to referenced examples as well as newly generated code. Ordinary modeling does not authorize changes to this skill bundle, project instruction files, Git state, or remote services.
