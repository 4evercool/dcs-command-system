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
`planning`, tell the Owner to finish `/dcs-plan` first.

**Command-chain check (entry gate):** confirm both entries exist —
`grep -n "command: typed" <incident_dir>/214-LOG.md` and `grep -n
"command: iap_review" <incident_dir>/214-LOG.md`. If either returns
nothing, the chain was skipped upstream — **stop**, route to `/dcs-plan`.

## 2. Verify the approval marker — redundant with dcs_gate.py by design

```bash
python -c "
import hashlib
raw = open(r'<incident_dir>/IAP.md', 'rb').read()
lf = raw.replace(b'\r\n', b'\n')
crlf = lf.replace(b'\n', b'\r\n')
print({hashlib.sha256(v).hexdigest() for v in (raw, lf, crlf)})
"
```

Compare `<incident_dir>/IAP-APPROVED` line 1 against this set — valid if
it matches **any member**. If missing or no match: **stop**, route to
`/dcs-plan` (the IAP was edited after approval).

## 3. Read the plan

Read `IAP.md` and every `204-TASKING/*.md`. Confirm the partition table's
execution mode (parallel / sequential / worktree-isolated).

## 3.5. Type 1: offer the deterministic variant

If the incident is Type 1, ask the Owner (`AskUserQuestion`) whether to
execute via the standard Agent-tool fan-out or emit a deterministic
Workflow script instead. Record the choice via `python "$HOME/.claude/dcs/tools/dcs_log.py" append <slug> --by <operator> "<text>"`. If the script
path is chosen, adapt — the deviation/Safety Officer gates below still apply.

## Escalation-trigger check — period boundary (doctrine principle 13)

Before spawning any specialist, check trigger (c): read `esg.max_periods_before_review` from `<project>/.dcs/config.json` (default `3`).
Count ATTEMPTS: the number of `IAP-APPROVED:` sentinel entries in `214-LOG.md` (recognized per `dcs_gate.py`'s grammar: "An entry begins at column zero with a mandatory bracketed timestamp; any other line is a continuation, never a sentinel, and quoting a whole prior entry inside a body requires indenting it off column zero."). If the attempt about to run exceeds the threshold, skip to "On any escalation trigger" below instead of step 4.

Also check trigger (d): if `<esg_root>/.dcs/esg/DELEGATION.md` is in force
and the IAP's territory touches a `forbidden_globs` entry not caught at
plan time, treat it the same way — do not fan out.
## 4. Fan out Ops Specialists

Up to 4 `dcs-ops-specialist` subagents, each given exactly one
`204-TASKING/{{ID}}.md` file's content plus the relevant IAP excerpt —
not the whole IAP, and not any other specialist's tasking.

Compute `worktree_root` from `git worktree list --porcelain`: match
`refs/heads/dcs/<slug>`, take the preceding `worktree` line.

Each specialist returns JSON per schemas.md #4 (ops-specialist return):
`status` (`"done"`|`"blocked"`|`"deviation"`), `files_touched` (string[],
subset of territory), `tests_run` (string[]), `evidence` (string),
`deviation` (object|null; required when `status` is `"deviation"`, with
keys `found`/`why_plan_wrong`/`proposal`).

- **Parallel:** only when the partition table shows disjoint territories.
- **Sequential:** when the IAP declared overlap-with-justification.
- **Worktree-isolated:** only when the IAP declares `isolation: worktree`
  for a specialist — set up that specialist's worktree per new.md step 7b
  before spawning it, and merge/reconcile after it returns.

**Re-tasking a specialist is a fresh spawn (doctrine principle 9b).** Never
resume the previous agent — it holds the old tasking; spawn a new
`dcs-ops-specialist` with the amended tasking file's full content.

**Command-point spawns (steps 6, 9 — doctrine "never a silent wait"):**
announce before spawning; a return with no decision block is a failed spawn
— re-spawn immediately.

## 5. Collect and validate structured returns

Validate each return: confirm a JSON block is present, all required fields
per schemas.md #4 (ops-specialist return): `status`, `files_touched`, `tests_run`, `evidence`,
`deviation` — required when `status` is `"deviation"`) are present, no
extra fields. Check `files_touched` against declared `territory` — any
file outside territory is a violation.

