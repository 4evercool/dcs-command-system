<!--
202-OBJECTIVES.md -- written by the IC together with the Owner, at the
start of EACH operational period (/dcs-plan). Re-drafted (new file content,
same filename) each time the incident re-enters the P-loop for another
period -- the prior period's 202 is preserved in 214-LOG.md's phase-
transition history and, once complete, in AAR.md's summary, not in this
file itself.
-->

# 202 — Objectives (Operational Period 1)

**Incident:** halt-enumeration-grammar-drift
**Period:** 1

## Goal

`vault/_scripts/incident_metrics.py` produces correct, regenerable halt counts for every incident — spanning both the pre-v0.6.9 (`SAFETY: halt`) and post-v0.6.9 (`SAFETY-HALT:`) grammar forms, counting only sentinels at column zero per `dcs_gate.py`'s GRAMMAR_LINE, never narrative mentions — and `vault/Metrics/incident-metrics.md` carries no stale derived number without a regenerating command beside it.

## Acceptance criteria (the Definition of Done)

1. `vault/_scripts/incident_metrics.py`'s halt-counting regex is anchored at column zero and matches both `SAFETY: halt` (pre-v0.6.9) and `SAFETY-HALT:` (post-v0.6.9) sentinel forms — a narrative mention, a continuation-line quotation, or a token without a bracketed timestamp prefix is never counted.
2. Running the script on this repo's `.dcs/incidents/` returns a halt count for `schema-citation-guard` (post-v0.6.9, one real `SAFETY-HALT:`) that is ≥ 1 and not zero.
3. Running the script on a repo with a pre-v0.6.9 incident (bread_bot's `energy-cost-model-rework`) returns a count ≤ the anchored-grep count, never inflated by narrative mentions.
4. `vault/Metrics/incident-metrics.md` carries no bare derived halt number — every count either has the regenerating command beside it (per principle 15), or the number is removed and replaced with the command output format (e.g. "regenerate with: `python vault/_scripts/incident_metrics.py <repo>`").
5. The script's halt-counting function is callable both as a CLI (`python vault/_scripts/incident_metrics.py <repo>`) and importable (`from vault._scripts.incident_metrics import count_halts` or equivalent) — the latter so `test_doctrine_integrity.py` or a future test can verify the count without scraping stdout.

## Out of scope this period

- `dcs_gate.py` ENTRY_PREFIX `*` quantifier (latent — backlog item 27)
- `execute.md` trigger (b) missing anchored regex (documentation gap — backlog item 28)
- Neither is in this incident's territory (`vault/**`); both are L-priority and were split out at the stem (`new.md` step 4a)

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

{{objectives_feedback from the chief-plan schema}}
