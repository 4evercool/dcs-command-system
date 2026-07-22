<purpose>
Gated execution: verify the approval marker is still valid, fan out Ops
Specialists against their 204 taskings, handle deviations by returning to
planning, and spawn the Safety Officer for a binding verdict before the
period can be considered complete.
</purpose>

<required_reading>
@$HOME/.claude/icc/references/doctrine.md
@$HOME/.claude/icc/references/schemas.md
</required_reading>

<process>

## 1. Verify incident state

```bash
cat "<project>/.icc/ACTIVE"
```

If no `ACTIVE`, or `phase` is not `execution`: stop. If `phase` is
`planning`, tell the Owner to finish `/icc-plan` first. If there's nothing
active, there's nothing to execute.

## 2. Verify the approval marker — do this even though the hook also checks it

```bash
python -c "import hashlib; print(hashlib.sha256(open(r'<incident_dir>/IAP.md','rb').read()).hexdigest())"
```

Compare against the first line of `<incident_dir>/IAP-APPROVED`. If the
file is missing, or the hash doesn't match: **stop.** Tell the Owner the
IAP needs re-approval — someone edited `IAP.md` after it was approved (or
it was never approved). Do not spawn any specialist and do not attempt any
edit yourself. Route to `/icc-plan`.

This check is redundant with `icc_gate.py` by design: the hook is the
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

## 4. Fan out Ops Specialists

Up to 4 `icc-ops-specialist` subagents, each given **exactly one**
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
this session is not running Fable**: spawn `icc-commander` via Task (model
`fable`) with the triggering specialist's full return, the current 202 and
its 204, and the execution state; its `deviation` decision (schemas.md #6)
governs the disposition — `replan` / `amend_tasking` / `escalate_owner` —
and is recorded in `214-LOG.md` (`command: deviation -> <disposition>
(IC=icc-commander)`). **If this session is Fable**, make the call yourself.
Then: update `202-OBJECTIVES.md` and/or the relevant `204-TASKING/*.md` to
reflect what was actually learned — incorporate the specialist's `proposal`
per the IC's directives (use `AskUserQuestion` if the disposition is
`escalate_owner` — the right call is genuinely the Owner's judgment, not
just a mechanical correction). This edit to the plan changes `IAP.md`'s content in the next
`/icc-plan` pass — its hash will differ from `IAP-APPROVED`, which
**mechanically** voids the current approval; that's the deviation doctrine
working as intended, not a bug to route around. Append to `214-LOG.md`:
`deviation reported by <ID>: <one-line summary> -- returning to planning`.
Tell the Owner to run `/icc-plan` again.

**Any `status: "blocked"`:** report the blocker to the Owner — this is an
external obstacle (missing credential, environment issue), not necessarily
a planning defect. The IC decides with the Owner whether to re-tasking
once unblocked or escalate.

## 7. All `done`: assemble evidence for the Safety Officer

Gather the combined `git diff` scope (all `files_touched` across
specialists) and each specialist's `tests_run` claims — these are what the
Safety Officer will independently re-check, not what it will accept as-is.

## 8. Spawn the Safety Officer

Spawn `icc-safety-officer` via Task with: the period's acceptance criteria
(from `202-OBJECTIVES.md`), the IAP's verification plan, the list of
touched files, and the specialists' claims (framed explicitly as claims to
verify, not facts). Its charter (see `agents/icc-safety-officer.md`) is to
attempt to refute completion using its own independent checks.

## 9. Handle the verdict — COMMAND POINT 4 (verdict disposition)

This is a command point (doctrine: "Transfer of command"). **If this
session is not running Fable**: spawn `icc-commander` via Task (model
`fable`) with the Safety Officer's verdict verbatim, the 202 acceptance
criteria, and the period history from `214-LOG.md`; its
`verdict_disposition` decision (schemas.md #6) selects the path below, and
its `directives` supply the fix-tasking content where applicable. Record it
in `214-LOG.md` (`command: verdict -> <disposition> (IC=icc-commander)`).
**If this session is Fable**, the judgment below is yours.

**`halt` (binding — no closing over this):** append to `214-LOG.md`:
`SAFETY: halt -- <summary of refutations>`. Two paths, the IC's judgment
which fits:
- **Fix-taskings:** if the refutation is narrow (e.g. a missed edge case
  in one file), write new focused `204-TASKING/*.md` entries addressing
  exactly the refutations, spawn Ops Specialists for those, then re-run
  the Safety Officer (back to step 8).
- **Return to planning:** if the refutation reveals the plan itself was
  wrong (not just incompletely executed), treat it like a deviation —
  route to `/icc-plan` for this period's re-plan.

**`pass`:** write/append `SAFETY.md` with the verdict **verbatim** (not
summarized or softened). Append to `214-LOG.md`:
`SAFETY: pass -- period <N> complete`. Assess against `202-OBJECTIVES.md`:
- **Goal fully met:** tell the Owner to run `/icc-close`.
- **Partially met / more work identified:** offer the next operational
  period — loop back to `/icc-plan`'s step 2 (fresh 202 for period N+1),
  noting what remains.

## 10. Report

Summarize what ran, what the Safety Officer found, and the exact next
command.

</process>