## 6. Handle non-`done` returns — COMMAND POINT 3 (deviation arbitration)

**Any `status: "deviation"`:** stop the execution phase. This is a command
point. **If not running Fable**: spawn `dcs-commander` via Task (model
`fable`) with the triggering specialist's full return, the current 202 and its
204, and execution state — for established facts, pass their source, never a
summary from memory. Its decision (schemas.md #6, commander decisions)
governs: `replan` / `amend_tasking` / `escalate_owner`. **If this session is
Fable**, make the call yourself. Use `AskUserQuestion` when the disposition is
`escalate_owner` — the right call is genuinely the Owner's judgment, not just
a mechanical correction. Record via `dcs_log.py append <slug> --by <operator> "<text>"`. Update `202-OBJECTIVES.md`
and/or the relevant `204-TASKING/*.md` to reflect what was learned — editing
the plan voids the approval mechanically (the deviation doctrine working as
intended). Append via `dcs_log.py append <slug> --by <operator> "deviation reported by <ID>: <summary> -- returning to planning"`. Tell the Owner to run `/dcs-plan` again.

**Any `status: "blocked"`:** report the blocker to the Owner — this is an
external obstacle, not necessarily a planning defect.

## 7. All `done`: assemble evidence for the Safety Officer

Gather the combined `git diff` scope (all `files_touched`) and each
specialist's `tests_run` claims — the Safety Officer independently
re-checks, not accepts. The work is an **uncommitted working-tree diff**;
the integration commit happens after the pass (step 9b); acceptance
criteria requiring a commit at verification time are mis-staged.

## 8. Spawn the Safety Officer

Spawn `dcs-safety-officer` via Task with: the period's acceptance criteria
(from `202-OBJECTIVES.md`), the IAP's verification plan, the list of
touched files, and the specialists' claims (framed as claims to verify, not
facts). **On a re-spawn** (step 9's `halt` branch routing fix-taskings
back here), also hand it the **prior verdict (verbatim)** and a
**changed-since manifest** (`git diff --name-only` of what fix-taskings
touched since that verdict). **Spawn-liveness fallback:** an empty,
errored, or no-decision return never returns a verdict — a FAILED spawn,
not a slow one: re-spawn on the next tier, log BOTH attempts, and never
treat either as "Safety verification happened."

The Safety Officer returns JSON per schemas.md #5 (safety-officer verdict):
`verdict` (`"pass"`|`"halt"`), `refutations` (object[]), `advisories`
(object[], optional), `checked` (string[]) — advisory/refutation bar per
`agents/dcs-safety-officer.md` step 6.

## 9. Handle the verdict — COMMAND POINT 4 (verdict disposition)

Validate the Safety Officer return: confirm a JSON block is present, all
required fields per schemas.md #5 (safety-officer verdict): `verdict`, `refutations`, `checked`;
`advisories` is optional) are present, no extra fields. Missing required
field or structural non-JSON = deviation — re-spawn (`agents/dcs-safety-officer.md` step 6).

**Preflight — Channel A:** run `grep -c halt_cycles
"<project>/.claude/hooks/dcs_gate.py"`; `0` means **phantom ceiling** —
note via `dcs_log.py append <slug> --by <operator> "<text>"` and treat halt count as **advisory**
(`agents/dcs-safety-officer.md` step 6).

