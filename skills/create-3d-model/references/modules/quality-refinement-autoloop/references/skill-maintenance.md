# Optional skill maintenance

Read only when the user requests developing or publishing the skill bundle. Routine artifact repair continues without this workflow.

Capture the failure evidence and identify a reusable gap. Apply writing-for-agents for a focused instruction change, separating source-specific details from reusable methods. Preserve license and provenance information. Add a helper only when it addresses a repeatable fragile operation.

Validate paths, routing, helper behavior and affected instructions. Use skill_graph_audit.py against the bundle root; use release_readiness_check.py for package integrity. The Codex reference bundle uses module-index.json and a separately configured BlenderMCP connection, not a vendored connector.

Commit, publish, push, install dependencies or change remote state only within the user's authorization. Prepare the actual change and validation before any missing approval. Do not make an artifact repair wait for publication or a version bump.
