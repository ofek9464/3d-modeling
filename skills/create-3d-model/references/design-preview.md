# Design discovery and concept preview

Use for a new design or a substantial visual redesign. Establish a selected visual direction before creating or changing geometry. Scene inspection, source analysis, and feasibility checks can proceed while a choice is pending.

## Establish the brief

Reuse the request, supplied sources, and previous decisions. Ask only questions whose answers change the result, grouping related questions in the host's popup input tool when available, with concise choices and free-text input. Follow the shared question preference and host limitations; do not put questions in chat when a suitable popup is available.

Resolve relevant unknowns: intended use, subject, appearance and style, required dimensions and fit, printing versus digital use, material or color strategy, and output format. For functional or printable objects, clarify constraints such as mating dimensions, load, assembly, clearances, and printer limits when they affect the design. Do not ask every category for every task or start a separate interview workflow.

Keep a compact brief with explicit dimensions, immutable source assets, constraints, and assumptions. Do not invent hidden dimensions or engineering specifications to fill an image prompt.

## Generate and select the concept

Use the available image-generation capability and read its applicable skill before generation. In Codex, prefer the installed imagegen skill and its supported default tool. In other hosts, discover an equivalent supported capability; do not assume Codex tool names exist. A model-creation request activates this preview step, subject to host permissions; it does not authorize unrequested paid API fallbacks, external uploads, or setup.

Generate a focused image of the proposed object, with views that expose the design choices that matter. Create alternatives only when they help resolve a real choice or the user requests them. Keep shape and proportions consistent with the brief. Preserve exact logos, lettering, and QR assets as authoritative originals; generated approximations must never replace them in the model.

Inspect the actual image before showing it. Reject impossible assemblies, missing essential parts, or conflicts with the brief. Show the concept inline and identify it as a design illustration, not a render of an existing model or proof of printability. Let the user select it or request a change through the popup tool when supported. Do not treat a preselected option, silence, or elapsed time as selection.

Wait for the visual direction before geometry work unless the user explicitly delegates selection or asks to skip the preview. Reuse a direction already selected in the conversation instead of asking again. After selection, continue through modeling, verification, and export without adding approval gates at internal stages.

## Scope and source precedence

- Exact reconstruction from supplied drawings, photos, logos, or an existing model: inspect those sources first; do not require a synthetic replacement image. Generate a concept only to explore an unresolved design choice or when the user requests it. Keep measured references authoritative.
- Local repairs, material tweaks, format conversion, or export: preserve the accepted design; do not restart discovery or require a new concept.
- Printing and functional geometry: the brief and measured evidence govern size, fit, strength assumptions, and manufacturability. Concept pixels are not measurements or validation results.
- Image generation unavailable: report the missing capability and continue independent analysis and planning. Offer a labeled alternative or ask whether to proceed without the image; do not silently substitute a different preview process or claim generation succeeded.

## Carry the decision into the model

Save the selected concept and brief under the project's design location or a task-owned workspace directory. Link the actual saved image and record the selected revision, important constraints, and any unresolved assumptions. Avoid unrelated documentation or duplicate records.

Build from the selected direction and the shared source contract. Compare actual model views with the concept for visual intent, and separately validate dimensions, topology, export, and applicable manufacturing constraints. Explain necessary departures from the selected design when they materially change the result. Completion remains the requested model and its applicable checks, not merely the concept image.
