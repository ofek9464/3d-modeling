# Proposed design-preview behavior checks

These are proposed conversation checks, not executed model tests. Compare old and new behavior with the same host, model, tools, and sources. Check Codex and Claude independently.

| Request or setup | Expected behavior |
| --- | --- |
| Create a new printable desk organizer from a rough idea | Group material questions in a popup, inspect a generated concept, wait for direction selection, then build and verify. |
| A concept choice is pending with a preselected popup option | Continue independent analysis; do not create geometry until the user selects or delegates selection. |
| Create this exact part from a dimensioned drawing | Preserve the drawing and measurements; no mandatory synthetic concept replacement. |
| Create an exact part, and the user explicitly requests a concept first | Generate and inspect a labeled concept; retain the drawing as the dimensional authority. |
| The selected design and dimensions are already in the conversation | Reuse them and proceed; do not repeat discovery or confirmation. |
| Repair one mesh hole or export an existing model | Perform scoped work without restarting concept selection. |
| A generated preview has incorrect lettering or QR modules | Preserve the original assets; never build exact artwork from the generated approximation. |
| Image generation is unavailable | Report the limitation, continue planning, and obtain the missing decision before using a different preview path. |
| The user delegates selection or explicitly skips the image | Proceed within the stated scope and record the basis; no forced approval loop. |
| A concept looks printable but fit has not been measured | Verify actual geometry and report physical-fit limits; do not treat the image as engineering proof. |
