# IAP — Incident Action Plan

**Incident:** status-md-enum-drift
**Type:** 3
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `204-TASKING/S1.md`

## Objectives (summary of 202)

**Goal:** `dcs/workflows/status.md`'s instruction to print the register table carries the correct seven-state enum matching `dcs/templates/REGISTER.md:26-27`, so `/dcs-status` output accurately reflects the incident portfolio.

**Acceptance criteria:**
1. `dcs/workflows/status.md:102-103` lists all seven register states: `QUEUED | ACTIVE | MERGED (deploy pending) | DEPLOYED | PARKED | KILLED | RESOLVED` — matching `dcs/templates/REGISTER.md:26-27` verbatim.
2. The word `CLOSED` does not appear as a register state in `dcs/workflows/status.md`. (The historical `ACTIVE → CLOSED` reference in `dcs/workflows/close.md` is a deliberately kept cross-reference target — out of scope.)
3. The surrounding prose correctly describes which rows give the Owner history at a glance (the terminal and post-close states: MERGED, DEPLOYED, KILLED, RESOLVED) rather than the non-existent `CLOSED`.
4. `python tests/test_doctrine_integrity.py` passes with the same count as before the change (no regression).
5. `grep -c "QUEUED" dcs/workflows/status.md` returns ≥ 1 (the fixed line is present and the state name still appears).

## Tactics (from the Planning Chief)

- Replace the drifted four-state parenthetical in `dcs/workflows/status.md` line 102-103 with the canonical seven-state enum from `dcs/templates/REGISTER.md:26-27`, using `|` as separator to match the template verbatim per criterion 1.
- Remove the word CLOSED as a register state and re-express the history-at-a-glance clause to name the actual terminal/post-close states (MERGED, DEPLOYED, KILLED, RESOLVED) per criterion 3 — the close.md historical references are untouched.

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | `dcs/workflows/status.md` | `dcs/templates/**`, `dcs/references/**`, `dcs/workflows/close.md`, `tests/**`, `agents/**`, `skills/**`, `dcs/hooks/**`, `dcs/VERSION`, `package.json`, `install.*` |

**Partition status:** disjoint — parallel execution (single specialist)

## Risks

- Single file, single tasking — no partition conflict possible. The close.md historical CLOSED references (lines 183, 221) are deliberately excluded from territory and forbidden; if the specialist accidentally touches close.md, the Safety Officer will catch it.

## Verification plan

1. Read `dcs/workflows/status.md` line 102-103 (and any continuation lines added): confirm the parenthetical lists all seven states `(QUEUED | ACTIVE | MERGED (deploy pending) | DEPLOYED | PARKED | KILLED | RESOLVED)` with `|` separator matching REGISTER.md verbatim.
2. Confirm CLOSED does not appear as a register state in status.md (`grep -n 'CLOSED' dcs/workflows/status.md` — no output).
3. Confirm the history-at-a-glance clause references the four terminal/post-close states (MERGED, DEPLOYED, KILLED, RESOLVED), not CLOSED.
4. Run `python tests/test_doctrine_integrity.py` — must pass.
5. Run the 201 repro path: read status.md at the corrected location and confirm it no longer shows the four-state drifted list.
6. Spot-check that `dcs/workflows/close.md` was not modified (`git diff --stat` shows only status.md changed).

## Deviation history (this period)

None — first IAP for this period.
