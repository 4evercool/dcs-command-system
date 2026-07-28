<!--
IAP.md -- the Integrated Action Plan, written by the IC during /dcs-plan.
This is the ONLY document specialists execute against once approved.
Editing this file after approval voids IAP-APPROVED automatically (hash
mismatch) -- deliberate, not a bug to route around.
-->

# IAP — Incident Action Plan

**Incident:** 2026-07-28-token-economy
**Type:** 1
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `203-ORG.md` · `204-TASKING/{S1,S2,S3,S4}.md` · logistics plan below

## Objectives (summary of 202)

**Goal:** Cut DCS's own token overhead everywhere `201-BRIEF.md` found it,
without trading away context-reset recovery, independent verification, or
the auditable command chain that make DCS safe to run unattended.

**Acceptance criteria:**

1. `run.md`/`loop.md` stop eagerly `@`-including all four phase workflow
   files; each phase's material loads only where the process body already
   reads it on entry (`doctrine.md` stays eager). Verified by `grep -n '^@'`
   showing no phase file in either unconditional block, plus an
   omission trace.
2. Five sites dealing with `214-LOG.md` outside the already-scoped
   `verdict_disposition` spawn and the legitimate AAR reads (`plan.md:38`,
   `plan.md:573`, `execute.md:25`, `agents/dcs-commander.md:63`,
   `agents/dcs-safety-officer.md`) become bounded checks. Verified by the
   corrected `rg` enumerator (`214-LOG.md` current output logged this
   period).
3. `REGISTER.md` keeps `Territory` as bare globs while `ACTIVE`; once
   terminal, `Territory`/`Outcome`/`Intake source` collapse to exactly one
   line each pointing to the incident's own record; `STRATEGY.md`'s
   `## Sessions` caps at 5 lines, routing rationale to the project's own
   decision store if `CLAUDE.md` documents one (never a literal path in
   shipped text). Verified by the column-attribution method, `new.md` step
   7b's check unaffected, and a `vault`-grep returning nothing. Compacting
   this project's own live files is **[IC]** work at close.
4. A 2nd/3rd Safety Officer spawn within a period may cite a prior
   same-period verdict's `checked[]` entry by reference for content it
   independently reconfirmed unchanged — never for anything a fix-tasking
   touched, never as a substitute for the reconfirmation. Verified against
   `register-field-repair-path`'s baseline (21,415 B, 3 verdicts).
5. **DROPPED** — see `202-OBJECTIVES.md` criterion 5 for the full
   reasoning (no mechanism can safely distinguish "same session" from
   "fresh spawn/reset"; escape hatch invoked). `doctrine.md` is in no
   tasking's territory this period.
6. `schemas.md`'s evidence-bearing fields plus three agent charters and
   `204-TASKING.md` state a brevity rule (cite excerpt/location, never
   paste full transcript) — same underlying defect as criterion 3, applied
   to a different file set. Verified by a grep across all five locations.

Full text, including every verification command and the reasoning behind
each correction made during this period's planning: `202-OBJECTIVES.md`.

## Tactics (from the Planning Chief)

