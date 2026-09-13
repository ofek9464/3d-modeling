# Wireframe extraction and model completion

Use line drawings as measured input. Inspect the images, establish scale and the shared coordinate convention, and separate structural outlines from guides, labels and decoration.

The bundled wireframe_analyzer.py extracts contours and curve control points. The curve recipes create an outline foundation. They do not by themselves solve filled surfaces, hidden depth, or a rigid model consistent across views.

Read [wireframe recipes](recipes.md) for analyzer options and curve construction. Use [algorithms](references/algorithms.md) when extraction needs tuning, [geometry patterns](references/blender-patterns.md) for lofted or revolved surfaces, and [troubleshooting](references/best-practices.md) for build or topology failures.

For a complete model, add the required geometry through blender-modeling or contour-to-mesh. Multiple views require registration and applicable fit checks. With one view, state depth assumptions; do not claim unseen geometry is measured.

Choose output format, texture size, rigs and file budgets from the requested target. Eyewear presets and lightweight-web examples apply only to those tasks. Verify the completed geometry and export, not just successful tracing.

Completion means the requested outline or completed model is delivered at its actual supported fidelity.
