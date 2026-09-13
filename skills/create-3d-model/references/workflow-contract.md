# Shared workflow contract

Establish only the fields needed for this task and reuse prior decisions. This document owns source precedence, coordinates, target budgets, and completion policy for the internal modules.

## Intent, ownership, and coordinates

Follow the user's requested output and constraints within host and tool permissions. A requested repair authorizes relevant local corrections and verification, not unrelated scene deletion, software setup, skill changes, or publication.

Record units, origin, axes, relevant objects, output paths, and important limits. Existing scene conventions win unless a conversion is required. New front-locked reconstruction may use X/Z for the front image and Y for depth; this is a convention, not a requirement for all models. Geometry, cameras, UV projection, and comparison tools must consume the same convention.

Treat supplied assets and existing objects as user-owned. Model edits do not make the whole scene disposable.

## Reference contract

Classify images and inspect their content. Record source roles, expected structural parts, important landmarks, supported views, and acceptance tolerances for exact matching. Separate reference planes and optional decoration from structural geometry.

User instructions and an agreed canonical policy determine reference precedence. A front view may be canonical for a logo when that matches the requested brand read; do not silently apply that choice to engineering drawings or contradictory views. Reuse an existing choice. Resolve material conflicts using measured evidence; continue independent analysis while a decision is pending.

Exact reconstruction consumes measured contours, scale, and landmarks. A plausible inferred back surface or a shallow visual skin is not evidence of a solved multi-view volume. Label unsupported depth and hidden-surface assumptions.

## Targets and example settings

Use the requested runtime, manufacturing use, file format, and size/quality budget. A recipe's 15 MB file budget, 1024px texture, camera lens, light energy, or triangle count is only an example for its stated target. Do not decimate geometry, reduce textures, remove animation, or change shading merely to fit a previous project's defaults.

Keep render effects separate from export claims. Check actual exporter and runtime support, baking or adapting unsupported effects when required. Procedural shaders, custom Python handlers, and arbitrary material keyframes need target verification.

## Verification and completion

Choose checks from the changed behavior. Geometry changes need affected dimensions, topology and view checks; texture changes need UV/material and relevant surface coverage; animation changes need sampled playback and export checks. Inspect every newly affected view or stage; reuse unchanged evidence when its dependencies remain valid.

Check exported files themselves when practical. Report structural and visual validation separately. If a required check cannot run, continue independent work and deliver the authorized draft with its precise limitation; do not claim the requested quality bar passed.

An internal quality gate calls for local correction, not repeated user approval. Pause for an unresolved material decision, unavailable authority or capability, or an explicit user review boundary. Routine artifact repair does not require editing, installing, versioning, or publishing skills.
