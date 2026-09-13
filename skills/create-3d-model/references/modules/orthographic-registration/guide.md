# Orthographic Registration

This skill prevents the common failure where the front view looks plausible but the side/back/top views are wrong.

## Coordinate contract

Reuse the agreed axes and canonical view policy. The following is the front-locked reconstruction convention used by these helpers; adapt inputs or transforms for an existing scene with another convention.

- Front view defines `X/Z` silhouette.
- Side view defines `Y/Z` depth envelope.
- Top view defines `X/Y` spread.
- Under a front-canonical policy, the back view defines rear silhouette/material without rewriting the agreed front silhouette. Other policies may assign different constraints.

## Workflow

1. Run `scripts/register_views.py` on the available view images.
2. Create orthographic reference planes/image empties with a single shared scale.
3. Align centerline and bbox centers before modeling.
4. Lock the boundary constraints selected by the canonical policy; use front X/Z only for a front-canonical reconstruction.
5. Add Y depth from side/top envelopes using modifiers/displacement or vertex groups.
6. Validate the supplied or required views before export; do not invent missing reference evidence.

## Failure policy

If views disagree, apply the canonical policy in the shared workflow contract; resolve an unchosen material conflict before dependent geometry changes. Document the conflict in `registration_report.json`.


## Front-plane rotation rule

In this Blender coordinate convention, the front camera looks along the Y axis and the reference silhouette lives in the X/Z plane. Therefore 2D rotations inside the front view are rotations around the **Y axis**, not around Z. Use `rotation_euler = (0, angle, 0)` for 2D component orientation in the front projection. Z rotation spins objects into/out of screen-space incorrectly for X/Z-plane meshes.

## Sources distilled

- Blender Image Empty/reference image controls for orthographic blueprints.
- OpenCV homography/alignment and geometric transforms for view registration.
