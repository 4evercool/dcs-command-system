<!--
Fixture for tests/test_doctrine_integrity.py (dcs/tools/preservation_map.py's
own test surface). Neutral fiction (a widget catalog's sync worker) --
never a real project's paths or prose. This directory is this incident's
own uncommitted product, not historical evidence: do not edit in place,
add a new fixture directory instead.
-->

# 202 -- Objectives (Operational Period 1, fixture)

**Incident:** widget-sync-fixture
**Period:** 1

## Goal

Keep the widget catalog's sync worker resilient to transient upstream
failures, and document the resulting operator-facing behaviour.

## Acceptance criteria (the Definition of Done)

1. `src/catalog/sync.py` retries a failed sync with exponential backoff.
2. `docs/sync-guide.md` documents the retry policy for operators.
3. `tests/test_sync.py` covers the timeout path.
4. `src/catalog/config.py` exposes a `max_retries` setting.
5. `docs/rollout.md` records the rollout checklist.
6. `src/catalog/sync.py` logs a warning on the final retry failure.

## Out of scope this period

(none)
