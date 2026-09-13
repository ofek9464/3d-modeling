# Blender rendering

Determine whether the user needs a preview, final still, frame sequence or encoded animation. Inspect the active camera, output scope and existing render configuration. Preserve unrelated scene and preference settings.

Choose engine, samples, resolution, denoising and color management for the quality and time budget. Use a cheap proof render for iterative appearance changes and increase quality when the result needs it. Do not rerender unrelated frames or unchanged views without a reason.

Read [render recipes](recipes.md) for the selected output mode and [render reference](references/overview.md) for advanced passes or performance. Verify Blender-version-specific properties before using a preset. GPU preference setup is a separate environment change.

Save to durable absolute paths. Inspect actual saved images for appearance claims. For animation, prefer recoverable frame output and inspect representative frames with animation-quality-gate.

Completion means the requested output exists, its visual evidence has been inspected, and any render or playback limitation is reported.
