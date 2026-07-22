<!--
IAP.md -- the Integrated Action Plan, written by the IC during /icc-plan.
This is the ONLY document specialists execute against once approved -- the
single source of truth doctrine principle 3 insists on. Editing this file
after approval voids IAP-APPROVED automatically (hash mismatch) -- that is
deliberate, not a bug to route around.
-->

# IAP — Incident Action Plan

**Incident:** {{slug}}
**Type:** {{5 | 3 | 1}}
**Operational period:** {{N}}
**Links:** `202-OBJECTIVES.md` · `203-ORG.md` · `204-TASKING/*.md`{{ · logistics plan below, Type 1 only}}

## Objectives (summary of 202)

{{goal + numbered acceptance criteria, copied from 202-OBJECTIVES.md so the IAP is self-contained for whoever reads it}}

## Tactics (from the Planning Chief)

{{tactics[] from the chief-plan schema}}

## File-territory partition

<!-- partition_ok must be true, or this section must justify sequential /
     worktree execution instead. The IC rejects and re-spawns the Planning
     Chief if this table shows overlapping territories with no
     justification. -->

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | {{globs}} | {{globs}} |
| S2 | {{globs}} | {{globs}} |

**Partition status:** {{disjoint -- parallel execution | overlap justified: <reason> -- sequential/worktree}}

## Deploy / environment plan (Type 1 only, from the Logistics Chief)

{{deploy_path, env_deps, migration_ordering, rollback_plan -- omit this section entirely for Type 3/5}}

## Risks

{{risks[] from the chief-plan schema, plus any the IC identified during integration}}

## Verification plan

{{verification_plan from the chief-plan schema -- what the Safety Officer will check}}

## Deviation history (this period)

<!-- Appended if this IAP is a re-issue after a deviation forced a return
     to planning. Empty on a period's first IAP. -->

{{none | link to the 214-LOG.md entries describing the deviation and what changed}}
