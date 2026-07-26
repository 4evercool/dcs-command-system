<purpose>
Drive the ENTIRE incident lifecycle from one command: stem → planning arc
→ execution (looping operational periods as needed) → close, in order, by
reading each phase workflow at that point and following its numbered
`<process>` EXACTLY as written. This workflow is a sequencer, not a
restatement — `new.md`, `plan.md`, `execute.md`, and `close.md` remain the
single source of truth for their own steps; nothing here duplicates or
paraphrases them. The Owner only answers `AskUserQuestion` gates instead
of typing each phase command by hand.
</purpose>

<required_reading>
@$HOME/.claude/dcs/references/doctrine.md
@$HOME/.claude/dcs/workflows/new.md
@$HOME/.claude/dcs/workflows/plan.md
@$HOME/.claude/dcs/workflows/execute.md
@$HOME/.claude/dcs/workflows/close.md
</required_reading>

<process>

## 1. Resolve the intake

`$ARGUMENTS` is either an intake description, or the literal flag
`--next`. If `--next`: read `<esg_root>/.dcs/esg/REGISTER.md` (v0.3:
resolve `esg_root` — the main checkout — per doctrine's "Parallel
operation"; never a worktree's own copy) for the
topmost `QUEUED` row (by the order `STRATEGY.md`'s ranked priorities
implies, or table order otherwise). If `REGISTER.md` doesn't exist, or
exists with no `QUEUED` rows: stop, and tell the Owner politely there's
nothing queued — run `/dcs-esg` to populate the register, or pass an
intake description directly instead of `--next`. Otherwise, that row's
title becomes the intake description used below — this is exactly the
`"next from the register"` intake `new.md` step 1 (v0.2) already knows how
to resolve, so step 3 just hands it through.

## 2. Check for an already-active incident

Read `<project>/.dcs/ACTIVE` (same check as `new.md` step 2). If present:
stop here exactly as a standalone `/dcs-new` would — report the active
incident (slug, type, phase) and tell the Owner to finish or close it
first. `/dcs-run` does not bypass the v0.1 single-incident constraint.

## 3. Run the stem — follow `new.md`

Read `$HOME/.claude/dcs/workflows/new.md` and execute its `<process>`
steps 1 through 8 verbatim, using the intake resolved in step 1 above as
`new.md`'s `$ARGUMENTS`. Every gate applies unchanged, including the v0.2
addition: command point 1 (typing) still spawns `dcs-commander` under the
same rules as a standalone `/dcs-new`, and the Owner still confirms typing
via `AskUserQuestion` — the Delegation of Authority never covers typing,
only IAP approval (per the ESG spec), so this gate always fires.

- **Type 5 short-circuits here.** `new.md` step 7a resolves it inline
  (one specialist, IC verifies, no incident directory, no gate). Report
  the completed fix to the Owner and end the `/dcs-run` turn — there is no
  plan/execute/close chain to continue.
- **Type 3 / Type 1** opens the gated incident directory (`new.md` step
  7b) with `phase=planning`. Continue to step 4.

## 4. Run the planning arc — follow `plan.md`

Read `$HOME/.claude/dcs/workflows/plan.md` and execute its `<process>`
steps 1 through 9 verbatim for the current operational period, including
its v0.2 Delegation-aware approval step (6/6b) unchanged. If bounds hold
and `auto_approve_type3` is on, the IC approves without an Owner
round-trip and `/dcs-run` continues straight through to step 5 in the same
turn. Otherwise the Owner's `AskUserQuestion` approval gate pauses this
turn exactly as it would for a standalone `/dcs-plan` — `/dcs-run` resumes
the chain on the Owner's next message the same way a fresh session would
resume via `/dcs-status`.

## 5. Run execution — follow `execute.md`

Read `$HOME/.claude/dcs/workflows/execute.md` and execute its `<process>`
steps 1 through 10 verbatim, including its v0.2 escalation-trigger checks
at the period boundary and after the Safety verdict. Four outcomes:

- **Deviation (step 6), or a `halt` verdict routed to "return to
  planning" (step 9):** loop back into step 4 above *within this same
  `/dcs-run` turn* instead of telling the Owner to type `/dcs-plan` by
  hand — this is the "deviation or safety-halt-with-replan loops back
  into the plan.md process automatically" transition. Before looping,
  apply the safety valve in step 6 below.
- **An escalation trigger fires** (either of `execute.md`'s v0.2 checks):
  follow `execute.md`'s own instructions verbatim — file the 209 sitrep,
  pause, put continue/pivot/demobilize to the Owner via
  `AskUserQuestion`. This is itself an Owner gate; `/dcs-run` pauses here
  exactly as the eventual decision dictates (continue resumes whatever
  this trigger interrupted; pivot goes to step 4; demobilize goes to step
  7 or ends the incident as abandoned per `plan.md` step 6b's Reject path).
- **`pass`, objectives fully met (`execute.md` step 9b):** continue to
  step 7.
- **`pass`, objectives partially met:** loop back to step 4 for the next
  operational period — the normal multi-period case, not a deviation.
  Apply the safety valve in step 6 first.

## 6. Safety valve — period cap

Every time this `/dcs-run` invocation is about to loop step 4 → 5 again
for this same incident without having reached step 7 (close), read the
count from `<incident_dir>/214-LOG.md` instead of tallying loop
iterations locally: count IAP stamps the same way `execute.md`'s trigger
(c) does (v0.5.12: attempts, not periods), and also read the halt count
with `python "<project>/.claude/hooks/dcs_gate.py" --halt-count
"<incident_dir>"` — the same runaway-loop failure, seen from the other
axis. Reading from the log rather than a turn-local tally is what makes
this valve hold across sessions: a multi-session incident must not reset
to zero just because a fresh session started a new turn. If the stamp
count would exceed 3, or the halt count is already sitting at
`dcs_gate.py`'s own ceiling: **stop looping automatically.** File a 209
sitrep (`$HOME/.claude/dcs/templates/209-SITREP.md`, same mechanism as an
`execute.md` escalation trigger) noting why, and put
continue/pivot/demobilize to the Owner via `AskUserQuestion` before
proceeding further.

This is independent of, and in addition to, `execute.md`'s own trigger (c)
(`esg.max_periods_before_review`, default 3 — doctrine principle 13): that
threshold is doctrine governing every incident regardless of how it's
driven and will very likely fire first; this one is `/dcs-run`'s own
runaway-loop guard specifically against driving an unbounded chain with no
human in the loop between periods, and fires even if trigger (c)'s config
value were ever raised or removed.

## 7. Run close-out — follow `close.md`

Read `$HOME/.claude/dcs/workflows/close.md` and execute its `<process>`
steps 1 through 7 (including v0.2's 6a register update) verbatim. Its
gates are unchanged: a green Safety verdict is required before this step
is even reachable (guaranteed by step 5 above), and the Owner-UAT check in
`close.md` step 1 / the IAP's verification plan is a real Owner gate —
pause here for the Owner's done / defer-with-explicit-consent answer via
`AskUserQuestion` exactly as a standalone `/dcs-close` would.

## 7a. After the close: the deploy train, if delegated (v0.4)

If `<esg_root>/.dcs/esg/DELEGATION.md`'s latest bounds have
`deploy.auto_after_close: true`: read
`$HOME/.claude/dcs/workflows/deploy.md` and run the deploy train now,
in-line — its own step 5 delegation check governs whether the ship
proceeds without a prompt or stops to ask (an out-of-bounds row still
asks; a migration-bearing row always asks). If `auto_after_close` is
absent or `false`, or there is no ESG: just report the close's
`deploy pending` state as before. This applies to **attended** `/dcs-run`
only — `/dcs-loop` never reaches this step's deploy branch (doctrine
automation-layers hard rule 2, unchanged: the unattended loop never
deploys, no matter what the Delegation says).

## 8. Command points throughout

Every command point `new.md`, `plan.md`, and `execute.md` define (typing,
IAP acceptance, deviation arbitration, verdict disposition) fires exactly
as those workflows specify while running under `/dcs-run` — spawn
`dcs-commander` when the session isn't Fable, decide directly when it is,
log every decision in `214-LOG.md` the same way. `/dcs-run` changes only
who has to type the next phase command, never who holds command judgment.

## 9. Report

On completion (closed — summarize `close.md` step 7's final sitrep) or on
any pause (Owner gate, escalation trigger, safety valve): state exactly
what phase the incident is in, what just happened, and the exact pending
`AskUserQuestion` awaiting the Owner's answer.

</process>
