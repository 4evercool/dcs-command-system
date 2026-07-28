<purpose>
The planning arc of the P-loop: objectives, chief-authored tactics and
tasking partition, integration into a single IAP, Owner approval, and a
hash-stamped approval marker that opens the gate for /dcs-execute.
</purpose>

<required_reading>
@$HOME/.claude/dcs/references/doctrine.md
@$HOME/.claude/dcs/references/schemas.md
@$HOME/.claude/dcs/references/forms.md
</required_reading>

<process>

## 1. Verify incident state

```bash
cat "<project>/.dcs/ACTIVE"
```

Parse `<slug>|<type>|<phase>`. If no `ACTIVE` file: stop, tell the Owner
there's no open incident — run `/dcs-new` first. If `phase` is
`execution`: this incident already has (or had) an approved IAP for the
current period. **First check whether this is a `## 6c.` amendment:** if
`214-LOG.md` holds a qualifying command-point-3/4 entry and `## 6c.`'s own
boundary conditions hold for the intended change, go there now instead of
proceeding to step 2 — `## 6c.` states its own entry types and conditions,
not restated here. Otherwise, ask the Owner whether they mean to revise
the plan (counts as a re-plan — proceed, but flag that this will void the
current approval once IAP.md changes) or actually meant `/dcs-status` /
`/dcs-execute`.

Determine the operational period number `N` — 1 if this is the first pass
through this step for this incident, else increment from the last period
recorded in `214-LOG.md`.

**Command-chain check (entry gate — do this before drafting anything):**
read `214-LOG.md` and confirm a `command: typed` entry exists (command
point 1). If it is missing, the Dispatcher in `/dcs-new` typed the
incident itself — a doctrine violation observed repeatedly in the field
(three times on day one, always by the weakest-model dispatcher, always
in its own voice: "this is clearly a Type N"). Repair NOW, before any
202 work: run command point 1 properly (spawn `dcs-commander` with the
201 text if this session is not Fable; decide yourself if it is), log
the decision, and if the commander's type differs from what the 201
recorded, correct the 201 and re-confirm with the Owner. Do not carry an
unratified typing decision into planning — the whole activation level
(chiefs, ceremony, approval requirements) hangs off it.

## 2. Draft 202-OBJECTIVES.md

Read `201-BRIEF.md`. Draft the goal (outcome-shaped) and numbered,
verifiable acceptance criteria using
`$HOME/.claude/dcs/templates/202-OBJECTIVES.md`. If this is a re-plan after
a deviation (see step 6 of `execute.md`), fold the deviation's `proposal`
into the goal/criteria explicitly rather than pretending it's a fresh
period with no history.

**Delegation-aware confirm (v0.5):** if the incident is Type 3 (from
`.dcs/ACTIVE`, step 1) AND `<project>/.dcs/esg/DELEGATION.md`'s latest
(highest `version`) `delegation-bounds` block has `auto_approve_type3:
true`, skip the `AskUserQuestion` below — write the draft straight to
`202-OBJECTIVES.md` and append to `214-LOG.md`: `202 confirm deferred to
IAP approval (Delegation v<N>)`. The Owner's first look at these
objectives is then the single delegated prompt at step 6b, if that step's
bound check fails; if it doesn't fail, the IAP auto-approves and the
objectives never need a separate look — that is the point of the
Delegation. Otherwise (Type 1, no Delegation, `auto_approve_type3` absent
or `false`) present the draft to the Owner via `AskUserQuestion` for a
quick confirm/edit as before — a lightweight check (forms.md: 202 is
authored by IC **+ Owner**), not the full IAP approval gate that comes
later. Either way, write the confirmed (or auto-passed) version to
`202-OBJECTIVES.md` in the incident directory.

## 3. Spawn the Planning Chief (and Logistics Chief for Type 1)

Spawn `dcs-planning-chief` via Task, passing **only** the full text of
`201-BRIEF.md` and `202-OBJECTIVES.md` inline in the prompt (not file
paths — the chief's information diet is deliberately restricted to what
these two files contain, per its agent charter). For Type 1, also spawn
`dcs-logistics-chief` in the same message with the same two files' text
(both can run in parallel — they don't depend on each other's output).

If this is a re-plan triggered by a deviation, also include the
triggering specialist's `found` / `why_plan_wrong` / `proposal` fields in
the Planning Chief's prompt.

