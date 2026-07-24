<purpose>
Gated execution: verify the approval marker is still valid, fan out Ops
Specialists against their 204 taskings, handle deviations by returning to
planning, and spawn the Safety Officer for a binding verdict before the
period can be considered complete.
</purpose>

<required_reading>
@$HOME/.claude/dcs/references/doctrine.md
@$HOME/.claude/dcs/references/schemas.md
</required_reading>

<process>

## 1. Verify incident state

```bash
cat "<project>/.dcs/ACTIVE"
```

If no `ACTIVE`, or `phase` is not `execution`: stop. If `phase` is
`planning`, tell the Owner to finish `/dcs-plan` first. If there's nothing
active, there's nothing to execute.

**Command-chain check (entry gate):** `214-LOG.md` must contain both a
`command: typed` and a `command: iap_review` entry. If either is missing,
the command chain was skipped somewhere upstream — **stop**, route to
`/dcs-plan`, whose own entry gate and pre-stamp checklist will repair the
chain. Do not fan out specialists on an unratified plan even if the
approval marker is technically valid.

## 2. Verify the approval marker — do this even though the hook also checks it

```bash
python -c "import hashlib; print(hashlib.sha256(open(r'<incident_dir>/IAP.md','rb').read()).hexdigest())"
```

Compare against the first line of `<incident_dir>/IAP-APPROVED`. If the
file is missing, or the hash doesn't match: **stop.** Tell the Owner the
IAP needs re-approval — someone edited `IAP.md` after it was approved (or
it was never approved). Do not spawn any specialist and do not attempt any
edit yourself. Route to `/dcs-plan`.

This check is redundant with `dcs_gate.py` by design: the hook is the
mechanical backstop that would block any specialist's edit anyway, but the
IC should never even attempt the fan-out against a stale plan — failing
here is cheaper than failing after spawning four subagents.

## 3. Read the plan

Read `IAP.md` and every `204-TASKING/*.md`. Confirm the partition table's
execution mode (parallel / sequential / worktree-isolated).

## 3.5. Type 1: offer the deterministic variant

If the incident is Type 1, ask the Owner (`AskUserQuestion`) whether to
execute via the standard Agent-tool fan-out (below) or emit a deterministic
Workflow script instead — schema-enforced returns, phases Execute then
Verify, no subagent judgment calls. Prefer the script when the taskings are
mechanical enough to specify exactly (e.g. a scripted migration + restart
sequence from the Logistics Chief's plan). Record the choice in
`214-LOG.md`. If the script path is chosen, the remainder of this section
still applies conceptually (fan-out becomes script phases, structured
returns still get collected and validated the same way) — adapt, don't
skip the deviation/Safety Officer gates below.

## Escalation-trigger check — period boundary (v0.2, doctrine principle 13)

Before spawning any specialist this period, check trigger (c): read
`esg.max_periods_before_review` from `<project>/.dcs/config.json`'s `esg`
key (default `3` if unset or the key is absent). If the operational
period number about to run exceeds that threshold, this period **is** the
mandatory escalation — do not fan out. Skip to "On any escalation
trigger" below instead of step 4.

Also check trigger (d) preemptively if `<esg_root>/.dcs/esg/DELEGATION.md`
(v0.3: ESG state lives in the main checkout only — resolve `esg_root` per
doctrine's "Parallel operation" before reading, never this worktree's copy)
is in force: if the IAP's declared territory for this period touches a
`forbidden_globs` entry that wasn't caught at `/dcs-plan` time (e.g. the
Delegation was tightened after this IAP was approved), treat it the same
way — do not fan out over a plan that now crosses a bound.

## 4. Fan out Ops Specialists

Up to 4 `dcs-ops-specialist` subagents, each given **exactly one**
`204-TASKING/{{ID}}.md` file's content plus the relevant IAP excerpt
(objectives summary, its acceptance criterion, the partition table, risks,
verification plan) — not the whole IAP dumped in raw, and not any other
specialist's tasking.

- **Parallel:** only when the partition table shows disjoint territories
  for this batch. Spawn all of them in one message with multiple Task
  tool_use blocks.
- **Sequential:** when the IAP declared overlap-with-justification. Spawn
  one, wait for its structured return, then spawn the next — later
  taskings may need to account for what an earlier one actually did.
- **Worktree-isolated:** if the IAP declares `isolation: worktree` for a
  specialist, set up the worktree (e.g. `git worktree add`) before
  spawning it, and merge/reconcile after it returns, per what the IAP
  specified.

