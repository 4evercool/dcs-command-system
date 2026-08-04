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

Parse `<slug>|<type>|<phase>`. If no `ACTIVE`: stop — run `/dcs-new` first. If `phase` is `execution`: check whether this is a `## 6c.` amendment first (if `214-LOG.md` holds a qualifying command-point-3/4 entry and 6c's boundary conditions hold, go there now). Otherwise ask the Owner: revise the plan (re-plan — voids current approval) or `/dcs-status` / `/dcs-execute`.

Determine period `N` — 1 on first pass, else increment from the last period in `214-LOG.md`.

**Command-chain check (entry gate):** confirm `command: typed` exists via `grep -n "command: typed" <incident_dir>/214-LOG.md`. If absent, the Dispatcher typed the incident itself — repair NOW: run command point 1 properly (spawn `dcs-commander` if not Fable; decide yourself if Fable), log it via `python "$HOME/.claude/dcs/tools/dcs_log.py" append <slug> --by <operator> "<text>"`, correct 201 if type differs, re-confirm with Owner.

## 2. Draft 202-OBJECTIVES.md

Read `201-BRIEF.md`. Draft goal (outcome-shaped) and numbered, verifiable acceptance criteria using `$HOME/.claude/dcs/templates/202-OBJECTIVES.md`. On a re-plan after deviation, fold the deviation's `proposal` into the criteria.

**Delegation-aware confirm (v0.5):** if Type 3 AND `DELEGATION.md`'s latest `delegation-bounds` has `auto_approve_type3: true` AND the session's current operating model appears in that block's `approved_models` (model floor — `approved_models` empty or absent means no model is approved), skip `AskUserQuestion` — write directly to `202-OBJECTIVES.md`, append via `dcs_log.py append <slug> --by <operator> "202 confirm deferred to IAP approval (Delegation v<N>)"`. Otherwise — including an unlisted model or the model-floor miss just described — present to Owner via `AskUserQuestion`, full v0.1 behavior. Write confirmed version to `202-OBJECTIVES.md`.

## 3. Spawn the Planning Chief (and Logistics Chief for Type 1)

Spawn `dcs-planning-chief` with **only** the full text of `201-BRIEF.md` and `202-OBJECTIVES.md` inline. For Type 1, also spawn `dcs-logistics-chief` in parallel. Planning Chief returns JSON per schemas.md #2 (chief plan): `objectives_feedback`, `tactics`, `taskings` (`id`/`task`/`territory[]`/`forbidden[]`/`evidence_required[]`), `partition_ok`, `risks`, `verification_plan`. Logistics Chief returns JSON per schemas.md #3 (Logistics-chief plan).

On a deviation re-plan, include the triggering specialist's `found`/`why_plan_wrong`/`proposal`.

**Every revision is a FRESH spawn (v0.5.5).** Never resume a previous chief — a resumed agent's transcript is not archived in any incident artifact. A fresh spawn preserves the paper trail principle 5 requires.

## 4. Validate the returns — COMMAND POINT 2 (IAP acceptance)

Validate each chief return structurally before proceeding to lint: confirm
a JSON block is present, all required fields per schemas.md #2 (chief plan; Planning
Chief: `objectives_feedback`, `tactics`, `taskings`, `partition_ok`,
`risks`, `verification_plan`) or #3 (Logistics Chief: `deploy_path`,
`env_deps`, `migration_ordering`, `rollback_plan`, `risks`) are present,
and no fields outside the declared schema appear. Missing required field
or structural non-JSON = deviation — re-spawn the chief rather than
proceeding to lint.

From the Planning Chief: the fields above match schemas.md #2 (chief plan).

### 4a. Tasking lint — mechanical, run BEFORE the command point (v0.5.1)

These checks are arithmetic, not judgment. Run them yourself; a failure
is yours to fix, never a reason to spend a command point (field lesson
2026-07-23 — `dcs/references/doctrine-appendix.md`, "Workflow field lessons", W1).

