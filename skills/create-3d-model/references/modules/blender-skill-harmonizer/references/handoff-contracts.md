# Blender reference handoff contracts

Use only handoffs needed by the selected workflow. Reuse existing reports and consume the shared workflow contract for coordinates, source priority and completion.

## Reference analysis → registration

Input: source image folders.
Output: `reference_manifest.json` with roles, expected parts, validation thresholds.

Registration must not invent part counts; it consumes the manifest.

## Registration → contour/mesh generation

Input: `registration_report.json`, canonical view policy, scale/axis contract.
Output: geometry recipe parameters and reference planes/cameras.

Contour/mesh generation consumes the agreed coordinate contract. In the front-locked example: front = X/Z, side = Y/Z, top = X/Y.

## Contour/mesh → UV fitting

Input: locked structural mesh names, source masks/contours, atlas regions.
Output: active UV maps and material assignments.

UV fitting may analyze atlas regions before geometry locks, but final UV writes wait for stable mesh topology or stable projected bounds.

## UV/material → lighting/look

Input: texture-fit report, material node graph, target original/look images.
Output: calibrated material values, emission strengths, aura/HUD color, lights, render settings.

Lighting must not be used to hide geometry or UV errors.

## Validation → repair optimizer

Input: multiview fit reports, texture/look reports.
Output: dependency-ordered repair queue.

Repair optimizer owns sequential/parallel scheduling after failures.

## Repair optimizer → export

Input: applicable verification evidence, target requirements and unresolved limitations.
Output: the requested formats and concise verification notes; GLB plus Blender source is the default only when no other output is specified.

A required gate must pass before claiming final quality. An authorized draft or diagnostic export may be saved with its exact limitations.