## 5. Collect and validate structured returns

Each specialist returns the schema in `references/schemas.md` #4. Check
`files_touched` against that specialist's declared `territory` — any file
outside territory is itself a violation worth flagging to the Owner even
if the specialist didn't self-report it as a deviation.

## 6. Handle non-`done` returns — COMMAND POINT 3 (deviation arbitration)

**Any `status: "deviation"`:** stop the execution phase here. Do not spawn
remaining specialists beyond ones already safely completed on disjoint
territory. This is a command point (doctrine: "Transfer of command"). **If
this session is not running Fable**: spawn `dcs-commander` via Task (model
`fable`) with the triggering specialist's full return, the current 202 and
its 204, and the execution state; its `deviation` decision (schemas.md #6)
governs the disposition — `replan` / `amend_tasking` / `escalate_owner` —
and is recorded in `214-LOG.md` (`command: deviation -> <disposition>
(IC=dcs-commander)`). **If this session is Fable**, make the call yourself.
Then: update `202-OBJECTIVES.md` and/or the relevant `204-TASKING/*.md` to
reflect what was actually learned — incorporate the specialist's `proposal`
per the IC's directives (use `AskUserQuestion` if the disposition is
`escalate_owner` — the right call is genuinely the Owner's judgment, not
just a mechanical correction). This edit to the plan changes `IAP.md`'s content in the next
`/dcs-plan` pass — its hash will differ from `IAP-APPROVED`, which
**mechanically** voids the current approval; that's the deviation doctrine
working as intended, not a bug to route around. Append to `214-LOG.md`:
`deviation reported by <ID>: <one-line summary> -- returning to planning`.
Tell the Owner to run `/dcs-plan` again.

**Any `status: "blocked"`:** report the blocker to the Owner — this is an
external obstacle (missing credential, environment issue), not necessarily
a planning defect. The IC decides with the Owner whether to re-tasking
once unblocked or escalate.

## 7. All `done`: assemble evidence for the Safety Officer

Gather the combined `git diff` scope (all `files_touched` across
specialists) and each specialist's `tests_run` claims — these are what the
Safety Officer will independently re-check, not what it will accept as-is.

**Commit staging (learned in the field 2026-07-22):** at this point the
work is an **uncommitted working-tree diff, and that is correct.** The
Safety Officer verifies the working-tree diff scoped to the territory
files (`git diff -- <territory files>`); **the absence of a commit is
never a refutation** — the integration commit is an IC step that happens
AFTER the pass (step 9), because only verified work gets committed.
Acceptance criteria that require the commit to exist at verification time
are mis-staged (they guarantee a first halt) — if the 202/IAP contains
one, treat it as satisfied by the post-pass integration step, and fix the
staging in the next period's 202.

## 8. Spawn the Safety Officer

Spawn `dcs-safety-officer` via Task with: the period's acceptance criteria
(from `202-OBJECTIVES.md`), the IAP's verification plan, the list of
touched files, and the specialists' claims (framed explicitly as claims to
verify, not facts). Its charter (see `agents/dcs-safety-officer.md`) is to
attempt to refute completion using its own independent checks.

## 9. Handle the verdict — COMMAND POINT 4 (verdict disposition)

