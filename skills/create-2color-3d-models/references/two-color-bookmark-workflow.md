# Two-Color Bookmark Workflow

## Decision Checklist

Before modeling, answer these in the working notes:

- What is the target physical size?
- Which color is structural/base and which color is decorative/detail?
- Should the second color be raised, flush/inlaid, recessed, or a separate top layer?
- Is the model intended for two independent extruders/toolheads, a filament swap, or manual color change?
- What is the nozzle size and practical minimum feature width?
- Should text be readable from the top face, and does it need mirroring for the chosen workflow?

If the user only supplies an image, use bookmark defaults from `SKILL.md` and state them.

## Image Preparation

Start from a high-contrast two-tone interpretation of the image. If the source is shaded, photographic, or colorful, posterize it into two printable regions:

- Color 1: base silhouette, border, or background support.
- Color 2: raised/engraved details, lettering, logo, or decorative line art.

Remove details that will not survive printing:

- Speckles smaller than 1.0 mm.
- Gaps narrower than one extrusion line.
- Long isolated strokes thinner than the nozzle can print.
- Floating islands that are not connected to the base or a color body.

For text, prefer bold fonts or stroke expansion. Thin serif details often fail at bookmark scale.

## Geometry Patterns

### Raised Detail

Use for logos, names, line art, and simple silhouettes.

- Base is color 1, typically 0.8-1.2 mm thick.
- Detail is color 2, typically 0.4-0.8 mm taller.
- Detail body sits directly on the base with the same XY outline as the vector region.
- This is usually easiest to print and most reliable for dual-head printers.

### Flush Inlay

Use when the top should feel flat or when color 2 should be embedded.

- Base contains pockets for color 2.
- Color 2 regions have the same top height as the base or slightly proud by 0.05-0.15 mm.
- Add XY clearance only if the slicer/printer workflow requires separate fitted parts. For multi-material single-print bodies, exact shared boundaries are usually preferable.
- Avoid many tiny disconnected inlays.

### Side-By-Side Regions

Use when both colors form large adjacent shapes.

- Bodies share boundaries and heights.
- Add a thin common backing if separate regions would create fragile unconnected pieces.
- Check that each color body is printable as part of the same assembly.

### Engraved Fill

Use for fine line art when raised detail would be too fragile.

- Engrave grooves or pockets into color 1.
- Fill with color 2 as a separate body, or leave recessed if the user wants contrast by shadow.
- Keep groove widths at least 0.8-1.0 mm for common 0.4 mm nozzle setups.

## Bookmark-Specific Constraints

- Keep the bookmark flexible but not floppy: 0.8-1.2 mm base thickness is a good starting range.
- Avoid tall raised details that catch on pages; keep total thickness near 1.4-2.0 mm unless the user wants a decorative plaque.
- Round outside corners to reduce snagging.
- Put fragile decorative details inside a border/frame when possible.
- If adding a tassel hole, keep at least 2.0-3.0 mm of material around it.
- Avoid deep relief on both sides unless the user explicitly wants a double-sided print.

## Export Strategy

Prefer one of these deliverables:

- `3MF`: one build plate with two material/tool bodies, if the software stack supports assigning materials.
- Two aligned STLs: import both together, assign each STL to the proper toolhead/material, and keep their origins locked.
- One preview render: top-down and angled view so the color separation is obvious.

When exporting aligned STLs:

- Use the same origin for both files.
- Do not auto-center one file independently after export.
- Include color/tool names in filenames.
- Mention that the slicer should load them as a single multi-part object if it supports that operation.

## Validation Checks

Run or reason through these checks before final response:

- All bodies have nonzero volume.
- Meshes are manifold or acceptable to the target slicer repair tool.
- The bottom face is flat at Z=0.
- No body contains accidental internal duplicate surfaces from overlapping extrusions.
- Minimum feature width is at least the stated threshold.
- Color 2 is not hidden below color 1 unless intentionally inlaid.
- Text orientation is correct from the top.
- Overall dimensions match the requested bookmark size.

## Common Failure Modes

- Treating a bitmap as a heightmap and producing a noisy relief instead of clean two-color regions.
- Creating decorative islands that are detached from the model.
- Exporting two STLs with different origins, causing slicer misalignment.
- Making lines thinner than the nozzle can print.
- Forgetting that bookmark details should not be too tall or sharp because they touch pages.
- Using color as visual styling only, without physically separate bodies or material assignments.
