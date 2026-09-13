# Blender UV and texturing

Choose unwrap, projection, atlas mapping, or baking from the changed surface and target. Inspect existing UVs and material nodes before editing. Use the agreed coordinate and source contract.

Keep image meaning and color space consistent with the map. Viewport UV display alone does not prove rendered or exported texture output. Check stretching and seams with a suitable checker or overlay.

Use [atlas fitting](../atlas-uv-fitting/guide.md) only for per-part atlas regions; it owns semantic part-to-region mapping. Use [surface coverage](../closed-surface-uv-coverage/guide.md) when closed or extruded assets expose front, back and side surfaces. Intentionally plain surfaces may satisfy the brief.

Read [UV recipes](recipes.md) for projection, region mapping and bake targets, or [UV reference](references/overview.md) for deeper detail. Verify exported material and texture behavior for the requested runtime.

Completion means the affected surfaces map as intended and applicable render, coverage and export checks pass.