1. **Self-contradiction** — for every tasking, `territory ∩ forbidden` must be empty.
2. **Orphaned deliverables** — every deliverable named in `tactics[]`, `verification_plan`, or Logistics-chief plan must map to an existing tasking `id`.
3. **Unassigned occurrences** — when the plan says "replace/remove X", `grep` for X: every occurrence must fall inside exactly one tasking's `territory`.
3a. **Sweeps must be enumeration-shaped (v0.5.9).** A criterion whose scope is a *population* ("all", "every", "no remaining", a pattern) must satisfy: **(i)** the 202 names the command that enumerates the population; **(ii)** the criterion is phrased as that command returning empty; **(iii)** you run the command now and record its output via `dcs_log.py append <slug> --by <operator> "<text>"`. A hand-listed population is a census — stale the moment the tree moves. Field lesson 2026-07-24 — `dcs/references/doctrine-appendix.md`, "Workflow field lessons", W2.
3b. **Claims about state outside the tree must be measured.** A criterion asserting anything outside the working tree (registry version, published status, remote ref, live service) is a measured claim. Mirror 3a: **(i)** the 202 names the command that establishes the fact; **(ii)** the criterion is phrased as that command's result; **(iii)** you run it now and record the output via `dcs_log.py append <slug> --by <operator> "<text>"`.
4. **Territory disjointness** — verify the globs don't intersect; don't trust `partition_ok: true`.
5. **Evidence executability** — each `evidence_required` command must be runnable in the specialist's harness (no browser/UI).
6. **Criterion coverage, both directions (v0.5.4)** — every 202 criterion must map to a tasking, or be tagged `[IC]`, `[Owner]`, or `[deploy period]`.
7. **Criterion satisfiability against the repo's own tests (v0.5.4)** — if a criterion changes behaviour an existing test asserts, name that test in the tasking.
8. **Territory stays inside this project (v0.6.2)** — resolve every `territory`/`forbidden` glob against the incident's project root. Any path escaping it is a lint defect. **One session, one project.**

