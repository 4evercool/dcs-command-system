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

**Command-chain check (entry gate):** confirm both entries exist —
`grep -n "command: typed" <incident_dir>/214-LOG.md` and `grep -n
"command: iap_review" <incident_dir>/214-LOG.md`. If either returns
nothing, the command chain was skipped somewhere upstream — **stop**,
route to `/dcs-plan`, whose own entry gate and pre-stamp checklist will
repair the chain. Do not fan out specialists on an unratified plan even
if the approval marker is technically valid.

## 2. Verify the approval marker — do this even though the hook also checks it

```bash
python -c "
import hashlib
raw = open(r'<incident_dir>/IAP.md', 'rb').read()
lf = raw.replace(b'\r\n', b'\n')
crlf = lf.replace(b'\n', b'\r\n')
print({hashlib.sha256(v).hexdigest() for v in (raw, lf, crlf)})
"
```

Compare the first line of `<incident_dir>/IAP-APPROVED` against this set —
valid if it matches **any member** of it. The set holds up to three digests
(raw bytes, LF-normalised, and CRLF-normalised derived from the LF form) and
fewer when those forms coincide: a pure-LF file yields two, since `raw` and
`lf` are the same bytes. If the file is missing, or the stored hash matches
no member: **stop.** Tell the Owner the IAP
needs re-approval — someone edited `IAP.md` after it was approved (or it
was never approved). Do not spawn any specialist and do not attempt any
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
key (default `3` if unset or the key is absent).

**Count ATTEMPTS, not periods (v0.5.12).** An attempt is any stamped IAP
this incident has executed — so period 2 attempt 1 and period 1 revision
3 both count, and the tally is simply the number of `IAP-APPROVED:`
sentinel entries (v0.6.9 — the same sentinel `dcs_gate.py` anchors the
halt ceiling on, recognized only through `dcs_gate.py`'s own published
grammar (`GRAMMAR_LINE`): "An entry begins at column zero with a mandatory
bracketed timestamp; any other line is a continuation, never a sentinel,
and quoting a whole prior entry inside a body requires indenting it off
column zero." — see `references/doctrine.md` principle 13) in
`214-LOG.md`. If the attempt
about to run exceeds the threshold, this attempt **is** the mandatory
escalation — do not fan out; skip to "On any escalation trigger" below
instead of step 4. Counting periods alone let a real incident run four
revisions of period 1 without ever tripping the cap (v0.5.12 field
lesson) — a re-plan is exactly as much evidence of trouble as a new
period, and usually more.

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

Compute `worktree_root` from `git worktree list --porcelain` — match the
branch line `refs/heads/dcs/<slug>`, then take the preceding `worktree`
line (its absolute path). Pass it to every specialist so territory globs
resolve relative to the incident's actual checkout.

Each specialist returns JSON per schemas.md #4 (ops-specialist return):
`status` (`"done"`|`"blocked"`|`"deviation"`), `files_touched` (string[],
subset of territory), `tests_run` (string[]), `evidence` (string),
`deviation` (object|null; required when `status` is `"deviation"`, with
keys `found`/`why_plan_wrong`/`proposal`).

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

**Re-tasking a specialist is a fresh spawn (v0.5.8, doctrine principle
9b).** Whenever a specialist must go again — a fix-tasking after a Safety
halt, an amended 204 after a deviation, a correction of any kind — spawn
a **new** `dcs-ops-specialist` with the amended tasking file's full
content. Never resume the previous agent: it still holds the OLD
tasking, so an amended territory gets edited against the stale one, and
every individual edit looks in-bounds to the gate for the tasking that
agent remembers. `dcs_gate.py` denies `SendMessage` while an incident is
active precisely to make this impossible rather than merely forbidden.

**Command-point spawns at steps 6 and 9 follow doctrine's "never a silent
wait" rule (v0.5.10):** announce the spawn before making it (no file
changes until it returns — a command-point agent writes nothing by
design), and treat a return with no decision block as a **failed spawn**,
not a slow one — re-spawn on the next tier immediately and log both
attempts. The same applies to a specialist or Safety Officer that returns
without its structured block: re-spawn, never wait, never resume.

## 5. Collect and validate structured returns

Validate each return before proceeding: confirm a JSON block is present,
all required fields per schemas.md #4 (ops-specialist return): `status`, `files_touched`,
`tests_run`, `evidence`, `deviation` — required when `status` is
`"deviation"`) are present, and no fields outside the schema appear.
Missing required field or structural non-JSON = deviation — handle per
step 6 as a deviation return. Check `files_touched` against that
specialist's declared `territory` — any file outside territory is itself a
violation worth flagging to the Owner even if the specialist didn't
self-report it as a deviation.

## 6. Handle non-`done` returns — COMMAND POINT 3 (deviation arbitration)

