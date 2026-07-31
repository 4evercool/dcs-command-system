# 202 — Objectives (Operational Period 1)

**Incident:** status-md-enum-drift
**Period:** 1

## Goal

`dcs/workflows/status.md`'s instruction to print the register table carries the correct seven-state enum matching `dcs/templates/REGISTER.md:26-27`, so `/dcs-status` output accurately reflects the incident portfolio.

## Acceptance criteria (the Definition of Done)

1. `dcs/workflows/status.md:102-103` lists all seven register states: `QUEUED | ACTIVE | MERGED (deploy pending) | DEPLOYED | PARKED | KILLED | RESOLVED` — matching `dcs/templates/REGISTER.md:26-27` verbatim.
2. The word `CLOSED` does not appear as a register state in `dcs/workflows/status.md`. (The historical `ACTIVE → CLOSED` reference in `dcs/workflows/close.md:183,221` is a deliberately kept cross-reference target — out of scope.)
3. The surrounding prose correctly describes which rows give the Owner history at a glance (the terminal and post-close states: MERGED, DEPLOYED, KILLED, RESOLVED) rather than the non-existent `CLOSED`.
4. `python tests/test_doctrine_integrity.py` passes with the same count as before the change (no regression).
5. `grep -c "QUEUED" dcs/workflows/status.md` returns ≥ 1 (the fixed line is present and the state name still appears).

## Out of scope this period

- Adding a mechanical guard in `tests/test_doctrine_integrity.py` to catch register-state-enum drift across files. That is a separate question; this incident fixes the known drifted surface.
- Altering `dcs/workflows/close.md:183,221` — the `CLOSED` references there are intentionally kept historical cross-reference targets with self-documented supersession.

## Chief feedback

(filled in after Planning Chief returns)
