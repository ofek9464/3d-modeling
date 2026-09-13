---
name: create-3d-model
description: Create, edit, validate, and export Blender 3D assets from text, references, or existing scenes.
---

# Create 3D model

Deliver the requested 3D asset or scene edit using Blender. Reuse settled dimensions, source priorities, output targets, and quality requirements. Infer reversible defaults; ask only when a missing choice changes the result.

Before the first Blender call, read [integration guidance](references/codex-integration.md) for tool discovery, scene ownership, and safe execution. Read the [workflow contract](references/workflow-contract.md) when establishing source priority, coordinates, output requirements, or verification. Reuse both once established.

Choose the smallest relevant route:
- **Existing scene edit:** use the affected domain module from the [capability map](references/capability-map.md).
- **New scene or multi-stage asset:** [production planning](references/modules/blender-pro-workflow/guide.md), then needed modeling, material, camera, light, and output modules.
- **Drawing or exact reference reconstruction:** [reference routing](references/modules/reference-to-3d/guide.md). Use [wireframe extraction](references/modules/wireframe-to-3d/guide.md) for line art and [mascot reconstruction](references/modules/mascot-logo-reconstruction/guide.md) for exact designed symbols.
- **Animation:** [animation](references/modules/blender-animation/guide.md), then [animation validation](references/modules/animation-quality-gate/guide.md). Load texture-state or HUD guidance only when those effects are requested.
- **Rejected or failing output:** [artifact repair](references/modules/quality-refinement-autoloop/guide.md); skill maintenance is separate work.
- **Export or format conversion:** [export](references/modules/blender-export/guide.md) for target settings and round-trip checks.

The 29 modules are internal reference documents, not independently installed skills. Read each selected guide before its recipes or helpers. The capability map lists all modules and their purpose.

Inspect supplied images and the existing scene. Work from primary form to necessary detail, preserving unrelated data and a recoverable baseline. Run focused structural checks and inspect visual evidence when appearance changes; use [visual validation](references/visual-validation.md) for those checks. Correct observed problems within the authorized scope.

Deliver the requested format; if none is named, provide a portable GLB and a versioned Blender source. Explicit render-only, animation-only, printing, or existing-project requests determine their own output contract. Verify saved files and relevant target behavior, then link the artifacts with concise evidence and any unverified limitations. Finish when the requested output and applicable checks are complete, rather than pausing at each internal phase.