**Any `status: "deviation"`:** stop the execution phase here. Do not spawn
remaining specialists beyond ones already safely completed on disjoint
territory. This is a command point (doctrine: "Transfer of command"). **If
this session is not running Fable**: spawn `dcs-commander` via Task (model
`fable`) with the triggering specialist's full return, the current 202 and
its 204, and the execution state — for any fact a prior seat already
established (what a specialist's own structured return already said it
touched, what an earlier command point already decided), pass its source
(the file path and line range, or the command that regenerates it), never
a summary retyped from memory; its `deviation` decision (schemas.md #6, commander decisions)
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
Tell the Owner to run `/dcs-plan` again — `amend_tasking`, `replan`, and
`escalate_owner` may all reach the proportionate route at `plan.md` step
6c, cited there by this entry's own timestamp; 6c's own boundary
conditions decide whether this specific amendment actually qualifies, and
the full steps-1-9 path runs unchanged for anything that doesn't.

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
verify, not facts). **On a re-spawn** (step 9's `halt` branch routing a
fix-taskings iteration back here), also hand it, framed the same way —
claims to verify, not facts: the **prior verdict (verbatim)** (this
period's earlier Safety Officer return(s), unabridged) and a
**changed-since manifest** (`git diff --name-only` of what the
fix-taskings touched since that verdict) — a second officer cannot cite
what it was never given. Its charter (see `agents/dcs-safety-officer.md`)
is to attempt to refute completion using its own independent checks.

The Safety Officer returns JSON per schemas.md #5 (safety-officer verdict):
`verdict` (`"pass"`|`"halt"`), `refutations` (object[]), `advisories`
(object[], optional), `checked` (string[]) — advisory/refutation bar per `agents/dcs-safety-officer.md` step 6.

## 9. Handle the verdict — COMMAND POINT 4 (verdict disposition)

Validate the Safety Officer return before proceeding to disposition: confirm
a JSON block is present, all required fields per schemas.md #5 (safety-officer verdict): `verdict`,
`refutations`, `checked`; `advisories` is optional) are present, and no
fields outside the schema appear. Missing required field or structural
non-JSON = deviation — re-spawn the Safety Officer rather than proceeding to
disposition. Advisory/refutation bar: `agents/dcs-safety-officer.md` step 6.

