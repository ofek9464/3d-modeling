---
name: create-2color-3d-models
description: Create printable two-color geometry from images, with aligned color bodies and validated dimensions.
---

# Create 2-Color 3D Models

## Core Rule

Do not jump straight from image to mesh. First define the manufacturable design: physical size, thickness, color split, raised/recessed areas, minimum feature width, output format, and printer/slicer assumptions. If any are unknown, make conservative defaults and state them.

## Workflow

1. Inspect the image and identify usable geometry:
   - Separate foreground, background, text, borders, cutouts, holes, and fine details.
   - Decide which details should become physical geometry and which should be simplified.
   - For bookmarks, preserve a strong outer silhouette and avoid fragile islands.

2. Choose the two-color strategy:
   - **Layer-swap style**: color B is raised above color A; export one model or two aligned models.
   - **Side-by-side/inlay style**: colors occupy adjacent regions at the same height; export separate aligned color bodies.
   - **Engraved/fill style**: color B fills recessed pockets in color A; maintain clearance and avoid loose slivers.
   - Prefer separate aligned bodies or a 3MF with per-object/material assignment when the printer has two heads.

3. For a bookmark request only, use these starting dimensions unless the user provides specs. For signs, tags, charms or other objects, choose dimensions and features for that object:
   - Size: about 35-50 mm wide, 120-180 mm tall.
   - Base thickness: 0.8-1.2 mm.
   - Raised detail: 0.4-0.8 mm above base.
   - Minimum line/feature width: at least 0.8 mm for a 0.4 mm nozzle; use 1.0-1.2 mm for reliability.
   - Corner radius: 1-3 mm unless a sharp outline is required.
   - Add a 3-5 mm tassel hole only when appropriate.

4. Build clean 2D vector regions before 3D extrusion:
   - Use tracing/vectorization for silhouettes and logos.
   - Clean speckles, micro-contours, tiny holes, self-intersections, and overlapping paths.
   - Simplify paths while preserving recognizable shapes.
   - Ensure every color region is closed and manifold before extrusion.

5. Convert to 3D:
   - Extrude base and detail regions as separate solids.
   - Keep all color bodies registered to the same origin and coordinate system.
   - Add small bevels/fillets only if they will not erase fine details.
   - Avoid unsupported floating pieces. Connect islands with bridges, frames, or convert them to engraved details.

6. Export slicer-ready output:
   - Prefer `3MF` for dual-color workflows when material/tool assignment can be preserved.
   - Otherwise export two aligned STL files named by color/tool, such as `bookmark_base_color1.stl` and `bookmark_detail_color2.stl`.
   - Also export a preview image or screenshot when possible so the user can inspect the result before printing.

7. Validate before finishing:
   - Check scale, thickness, minimum feature width, manifold geometry, nonzero volume, and aligned origins.
   - Confirm no color body is hidden inside another unless it is intentionally embedded/inlaid.
   - Confirm the model lies flat on the build plate and has no tiny loose fragments.

For a bookmark's modeling heuristics and failure checks, read [the bookmark workflow](references/two-color-bookmark-workflow.md). Other object types use their own geometry and print constraints.

## Tool Guidance

Use the tools already available in the environment. Reasonable options include:

- Inkscape, potrace, or image-processing libraries for vector tracing.
- Blender Python, OpenSCAD, CadQuery, Trimesh, or similar geometry tools for modeling.
- Mesh repair/check tools such as Blender, MeshLab, PrusaSlicer/Bambu Studio repair, Trimesh, or manifold checks.

Prefer reproducible scripts when creating geometry so dimensions and color splits can be adjusted after preview.

## Communication

When delivering results, include:

- Assumed dimensions and printer/nozzle constraints.
- Which regions belong to color/tool 1 and color/tool 2.
- Output files and how they should be imported into the slicer.
- Any compromises made to keep the bookmark printable.
