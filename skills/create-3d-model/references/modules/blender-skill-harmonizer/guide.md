# Coordinate coupled Blender work

Use this when several required modules depend on the same source, coordinates, objects or validation result. Choose one owner for each decision. The [shared contract](../../workflow-contract.md) owns source precedence, coordinate conventions and target budgets.

Select stages by actual inputs. Source analysis and registration precede exact geometry; stable geometry precedes final UV assignment; relevant structure and appearance checks precede a final export claim. A task without an atlas or multiview sources needs no atlas or registration report.

Reconcile conflicting assumptions before dependent edits. Reuse an agreed canonical policy instead of selecting front-wins again. Keep user-owned geometry recoverable. Rejected output routes to artifact repair; library maintenance is not a prerequisite.

Work may proceed independently only with disjoint write scopes and satisfied dependencies. Never have two operations mutate the same Blender objects or UV data concurrently. Tooling and source measurements may run independently when the current environment permits it.

Read [handoff contracts](references/handoff-contracts.md) only for the active module boundaries. Save the applicable decisions and evidence with the task outputs; create no empty mandatory reports.

Use scripts/skill_graph_audit.py for bundle path and routing audits when maintaining the package. Completion means active modules share consistent inputs and their combined checks cover the requested result.
