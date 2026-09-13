# Order artifact repairs

Consume failed validation reports and the shared source policy. Preserve the current artifact as a baseline. Repair upstream causes before dependent symptoms: unresolved source conflict, structural parts, geometry and scale, UV mapping, appearance, then export or playback.

For each useful repair item record its observed failure, proposed correction, affected objects or files, prerequisites and acceptance check. Use a compact queue; create a separate report only when the task needs one. The bundled scripts/fit_repair_queue.py can produce a starting queue.

Independent analysis can continue while a dependency is blocked. Parallel work requires disjoint write scopes; do not concurrently edit the same geometry, transforms or UV assignments.

When a failure repeats, use quality-refinement-autoloop to reconsider evidence and repair strategy. This is an artifact diagnosis step, not a requirement to change skills. Reuse settled canonical decisions; ask only for an unresolved conflict that changes the intended result.

Completion means corrections are applied in a valid order and affected checks pass, or the remaining blocking evidence is clear.
