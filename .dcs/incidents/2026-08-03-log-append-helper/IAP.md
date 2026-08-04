<!--
IAP.md -- the Integrated Action Plan, written by the IC during /dcs-plan.
This is the ONLY document specialists execute against once approved -- the
single source of truth doctrine principle 3 insists on. Editing this file
after approval voids IAP-APPROVED automatically (hash mismatch) -- that is
deliberate, not a bug to route around.
-->

# IAP — Incident Action Plan

**Incident:** log-append-helper
**Type:** 1
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `203-ORG.md` · `204-TASKING/S1.md` · `204-TASKING/S2.md` · `204-TASKING/S3.md` · `204-TASKING/S4.md` · logistics plan below

## Objectives (summary of 202)

**Goal:** 214-LOG.md phase-transition entries across future DCS incidents are written by a canonical, timestamp-honest append tool instead of by hand, carrying real-clock timestamps and operator identity — and a close-time guard catches any entry that still arrives backfilled or out of chronological order.

**Acceptance criteria:**
1. A stdlib-only append tool `dcs_log.py` (**`dcs/tools/dcs_log.py`** — decided at command point 2) whose `append <slug> --by <operator> "<text>"` appends one line carrying a real-clock timestamp, never a caller-supplied override.
2. The appended line's sentinel grammar is unchanged for `dcs_gate.py`'s existing parser — no edit to `dcs_gate.py` required.
3. Every entry records the operator identity supplied at the call site; the tool refuses to append when it's missing or empty.
4. All 6 genuine hand-written append sites (`new.md`, `plan.md`, `execute.md`, `close.md`, `run.md`, `loop.md`; `status.md` is read-only, untouched) now invoke the tool, with 2 published exceptions, enforced by a new permanent merge-guard check.
5. `dcs/templates/214-LOG.md` and `dcs/references/forms.md` document the new format, quoting the tool's own exported constants verbatim; `doctrine.md` principle 13's `GRAMMAR_LINE` stays byte-exact.
6. A new close-time criterion in `record_integrity.py` catches N+ duplicate timestamps or out-of-order entries, date-scoped so history is never retroactively broken, with unparseable/incomparable brackets reported as notes, never findings or crashes.
7. The new criterion is wired into `record_integrity.py`'s existing findings chain.
8. New regression test coverage exists, proven non-vacuous by control runs.
9. All 3 existing test suites pass at 100%, re-run independently by the IC. [IC]
10. `CHANGELOG.md` gains an entry under the existing unpublished `0.8.0` heading; no version bump. [IC]

Full text, including the tasking-lint revision history and Chief-feedback resolution log: `202-OBJECTIVES.md`.

## Tactics (from the Planning Chief)

1. **Import the rule, never re-derive it** — `dcs_log.py` loads `dcs_gate.py` dynamically (`importlib.util.spec_from_file_location`, the same idiom `record_integrity.py` already uses) and calls only its `render_entry()`, `sentinel_of()`, `find_project_root()`, `resolve_incident_dir()` — no regex, no entry template, no path literal typed a second time anywhere.
2. **Self-validation before write** — after rendering, the tool classifies its own output through the real `sentinel_of()` and refuses to append unless the classification matches what was requested. A future grammar change breaks the tool loudly at call time, never quietly at audit time.
3. **Containment lives in the tool** — `dcs_gate.py` matches only Edit/Write/NotebookEdit, never Bash, so a Bash-invoked log writer is structurally invisible to it. The tool takes a slug, never a path, resolves only through the imported project/incident-directory functions, and refuses on any slug containing a path separator or `..`, or when the target doesn't already exist.
4. **Fail closed, documented as a deliberate exception** to `CLAUDE.md`'s "every hook fails open" default — a silently dropped log entry is exactly the defect this incident exists to close.
5. **The clock is the tool's, full stop** — offset-aware, second-resolution, explicitly passed (never the module's naive default), no flag/env/config channel to override it.
6. **Date-scope the new criterion** exactly like the existing `record_integrity.py` safety-fence pattern — a rule never retroactively reddens logs written before it existed, with three always-printed dispositions, never a silent skip.
7. **Pure comparator / IO collector split** for the new criterion, mirroring this module's own existing convention — lets the decision logic be unit-tested with no filesystem fixture at all.
8. **Duplicate detection needs no parsing; order detection does** — duplicates are found on the raw bracket string (works on every legacy shape); only adjacent, mutually-comparable, parseable pairs are checked for order, with everything else reported as a note.
9. **Criterion 4 becomes a permanent merge-guard check**, not a one-time sweep — a prose instruction decays the first time someone adds a workflow step.
10. **Bind docs to code with a carrier check** — the tool's own exported `INVOCATION`/`FORMAT_LINE` constants are quoted verbatim in `forms.md` and bound there by a new merge-guard case, the same pattern this repo already uses for `preservation_map.py` and `record_integrity.py`.