Log the lint result via `dcs_log.py append <slug> --by <operator> "tasking lint: pass"` (or `"tasking lint: N defects fixed pre-review — <one-line each>"`). Only a
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
returns; its `iap_review` decision (schemas.md #6, Commander decisions) governs — on
`"reject"`, use its `required_changes` verbatim as the re-spawn
instruction to the Planning Chief and repeat this step; on `"accept"`,
proceed. **If the spawn returns no decision block** (quota exhausted, API
error, early termination): that is a failed spawn — re-spawn on the next
tier at once, log both attempts, and never sit waiting on it. Record via `dcs_log.py append <slug> --by <operator> "command: iap_review <verdict> (IC=dcs-commander)"`. **If this session is
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

- `203-ORG.md` — from template. Type 1: always write. Type 3: skip if default activation (IC + Planning Chief + specialists = tasking count, plain parallel); log `203 skipped (default Type 3 activation)`.
- `204-TASKING/S1.md`, `S2.md`, ... — one per tasking, from chief's `taskings[]`.
- `IAP.md` — from template: links, partition table, risks, verification plan, Logistics Chief's plan (Type 1).

## 5a. Refine the register's territory (v0.3)

Resolve `esg_root` (`git worktree list --porcelain`, first entry). Update row's `territory` to union of all `204-TASKING/*.md` `territory[]` globs. Skip if no register.

## 6. Approve the IAP — Delegation-aware (v0.2)

**Delegation check (Type 3):** if Type 3 AND `DELEGATION.md` exists, parse latest `delegation-bounds` JSON (schemas.md #7, Delegation bounds). Evaluate: `max_files` ≥ file count; no `territory[]` hits `forbidden_globs`; 201/202 misses `forbidden_topics`; `max_specialists` ≥ tasking count; `require_tests_green` → concrete tests named; the session's current operating model appears in `approved_models` (model floor).

**All bounds hold (model floor included) AND `auto_approve_type3: true`:** IC approves — skip 6b, stamp `approved_by: IC (Delegation v<N>)`. Log. Tell Owner.

**Any bound fails — model floor included: an unlisted model, or `approved_models` empty or absent (no model approved), is a failed bound on its own — no Delegation, or Type 1:** fall through to 6b — name failed bound(s), full v0.1 behavior. No DELEGATION.md → fallback to `config.json` (conservative, no per-bound audit): on that path auto-approve **only** if Type == 3 AND `auto_approve_type3: true` AND the IAP touches no file matching any `guarded_paths` glob outside the ordinary source tree — i.e. nothing that already looks unusual for a routine change. Anything else falls to 6b.

## 6b. Present the IAP to the Owner

Use `AskUserQuestion` (**not** plan mode). Summarize 202 objectives + IAP (tactics, partition, risks). Name failed delegation bounds if any. Options: approve / request changes / reject. Reject → return to intake or close as abandoned.

## 6c. The proportionate amendment path

A cheaper route to step 7, for a change that is genuinely narrow — never a way to keep a real re-plan away from the Owner's eyes.

**Entry — who may reach it, and only from here:**
- from `execute.md` step 6, with an already-logged `command: deviation ->
  amend_tasking` / `-> replan` / `-> escalate_owner` entry (command point
  3), cited by its timestamp;
- from `execute.md` step 9's `halt` branch, with an already-logged
  `command: verdict -> fix_taskings` entry (command point 4), cited by
  its timestamp;
- from `execute.md` step 9's advisories-on-a-pass paragraph, when an
  advisory's fix (per `agents/dcs-safety-officer.md` step 6) touches `IAP.md`'s content, with that pass's
  already-logged `command: verdict -> close` / `-> next_period` entry
  (command point 4), cited by its timestamp.

None of the three is self-authorizing — each must clear every boundary condition below. Each cited entry must postdate the `IAP-APPROVED` stamp currently in force.

**Halt-ceiling clamp.** `## 6c.` may not re-stamp while the halt tally
(`dcs_gate.py --halt-count <incident_dir>`) stands at
`esg.max_halts_per_attempt` — at the ceiling, the route is trigger
(b)/(c) escalation, never a cheap re-stamp. Trigger (b) (counted
log-wide, never reset by a stamp) and trigger (c) (cumulative
`IAP-APPROVED:` count) are the load-bearing ceilings; this clamp backs
them.

**Boundary — all four, or it's the full path:**
1. **Per-artifact invariant.** The amendment's real touched set — every
   file it touches, from the triggering entry through to any
   `IAP.md`/`203-ORG.md` bookkeeping — is admissible **iff every touched
   artifact is one of**: a `204-TASKING/*.md` the triggering decision
   itself names; this incident's `IAP.md`; this incident's `203-ORG.md`
   where tasking-count/execution-mode change necessitates it. **And none
   of**: `.dcs/esg/**`, `.dcs/config.json`, `201-BRIEF.md`,
   `202-OBJECTIVES.md`, or any acceptance-criterion text (in either
   `202-OBJECTIVES.md` or `IAP.md`'s summary). Mandatory bookkeeping the
   path itself writes (`214-LOG.md` appends, `IAP-APPROVED` rewrite,
   `.dcs/ACTIVE` update, register status transitions, 209 sitreps) is
   not part of this screened set. A content edit to `DELEGATION.md`'s
   bounds or `REGISTER.md`'s territory/title remains excluded. Step 5a's
   register-territory refresh is degenerate when condition 3 holds; an
   amendment creating a new tasking must recompute the territory union.
2. No change to any acceptance criterion — in `202-OBJECTIVES.md` or
   `IAP.md`'s summary.
3. No change to any `204-TASKING/*.md`'s `territory` OR `forbidden` list
   — every specialist's editable set stays exactly what the last full
   approval declared.
4. No premise change — the goal, tactics, and reasoning the Owner saw are
   still on the table.

**Symmetric fallback:** failing even one of the four takes the full
steps-1-9 path from step 1. The boundary decides, never the
disposition's label.

**What steps 1-6 contribute: most of it, skipped.** Steps 1-3 do not
run — no new incident-state check, no 202 redraft, no chief re-spawn.
Step 4's command point 2 does not run: 6c is ratified by the Entry
above, not a fresh `command: iap_review`. **All of lint 4a still runs,
unconditionally** — checks 1-8 over the complete post-amendment
`204-TASKING/*.md` set. This costs 0 agent spawns and 0 Owner
round-trips.

**Ceremony count:** full `plan.md` steps-1-9 costs ≥2 agent spawns + up
to 2 Owner round-trips. Step 6c costs 0 agent spawns + at most 1 Owner
round-trip — reusing step 6's Delegation check scoped to the amendment's
delta: `forbidden_globs` against the amendment's declared
`territory`/`forbidden` globs, `forbidden_topics` against only the
amendment's new/changed text. Boundary conditions 2/3/4 guarantee the
unchanged body was already screened.

**Failed-bound inheritance.** `max_files`, `max_specialists`,
`forbidden_globs`, and `require_tests_green` — if any failed at the last
full approval, the amendment inherits that failure: it takes the
lightweight approve/reject path, never a silent auto-approval.

**New-partition-line clamp.** An amendment whose touched set includes a
`204-TASKING/*.md` that did not exist at the current `IAP-APPROVED`
stamp never auto-approves — it always takes the Owner approve/reject
round-trip.

**Preservation-map duty (pre-stamp, 6c-only).** Before the marker is re-stamped, every 202 acceptance criterion the triggering amendment does not name is paired with the artifact section that satisfies it in the artifact as it now stands — schemas.md #9 (preservation map); each pairing carries a literal anchor from that section plus the command output showing it present; the map is appended to `214-LOG.md` as a fenced JSON block indented off column zero (`dcs_gate.py`'s grammar: a line at column zero without a bracketed timestamp is not an entry, so the fence must be indented). Verify it by running, verbatim and on one line:

`python "$HOME/.claude/dcs/tools/preservation_map.py" <incident_dir>`

A non-zero exit is a hard stop — no re-stamp until the artifact or the map is repaired.

Then: proceed to **step 7** and **step 8** exactly as written below — 6c does not fork or restate their mechanics.

## 7. On approval: stamp the marker

**Pre-stamp checklist (hard stop):** confirm `command: typed` and `command: iap_review` entries exist in `214-LOG.md`. If absent: stop, run the missed command point, log it via `dcs_log.py append <slug> --by <operator> "<text>"`, then proceed.

**Bounded exception (6c only):** on an amendment, the `command: iap_review` check is satisfied by the command-point-3/4 decision 6c's Entry cited by timestamp — not the period's first-pass `command: iap_review`.

Compute sha256 of `IAP.md`:
```bash
python -c "import hashlib; print(hashlib.sha256(open(r'<incident_dir>/IAP.md','rb').read()).hexdigest())"
```

Write `IAP-APPROVED` — hash on first line, then `approved_by`, `approved_at`, `period`. No BOM.

## 8. Open the gate

Update `.dcs/ACTIVE` to `<slug>|<type>|execution`. Append via `dcs_log.py append <slug> --by <operator> --sentinel stamp "<first 12 chars of hash> -- phase: planning -> execution (period <N>)"` — on a 6c amendment (phase unchanged), the text is instead `"<first 12 chars of hash> -- re-stamp, no phase transition (still execution, period <N>)"`.

The `IAP-APPROVED:` sentinel anchors the halt-ceiling counter — must carry ≥8 hex chars of the stamped hash per `dcs_gate.py`'s published grammar (`GRAMMAR_LINE`): "An entry begins at column zero with a mandatory bracketed timestamp; any other line is a continuation, never a sentinel, and quoting a whole prior entry inside a body requires indenting it off column zero."

## 9. Report

Tell the Owner the gate is open and the next step is `/dcs-execute`.
