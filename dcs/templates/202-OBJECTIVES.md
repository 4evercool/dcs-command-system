<!--
202-OBJECTIVES.md -- written by the IC together with the Owner, at the
start of EACH operational period (/dcs-plan). Re-drafted (new file content,
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
     2026-07-22, predates self-hosting). Also: only criteria agents can verify in THEIR harness --
     browser/UI observations belong in an Owner-UAT section, not here.

     OWNERSHIP TAG (v0.5.4): every criterion is satisfiable by SOMEBODY.
     Tag any criterion no specialist can own -- specialists are barred
     from `.dcs/**`, so re-issuing a gate, amending the IAP, or updating
     the register is [IC]; UAT and sign-off are [Owner]; shipping is
     [deploy period]. Untagged criteria are assumed specialist work and
     MUST map to a tasking (plan.md lint 4a check 6). An untagged
     criterion nobody can execute surfaces as a false Safety halt at the
     END of the period, after all the execution cost is spent (field
     lesson 2026-07-24: a criterion required editing IAP.md, a file no
     tasking may touch by construction).

     MEASURED CLAIM: if a criterion asserts anything outside this working
     tree -- a registry version, whether something is published, an
     installed or deployed copy, another repository, a remote ref, a live
     service -- write the command that establishes it inside the
     criterion, and phrase the criterion as that command's result
     ("`npm view <pkg> version` returns < X"), never as a bare claim ("X
     is unpublished"). Classify while writing: plan.md lint 4a check 3b
     is the second line of defence, not the first, and it will run the
     command and record the output. An in-tree fact needs no such
     command -- `grep -n "^## Unreleased" CHANGELOG.md` settles itself.
     Field lesson 2026-07-26, incident `criterion-unmeasured-fact`: a criterion waived a version bump on
     "0.6.9 is unpublished"; it had been published 75 minutes earlier,
     and the version shipped twice with different contents. -->

1. {{criterion 1 -- verifiable}}
2. {{criterion 2 -- verifiable}} {{[IC] | [Owner] | [deploy period] -- omit if specialist work}}

## Out of scope this period

<!-- Explicit non-goals, especially useful when a deviation in a prior
     period surfaced adjacent work that belongs in a LATER period, not
     silently folded into this one. -->

{{explicit non-goals, or "none"}}

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

{{objectives_feedback from the chief-plan schema -- if the Chief flagged a
criterion as untestable, note the resolution here: revised criterion, or
Owner accepted the risk}}