## File-territory partition

| Specialist | Territory | Forbidden (highlights) |
|---|---|---|
| S1 | `dcs/tools/dcs_log.py` | `dcs/hooks/dcs_gate.py`, `dcs/tools/{record_integrity,preservation_map,verdict_rerun}.py`, `dcs/workflows/**`, `tests/**`, `.dcs/**` |
| S2 | `dcs/tools/record_integrity.py` | `dcs/hooks/**`, `dcs/tools/dcs_log.py`, `dcs/tools/{preservation_map,verdict_rerun}.py`, `dcs/workflows/**`, `tests/**`, `.dcs/**` |
| S3 | `dcs/workflows/{new,plan,execute,close,run,loop}.md`, `dcs/templates/214-LOG.md`, `dcs/references/forms.md` | `dcs/workflows/{status,init,deploy,esg}.md`, `dcs/references/{doctrine,doctrine-appendix,schemas}.md`, `dcs/hooks/**`, `dcs/tools/**`, `tests/**` |
| S4 | `tests/test_dcs_log.py`, `tests/test_doctrine_integrity.py`, `tests/fixtures/log-order/**` | `tests/{test_dcs_gate,test_dcs_intake,test_dcs_cli,payload_check,release_provenance_check}.py`, existing `tests/fixtures/**` dirs, `dcs/**`, `.dcs/**` |

**Partition status:** disjoint — parallel execution. Verified by the IC's tasking-lint pass (checks 1/4) both before and after command point 2's directory correction moved S1 into `dcs/tools/`, alongside S2; the two now share a directory but not a file, and each explicitly forbids the other's file.

**Execution mode note (command point 2 ruling):** all four specialists run in parallel. S4's own suite will legitimately report red-by-name on its guarded-import cases until S1 and S2 land — a documented, precedented pattern in this repo (`test_doctrine_integrity.py:2343-2352`, `close-integrity-guard-bundle`'s own four-way parallel tasking) and the required non-vacuity control-run evidence for criterion 8, not a partition violation or a sign of trouble.

## Deploy / environment plan (Logistics Chief)

**Deploy path:** standard single-shot `install.ps1`/`install.sh` after `/dcs-close`, run from the clean `C:\DCS` main checkout — `robocopy /E` copies the whole `dcs/` tree, so `dcs/tools/dcs_log.py` needs no file-specific registration anywhere; witnessed by `tests/payload_check.py`'s content witness (expected: exit 0, all identical). No scoped or staged deploy is needed or possible.