**Every revision is a FRESH spawn, never a resumed agent (v0.5.5).** When
a chief's return is sent back — for lint defects (4a), for an IC
`reject`'s `required_changes`, or for any revision — spawn a **new**
chief and put everything it needs in the new prompt: the 201 + 202 text
as always, plus the specific defects or required changes verbatim, plus
any earlier revision's decisions that must survive. Do **not** continue
the previous chief agent through a message-resume, however economical it
looks on revision 3.

The reason is principle 5, not tidiness: a resumed agent's reasoning
lives in its own transcript, which **no incident artifact records**.
Resume it and the chief's information diet stops being "exactly 201 +
202 + these named corrections" and becomes "those, plus an unarchived
conversation" — so a later session reading the incident directory cannot
reconstruct why revision 3 said what it said, and the IC reviewing at
command point 2 can no longer state what the chief was actually working
from. The paper trail is the only channel that survives a context reset;
an agent transcript is not part of it. A fresh spawn also costs less
wall-clock than it appears — resumed agents run asynchronously in the
background, which is why a resume reads as a hang.

If carrying a revision forward needs more than a few lines of context,
that is a signal the 202 is unstable — see 4b's repeated-reject trigger.

## 4. Validate the returns — COMMAND POINT 2 (IAP acceptance)

From the Planning Chief: `objectives_feedback`, `tactics[]`, `taskings[]`,
`partition_ok`, `risks[]`, `verification_plan` (schema in
`references/schemas.md` #2, chief plan).

### 4a. Tasking lint — mechanical, run BEFORE the command point (v0.5.1)

These checks are arithmetic on the chief's structured return, not
judgment. Run them yourself; a failure is **yours to fix or re-spawn the
chief over — never a reason to spend a command point.** Field lesson
2026-07-23: an entire IAP review cycle (the IC's second REJECT on one
incident) was consumed by defects in this list, and the IC's own verdict
was that both were *Dispatcher transcription errors, not the chief's*.

1. **Self-contradiction** — for every tasking, `territory ∩ forbidden`
   must be empty. A tasking naming a file in both directs a specialist to
   edit what it is forbidden to touch, forcing either a partition
   violation or a mid-execution deviation.
2. **Orphaned deliverables** — every deliverable named anywhere in
   `tactics[]`, `verification_plan`, or a Logistics-chief plan must map to
   an existing tasking `id`. A deliverable assigned to a tasking that
   doesn't exist in *this* revision (e.g. carried over from a superseded
   plan) has no owner and will silently not happen.
3. **Unassigned occurrences** — when the plan says "replace/remove X",
   `grep` for X yourself: every occurrence must fall inside exactly one
   tasking's `territory`. Occurrences in no territory are unowned work;
   occurrences in two are a partition break the `partition_ok` flag
   won't catch.
3a. **Sweeps must be enumeration-shaped (v0.5.9).** A criterion whose
   scope is a *population* rather than a named site — it says "all",
   "every", "no remaining", "the rest of", or names a pattern instead of
   a file — must satisfy three things, or it is a lint defect:
   **(i)** the 202 names the **command that enumerates the population**
   (a `grep`/`ast-grep`/query), not a hand-written list of sites;
   **(ii)** the acceptance criterion is phrased as *that command returning
   empty*, never as "these N sites are fixed"; **(iii)** you run the
   command yourself now and record its current output in `214-LOG.md`.
   A hand-listed population is a census, and a census is exactly the
   derived fact principle 15 forbids — it is stale the moment the tree
   moves, and its incompleteness only surfaces when the Safety Officer
   finds instance N+1. Field lesson 2026-07-24: an incident took **four
   Safety halts** on one objective, each closing the named instances and
   revealing another of the same class, because the criterion enumerated
   sites instead of asserting an invariant.
