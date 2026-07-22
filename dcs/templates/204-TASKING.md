<!--
204-TASKING/{{ID}}.md -- one file per specialist, transcribed verbatim by
the IC from the Planning Chief's `taskings[]` array (schemas.md #2). The
specialist receives exactly this file's content plus the relevant IAP
excerpt -- nothing else. If the tasking is ambiguous, that's a planning
defect to fix during /dcs-plan, not something for the specialist to
resolve by guessing.
-->

# 204 — Tasking {{ID}}

**Incident:** {{slug}}
**Period:** {{N}}
**Specialist:** dcs-ops-specialist ({{ID}})

## Task

{{task -- specific, references a 202 acceptance criterion by number}}

## File territory (may edit only within these globs)

- {{glob 1}}
- {{glob 2}}

## Forbidden zones (explicitly, even if it seems related)

- {{glob -- usually another specialist's territory}}

## Evidence required in the return

<!-- Concrete commands whose REAL output must be pasted into the
     structured return's `evidence` field -- not a description of what
     should happen. -->

- {{e.g. "pytest Copilot/tests/test_inventory_repo.py -x -- full output"}}

## On discovering the plan doesn't fit reality

STOP. Do not improvise a different fix. Return `status: "deviation"` per
`references/schemas.md` #4, with `found`, `why_plan_wrong`, and a
`proposal` (a recommendation, not an action). The IC will re-enter
planning around your finding.