- Criterion 1, half one: delete `@{new,plan,execute,close}.md` from
  `run.md`'s `required_reading`, keep `@doctrine.md`; leave `loop.md`'s
  block structurally alone (`run.md` is not a phase workflow, executed
  unconditionally every sweep — `loop.md`'s saving is transitive).
- Criterion 1, half two (the omission guard — the actual safety content of
  this criterion): every "Read `<phase>.md` and execute its process"
  instruction in `run.md` steps 3/4/5/7 must also instruct reading that
  workflow's own `required_reading` block, phrased generically, never
  hand-listed (principle 15) — because the Read tool returns `@` lines as
  literal text and does not resolve them, so deleting the eager block
  alone would silently omit those phases' own references.
- Criterion 2: bind each read with the command that decides it, not an
  adjective — existence checks become named greps, a count becomes
  `grep -c`, history-shaped reads take `execute.md:227`'s existing bound
  verbatim. `close.md`'s AAR reads stay full.
- Criterion 4: the by-reference allowance keys on a command the officer
  itself ran, never a claim it was handed (charter half, S2); `execute.md`
  step 8 hands a re-spawned officer the prior verdict(s) verbatim plus a
  changed-since manifest (input half, S3) — the two halves must state the
  contract in the same words with no channel between the specialists.
- Criterion 3: collapse keyed to the state transition, ACTIVE-row
  invariant preserved (`new.md` step 7b needs bare globs while active —
  neither `new.md` nor `plan.md` needs editing), caps stated as numbers,
  placed at the three write points that already touch a register row
  rather than a separate archival pass. Shipped-safe phrasing: "the
  project's own decision store, if its `CLAUDE.md` documents one" — never
  `vault/Decisions/` literally.
- Criterion 6: brevity rule as short clauses inside existing field tables
  (schemas.md has 719 B of hot-path slack, measured this period) — must
  not read as licence to paraphrase; the existing "not a paraphrase"
  language survives everywhere it already appears.
- No tactic for criterion 5 — dropped; `doctrine.md` deliberately in no
  tasking's territory.

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | `dcs/workflows/run.md`, `dcs/workflows/loop.md` | `dcs/workflows/{new,plan,execute,close,esg,deploy,status,init}.md`, `agents/**`, `dcs/references/**`, `dcs/templates/**`, `dcs/hooks/**`, `skills/**`, `tests/**`, `bin/**`, `.dcs/**`, `install.ps1`, `install.sh`, `package.json`, `dcs/VERSION` |
| S2 | `agents/dcs-{safety-officer,ops-specialist,planning-chief,commander}.md`, `dcs/references/schemas.md`, `dcs/templates/204-TASKING.md` | `agents/dcs-{logistics-chief,situation-analyst}.md`, `dcs/references/{doctrine,doctrine-appendix,typing,forms}.md`, `dcs/workflows/**`, `dcs/templates/{REGISTER,STRATEGY,214-LOG,201-BRIEF,202-OBJECTIVES,203-ORG,209-SITREP,AAR,DELEGATION,IAP,config.json}`, `dcs/hooks/**`, `skills/**`, `tests/**`, `bin/**`, `.dcs/**`, `install.ps1`, `install.sh`, `package.json`, `dcs/VERSION` |
| S3 | `dcs/workflows/plan.md`, `dcs/workflows/execute.md` | `dcs/workflows/{run,loop,new,close,esg,deploy,status,init}.md`, `agents/**`, `dcs/references/**`, `dcs/templates/**`, `dcs/hooks/**`, `skills/**`, `tests/**`, `bin/**`, `.dcs/**`, `install.ps1`, `install.sh`, `package.json`, `dcs/VERSION` |
| S4 | `dcs/workflows/{esg,close,deploy}.md`, `dcs/templates/{REGISTER,STRATEGY}.md` | `dcs/workflows/{new,plan,execute,run,loop,status,init}.md`, `agents/**`, `dcs/references/**`, `dcs/templates/{204-TASKING,214-LOG,201-BRIEF,202-OBJECTIVES,203-ORG,209-SITREP,AAR,DELEGATION,IAP,config.json}`, `dcs/hooks/**`, `skills/**`, `tests/**`, `bin/**`, `.dcs/**`, `install.ps1`, `install.sh`, `package.json`, `dcs/VERSION` |

**Partition status:** disjoint — parallel execution. Verified independently
twice: the Dispatcher (dedup check across the combined 15-file territory
list, zero duplicates, `partition_ok: true` confirmed true not merely
trusted) and `dcs-commander` at command point 2 (own enumeration, same
result — 15 distinct paths, none in two territories, none in its own
tasking's forbidden list).

## Deploy / environment plan (Type 1, from the Logistics Chief)

**Deploy path:** Full payload install via `/dcs-deploy`, run from `C:\DCS`
(the main checkout / `esg_root`), **after** `/dcs-close` merges. Command,
from `CLAUDE.md` verbatim: `powershell -ExecutionPolicy Bypass -File
C:\DCS\install.ps1` (POSIX: `./install.sh`). No scoped deploy exists or is
needed — `install.ps1` robocopies the payload roots wholesale (`dcs/`
recursively, `agents/dcs-*.md`, `skills/dcs-*/`) and all 15 blast-radius
files sit inside `dcs/` and `agents/`. Verification: `python
tests/payload_check.py` before and after the install, recording `git
rev-parse HEAD` at `esg_root` each time — dispositions per `deploy.md` step
7 (exit 0 → DEPLOYED; exit 3 → DEPLOYED with a stale-file flag; exit 1/2 →
stop). **Never run `install.ps1` from the worktree** — it uses
`$PSScriptRoot`, so invoking the worktree copy would install unmerged
branch content.

**Environment/dependency changes:** none. No new env vars, no new package
dependencies (hooks stay stdlib-only Python, untouched this period). No
version bump is required for the install path itself — `dcs/VERSION` ==
`package.json` equality is what the merge guard checks, not a bump — but
**the routine atomic version bump does apply at this incident's own
close**, per `dcs-commander`'s resolution at command point 2: Delegation
v4's `forbidden_topics` (which lists "version bump") bounds only Type-3
*auto*-approval, never in play for this Owner-approved Type 1, and a
version bump is deliberately an incident's own job precisely so a
release-bearing change gets Owner eyes — which this incident's own step 6b
already provides. `npm publish` specifically remains a separate,
Owner-only act (2FA OTP) that no session attempts.

**Migration ordering:** none — no schema, no persisted state, no running
service; every edit is in-place/additive to a file that already exists.
Binding ordering constraint is the installed-copy/running-session split:
(1) `/dcs-close` step 1a's guards must be green before merge; (2) never
install while an incident is active; (3) witness → install → witness; (4)
the behaviour change (criterion 1's/2's reduced reads) takes effect only
for sessions started after install — do not try to measure the saving in
the session that shipped it.

**Rollback plan:** additive case, no down-migration needed — nothing is
created, renamed, or deleted, so a re-checkout of the prior main commit
plus re-running the same install command fully restores the prior
payload. Rollback reference is the `dcs/token-economy` branch, kept until
`/dcs-deploy` confirms the ship. Blast radius of a bad ship is confined to
this machine's `~/.claude` — nothing is published.

## Risks

**From the Planning Chief:**

- Partition is by file, not by criterion, deliberately — criteria 2 and 4
  each span multiple taskings (2: S1/S2/S3; 4: S2/S3). Verified disjoint
  by inspection regardless.
- Criterion 4's two halves (S2's charter rule, S3's workflow inputs) must
  agree with no channel between the specialists during execution — both
  taskings state the contract in the same words; if they still drift, the
  mechanism is inert, never harmful (it just never fires).
- `schemas.md` is the one hot-path file in this partition, 719 B of
  measured slack. `doctrine.md` is in no territory, so the rest of the hot
  path cannot move this period. If S2 overshoots, the merge guard goes red
  at `/dcs-close` step 1a.
- Every criterion is verified **statically** this period, by construction
  of self-hosting: the running session reads the installed copy, this
  incident edits the repo, and the two don't converge until
  `/dcs-deploy`. No criterion can be verified by executing the changed
  workflow.
- The `@`-include resolution depth question (single- vs multi-level)
  stays open and is deliberately moot — criterion 1's fix is correct under
  either reading, and no criterion asserts a byte figure for the saving.
- This project's own ~250-line workflow budget is already breached
  (`plan.md` 663, `execute.md` 417, `deploy.md` 275, `close.md` 269) and
  enforced by nothing — a known, separate gap. S3/S4 must not grow their
  files materially and must report the delta.
- Two deliberate residuals: `dcs/templates/214-LOG.md`'s own header still
  describes a full resume-read (correctly untouched — may be genuinely
  necessary, the same principle-5 tension that sank criterion 5);
  criterion 6's brevity rule reaches only the five named locations, not
  `dcs-logistics-chief.md`/`dcs-situation-analyst.md` (AAR candidates, not
  this period).
- Criterion 3's only measurable deliverable this period is a **mechanism**,
  not a smaller live file — the 178,236 B figure does not move until the
  IC applies it at close. A Safety Officer finding the register unchanged
  has found the plan working as designed.

**From the Logistics Chief:**

- Hot-path budget (719 B headroom) is the one deploy-relevant ship-stopper
  risk, mitigated by criterion 5's drop (removes `doctrine.md` from every
  territory) and S2's own pre-return re-measurement.
- The budget is set on the **merge result**, and `main` can move under the
  incident — re-measure immediately before close, not against this
  branch.
- Check 13 (schema citation anchors) is sensitive to renumbering/retitling
  a `schemas.md` section — criterion 6 must stay additive within existing
  sections.
- CRLF/BOM on Windows is the likeliest way a routine merge turns red —
  covered by this project's existing Write/Edit-tools-only rule.
- No mechanical guard covers criterion 1's replacement read instructions
  (they become prose, not `@`-includes) — recommend a smoke-test of the
  automation layer in a fresh session after install, since this behaviour
  manifests only on a new session.
- The deploy train is portfolio-wide and serialized (`max_rows_per_train:
  3`) — re-measure the pending-row count at deploy time, not now.

## Verification plan

No behavioral repro path exists for this incident by construction (201:
measured static-loading and schema-completeness patterns, not a behavioral
bug), and no criterion can be verified by *running* the changed workflows
— the session executes the installed copy while this incident edits the
repo. Verification is: the enumerators return what the criteria say, the
guards stay green, and the two cross-tasking contracts (criterion 2's
three-specialist span, criterion 4's two-specialist span) actually meet.

1. **Guards, whole-tree, after all four specialists return:** `python
   tests/test_dcs_gate.py`, `python tests/test_dcs_intake.py`, `python
   tests/test_doctrine_integrity.py` — each read for its own `N/M passed`
   line (83/83 on the third before this period; regenerate, do not
   compare to a number written anywhere). The third also carries the
   hot-path budget check and is the merge-time guard at `/dcs-close` step
   1a.
2. **Criterion 1:** `grep -n '^@'` shows no phase-workflow file in either
   eager block, `@doctrine.md` in both, `@run.md` in `loop.md`'s. Then the
   omission check: for each of new/plan/execute/close.md, confirm run.md's
   corresponding step covers that workflow's `required_reading`
   generically. A step that reads the phase but not its references is a
   **refutation**, not a style note.
3. **Criterion 2:** run the corrected enumerator over the whole
   population; confirm every hit except `close.md:44`/`:69` is bounded.
   Known non-defects in the same output: `run.md:101-102`, `loop.md:49/
   102-103`, `plan.md:264`, `execute.md:248-252` are append instructions,
   not reads.
4. **Criterion 4, the interaction check:** read S3's `execute.md` step 8
   and S2's `agents/dcs-safety-officer.md` step 2 together; confirm the
   charter consumes exactly the inputs the workflow supplies, by name.
   Confirm by-reference citation is conditioned on a command the officer
   itself ran and is unavailable for anything in `files_touched`.
   Independently re-run S2's dry-run against
   `register-field-repair-path/SAFETY.md` (21,415 B / 3 verdicts) and
   spot-check two classifications, including the must-re-derive one.
5. **Criterion 3:** confirm `new.md` step 7b's ACTIVE-row scan is
   unaffected (both files unchanged is the correct, expected result);
   confirm the collapse instruction exists at all three write points and
   caps are numbers; confirm a `vault`-grep over the five touched files
   returns nothing. Do **not** expect the live register to have shrunk —
   that is `[IC]` work at close.
6. **Criterion 6:** grep confirms the rule in all five locations;
   re-measure the hot path (`doctrine + schemas <= 37,888 B`); confirm the
   rule did not become licence to paraphrase.
7. **Criterion 5:** nothing to verify — dropped. If still referenced
   anywhere as live, that is an IC bookkeeping miss to report, not an
   unmet criterion to halt on.
8. **IC work not in any tasking, owed before/at close:** compact this
   project's own live `REGISTER.md`/`STRATEGY.md` using S4's mechanism
   (re-running `wc -c` at that moment, not trusting this period's
   118,525 + 59,711 = 178,236 B reading); the atomic `dcs/VERSION` +
   `package.json` bump the merge guard requires.

## Deviation history (this period)

None — this is period 1's first IAP.