3b. **Claims about state outside the tree must be measured.** A
   criterion — or a waiver inside one — asserting anything the working
   tree does not contain (a registry version, whether something is
   published, an installed or deployed copy, another repository, a
   remote ref, a live service) is a **measured claim**; size is
   irrelevant, one external boolean counts as much as a population.
   Mirror 3a: **(i)** the 202 names the **command that establishes the
   fact** (`npm view <pkg> version`, `git ls-remote`, a witness script),
   not prose and not a reading carried over from an earlier artifact;
   **(ii)** the criterion is phrased as *that command's result* ("`npm
   view <pkg> version` returns < X"), never as a bare assertion ("X is
   unpublished"); **(iii)** you run it yourself **now** and record the
   actual output in `214-LOG.md`. A fact settled by reading or grepping
   this project's own files is not in scope — that is ordinary evidence
   (check 5), and a tree-wide sweep is 3a. A label on an old reading
   ("measured during the last deploy") is provenance, not truth. Field
   lesson 2026-07-26: a criterion waived a version bump on "0.6.9 is
   unpublished" — the Owner had published it 75 minutes before this lint
   ran, and the version shipped twice with different contents.
4. **Territory disjointness** — verify the globs actually don't intersect
   rather than trusting `partition_ok: true` (it is a claim, not a fact).
5. **Evidence executability** — each `evidence_required` command must be
   runnable in the specialist's harness (no browser/UI observation from a
   browserless agent; see the 202 staging rule).
6. **Criterion coverage, both directions (v0.5.4)** — every 202 acceptance
   criterion must map to at least one tasking, **or** be explicitly marked
   in the 202 as *IC work* (artifacts under `.dcs/**`: re-issuing a gate,
   amending the IAP, register updates — specialists are barred from that
   tree), *Owner work* (UAT, sign-off), or *deploy-period work*. A
   criterion in none of those buckets is unsatisfiable-as-written and will
   surface as a false Safety halt at the end of the period, after all the
   execution cost has been spent. Field lesson 2026-07-24: a period was
   planned with a criterion requiring an edit to `IAP.md` — a file no
   tasking may touch by construction.
7. **Criterion satisfiability against the repo's own tests (v0.5.4)** — if
   a criterion requires changing behaviour that an existing committed test
   asserts, name that test in the tasking that owns the change. A
   criterion whose fulfilment turns a green test red is not wrong, but the
   test update must be *owned by someone*, not discovered mid-execution.
   (See principle 15's test clause: a test pinning a moving ref makes this
   collision routine rather than rare.)
8. **Territory stays inside this project (v0.6.2)** — resolve every
   `territory` and `forbidden` glob against the incident's own project
   root (the tree holding the `.dcs/` this incident lives in). Any path
   that escapes it — an absolute path into another repo, a `../` climb —
   is a lint defect, not a plan. An incident belongs to **the repository
   whose files it changes**; work in another repo is that repo's own
   incident, opened from a session rooted there. Nothing else catches
   this: the gate deliberately allows targets outside the project (it
   cannot judge a tree it has no `.dcs/` for), so a cross-project
   territory would be silently ungated — every edit permitted, the
   incident archive landing in the wrong repo's history, and the other
   project's register, delegation and worktree conventions never
   consulted. **One session, one project.**

Log the lint result in `214-LOG.md` in one line (`tasking lint: pass` or
`tasking lint: N defects fixed pre-review — <one-line each>`). Only a
clean lint proceeds to the command point below.

### 4b. Repeated-reject trigger (v0.5.1)

Count `command: iap_review REJECT` entries for the **current period** in
`214-LOG.md`. On the **third** reject in one period: stop iterating and
treat it as **escalation trigger (f)** (doctrine principle 13). Three
rejects is not a plan being polished — it is a signal that the objectives
are wrong, the chief's information diet is too narrow, or the incident is
too large to plan as one unit. File a 209 sitrep, pause, and put
continue / re-scope the 202 / decompose into separate incidents to the
Owner. Do not spend a fourth review cycle to find out.

This is a command point (doctrine: "Transfer of command"). **If this
session is not running Fable**: announce the spawn first (doctrine, "A
command point is never a silent wait" — say that no file changes until
the decision returns), then spawn `dcs-commander` via Task (model
`fable`) with the full 201 + 202 text and the chiefs' complete structured
returns; its `iap_review` decision (schemas.md #6, commander decisions) governs — on
`"reject"`, use its `required_changes` verbatim as the re-spawn
instruction to the Planning Chief and repeat this step; on `"accept"`,
proceed. **If the spawn returns no decision block** (quota exhausted, API
error, early termination): that is a failed spawn — re-spawn on the next
tier at once, log both attempts, and never sit waiting on it. Record the decision in `214-LOG.md`
(`command: iap_review <verdict> (IC=dcs-commander)`). **If this session is
Fable**, apply the checks below yourself.

**Partition check (hard gate):** if `partition_ok` is `false`, read
`risks[]` for a justification (sequential staging or worktree isolation).
If the justification is present and coherent, proceed — the IAP will
record it as a sequential/worktree execution mode. If `partition_ok` is
`false` with no real justification, or `true` but the `territory[]` arrays
visibly overlap anyway: **reject.** Re-spawn `dcs-planning-chief` with a
one-line explanation of what was wrong, and repeat this step. Do not
integrate a plan with an unjustified overlapping partition into the IAP —
this is doctrine principle 6, non-negotiable.

If `objectives_feedback` flags a 202 criterion as untestable, resolve it
now: either revise 202 (brief Owner confirm) or explicitly accept the risk
and note why.

## 5. Write the planning artifacts

- `203-ORG.md` — activated positions this period, from
  `$HOME/.claude/dcs/templates/203-ORG.md`. **Type 1:** always write it.
  **Type 3 (v0.5):** write it only if activation differs from the default
  (IC + Planning Chief + specialists matching the 204 tasking count,
  executed in plain parallel) — i.e. a Logistics Chief was activated, the
  specialist count doesn't match the 204 tasking count, or the execution
  mode is sequential/worktree-isolated rather than plain parallel.
  Otherwise skip it and append to `214-LOG.md`: `203 skipped (default
  Type 3 activation)` — the IAP's partition table already carries the
  same activation information for the default case.
- `204-TASKING/S1.md`, `S2.md`, ... — one per tasking, transcribed from the
  chief's `taskings[]`, using `$HOME/.claude/dcs/templates/204-TASKING.md`.
- `IAP.md` — integrated from `$HOME/.claude/dcs/templates/IAP.md`: links
  202+203+204 (or just 202+204 if 203 was skipped per the rule above —
  say so in the link line rather than linking a file that doesn't
  exist), the partition table (with disjoint/overlap-justified status),
  risks, verification plan, and (Type 1) the Logistics Chief's
  deploy/env/migration/rollback plan.

## 5a. Refine the register's territory (v0.3)

Now that `IAP.md`'s partition table is final, resolve `esg_root`
(doctrine "Parallel operation": `git worktree list --porcelain`, first
entry). If `<esg_root>/.dcs/esg/REGISTER.md` exists, update this
incident's row's `territory` column to the **union** of every
`204-TASKING/*.md`'s `territory[]` globs — this replaces the coarser
201-blast-radius estimate `/dcs-new` recorded when the incident opened,
with the plan's own precise partition. This is what keeps the portfolio-
level territory check in `new.md` step 7b accurate for whatever incident
gets typed next. If `REGISTER.md` doesn't exist, skip this step.

## 6. Approve the IAP — Delegation-aware (v0.2)

**Delegation check (Type 3 only):** if the incident is Type 3 AND
`<project>/.dcs/esg/DELEGATION.md` exists, parse its latest (highest
`version`) fenced ```delegation-bounds``` JSON block — never the prose
around it (schemas.md #7, delegation bounds, is the authoritative shape).
Evaluate ALL of:

- `max_files` is >= the IAP's total partitioned file count.
- every `territory[]` glob across every `204-TASKING/*.md` misses every
  entry in `forbidden_globs`.
- the `201-BRIEF.md` / `202-OBJECTIVES.md` text doesn't match any string
  in `forbidden_topics`.
- `max_specialists` is >= the 204 tasking count.
- if `require_tests_green` is `true`, the chief's `verification_plan`
  names a concrete automated test run, not "manual only."

**All bounds hold AND `auto_approve_type3` is `true`:** the IC approves on
the Owner's behalf — skip the `AskUserQuestion` in step 6b below and
proceed directly to step 7 (stamp the marker), with `approved_by: IC
(Delegation v<N>)` instead of `approved_by: Owner` in `IAP-APPROVED`'s
metadata. Append to `214-LOG.md`: `approved under Delegation v<N> (Type 3,
bounds held)`. If `<project>/.dcs/esg/REGISTER.md` exists, also update or
add this incident's row there (id, title, type, priority, intake source,
opened date) so the register reflects every incident that ran, delegated
or not — doctrine principle 12: never silent. **Tell the Owner in one
visible line regardless:** e.g. "IAP for `<slug>` auto-approved under
Delegation v`<N>` (all bounds held); proceeding to `/dcs-execute`."

**Any bound fails, `auto_approve_type3` is `false`/absent, no
`DELEGATION.md`, or Type 1:** fall through to step 6b — if a delegation
check was attempted and failed, name the specific failed bound(s) in the
summary so the Owner sees exactly why it didn't auto-approve.

**No `DELEGATION.md` at all (project has no ESG):** `config.json`'s
`auto_approve_type3` key is superseded by, but still the fallback for,
projects without an ESG — it carries no bounds beyond the Type/config
check itself (no `max_files`, no `forbidden_globs`), so treat it far more
conservatively: only auto-approve on this fallback path if `Type == 3`
AND `auto_approve_type3: true` AND the IAP touches no file matching any
glob in `guarded_paths` outside the ordinary source tree (i.e. nothing
that already looks unusual for a routine change). This fallback predates
v0.2 and is unchanged by it; a project that runs `/dcs-esg` and gets a
real `DELEGATION.md` should prefer that path — it is auditable per-bound,
this one isn't.

## 6b. Present the IAP to the Owner

Use `AskUserQuestion` — **not** plan mode. This is deliberate: DCS's own
approval gate is a distinct mechanism from the global ExitPlanMode
handoff hook, and routing IAP approval through plan mode would collide
with it. Summarize the **202 objectives (goal + acceptance criteria) in
full together with the IAP** (tactics, partition, risks) — if step 2's
confirm was deferred under the delegation-aware skip, this is the Owner's
first look at the objectives, so include them in full, not just
cross-referenced — and, if a delegation check ran and failed, the named
failed bound(s) — then ask: approve / request changes / reject.

- **Request changes:** revise the relevant artifact(s) (202, taskings, or
  IAP integration) and re-present. Loop until approved or rejected.
- **Reject:** the incident doesn't proceed this period — return to intake
  framing (more analyst work via a fresh `/dcs-new`-style investigation)
  or consider closing the incident as abandoned; this is rare and mostly
  signals the Type or the whole premise needs rethinking, not just the
  plan.

## 6c. The proportionate amendment path

A cheaper route to step 7, for a change that is genuinely narrow — never
a way to keep a real re-plan away from the Owner's eyes (see the
symmetric fallback below).

**Entry — who may reach it, and only from here:**
- from `execute.md` step 6, with an already-logged `command: deviation ->
  amend_tasking` / `-> replan` / `-> escalate_owner` entry (command point
  3), cited by its timestamp;
- from `execute.md` step 9's `halt` branch, with an already-logged
  `command: verdict -> fix_taskings` entry (command point 4), cited by
  its timestamp;
- from `execute.md` step 9's advisories-on-a-pass paragraph, when an
  advisory's own fix touches `IAP.md`'s content, with that pass's
  already-logged `command: verdict -> close` / `-> next_period` entry
  (command point 4), cited by its timestamp.

None of the three is self-authorizing — each still has to clear every
boundary condition below before it may take this path. Each cited entry
must also postdate the `IAP-APPROVED` stamp currently in force — an
entry from an earlier attempt or revision ratifies nothing here, the
same freshness step 7's own bounded exception already requires of its
own ratifying entry (which likewise refuses the period's first-pass
`command: iap_review` entry as a stand-in for a fresh one).

**Halt-ceiling clamp.** `## 6c.` may not be used to re-stamp while the
halt tally (`dcs_gate.py --halt-count <incident_dir>`) stands at
`esg.max_halts_per_attempt` — at the ceiling, the route is trigger
(b)/(c) escalation, never a cheap re-stamp. A re-stamp's own
`IAP-APPROVED:` sentinel is itself a reset anchor for that tally
(`dcs_gate.py`'s `halt_cycles()`), so letting 6c fire at the ceiling
would let a lightweight approve/reject clear a wall the doctrine put
there on purpose; only an Owner decision at escalation may authorize
continuing past it, never a re-stamp on its own. Because that same
re-anchoring happens on every 6c re-stamp, this clamp rarely binds in the
exact halt/fix/re-verify cycle it governs — a run of halts each followed
by a re-stamp keeps the tally low even after several halts. It is not
the load-bearing ceiling: trigger (b) (counted log-wide, across the whole
objective, never reset by a stamp) and trigger (c) (the cumulative
`IAP-APPROVED:` count against `esg.max_periods_before_review`) are what
actually stop an unbounded same-class loop, and both already run
independently of this clamp.

**Boundary — all four, or it's the full path:**
1. **A single per-artifact invariant, not a branch choice.** Evaluate the
   amendment's whole real touched set — every file it actually touches,
   from the triggering command-point entry through to any
   `IAP.md`/`203-ORG.md` bookkeeping it necessitates — against one test,
   applied per artifact. An amendment is admissible on this axis **iff
   every touched artifact is one of**:
   - a `204-TASKING/*.md` file the triggering logged commander decision
     itself names (one or several — a single deviation/verdict decision
     may legitimately touch more than one tasking; no "exactly one"
     cap);
   - this incident's own `IAP.md`;
   - this incident's own `203-ORG.md`, where the tasking-count or
     execution-mode change makes its bookkeeping a consequence of the
     same amendment;

   **and none of**:
   - `.dcs/esg/**` (any file — `DELEGATION.md`, `REGISTER.md`, or
     anything else under it);
   - `.dcs/config.json`;
   - `201-BRIEF.md`;
   - `202-OBJECTIVES.md`;
   - any acceptance-criterion text, whether in `202-OBJECTIVES.md` or in
     `IAP.md`'s own summary of it — "criterion" means both copies, never
     only the 202-side one.

   **Mandatory bookkeeping the path itself writes is not part of this
   screened set at all** — it is the process's own required side effect,
   never an artifact being evaluated for planning-shaped content, so it
   needs to satisfy neither the "iff every touched artifact is one of"
   list above nor the "none of" exclusions, even where it physically
   sits under `.dcs/`. This includes, but is not limited to: `214-LOG.md`
   appends; the `IAP-APPROVED` marker rewrite (step 7); `<project>/.dcs/ACTIVE`'s
   own update (step 8); a register **status** transition (e.g. `ACTIVE`
   <-> `ESCALATED`) an escalation trigger performs; and the 209 sitrep an
   escalation trigger files under `.dcs/esg/SITREPS/` — the other
   mandatory half of the same escalation act whose register-status half
   is already named. A **content** edit — `DELEGATION.md`'s bounds, or
   `REGISTER.md`'s territory or title fields, or any register field other
   than the status transition itself — remains excluded by the "none of"
   list above exactly as already stated; the exemption reaches mandatory
   process bookkeeping alone, never a planning-shaped content change,
   however that change's file happens to be classified.

   **Step 5a's register-territory refresh is a distinct case, not covered
   by the bookkeeping exemption above, because its content is exactly
   planning-shaped.** It is degenerate — nothing to do — whenever
   condition 3 holds and no tasking is created, since the union of
   territory globs is then unchanged by construction. An amendment that
   *does* create a new tasking (condition 1's first bullet) changes that
   union: the amendment either takes this path and the IC recomputes
   `REGISTER.md`'s territory column as the same kind of mandatory
   bookkeeping named above (a mechanical union, not new planning
   content), or — if the IC does not — the amendment must take the full
   path instead, so the portfolio-level territory check in `new.md` step
   7b never reads a stale union.
2. No change to any acceptance criterion — in `202-OBJECTIVES.md` or in
   `IAP.md`'s own summary of it, "criterion" meaning both copies exactly
   as condition 1's "none of" list already states.
3. No change to any `204-TASKING/*.md`'s `territory` OR `forbidden` list
   — in the tasking file itself, or in `IAP.md`'s own partition table
   (the same copy every specialist actually receives, per `execute.md`'s
   fan-out step): every specialist's editable set, and what it is barred
   from touching, are exactly what the last full approval declared, in
   whichever copy a reader consults.
4. No premise change — the goal, the tactics, and the reasoning the Owner
   already saw are still the ones on the table.

**Symmetric fallback, stated plainly:** anything that fails even one of
the four — most `replan` dispositions included, since "the plan's premise
is wrong" (`agents/dcs-commander.md`'s own definition of that disposition)
is condition 4 failing by definition — takes the full steps-1-9 path
unchanged, from step 1. The boundary decides, never the disposition's
label by itself; this is what keeps the cheap route unreachable for a
genuine re-plan.

**What steps 1-6 contribute here: most of it, skipped.** Steps 1-3 do not
run — there is no new incident-state check to redo, no 202 redraft, and
no chief to re-spawn; nothing about the amendment needs chief-level
judgment by construction (boundary conditions 2 and 4). Step 4's command
point 2 does not run either: 6c is ratified by the entry named under
Entry above, not a fresh `command: iap_review` — see step 7's bounded
exception below. **All of lint 4a still runs, unconditionally — no check
is skipped and none is waived.** (Illustrative, not authoritative, as of
this writing: checks 1 self-contradiction, 2 orphaned deliverables, 3/3a
unassigned occurrences and enumeration-shaped sweeps, 3b measured claims,
4 territory disjointness, 5 evidence executability, 6 criterion coverage,
7 criterion satisfiability, 8 territory inside the project — step 4a
above is the operative list; a check added there runs here too without
this parenthetical needing an edit.) Checks 1, 4, and 8 in
particular run over the **complete post-amendment `204-TASKING/*.md`
set** — every tasking file as it would stand once the amendment is
applied, including any tasking file the amendment itself creates — never
only the file(s) condition 1 names as touched, so a new territory/
forbidden pair is checked against every sibling that already exists
rather than assumed safe by construction. Every check runs scoped to
whatever the amended tasking(s), `IAP.md`, or `203-ORG.md` edit actually
contains: an amendment can still orphan a deliverable, add an
unenumerated sweep, cite a command that doesn't run, contradict itself,
overlap a sibling's territory, or carry a glob that escapes the project —
every one of those is caught by an actual check run now, none of it
waived by a boundary condition. This costs 0 additional agent spawns and
0 additional Owner round-trips under criterion 1's own ceremony
accounting: the session runs lint itself, inline, exactly the way step 4a
always has for a full pass — it is not a new spawn and not a new
round-trip, so running the full set here is free under the very metric
that motivated skipping part of it before.

**Ceremony, as a count, not an impression:** a full `plan.md` steps-1-9
pass costs ≥2 agent spawns (the chief at step 3, `dcs-commander` at
command point 2) + up to 2 Owner round-trips (the 202 confirm at step 2,
the approval at step 6b). Step 6c costs 0 agent spawns + at most 1 Owner
round-trip — reusing step 6's own Delegation check, but **scoped to the
amendment's own delta, never the whole plan**: `forbidden_globs` against
the amendment's own declared `territory`/`forbidden` globs (not the
files the amendment happens to edit — an amendment's own edits are
always `.dcs/**` paths, which no `forbidden_globs` entry matches by
construction, so the glob check's real object is the *territory it
grants*, same as a full-plan pass), `forbidden_topics` against only the
amendment's own new/changed text — never the unchanged `201-BRIEF.md` /
`202-OBJECTIVES.md` body. This scoping is sound, not a weaker check:
boundary conditions 2, 3, and 4 already guarantee that body is unchanged
from what the last full approval already screened in full and the Owner
already saw, so re-screening it again finds nothing a first screening
didn't — noise, not a second safety check. 0 where it auto-approves the
amendment, 1 (a lightweight approve/reject) otherwise, never more, since
nothing here needs fresh chief-level judgment. (This count is 6c's own
Delegation-check contact only — an escalation-trigger round-trip under
doctrine principle 13, e.g. trigger (c)'s mandatory attempt-threshold
review, is a separate, additional Owner contact that no path removes,
and the field-measurement savings below never claim otherwise.)

**Failed-bound inheritance.** `max_files`, `max_specialists`,
`forbidden_globs`, and `require_tests_green` are none of them re-derived
in full by the delta-scoped re-check above (`forbidden_globs` only
against the amendment's own touched file(s), the other three not
re-checked here at all) — so if any of the four failed at the last full
approval, that failure cannot be turned into a pass by a check that never
looks broadly enough to find it again: the amendment **inherits** it and
takes the lightweight approve/reject path above (at most 1 Owner
round-trip), never a silent auto-approval. `forbidden_topics` inherits
nothing, because it isn't in that position: boundary conditions 2, 3, and
4 guarantee the rest of the `201-BRIEF.md` / `202-OBJECTIVES.md` body is
identical to what the last full approval already ruled on, failed bound
or not — so a delta-clean `forbidden_topics` result means only that the
amendment's own new/changed text introduces no **new** forbidden topic,
not that the standing plan as a whole trips none. That is the residual
this inheritance clause deliberately accepts: the delta screen answers a
narrower question than the original full-plan screen did, and conditions
2/3/4 are exactly what makes the narrower answer sufficient here — the
broader question was already answered, by the last full approval, over
text this amendment cannot have changed.

**New-partition-line clamp.** An amendment whose touched set includes any
`204-TASKING/*.md` file that did **not** exist at the `IAP-APPROVED`
stamp currently in force never auto-approves under the delta-scoped
Delegation screen above, regardless of what that screen finds — it always
takes the lightweight Owner approve/reject round-trip (still within the
"at most 1" ceremony count above), because a new territory/forbidden pair
is planning-shaped content the Owner has never seen: the delta screen
answering "clean" says only that this pass introduced no forbidden topic
or forbidden-glob hit, never that the Owner has seen the new partition
line itself. The Entry requirement that the triggering logged decision
must *name* the file is unchanged by this clamp — naming the file
authorizes creating it, not auto-approving its content.

Then: proceed to **step 7** and **step 8** exactly as written below — 6c
does not fork or restate their mechanics. The hash, the marker, and the
`IAP-APPROVED:` sentinel are computed and written identically regardless
of which path reached them, which is what keeps `marker_valid()` and the
attempt tally accurate by construction.

## 7. On approval: stamp the marker

**Pre-stamp checklist (hard stop):** before computing any hash, read
`214-LOG.md` and confirm it contains a `command: typed` entry (command
point 1, from `/dcs-new`) and a `command: iap_review` entry (command point
2, step 4 above). If either is missing, the command points were skipped —
this is the exact drift transfer-of-command exists to prevent. **Stop, run
the missed command point now** (spawn `dcs-commander` if not Fable, decide
yourself if Fable), log it, and only then proceed. Never stamp an approval
over an unlogged command chain.

**Bounded exception, reached only via step 6c:** on an amendment, the
`command: iap_review` entry above is satisfied by the command-point-3/4
decision that 6c's Entry condition already cited by timestamp — not a
fresh `command: iap_review`. Stated explicitly, because the checklist
above would otherwise already be "satisfied" by the period's first-pass
`command: iap_review` entry still sitting in `214-LOG.md` — that entry
ratified the ORIGINAL plan, not this amendment, and accepting it here
would stamp the amendment over a decision that never saw it.

Compute the sha256 of the final `IAP.md`:

```bash
python -c "import hashlib; print(hashlib.sha256(open(r'<incident_dir>/IAP.md','rb').read()).hexdigest())"
```

(or `certutil -hashfile IAP.md SHA256` on Windows if Python isn't
convenient in context — the value must match what `dcs_gate.py` computes,
which is a plain sha256 of the file's bytes).

Write `IAP-APPROVED` with the hash as its **first line** (the gate hook
only reads that line), followed by metadata:

```
<hex sha256>
approved_by: Owner
approved_at: <ISO8601 local timestamp>
period: <N>
```

(v0.2: if step 6 auto-approved under a Delegation, `approved_by: IC
(Delegation v<N>)` instead — the hash mechanism and every other line are
identical either way.)

**Windows caveat:** write this file WITHOUT a BOM. PowerShell 5.1's
`Set-Content -Encoding utf8` prepends one; use the Write tool, or
`[System.IO.File]::WriteAllText(path, content)`. The gate hook tolerates a
BOM since v0.1.1, but a BOM-free file is the contract. Same applies to
`.dcs/ACTIVE`.

## 8. Open the gate

Update `<project>/.dcs/ACTIVE` to `<slug>|<type>|execution`.

Append to `214-LOG.md`:
```
[<timestamp>] IAP-APPROVED: <first 12 hex chars of IAP.md's sha256> -- phase: planning -> execution (period <N>)
```

For example (fictional hash):
```
[2026-07-22T14:03:00+11:00] IAP-APPROVED: d6d1409c1234 -- phase: planning -> execution (period 1)
```

**On a `## 6c.` amendment, the phase does not change** — execution was
already the phase every 6c Entry route requires, so the
`phase: planning -> execution` clause above is false on this path. Use
this form instead:
```
[<timestamp>] IAP-APPROVED: <first 12 hex chars of IAP.md's sha256> -- re-stamp, no phase transition (still execution, period <N>)
```
For example (fictional hash):
```
[2026-07-22T14:03:00+11:00] IAP-APPROVED: d6d1409c1234 -- re-stamp, no phase transition (still execution, period 1)
```

This line is also a reset anchor for the halt-iteration count `dcs_gate.py`
enforces (doctrine's halt ceiling) — but only conditionally: the sentinel
must satisfy `dcs_gate.py`'s own published grammar (`GRAMMAR_LINE`): "An
entry begins at column zero with a mandatory bracketed timestamp; any other
line is a continuation, never a sentinel, and quoting a whole prior entry
inside a body requires indenting it off column zero." — the bracketed
timestamp is mandatory, `IAP-APPROVED:` follows it immediately (`dcs_gate.py`'s
`STAMP_RE`) — and the hex prefix it carries must be **at
least 8 characters** of the hash just written to `IAP-APPROVED` above. The
stamped marker is the authority; this log line only fixes the marker's
position in time — a line that merely mentions the token, or carries a
stale or invented hash, is never an anchor.

## 9. Report

Tell the Owner the gate is open and the next step is `/dcs-execute`.

</process>
