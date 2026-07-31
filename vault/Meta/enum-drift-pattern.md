# Enum-Drift Pattern — Two Instances, One Root

Two shipped incidents, one defect class: a prose restatement of a structured
enumeration drifts from its canonical definition, and no mechanical check
catches it. Both were caught by human inspection during unrelated incident
work.

## Instances

| # | Incident | Drifted surface | Canonical source | Closed |
|---|---|---|---|---|
| 1 | `halt-enumeration-grammar-drift` | `vault/_scripts/incident_metrics.py` — regex counting halt sentinels | `dcs_gate.py`'s `GRAMMAR_LINE` grammar | 2026-07-30 |
| 2 | `status-md-enum-drift` | `dcs/workflows/status.md:102-103` — four-state list with non-existent `CLOSED` | `dcs/templates/REGISTER.md:26-27` — seven-state enum | 2026-07-31 |

## Common shape

1. A **canonical definition** exists in one file (grammar in `dcs_gate.py`,
   state enum in `REGISTER.md`).
2. A **consumer** restates it in prose (regex in a metrics script, a
   parenthetical in a workflow instruction).
3. The consumer **drifts** — the canonical source is updated, the prose copy
   is not.
4. **No mechanical check** compares the consumer against the source of truth.
5. The drift is found by **human inspection** during unrelated work.

## What was fixed

- Instance 1: fixed the metrics script's regex to match the grammar.
- Instance 2: fixed the status.md parenthetical to match the register enum.

## What was NOT fixed

Neither incident added a guard that mechanically compares consumer surfaces
against their canonical sources. The set of enumeration-carrying surfaces is
small (4 files carry the state enum; the grammar has one consumer), and a
check would be cheap — but neither incident's scope included building one.
That remains a candidate for a future incident.

## Related

- `vault/Decisions/` — no decision record yet for whether to add a guard
- `dcs/workflows/close.md:183,221` — intentionally kept historical `CLOSED`
  references with self-documented supersession; not drift, but a reminder
  that every kept historical reference is a future grep false-positive
