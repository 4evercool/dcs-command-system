<!--
IAP.md -- the Integrated Action Plan, written by the IC during /dcs-plan.
This is the ONLY document specialists execute against once approved.
-->

# IAP — Incident Action Plan

**Incident:** token-economy-advisory-fixes
**Type:** 3
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `204-TASKING/*.md` (203 skipped — default Type 3 activation)

## Objectives (summary of 202)

**Goal:** Four one-line package-text defects the Safety Officer flagged during `token-economy` (period 1, verdict 1, advisories 2/3/4/6) and the IC deferred at command point 4 are fixed in the repo copies, each matching the advisory text that described it. No behavior changes, no schema changes — text-only corrections to shipped documentation.

**Acceptance criteria:**
1. `dcs/templates/204-TASKING.md` line 37 example no longer says `-- full output` — it now says `-- cite the failing assertion`. Verify: `grep -n "full output" dcs/templates/204-TASKING.md` → returns nothing.
2. `dcs/workflows/run.md` step 3's doctrine.md re-read instruction no longer contains the "real doubt it is still in context" model-self-report clause. Verify: `grep -n "real doubt" dcs/workflows/run.md` → returns nothing.
3. `agents/dcs-safety-officer.md` by-reference exception now states: for a derived subject, "unchanged" requires its inputs unchanged, not just the file that produced it. Verify: `grep -n "derived subject" agents/dcs-safety-officer.md` → returns the added caveat.
4. `dcs/templates/STRATEGY.md` Sessions-log cap comment is internally consistent: cap reads "4 LINES" matching the four enumerated items, and the optional-pointer placeholder is unwrapped to one physical line. Verify: `grep -A8 "CAP:" dcs/templates/STRATEGY.md` → cap matches enumerated count, placeholder on one line.

## Tactics (from the Planning Chief)

1. Replace the contradictory example in 204-TASKING.md line 37: swap `-- full output` for `-- cite the failing assertion` so the example matches the rule two lines above it.
2. Replace the model-self-report conditional in run.md lines 51-53 with an unconditional statement: doctrine.md is `@`-included at the top (line 13) and therefore already loaded — no re-read conditional needed.
3. Add the derived-subject-inputs caveat to safety-officer.md lines 57-59: after "a scoped git diff returning empty, or equivalent", insert a sentence stating that for a derived subject, "unchanged" requires unchanged inputs, not merely the source file.
4. Fix STRATEGY.md's cap inconsistency: change "5 LINES" to "4 LINES" on line 41, and unwrap lines 47-52 (the optional-pointer placeholder) into a single physical line.

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | `dcs/templates/204-TASKING.md` | `dcs/workflows/**`, `agents/**`, `dcs/templates/STRATEGY.md` |
| S2 | `dcs/workflows/run.md` | `dcs/templates/**`, `agents/**` |
| S3 | `agents/dcs-safety-officer.md` | `dcs/workflows/**`, `dcs/templates/**` |
| S4 | `dcs/templates/STRATEGY.md` | `dcs/templates/204-TASKING.md`, `dcs/workflows/**`, `agents/**` |

**Partition status:** disjoint — parallel execution

## Risks

- S4's unwrap of lines 47-52 into one physical line will produce a long line (>80 chars) — acceptable for a template comment block, but it will look different from the surrounding wrapped comments. The acceptance criterion explicitly asks for this.
- S2's replacement text for the run.md clause should not introduce new conditional language or model-self-reports — the tasking constrains it to an unconditional statement of the existing `@`-include fact.
- All four files are in different directory subtrees (dcs/templates/, dcs/workflows/, agents/) and are fully disjoint — no concurrent-editor risk.

## Verification plan

Run all four grep checks from the 202 acceptance criteria and confirm each returns the expected result. Then run `git diff -- dcs/templates/204-TASKING.md dcs/workflows/run.md agents/dcs-safety-officer.md dcs/templates/STRATEGY.md` and confirm the diff contains exactly four hunks — one per file, each a one-line text change with no collateral edits, no reformatting spill, and no unintended prose alterations. Finally, confirm no other files in the repo were touched.

## Deviation history (this period)

None — first IAP for this period.