This is a command point. **If not running Fable**: spawn `dcs-commander`
via Task (model `fable`) with: the Safety Officer's verdict verbatim, the
202 acceptance criteria, the period history from `214-LOG.md` (**scoped:
current period entries plus last ~20 lines**), the **original goal from
`201-BRIEF.md`** (so goal drift is visible), and **one ESG-state line,
sourced not summarized** (whether `<esg_root>/.dcs/esg/` is founded, plus
this incident's row from `REGISTER.md`, or "no ESG founded / no register
row"). Its `verdict_disposition` decision (schemas.md #6, commander decisions) selects the path
below. **If this session is Fable**, make the call yourself.

**`halt` (binding):** append to `214-LOG.md` via `dcs_log.py append <slug> --by <operator> --sentinel halt "<summary of refutations>"`.
Read the count: `python "<project>/.claude/hooks/dcs_gate.py" --halt-count
"<incident_dir>"`. Two paths:
- **Fix-taskings:** narrow refutation with room left: write focused
  `204-TASKING/*.md` entries, spawn Ops Specialists, re-run the Safety
  Officer (step 8). A fix touching only `204-TASKING/*.md` needs no
  re-stamp; a fix changing `IAP.md` routes through `plan.md` step 6c. If
  the next iteration would hit the ceiling, this path is **unavailable**.
- **Return to planning:** if the refutation reveals the plan itself was
  wrong, route to `/dcs-plan`.

**Convergence read — MANDATORY from the second halt on one objective
(doctrine principle 13, trigger (b)).** Classify new refutations against
the previous halt's:
- **Same class** — fix closed named instances, officer found another of the
  same kind. **Lead with raising the altitude** (a guard that makes the
  whole class unrepresentable); say plainly site-by-site has no bounded end.
- **Different class** — genuinely new ground; complex but converging.
State the read in one sentence the Owner can act on.

**`pass`:** write/append `SAFETY.md` with the verdict **verbatim**. Append to `214-LOG.md` via `dcs_log.py append <slug> --by <operator> --sentinel pass "period <N> complete"`.

**Advisories on a pass:** a `pass` carrying `advisories[]` is normal. The IC
fixes them now, folding into the integration commit at 9b — they are
artifact edits inside territory; routing through fix-taskings wastes a
cycle. Record each in `SAFETY.md`. **If a fix touches `IAP.md`'s own
content**, the marker goes stale — route through `plan.md` step 6c.
Advisories confined to territory files need no re-stamp. **Never upgrade
an advisory to a halt** (`agents/dcs-safety-officer.md` step 6).

## Escalation-trigger check — after the Safety verdict (doctrine principle 13)

Before 9b (on `pass`) or looping back (on `halt`), check verdict-time triggers:

- **Trigger (b):** second `SAFETY-HALT:` entry in `214-LOG.md` for the
  same objective (same 202 goal text). Grep for prior `SAFETY-HALT:` lines.
- **Trigger (a):** combined `files_touched` exceeds the blast radius
  `201-BRIEF.md` declared, unaccounted for in the partition table.

**On any escalation trigger (a/b/c/d/e/f):** write
`<esg_root>/.dcs/esg/SITREPS/<slug>-p<N>.md` from
`$HOME/.claude/dcs/templates/209-SITREP.md` (resolve `esg_root` per
doctrine's "Parallel operation"). Fill in status, objectives, safety,
resource spend, and the three options. Pause — ask the Owner via
`AskUserQuestion`: continue / pivot / demobilize. For trigger (e),
**convene ESG** as first option: mark the `REGISTER.md` row `ESCALATED`,
route to `/dcs-esg`. Record the decision in the sitrep and append via `dcs_log.py append <slug> --by <operator> "ESCALATION: trigger <a|b|c|d|e|f> -- <reason> -- Owner: <decision>"`. Proceed per the decision: **continue** resumes; **pivot**
routes to `/dcs-plan`; **demobilize** routes to `/dcs-close` (or treat as
abandoned per `/dcs-plan` step 6b).

## 9b. After the pass: the integration commit

Stage territory files **explicitly by path** (`git add <file> ...`). Never
`git add -A` / `git add .`. Message references intake source ids and
summarizes the period's change. Append via `dcs_log.py append <slug> --by <operator> "integration commit <short sha> (<n> files)"`.

Assess against `202-OBJECTIVES.md`:
- **Goal fully met:** tell the Owner to run `/dcs-close`.
- **Partially met: CLOSE AND REQUEUE is the default; another period is the
  exception that must be argued.** A Safety-passed period holds proven work.
  Keeping the incident open keeps it in a branch — unmerged, unshipped, and
  fixing nothing. Only keep open when the remaining work is genuinely
  inseparable (schema change whose readers are not yet updated, contract
  half-migrated). State which via `dcs_log.py append <slug> --by <operator> "<text>"`. (field lesson 2026-07-24 —
  `dcs/references/doctrine-appendix.md`, "Workflow field lessons", W3)

## 10. Report

Summarize what ran, what the Safety Officer found, and the exact next
command.

</process>
