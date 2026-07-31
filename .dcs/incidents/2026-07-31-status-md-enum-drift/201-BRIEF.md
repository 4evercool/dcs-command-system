# 201 — Incident Brief

**Incident:** status-md-enum-drift
**Opened:** 2026-07-31
**Type:** 3

## Symptom

`dcs/workflows/status.md:102-103` instructs printing the register table with a four-state list (`QUEUED / ACTIVE / PARKED / CLOSED`) that does not match the canonical seven-state enum defined in `dcs/templates/REGISTER.md:26-27` (`QUEUED | ACTIVE | MERGED (deploy pending) | DEPLOYED | PARKED | KILLED | RESOLVED`). The value `CLOSED` is a pre-v0.3 term (superseded by `MERGED (deploy pending)`) and is not a current state. Three states (`MERGED`, `DEPLOYED`, `KILLED`) and the terminal state `RESOLVED` are missing from the status.md paraphrase. A user running `/dcs-status` sees an instruction that references states that do not exist and omits states that do.

## Evidence

- `dcs/workflows/status.md:102-103` — incorrect four-state list: `QUEUED / ACTIVE / PARKED / CLOSED`, with `CLOSED` described as "gives the Owner history at a glance" (source: file read, Analyst 1)
- `dcs/templates/REGISTER.md:26-27` — canonical state enum: `QUEUED | ACTIVE | MERGED (deploy pending) | DEPLOYED | PARKED | KILLED | RESOLVED` — seven states, `CLOSED` is not among them (source: file read, both analysts)
- `dcs/references/forms.md:22` — correct restatement of all seven states: `QUEUED / ACTIVE / MERGED / DEPLOYED / PARKED / KILLED / RESOLVED` (source: file read, Analyst 2)
- `dcs/workflows/close.md:183,221` — carries a deprecated `ACTIVE → CLOSED` reference, but self-documents the supersession at line 220-221: "v0.3: this transition now happens at step 5a.3 (`ACTIVE` → `MERGED`, not `ACTIVE` → `CLOSED`)" — this is a deliberately kept historical cross-reference target, not a defect (source: file read, Analyst 2)
- `tests/test_doctrine_integrity.py` — 123/123 tests pass; no check validates register-state-enum consistency across consumer files (source: test run, both analysts)
- `grep -rn "QUEUED" dcs/ --include=*.md` — four enumeration-carrying surfaces: REGISTER.md (×2, canonical), forms.md (correct), status.md (incorrect) — three correct, one drifted (source: grep, Analyst 2)

## Reproduction path

1. Open `dcs/workflows/status.md` at line 102.
2. Observe: `Read REGISTER.md and print its full table (QUEUED / ACTIVE / PARKED / CLOSED, all rows — CLOSED rows give the Owner history at a glance).`
3. Open `dcs/templates/REGISTER.md` at line 26.
4. Observe the canonical comment: `QUEUED | ACTIVE | MERGED (deploy pending) | DEPLOYED | PARKED | KILLED | RESOLVED` — seven states, `CLOSED` is absent.
5. The gap is visible by inspection: status.md names 4 states including one that does not exist; the real enum has 7.

## Blast radius (best guess at intake)

- `dcs/workflows/status.md` — the drifted file, lines 102-103
- `dcs/templates/REGISTER.md` — authoritative source, not changed
- `dcs/references/forms.md` — correct restatement, not changed
- `dcs/workflows/close.md` — carries intentional historical `CLOSED` reference with self-documented supersession; not a defect
- `tests/test_doctrine_integrity.py` — no check exists for this class of drift; adding one is a separate question, not part of this incident

## Prior art

Discovered and registered as `status-md-enum-drift` on 2026-07-27, split from the `direct-resolution-lane` incident's stem (`.dcs/incidents/2026-07-27-direct-resolution-lane/201-BRIEF.md:180-181`). Ranked at position 17 in the sixth `/dcs-esg` (2026-07-27), later at position 13. Never opened until now.

Related class: `halt-enumeration-grammar-drift` (2026-07-30, DEPLOYED) — same structural defect shape (a copy drifts from its source of truth, no mechanical check catches it) in a different surface (`vault/_scripts/incident_metrics.py`). Its AAR lesson: "A metrics script whose counting regex rots against the grammar it is counting produces numbers that mislead in both directions."

## Type + rationale

**Proposed type:** 3
**Rationale:** Bounded to one workflow file, but the fix is a wording judgment, not a find-and-replace — the "CLOSED rows give the Owner history at a glance" clause must be re-expressed under the v0.3 seven-state model — it is the second recurrence of the enum-drift class in a shipped workflow surface with no consistency check in the test suite, and project guidance types workflow changes as Type 3, so "when in doubt, type up" applies. (IC=dcs-commander, fable)
**Owner confirmation:** confirmed as proposed (Type 3)

## Intake source

`.dcs/esg/REGISTER.md` — QUEUED row `status-md-enum-drift`, ranked L (rank 13), originally split from `direct-resolution-lane` stem (2026-07-27)
