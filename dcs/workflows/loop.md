<purpose>
Cycle /dcs-run --next over the register queue, unattended, with the Owner
involved only at real decisions. One sweep of the queue per invocation.
Legitimate only because the ESG's Delegation of Authority defines, in
writing, what "routine" means — see doctrine's "Automation layers"
section for the three hard rules this workflow enforces without exception.
</purpose>

<required_reading>
@$HOME/.claude/dcs/references/doctrine.md
@$HOME/.claude/dcs/workflows/run.md
</required_reading>

<process>

## 1. Preconditions

Check, in order, and stop with plain instructions if any fails:

- `<project>/.dcs/esg/` must exist, with both `REGISTER.md` and
  `DELEGATION.md` present. If missing: stop — tell the Owner `/dcs-loop`
  needs an ESG in place first; run `/dcs-esg`'s founding session (it
  creates `.dcs/esg/` from templates).
- Parse `DELEGATION.md`'s latest `delegation-bounds` block and **state
  plainly, every run, regardless of outcome:** with `auto_approve_type3:
  false` (the template default), every Type 3 incident will still pause
  at IAP approval — hands-off operation effectively requires an active
  delegation (`auto_approve_type3: true`, with real bounds the Owner has
  actually reviewed at an `/dcs-esg` session). This is expectation-setting
  before the sweep starts, not a failure condition.

## 2. Take the top QUEUED item

Read `REGISTER.md`. If there is no `QUEUED` row: report "queue empty,
nothing to run" and stop — this is a clean, successful end state, not an
error.

**Hard rule 1 — never execute a Type 1 incident unattended.** If the top
`QUEUED` row's recorded type is `1`: do not run it. Mark its register row
`PARKED` with reason `"awaits Owner"`, append the same note to that
incident's `214-LOG.md` if an incident directory already exists for it,
and continue to the next `QUEUED` row instead. If every remaining `QUEUED`
row is Type 1 (or turns out to be after typing — see step 3), stop the
sweep entirely and report the parked list to the Owner.

## 3. Run `/dcs-run` for that item

Follow `$HOME/.claude/dcs/workflows/run.md`'s `<process>` in full for this
item — its own steps already resolve the `--next`-equivalent intake,
typing, planning, execution (with escalation triggers), and close. Two
additions specific to the loop context:

**Re-check Type after typing (command point 1).** `REGISTER.md`'s
recorded type is a pre-typing guess; the real type is only settled inside
`new.md`'s command point 1, which `run.md` step 3 runs. If that resolves
to Type 1 even though the register guessed otherwise: apply hard rule 1
immediately — do not proceed into planning. Mark the register row
`PARKED` ("awaits Owner"), log it, and return to step 2 for the next item.
This is the one place `/dcs-loop` overrides `run.md`'s normal flow,
because `run.md` alone has no queue to fall back to.

**Hard rule 2 — never deploy from the loop.** `run.md`'s close-out (step
7, following `close.md`) never invokes a deploy script, regardless of
what the incident's changes would normally call for — every incident this
loop drives stops at committed + safety-passed. Where `close.md`'s AAR
fields (Deploy status, per its facts-only rule) would normally prompt "is
this deployed?", the loop context answers **not deployed** and adds
`"deploy pending"` to that incident's register-row outcome, instead of
pausing to ask — a deliberate, honest substitution, not a skipped check;
the AAR still records deploy status as pending, truthfully.

## 4. On any Owner gate the Delegation doesn't cover

`run.md` already pauses its own turn at every such gate: typing confirm
(always — the Delegation never covers typing, only IAP approval),
un-delegated IAP approval, deviation/verdict `escalate_owner`, any
escalation-trigger continue/pivot/demobilize, and Owner-UAT. When one
fires mid-sweep:

**Hard rule 3 — never busy-wait, never self-approve outside Delegation
bounds.**

1. Send **one** notification if a push/notification tool is available in
   this session — check what's actually available; don't assume one
   exists just because this is an automation context.
2. Confirm the pause state is genuinely on disk (the incident directory,
   `.dcs/ACTIVE`'s phase, `214-LOG.md`) — the underlying workflows are
   already paper-based (doctrine principle 5), so this is a check, not
   extra writing: don't end the turn on an assumption.
3. **End the loop turn.** Do not proceed to the next register item while
   this incident sits mid-phase and unresolved — the whole point of the
   pause is that only the Owner can move it forward, and starting a
   different incident here would collide with `.dcs/ACTIVE`'s
   single-incident lock anyway (a fresh incident cannot open while this
   one is still `ACTIVE`).

Note the expected degenerate case: because typing confirm is an Owner gate
the Delegation never covers, a truly unattended sweep will pause at the
**first** incident's typing confirm every time nobody answers it. That is
correct behavior, not a defect — `/dcs-loop` is not meant to invent
authority the Owner never granted.

## 5. Continue the sweep

On a clean close (step 7 of `run.md`/`close.md` completes) or a clean
`PARKED` skip (hard rule 1): return to step 2 for the next `QUEUED` item.

## 6. Stop conditions

- **Queue empty** (step 2): report the sweep summary — incidents closed,
  incidents parked (and why), any `"deploy pending"` rows — and stop.
- **Any Owner-gate pause** (step 4): stop, per hard rule 3.
- **Safety valve** inherited from `run.md` step 6 (an incident running
  more than 3 operational periods without closing): this is itself an
  Owner-gate pause — treat it the same as step 4.

## 7. Recurrence

`/dcs-loop` runs **one sweep** of the queue per invocation — it does not
reschedule itself. For standing recurrence, the Owner pairs it with the
harness's own scheduling (e.g. a `/loop` wrapper skill, or a scheduled
routine that invokes `/dcs-loop` on a cadence). DCS itself stays
scheduler-agnostic: no cron, no daemon, no self-rescheduling logic — this
matches the ESG spec's "no automated cron/scheduled ESG sessions in v0.2"
non-goal, extended here to the loop driver itself.

## 8. Dispatcher-model note

Unattended dispatch (the main session driving this sweep) should run on
Sonnet or stronger — this is not a recommended Haiku seat. Command points
inside each incident still transfer to `dcs-commander` (Fable, with
doctrine's model-availability fallback) exactly as they would under any
other entry point; `/dcs-loop` changes only who's watching, never who
holds command judgment.

## 9. Report

Per the stop condition reached — see step 6.

</process>