**Preflight — Channel A: confirm this project's gate carries the halt
ceiling before relying on it.** A package update refreshes
`dcs/workflows`/`dcs/references`, never the project's own copy of the hook
— only `/dcs-init` places `<project>/.claude/hooks/dcs_gate.py`. Run
`grep -c halt_cycles "<project>/.claude/hooks/dcs_gate.py"`; `0` means no
counter (a **phantom ceiling**). Say so in one named `214-LOG.md` line
(`halt ceiling: advisory -- dcs_gate.py has no halt_cycles counter, run
/dcs-init`) and treat the count below as **advisory** (per `agents/dcs-safety-officer.md` step 6), not enforced.

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
for is accretion, not convergence), and **one ESG-state line, sourced not
summarized** (v0.3.2 — whether `<esg_root>/.dcs/esg/` is founded, plus
this incident's own row quoted directly from
`<esg_root>/.dcs/esg/REGISTER.md` rather than paraphrased from memory, or
"no ESG founded / no register row" confirmed the same way; principle 14's
ESG-absence cue cannot fire on evidence the commander was never given,
and a retyped row is exactly the fact Rec 2 exists to keep sourced). Its
`verdict_disposition` decision (schemas.md #6, commander decisions) selects the path below, and
its `directives` supply the fix-tasking content where applicable. Record it
in `214-LOG.md` (`command: verdict -> <disposition> (IC=dcs-commander)`).
**If this session is Fable**, the judgment below is yours — with the same
two inputs checked, not assumed.

**`halt` (binding — no closing over this):** append to `214-LOG.md`:
```
[<timestamp>] SAFETY-HALT: <summary of refutations>
```
Before choosing a path, read
the count: `python "<project>/.claude/hooks/dcs_gate.py" --halt-count
"<incident_dir>"` — the gate's eventual denial is a **backstop, not the
way one learns the news**. Two paths, the IC's judgment which fits:
- **Fix-taskings:** narrow refutation (e.g. one file's missed edge case)
  and the count leaves room: write focused `204-TASKING/*.md` entries,
  spawn Ops Specialists, re-run the Safety Officer (step 8). A fix whose
  content stays inside a `204-TASKING/*.md` file leaves `IAP.md` untouched
  and needs no re-stamp at all; a fix that also changes `IAP.md`'s own
  content (an IC-owned criterion, a partition-table line) does need one,
  and that re-stamp routes through `plan.md` step 6c, citing this
  `command: verdict -> fix_taskings` entry by timestamp, subject to 6c's
  own boundary conditions. If the next
  iteration would hit the ceiling instead, this path is **unavailable** —
  only a fresh IAP stamp resets it (`plan.md` step 8); an Owner "continue"
  at trigger (b) below is a decision, not a reset.
- **Return to planning:** if the refutation reveals the plan itself was
  wrong (not just incompletely executed), treat it like a deviation —
  route to `/dcs-plan` for this period's re-plan.

**Convergence read — MANDATORY from the second halt on one objective
(v0.5.9).** Trigger (b) already pauses here; what it lacked was a
*diagnosis*, so the same "continue" answer could be given four times.
Before presenting options, the IC must classify the new refutations
against the previous halt's and record the verdict in the 209 and
`214-LOG.md`:

- **Same class** — the fix closed the named instances and the officer
  found another of the same kind (a defect of **form**, not of site).
  This is whack-a-mole against an unbounded population, and each further
  pass costs a full execute+verify cycle to remove one instance. The
  options presented to the Owner must therefore **lead with raising the
  altitude of the fix** — an instrumental or general guard that makes the
  whole class unrepresentable (a lint, a test over the enumeration, a
  type, an invariant) — and must say plainly that continuing site-by-site
  has no bounded end. "Continue with fix-taskings" is still offered, but
  never first and never unqualified.
- **Different class** — genuinely new ground each time; the incident is
  complex but converging. Say so, and continuing is the reasonable
  default.

State the read in one sentence the Owner can act on: *"halt N is the same
class as halt N-1 — the population is unenumerated, so the fix belongs at
the guard level, not the site level."* This read used to depend entirely
on someone asking for it; the halt-count ceiling in step 9's `halt` branch
now backs it with a mechanical stop, so a same-class rotation ends even if
nobody does.

**`pass`:** write/append `SAFETY.md` with the verdict **verbatim** (not
summarized or softened). Append to `214-LOG.md`:
```
[<timestamp>] SAFETY-PASS: period <N> complete
```

**Advisories on a pass (v0.6.5):** a `pass` carrying `advisories[]` is a
normal, healthy verdict — the deliverable is sound and the paperwork
needs a touch-up. This is the default the bar sets
(`agents/dcs-safety-officer.md` step 6): an artifact-hygiene finding is
an advisory unless it clears one of that step's bars. **The IC fixes
them itself, now**, folding them into the integration commit at 9b: they
are artifact edits (a stale count in a docstring, a hash in a comment,
an un-regenerable census in an AAR), they are inside the incident's own
territory, and routing them through a fix-tasking would spend an
execute-and-verify cycle on prose. Record each advisory and its
resolution in `SAFETY.md`, and re-verify nothing — the officer already
passed the criteria. **Never upgrade an advisory to a halt** to be
thorough; the halt is the only lever that stops a merge and its value
comes entirely from being reserved.

**If any advisory's fix touches `IAP.md`'s own content** (not just a file
inside a `204-TASKING/*.md` territory): folding it in still changes
`IAP.md` the same way any edit does, and the marker goes stale the moment
it's saved — the gate then denies every further non-`.dcs/**` edit,
including the close-time memory-routing write into whatever memory store
the project's `CLAUDE.md` documents, until re-stamped.
Do not fix it "now" and move on as if nothing needs re-approval: route
that specific fix through `plan.md` step 6c, citing this pass's
already-logged `command: verdict -> close` / `-> next_period` entry by
timestamp — 6c's cheap path re-stamps without re-running the Safety
Officer, since nothing about the criteria was refuted. Advisories confined
to territory files never touch the marker and need no re-stamp at all.

## Escalation-trigger check — after the Safety verdict (v0.2, doctrine principle 13)

Before moving on to 9b (on `pass`) or looping back into fix-taskings /
re-plan (on `halt`), check the two verdict-time triggers:

- **Trigger (b):** this is the **second** `SAFETY-HALT:` entry in
  `214-LOG.md` for the same objective (same 202 goal text, not merely the
  same incident — a halt on a *different* period's objective doesn't
  count). Grep `214-LOG.md` for prior `SAFETY-HALT:` lines before deciding.
  The halt ceiling checked in step 9's `halt` branch above is a separate,
  mechanical thing: it works whether or not this trigger fired, and
  whether or not the Owner was ever asked.
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
- **Partially met / more work identified: CLOSE AND REQUEUE is the
  default (v0.5.12); another period is the exception that must be
  argued.** A Safety-passed period holds *proven* work. Keeping the
  incident open keeps that work in a branch — unmerged, unshipped, and
  fixing nothing — for as long as the remaining scope takes. Field
  lesson 2026-07-24, in the incident's own AAR: period 1 produced a
  Safety-passed fix for a bug that was actively corrupting production
  data, and *"that fix then sat in a branch. A fix that is not shipped
  fixes nothing, and the defect kept corrupting production data the whole
  time"* — a second period existed only to make the first one shippable.

  So: **close the incident, merge, ship, and register the remainder as a
  follow-up incident** whose 201 evidence is this incident's AAR (a cheap
  stem — the investigation is already done). Only keep the incident open
  for another period when the remaining work is genuinely inseparable —
  the delivered part **cannot** be merged or shipped on its own (a schema
  change whose readers are not yet updated, a contract half-migrated).
  State which of those it is in `214-LOG.md`; "there is more to do" is
  not by itself a reason, because that is what the register is for.

## 10. Report

Summarize what ran, what the Safety Officer found, and the exact next
command.

</process>