**Environment / dependencies:** none. Stdlib-only tool, no `package.json`/`dcs/VERSION` change. **Binding:** workflows invoke the tool by its installed-copy absolute path (`$HOME/.claude/dcs/tools/dcs_log.py`), never the repo-relative form — the repo-relative form would silently lose every onboarded non-DCS project's log. `dcs_log.py` must never be added to `new.md`'s project-hook-copy list (`init.md:73-77`'s "all three hooks") — it stays payload-referenced by absolute path, not project-copied, or it inherits the drifting-second-copy problem the dynamic-import pattern exists to avoid.

**Migration ordering:** none beyond the existing single-copy install; `CLAUDE.md`'s "never install mid-incident" hard rule is the only ordering constraint and fully covers the version-skew hazard between old/new workflow text and the tool's presence. This incident's own `214-LOG.md` is the one log spanning the ship; it closes before install and so is never judged by the new criterion (criterion 6's date scope confirms this — see 202 criterion 6 and S2's tasking).

**Rollback plan:** normal path — `git revert` on `main`, re-run `install.ps1`, re-run `payload_check.py`. Neither installer purges deleted files, so a rollback leaves `dcs_log.py` orphaned on disk (harmless; witness reports `installed-only`, `deploy.md` step 7's existing non-stop disposition — not a fresh failure mode). **The one real deadlock to plan around, not discover:** if the new close-time criterion false-positives while a future incident is `ACTIVE`, that incident cannot merge (fail-closed, escalation trigger a) and install is forbidden mid-incident, so the only exit is a 209 sitrep to the Owner. Mitigated by the binding pre-ship corpus dry-run (S2's tasking) run before this incident's own close trains.

**Risks (Logistics):** `dcs/hooks/**` sat in the current Delegation's `forbidden_globs` at both levels; moving the tool to `dcs/tools/` removes it from that specific glob, but Type 1 already requires full Owner IAP approval regardless, so there is no marginal delegation cost now — noted for `/dcs-deploy` later, where the model floor (`approved_models` absent from Delegation v6) already forces an Owner prompt on any row.

## Risks (integrated — Planning Chief + Logistics Chief, all threaded into taskings as hard constraints)

- **R1 — line budget.** `close.md`/`execute.md` measured at exactly 250/250 lines (zero margin), `plan.md` 249/250. S3's conversion is net-line-negative by construction if executed as specified; the before/after budget table is required evidence with no rescue path elsewhere (S4 is explicitly forbidden from touching `WORKFLOW_GRANDFATHERED_LINES`).
- **R2 — check 12's sole stamp witness** lives in `forms.md`'s fenced example block (S3's territory); must survive intact alongside the new tool invocation, never replaced by it.
- **R3 — S4 legitimately red until S1/S2 land** — precedented, captured as control-run evidence, not a defect (see execution-mode note above).
- **R4 — this incident's own close could be reddened by its own new criterion** — mitigated by date-scoping keyed to the incident directory's opening date (`2026-08-03`), confirmed by S2's required control run against the live log. **Sharpened at command point 2:** real time crossed the effective date (`2026-08-04`) mid-incident, so this log's own later entries carry an `08-04` bracket without that changing the directory's opening date — the scope test must key on the directory name, never on individual entries.
- **R5 — no live end-to-end verification is possible this period** (sessions read workflows from the installed copy; install is the deploy step) — explicitly out of scope, not a gap to chase.
- **R6 — CHANGELOG/version bump is unowned by any specialist, by design**, to prevent a two-specialist collision on `package.json`/`dcs/VERSION`. Owned by the IC as 202 criterion 10.
- **R7 — containment: Bash-invoked writers are invisible to `dcs_gate.py`'s Edit/Write/NotebookEdit matching.** Pre-existing exposure (any Bash-capable agent already has unmediated `>>`), and the tool narrows rather than widens it — but the Safety Officer must independently probe both containment refusals named in S1's and S4's taskings (command point 2, binding).
- **R8 — S3/S4 depend on S1's exported constants without seeing the file land.** Mitigated: `INVOCATION`'s exact text is pinned in this IAP and in S1's tasking; S1 must return `file:line` proof; S3 must re-read the landed file before finishing.
- **R9 — the `--sentinel stamp` self-check enforces `plan.md` step 8's existing hash-first rule mechanically** — S3's own step-8 invocation must order the stamp body hash-first or the tool will correctly refuse it.

## Verification plan

**A. The original 201 repro path gets a mechanical answer.** Re-run all four of the 201's repro steps; the decisive one is running the new criterion (date scope bypassed in a scratchpad copy) against the two real logs the 201 cites (`status-md-enum-drift`, `worktree-path-propagation`) — it must find the 11-entry identical-bracket run and must not crash on the mixed-offset/timestamp-less lines.

**B. All three existing suites plus the new one pass, re-run independently by the IC** (criterion 9): `test_dcs_gate.py`, `test_dcs_intake.py`, `test_doctrine_integrity.py` (baselines 100/100, 18/18, 196/196 — must show MORE than 196 cases post-integration, or S4's new checks silently failed to register), `test_dcs_log.py` (new).

**C. Check 12 survives the prose edits** — verified directly (not inferred from the suite's aggregate pass) via the script in the Planning Chief's verification_plan §C: every population file quotes `GRAMMAR_LINE` verbatim, every fenced sentinel line classifies non-`None`, at least one `'stamp'` witness survives, and `close.md`/`new.md`/`loop.md` gained no sentinel-token literal.

**D. The workflow budget holds** — every touched file at or under its ceiling, counted with the guard's own semantics, and `WORKFLOW_GRANDFATHERED_LINES` still names only `new.md`.

**E. The partition held** — `git diff --name-only` against `main` shows every changed path in exactly one specialist's declared territory; `dcs/hooks/dcs_gate.py` and `dcs/references/doctrine.md` are confirmed unchanged.

**F. One manual read.** The four lines S1's round-trip evidence produces, read as an audit trail by a human: real offset-aware timestamp, legible body, an operator identity someone could be held to. The whole incident exists because 33 logs on disk look auditable but aren't — a format that satisfies every mechanical criterion and still reads as noise would be a failure the tests can't see.

**G. Not verifiable this period, and should not be attempted:** a live session actually appending through the tool. That proof belongs to `/dcs-deploy`, after install — not to this period's Safety Officer.

## Deviation history (this period)

None — first IAP of period 1.
