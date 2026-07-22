<!--
202-OBJECTIVES.md -- written by the IC together with the Owner, at the
start of EACH operational period (/icc-plan). Re-drafted (new file content,
same filename) each time the incident re-enters the P-loop for another
period -- the prior period's 202 is preserved in 214-LOG.md's phase-
transition history and, once complete, in AAR.md's summary, not in this
file itself.
-->

# 202 — Objectives (Operational Period {{N}})

**Incident:** {{slug}}
**Period:** {{N}} (increments each time the incident returns to this step)

## Goal

<!-- Outcome-shaped, not task-shaped. "Orders past their delivery window
     stop being flagged as blocking" not "edit get_blocking_ingredients". -->

{{goal}}

## Acceptance criteria (the Definition of Done)

<!-- Each criterion must be verifiable -- by a test, a repro step, or a
     concrete observation. This is what the Safety Officer checks against;
     vague criteria produce a vague verdict. Number them -- taskings and
     the Safety Officer both reference these numbers.

     STAGING RULE: never write a criterion that requires a POST-verification
     artifact to exist AT verification time -- "changes are committed",
     "deployed to prod". The Safety Officer verifies the working-tree diff;
     the integration commit happens AFTER its pass (execute.md 9b), deploy
     after close. Such criteria guarantee a first halt (field lesson,
     2026-07-22). Also: only criteria agents can verify in THEIR harness --
     browser/UI observations belong in an Owner-UAT section, not here. -->

1. {{criterion 1 -- verifiable}}
2. {{criterion 2 -- verifiable}}

## Out of scope this period

<!-- Explicit non-goals, especially useful when a deviation in a prior
     period surfaced adjacent work that belongs in a LATER period, not
     silently folded into this one. -->

{{explicit non-goals, or "none"}}

## Chief feedback (filled in after /icc-plan spawns the Planning Chief)

{{objectives_feedback from the chief-plan schema -- if the Chief flagged a
criterion as untestable, note the resolution here: revised criterion, or
Owner accepted the risk}}
