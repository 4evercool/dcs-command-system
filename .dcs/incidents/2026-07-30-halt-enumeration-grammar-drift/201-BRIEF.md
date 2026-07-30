<!--
201-BRIEF.md — written by the IC from dcs-situation-analyst findings, once,
at the stem (/dcs-new). Never edited after typing is confirmed except to
append a note if a later period's assessment reveals the original blast
radius was wrong (append, don't rewrite -- 214-LOG.md is the append-only
one, but this file's Symptom/Evidence should stay a true record of what was
known at intake).
-->

# 201 — Incident Brief

**Incident:** halt-enumeration-grammar-drift
**Opened:** 2026-07-30
**Type:** 3

## Symptom

`vault/_scripts/incident_metrics.py:52` cannot regenerate correct halt counts. Its regex — `re.findall(r"SAFETY: halt", log)` — is an unanchored whole-file substring search using the pre-v0.6.9 grammar. This produces errors in BOTH directions: it over-counts (narrative text quoting a sentinel inside a body counts as a verdict — reports 10 "halts" for `energy-cost-model-rework` where an anchored grep finds 4 real `SAFETY: halt` sentinels) AND under-counts to zero (the regex cannot see the `SAFETY-HALT:` hyphen form v0.6.9 introduced — reports 0 halts for `schema-citation-guard`, which had one real `SAFETY-HALT:` sentinel). No single command currently regenerates correct halt counts spanning both grammars. The metrics doc (`vault/Metrics/incident-metrics.md`) carries derived halt counts that were produced by this broken script and are themselves unreliable — a stale, unreproducible number without the regenerating command beside it (principle 15).

The gate's own `halt_cycles()` is correct — both analysts independently verified it returns 0 for every incident log tested (all halts properly reset by PASS or STAMP anchors). The drift is entirely in the external telemetry surface.

## Evidence

- `vault/_scripts/incident_metrics.py:52`: `halts=len(re.findall(r"SAFETY: halt", log))` — unanchored, pre-v0.6.9 grammar. Source: Analyst 1 (codegraph+prior art), corroborated by Analyst 2 (repro+logs).
- Over-count proof: `energy-cost-model-rework` — script reports 10 halts; anchored `grep -c -E '^\[[^]]*\]\s+SAFETY: halt'` finds 4 real verdicts (lines 84, 194, 332, 356). Source: Analyst 1, register row's own Intake source cell.
- Under-count proof: `schema-citation-guard` — script reports 0 halts; `python dcs/hooks/dcs_gate.py --halt-count .dcs/incidents/2026-07-26-schema-citation-guard` returns 1. Source: Analyst 1, register row's own Intake source cell.
- `vault/Metrics/incident-metrics.md` lines 15-26 self-documents the defect: "reports 10 halts for energy-cost-model-rework where grep finds 4 real verdicts... cannot see the SAFETY-HALT: grammar v0.6.9 introduced, so it reports 0 halts for schema-citation-guard." Source: Analyst 1.
- Pre-v0.6.9 grammar form: `SAFETY: halt` (colon-space). Post-v0.6.9 grammar form: `SAFETY-HALT:` (hyphen, no space). Both grammars exist in incident logs. No single anchored regex currently spans both. Source: Analyst 1.
- `halt_cycles()` (dcs_gate.py:399-477) verified correct across all 20 incident directories — returns 0 for every closed incident. Source: Analyst 2.
- GRAMMAR_LINE text is verbatim-identical across all four prose surfaces (dcs_gate.py:133-137, doctrine.md principle 13, execute.md trigger (c), run.md step 6) — verified by test_doctrine_integrity.py check 12(c). Source: Analyst 1.

## Reproduction path

1. Run `python vault/_scripts/incident_metrics.py C:/DCS` — halts for `schema-citation-guard` (post-v0.6.9) = 0, halts for `energy-cost-model-rework` (pre-v0.6.9) inflated.
2. Run `python dcs/hooks/dcs_gate.py --halt-count C:/DCS/.dcs/incidents/2026-07-26-schema-citation-guard` — returns 1 (correct).
3. Read `vault/_scripts/incident_metrics.py:52` — regex is `r"SAFETY: halt"`, no anchor, wrong grammar form for post-v0.6.9 incidents.

## Blast radius (best guess at intake)

- `vault/_scripts/incident_metrics.py` — the broken regex
- `vault/Metrics/incident-metrics.md` — carries the unreliable derived numbers

Both in `vault/**` — unguarded by the gate (not in the guarded set). Territory is disjoint from any currently ACTIVE row (0 ACTIVE rows portfolio-wide at open).

## Prior art

Split from `safety-halt-functional-scope` at its stem (`new.md` step 4a), 2026-07-26. Register row already exists with evidence gathered by that incident's situation analysts. Promoted to rank 2 at the thirteenth `/dcs-esg`, 2026-07-30, as the Fable roadmap Phase 3 telemetry enabler (gates rec 8). The incident `halt-loop-unbounded` (2026-07-25) designed the current sentinel grammar — ENTRY_PREFIX, HALT_RE/PASS_RE/STAMP_RE, sentinel_of(), GRAMMAR_LINE — and its period 1 went through 3 revisions to eliminate the "one published form, one unpublished implementation detail" class of defect.

## Decomposition (step 4a — this stem's situation analysts found two additional latent defects)

| # | Defect | Territory | Verdict |
|---|--------|-----------|---------|
| B | `ENTRY_PREFIX` regex `*` quantifier: `^\[[^\]]*\]\s+` allows empty bracket content — `[] SAFETY-HALT:` classifies as 'halt', contradicting GRAMMAR_LINE's "mandatory timestamp." Latent, never exploited in any actual log. | `dcs/hooks/dcs_gate.py` | Split to `vault/Backlog.md` item 27 (L) |
| C | `execute.md` trigger (b) line 374: "Grep 214-LOG.md for prior SAFETY-HALT: lines before deciding" — provides no anchored regex pattern. A literal `grep "SAFETY-HALT:"` would count continuation-line quotations as verdicts. | `dcs/workflows/execute.md` | Split to `vault/Backlog.md` item 28 (L) |

## Type + rationale

**Proposed type:** 3
**Rationale:** Fix touches 2 vault files (incident_metrics.py regex + derived numbers in incident-metrics.md), problem is fully understood with both over-count and under-count independently verified, scope is bounded and estimable — but fails Type 5's ≤1-file criterion so Type 3 applies per 'when in doubt, type up'. Commander (dcs-commander, fable) at command point 1.
**Owner confirmation:** confirmed as proposed (Type 3)

## Intake source

QUEUED register row `halt-enumeration-grammar-drift` (rank 2, thirteenth `/dcs-esg`, 2026-07-30).
