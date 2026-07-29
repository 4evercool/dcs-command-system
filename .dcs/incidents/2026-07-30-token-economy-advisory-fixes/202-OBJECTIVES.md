<!--
202-OBJECTIVES.md -- written by the IC together with the Owner, at the
start of EACH operational period (/dcs-plan). Re-drafted (new file content,
same filename) each time the incident re-enters the P-loop for another
period -- the prior period's 202 is preserved in 214-LOG.md's phase-
transition history and, once complete, in AAR.md's summary, not in this
file itself.
-->

# 202 — Objectives (Operational Period 1)

**Incident:** token-economy-advisory-fixes
**Period:** 1

## Goal

Four one-line package-text defects the Safety Officer flagged during `token-economy` (period 1, verdict 1, advisories 2/3/4/6) and the IC deferred at command point 4 are fixed in the repo copies, each matching the advisory text that described it. No behavior changes, no schema changes — text-only corrections to shipped documentation.

## Acceptance criteria (the Definition of Done)

1. `dcs/templates/204-TASKING.md` line 37 example no longer says `-- full output` — it now says `-- cite the failing assertion`, matching the rule on line 34 ("never a full unabridged transcript"). Verify with `grep -n "full output" dcs/templates/204-TASKING.md` → returns nothing.

2. `dcs/workflows/run.md` step 3's doctrine.md re-read instruction no longer contains the "real doubt it is still in context" model-self-report clause — replaced with the unconditional fact that doctrine.md is `@`-included at run.md's top. Verify with `grep -n "real doubt" dcs/workflows/run.md` → returns nothing.

3. `agents/dcs-safety-officer.md` by-reference exception (step 2, the "unchanged" subject passage) now states: for a derived subject (a test result, a byte budget, a count), "unchanged" requires its INPUTS unchanged, not just the file that produced it. Verify with `grep -n "derived subject" agents/dcs-safety-officer.md` → returns the added caveat.

4. `dcs/templates/STRATEGY.md` Sessions-log cap comment is internally consistent: either the cap states 4 (matching the enumerated items) or the fifth line's purpose is named. The optional-pointer placeholder is unwrapped to one physical line. Verify with `grep -A8 "CAP:" dcs/templates/STRATEGY.md` → cap number matches enumerated count, placeholder on one line.

## Out of scope this period

- Advisory 1 (202-OBJECTIVES.md criterion 3(c) grep expectation) — incident artifact, not shipped package text.
- Advisory 5 (stale ESG figure) — a measurement the IC takes at close, not a package-text fix.
- Any behavioral change, schema change, or test-suite modification.

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

{{objectives_feedback from the chief-plan schema}}