This is a command point (doctrine: "Transfer of command"). **If this
session is not running Fable**: spawn `dcs-commander` via Task (model
`fable`) with: the Safety Officer's verdict verbatim, the 202 acceptance
criteria, the period history from `214-LOG.md` (**scoped, v0.5.1: entries
for the CURRENT period plus the last ~20 lines — never the whole file. A
long-running Type 1's log passes 100 KB, and pasting it into every
command-point spawn buys latency, not judgment. If an earlier period is
genuinely load-bearing, quote the specific entries rather than the
file**), **the ORIGINAL goal from
`201-BRIEF.md`** (v0.3.2 — so goal drift across periods is visible to a
stateless judge: a `next_period` proposing objectives the 201 never asked
for is accretion, not convergence), and **one ESG-state line** (v0.3.2 —
whether `<esg_root>/.dcs/esg/` is founded and this incident's register
row, or "no ESG founded / no register row"; principle 14's ESG-absence
cue cannot fire on evidence the commander was never given). Its
`verdict_disposition` decision (schemas.md #6) selects the path below, and
its `directives` supply the fix-tasking content where applicable. Record it
in `214-LOG.md` (`command: verdict -> <disposition> (IC=dcs-commander)`).
**If this session is Fable**, the judgment below is yours — with the same
two inputs checked, not assumed.

**`halt` (binding — no closing over this):** append to `214-LOG.md`:
`SAFETY: halt -- <summary of refutations>`. Two paths, the IC's judgment
which fits:
- **Fix-taskings:** if the refutation is narrow (e.g. a missed edge case
  in one file), write new focused `204-TASKING/*.md` entries addressing
  exactly the refutations, spawn Ops Specialists for those, then re-run
  the Safety Officer (back to step 8).
- **Return to planning:** if the refutation reveals the plan itself was
  wrong (not just incompletely executed), treat it like a deviation —
  route to `/dcs-plan` for this period's re-plan.

**`pass`:** write/append `SAFETY.md` with the verdict **verbatim** (not
summarized or softened). Append to `214-LOG.md`:
`SAFETY: pass -- period <N> complete`.

## Escalation-trigger check — after the Safety verdict (v0.2, doctrine principle 13)

Before moving on to 9b (on `pass`) or looping back into fix-taskings /
re-plan (on `halt`), check the two verdict-time triggers:

- **Trigger (b):** this is the **second** `SAFETY: halt` entry in
  `214-LOG.md` for the same objective (same 202 goal text, not merely the
  same incident — a halt on a *different* period's objective doesn't
  count). Grep `214-LOG.md` for prior `SAFETY: halt` lines before deciding.
- **Trigger (a):** the specialists' combined `files_touched` (step 5)
  exceeds the blast radius `201-BRIEF.md` declared, in a way the IAP's
  partition table didn't already account for.

**On any escalation trigger (a/b/c/d/e/f — f is raised in `plan.md` step
4b, not here; c and d are checked at the period
boundary above, before fan-out; **(e)** is an IC-requested ESG activation,
raised via the `esg_activation` field on any command decision — doctrine
principle 14):** write
`<esg_root>/.dcs/esg/SITREPS/<slug>-p<N>.md` (v0.3: `esg_root` = the main
checkout per doctrine's "Parallel operation" — a sitrep written into a
worktree's own gitignored copy is a sitrep the ESG never sees) from
`$HOME/.claude/dcs/templates/209-SITREP.md` (create the `SITREPS/`
directory if it doesn't exist yet). Fill in status, objectives state,
safety state, resource spend, and the three options. Pause the incident —
do not proceed to 9b or back into planning yet. Ask the Owner via
`AskUserQuestion`: continue / pivot / demobilize — and for trigger (e),
**convene ESG** as the first option: mark the incident's `REGISTER.md`
row `ESCALATED` and route the Owner to `/dcs-esg`, whose agenda takes
IC-requested activations first; the Owner may still decide inline, in
which case record in the sitrep why a session wasn't needed. Record the
decision in
the sitrep's `decision`/`decided_by` fields and append to `214-LOG.md`:
`ESCALATION: trigger <a|b|c|d|e|f> -- <one-line reason> -- Owner: <decision>`.
Then proceed per the decision: **continue** resumes the normal path this
step interrupted (9b, or the fix-tasking/re-plan branch above);
**pivot** routes to `/dcs-plan` for a re-scoped period; **demobilize**
routes to `/dcs-close` with the sitrep's outcome noted (or, if objectives
were never met, treat it as an abandoned incident per `/dcs-plan` step
6b's Reject path).

## 9b. After the pass: the integration commit

Now — and only now — the IC assembles the single integration commit:

- Stage the territory files **explicitly by path** (`git add <file> ...`).
  Never `git add -A` / `git add .` — the working tree may hold unrelated
  changes from other work, and sweeping them in silently is exactly the
  drift DCS exists to prevent.
- Message references the intake source ids (e.g. `audit_results #NNN-NNN`)
  and summarizes the period's change.
- Append to `214-LOG.md`: `integration commit <short sha> (<n> files)`.

Then assess against `202-OBJECTIVES.md`:
- **Goal fully met:** tell the Owner to run `/dcs-close` (which verifies
  this commit mechanically).
- **Partially met / more work identified:** offer the next operational
  period — loop back to `/dcs-plan`'s step 2 (fresh 202 for period N+1),
  noting what remains.

## 10. Report

Summarize what ran, what the Safety Officer found, and the exact next
command.

</process>
