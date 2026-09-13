# Multiview Fit Loop

This skill closes the missing loop: **render → compare → adjust → render again**. It is mandatory when a user says the model still does not fit the templates/originals.

## Required loop

1. Establish evidence for the supplied or required views using flat, material-independent silhouettes. After a correction, re-render affected views and reuse unchanged evidence only when its geometry/camera dependencies remain valid.
2. Extract the template object mask, excluding labels, cyan guides, and background.
3. Compare template vs render per view:
   - bbox center and size
   - centroid drift
   - silhouette coverage/IoU where modality is valid
   - visual overlay
4. Convert measured deltas into model/camera/recipe adjustments.
5. Rebuild or transform the model.
6. Repeat until all hard gates pass or document the remaining conflict.

## Constraint inconsistency gate

Before forcing adjustments, check whether the supplied orthographic templates are mutually consistent. A single rigid 3D model cannot simultaneously satisfy contradictory physical ratios, for example if side view says total depth is 0.39 of height but top view says depth is 0.98 of width. When this occurs, stop claiming final fit, record the conflict and apply the already agreed canonical policy. If no policy resolves it, ask for the material choice before dependent changes; create variants only when they help the requested decision.

## Example tolerances; the agreed manifest is authoritative

- all required views have validation reports and overlays;
- bbox center drift <= 1.5% of image width;
- bbox size drift <= 3% for front, <= 5% for side/top/back first-pass depth;
- structural part count exact;
- texture UV regions still valid after geometry changes.

## View mask rule

For annotated wireframes, choose a template mask mode that isolates the intended construction/object lines and excludes guide colors, labels, captions, and background annotations. For Blender validation renders, use a flat white silhouette on black, not beauty renders with glow/context elements.

## Scripts

- `scripts/multiview_fit_report.py` compares view pairs and writes JSON + overlays.

## Adjustment rule

Prefer changing recipe parameters or source geometry over camera scale tricks. Camera scale may be used only after model dimensions are correct.
