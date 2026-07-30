<!--
IAP.md -- the Integrated Action Plan, written by the IC during /dcs-plan.
This is the ONLY document specialists execute against once approved.
-->

# IAP — Incident Action Plan

**Incident:** halt-enumeration-grammar-drift
**Type:** 3
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `204-TASKING/S1.md` · `204-TASKING/S2.md` (203 skipped — default Type 3 activation)

## Objectives (summary of 202)

**Goal:** `vault/_scripts/incident_metrics.py` produces correct, regenerable halt counts for every incident — spanning both the pre-v0.6.9 (`SAFETY: halt`) and post-v0.6.9 (`SAFETY-HALT:`) grammar forms, counting only sentinels at column zero per `dcs_gate.py`'s GRAMMAR_LINE, never narrative mentions — and `vault/Metrics/incident-metrics.md` carries no stale derived number without a regenerating command beside it.

**Acceptance criteria:**
1. `vault/_scripts/incident_metrics.py`'s halt-counting regex is anchored at column zero and matches both `SAFETY: halt` (pre-v0.6.9) and `SAFETY-HALT:` (post-v0.6.9) sentinel forms — a narrative mention, a continuation-line quotation, or a token without a bracketed timestamp prefix is never counted.
2. Running the script on this repo's `.dcs/incidents/` returns a halt count for `schema-citation-guard` (post-v0.6.9, one real `SAFETY-HALT:`) that is ≥ 1 and not zero.
3. Running the script on a repo with a pre-v0.6.9 incident returns a count ≤ the anchored-grep count, never inflated by narrative mentions. (Verified against this repo's own pre-v0.6.9 incidents — `halt-loop-unbounded` has 2 real `SAFETY: halt` sentinels, not 3.)
4. `vault/Metrics/incident-metrics.md` carries no bare derived halt number — every count either has the regenerating command beside it (per principle 15), or the number is removed and replaced with the command output format.
5. The script's halt-counting function is callable both as a CLI and importable — so `test_doctrine_integrity.py` or a future test can verify the count without scraping stdout.

## Tactics (from the Planning Chief)

1. Import the anchored column-zero rule from dcs_gate.py's ENTRY_PREFIX (`^\[[^\]]*\]\s+`) into incident_metrics.py — a physical line lacking the mandatory bracketed timestamp at column zero is never a sentinel (the gate's GRAMMAR_LINE rule, which the metrics script currently ignores). This single change eliminates the over-count.
2. Extend the halt regex to span both grammar eras with a single compiled pattern: `^\[[^\]]*\]\s+SAFETY[:-]\s*HALT\b` with `re.IGNORECASE|re.MULTILINE`. The two forms are disjoint (`SAFETY:` vs `SAFETY-`) so no double-counting is possible.
3. Extract `count_halts(log_text)` as a module-level function, callable both from the `row()` helper and via `from vault._scripts.incident_metrics import count_halts`.
4. Strip every bare derived halt number from vault/Metrics/incident-metrics.md per principle 15. The snapshot table's halt column values were produced by the broken regex and are themselves unreliable. Each is either replaced with the regenerating command or removed.

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | vault/_scripts/incident_metrics.py | vault/Metrics/**, dcs/**, .dcs/**, tests/** |
| S2 | vault/Metrics/incident-metrics.md | vault/_scripts/**, dcs/**, .dcs/**, tests/** |

**Partition status:** disjoint — parallel execution

## Risks

1. The three sibling counters — `passes` (line 57, `re.findall(r'SAFETY: pass', log)`), `rejects` (line 58), and `escalations` (line 59) — share the identical unanchored, single-grammar defect as `halts`. They are explicitly out of scope this period, so the table output after S1's fix will show correct halt numbers alongside potentially incorrect passes/rejects/escalations. A reader who trusts the row as a whole could be misled. Record in the AAR as a known asymmetry.
2. The dual-grammar regex relies on `re.IGNORECASE` to span both `halt` (pre-v0.6.9 lowercase) and `HALT` (post-v0.6.9 uppercase). The gate's own HALT_RE is case-sensitive by construction. Deliberate divergence — no real log entry uses mixed case — recorded so it is not silently rediscovered as a discrepancy.
3. The script's `re.findall()` with `re.MULTILINE` flag processes the entire log as one string. The gate processes line-by-line via `sentinel_of(line)`. Both approaches produce identical results for the anchored regex.

## Verification plan

1. Run the fixed script against this repo's incident portfolio: `python vault/_scripts/incident_metrics.py C:\dcs`. Confirm the halt column for `schema-citation-guard` is ≥ 1 (was 0) and `halt-loop-unbounded` is 2 (was 3).
2. Run `python -c "from vault._scripts.incident_metrics import count_halts; print(callable(count_halts))"` — must print True.
3. Read `vault/Metrics/incident-metrics.md` and confirm no bare halt number survives without a regenerating command beside it.
4. As a differential check, run the anchored grep against both grammar forms on the same incident logs and confirm the script's output matches.

## Deviation history (this period)

none
