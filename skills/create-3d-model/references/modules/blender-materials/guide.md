# Blender materials

Inspect the target objects, existing material nodes and output contract. Change only the requested surfaces. Choose physical or stylized parameters for the actual material, preserving supplied texture meaning and color spaces.

For portable assets, prefer exporter-supported inputs and verify the exported appearance. For render-only work, surface, emission and volume shaders may differ. Do not promise the same effect in GLB without target verification; bake or adapt unsupported effects when needed.

Read [material recipes](recipes.md) for the selected substance or node pattern and [material reference](references/overview.md) for advanced parameters and baking. Treat exact parameter values and Blender API examples as version- and scene-dependent. For atlas or UV changes, use the relevant UV guide rather than reading all texturing modules.

Inspect the result under suitable lighting; distinguish a lighting mismatch from a material defect. Completion means the requested appearance is checked and export limitations are visible.
