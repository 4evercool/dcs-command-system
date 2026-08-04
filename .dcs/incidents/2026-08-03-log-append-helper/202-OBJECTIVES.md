<!--
202-OBJECTIVES.md -- written by the IC together with the Owner, at the
start of EACH operational period (/dcs-plan). Re-drafted (new file content,
same filename) each time the incident re-enters the P-loop for another
period -- the prior period's 202 is preserved in 214-LOG.md's phase-
transition history and, once complete, in AAR.md's summary, not in this
file itself.
-->

# 202 — Objectives (Operational Period 1)

**Incident:** log-append-helper
**Period:** 1 (increments each time the incident returns to this step)

## Goal

214-LOG.md phase-transition entries across future DCS incidents are written by a canonical, timestamp-honest append tool instead of by hand, carrying real-clock timestamps and operator identity — and a close-time guard catches any entry that still arrives backfilled or out of chronological order.

## Acceptance criteria (the Definition of Done)

<!-- Revised after Planning Chief + Logistics Chief review, period 1, before command point 2 -- tasking-lint 4a fixes (criteria 1/3/4/6 reworded, criterion 10 added), applied by the IC per plan.md step 4a ("a failure is yours to fix, never a reason to spend a command point"). Original wording preserved in 214-LOG.md's lint-result entry. -->

