<!--
AAR.md -- After Action Report, written by the IC during /dcs-close.
-->

# AAR — After Action Report

**Incident:** check-14-hardening
**Type:** 3
**Opened:** 2026-07-29
**Closed:** 2026-07-29
**Operational periods:** 1 (revision 2 after deviation)

## Outcome

All 5 acceptance criteria met. Check 14 (`tests/test_doctrine_integrity.py`) now catches both known silent-pass failure modes:

1. **Facet (a) — vacuous pass on dropped citation:** `check_zero_cite=True` wired into the per-file comparator loop. A declaring paragraph with zero `agents/dcs-safety-officer.md` step citations now causes check 14 to FAIL. Negative-proof test added. Four pre-existing zero-citation sites in `agents/dcs-safety-officer.md`, `dcs/references/schemas.md`, `dcs/workflows/execute.md`, and `dcs/workflows/plan.md` each received explicit step-6 citations.

2. **Facet (b) — bare census outside charter scope:** Bare-`N of M` census check extended to `dcs/references/doctrine-appendix.md` with quotation-aware regex — catches `N of M` inside double-quoted spans without false-positiving on ordinary prose. The bare "13 of 17" replaced with qualitative language.

3. **Vocabulary:** "declaring site" (token co-occurrence) distinguished from "citation" (explicit charter reference) in check output and comments.

122/122 tests pass. 0 Safety refutations, 0 advisories. All three test suites green (doctrine_integrity 122/122, dcs_gate 100/100, dcs_intake 10/10).

## What worked

- Planning Chief's partition was correct: single specialist, disjoint 4-file territory for the citation-addition replan
- The `check_zero_cite` parameter design was sound — the function accepted it, the negative-proof test used it, only the per-file loop wiring was missed
- The deviation surfaced real pre-existing gaps rather than false positives — the check earned its keep on its first run
- Delegation v4 auto-approval worked correctly for both the original IAP and the replan (all bounds held)

## Lessons

- A mechanical guard that finds real instances on its first activation is working correctly, not failing — the 118/122 result was the check doing its job, and the deviation was a scope question (fix the found instances or document them), not a planning defect
- When adding a boolean flag to a function called from multiple sites, audit every call site — the negative-proof test passing doesn't mean the per-file loop uses it
- The declaring-site predicate (advisory token AND refutation/halt token co-occurrence) in the charter file itself creates a self-citation requirement — the charter defining step 6 must cite step 6

## Deviations this incident

1. **Safety halt (period 1):** Criterion 1 — per-file loop at line 873-874 called `_bar_paragraph_problems()` without `check_zero_cite=True`. Fixed with `fix_taskings` → one argument added.

2. **Deviation (fix-tasking S1-fix1):** `check_zero_cite=True` correctly flagged 4 pre-existing zero-citation sites outside the specialist's territory. Owner chose to expand scope → replan with widened territory (2 → 6 files). Full `plan.md` cycle (6c unavailable — territory change).

## Memory routing

Project CLAUDE.md documents `vault/` as the memory system. Lesson routed to `vault/Meta/building-dcs-lessons.md` (or nearest equivalent) — the "audit every call site when adding a parameter" lesson. The two deviation instances are already recorded in the incident's own artifacts.

## Intake source closure

`vault/Backlog.md` item 16 — internal DCS backlog. Flagged for Owner: mark item 16 as resolved (the two facets it describes are now fixed). Not written directly — Owner action via `/dcs-esg` or manual update.

## Deploy status

Not deployed — merged to `dcs/check-14-hardening`, pending merge to main and `/dcs-deploy`. Deploy evidence will be `python tests/payload_check.py` exit 0 after install.

## Safety Officer's final verdict (verbatim)

**Verdict:** pass
**Refutations:** 0
**Advisories:** 0

All 5 acceptance criteria verified independently. 122/122 tests pass. `check_zero_cite=True` confirmed at per-file loop. All 9 citations added across 4 files confirmed. Bare-census fix confirmed. Vocabulary confirmed. Three test suites green.