1. A stdlib-only append tool named `dcs_log.py` exists (final location — `dcs/hooks/` or `dcs/tools/` — decided at command point 2, per this repo's own hooks-vs-tools taxonomy) whose `append <slug> --by <operator> "<text>"` subcommand appends one line to `<slug>`'s `214-LOG.md`, carrying a real-clock timestamp derived at call time — never a caller-supplied override — verifiable by running it against a fixture incident directory and reading the resulting line, and by grepping its imports for stdlib-only modules.
2. The appended line's sentinel grammar is unchanged for `dcs_gate.py`'s existing parser: a sentinel token (`IAP-APPROVED:`, `SAFETY-HALT:`, `SAFETY-PASS:`) immediately after the bracket is still recognized by `sentinel_of()`/`halt_cycles()`, with no edit to `dcs_gate.py` itself required — verifiable by running `python dcs/hooks/dcs_gate.py --halt-count <fixture-dir>` against a fixture log written by the new tool and confirming the count matches hand-written entries of equivalent content.
3. Every entry the tool appends records the operator identity supplied at the call site, in a fixed position that leaves `dcs_gate.py`'s grammar intact, and the tool refuses to append when that identity is missing or empty — verifiable by criterion 2's proof plus an explicit refusal-on-missing-identity test.
4. Every genuine hand-written `214-LOG.md` append site — measured at the stem as 48 `214-LOG` mentions across 7 files, refined at planning to the six files that actually write (`new.md`, `plan.md`, `execute.md`, `close.md`, `run.md`, `loop.md`; `status.md` is read-only, confirmed by its own "No writes" text, and is not touched) — now invokes the append tool instead of free-text Edit/Write, with exactly two published exceptions (`new.md`'s template initialization, which creates rather than appends; `plan.md`'s multi-line preservation-map attachment, indented off column zero). Enforced as a new, permanent merge-guard check in `test_doctrine_integrity.py` that walks `dcs/workflows/*.md` and requires every append-instruction line to name the tool, with the two exceptions published and a non-empty-population degeneracy guard — verifiable by that check passing (a command returning no offending line), not by a one-time human-read grep.
5. `dcs/templates/214-LOG.md` and `dcs/references/forms.md` document the new canonical format (including the operator-identity field and the tool invocation, quoted verbatim from the tool's own exported constants), and `dcs/references/doctrine.md` principle 13's `GRAMMAR_LINE` quotation stays byte-exact — verifiable by `python tests/test_doctrine_integrity.py`'s existing verbatim-quote check (check 12) still passing, including its sole `sentinel_of() == 'stamp'` witness (`forms.md`'s rendered example block) surviving.
6. A new close-time criterion in `dcs/tools/record_integrity.py`, built on the existing `dcs_gate.py` dynamic-import + `split_log_entries()` pattern (not a re-derived copy of the grammar), goes red when a `214-LOG.md` dated on or after the criterion's effective date (historical logs are never retroactively broken) has N-or-more entries sharing one identical bracketed timestamp (N chosen and justified in the implementation) or two chronologically-comparable entries out of order; a bracket that fails to parse, or a comparison between a naive and an offset-aware timestamp, is reported as a note and is never a finding or a crash — proven against a clean fixture and at least one fixture of each violation shape, including the real legacy shapes named in this incident's 201 (bare dates, colon-less `+HHMM` offsets).
7. The new criterion from #6 is wired into `record_integrity.py`'s existing findings-collection flow, the same place the other five criteria run — not a standalone, unreferenced function.
8. New regression test coverage exists for `dcs_log.py` and the new close-time criterion, and a control run against the pre-fix state (or a deliberately broken fixture) demonstrates the new tests actually catch the defect shapes named in this incident's 201 — not passing vacuously.
9. `python tests/test_doctrine_integrity.py`, `python tests/test_dcs_gate.py`, and `python tests/test_dcs_intake.py` all pass at 100%, re-run independently by the IC — never trusted from a specialist's self-report alone. [IC]
10. `CHANGELOG.md` gains an entry for this incident's change under the existing, unpublished `## 0.8.0` heading — never a new version heading — with no `dcs/VERSION`/`package.json` bump. Measured claim, re-verified at planning time: `npm view dcs-command-system version` → `0.7.2` (2026-08-04), confirming 0.8.0 has not been published. [IC]

## Out of scope this period

Retrofitting any existing incident's historical `214-LOG.md` entries — the log is append-only and a past entry is never edited, per `references/forms.md`'s note on why. Widening `dcs_gate.py`'s `ENTRY_PREFIX` regex itself (already an independent, registered defect: `vault/Backlog.md` item 27). Adding `RECORD-CORRECTION:` to check 12's three-token sentinel census (split out at this incident's own stem as an independent root cause, routed to `vault/Backlog.md` item 31 rather than folded in here). An end-to-end demonstration of a live session actually appending through the tool — sessions read workflows from the installed copy, install is forbidden mid-incident (`CLAUDE.md` hard rule) and is itself the deploy step, so that proof belongs to `/dcs-deploy`, not this period's Safety Officer.

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

Planning Chief flagged 7 points (verbatim in `214-LOG.md`'s tasking-lint entry and the Planning Chief's own transcript); the IC resolved the wording-level ones directly per lint 4a and left one open for command point 2:

1. Criterion 4's original population claim was measured-false (`status.md` has zero write sites; `loop.md` has one, not several) — **resolved**: criterion 4 reworded above to the correct 6-file population, `status.md` explicitly excluded.
2. Criterion 4 wasn't enumeration-shaped (lint 3a) — **resolved**: reworded to name the mechanical merge-guard check (T9) as the actual proof.
3. Criterion 1 pinned `dcs/hooks/` when this repo's own taxonomy (operator-invoked CLIs live in `dcs/tools/`, alongside `record_integrity.py`/`preservation_map.py`/`verdict_rerun.py`) argues for `dcs/tools/` — **left open for command point 2**, since it's a real design judgment, not arithmetic. Criterion 1 reworded to not hardcode the answer.
4. Criterion 6's `N` needed cross-tasking coordination — **resolved by the Chief itself** (plan decision: `DUPLICATE_TIMESTAMP_THRESHOLD = 3`, exported as a constant S4 reads rather than retypes).
5. Criterion 6's "out of chronological order" wasn't decidable over the real corpus (`datetime.fromisoformat` rejects colon-less `+HHMM` offsets and can't compare naive-vs-aware) — **resolved**: criterion 6 reworded to require unparseable/incomparable brackets be reported as notes, never findings or crashes.
6. Criterion 3's "records operator/model identity" wasn't independently verifiable (a process can't attest which model invoked it) — **resolved**: reworded to "records the operator identity supplied at the call site... refuses to append when missing/empty," which is checkable.
7. No unmeasured volatile claims found; criterion 9 correctly [IC]-tagged; `doctrine.md` needs no edit this period (principle 16 already covers new `record_integrity.py` criteria generically).

Point 3 (tool location) and the Logistics Chief's independent, convergent finding of the same datetime-parsing hazard (point 5) go to command point 2 alongside the full IAP.
