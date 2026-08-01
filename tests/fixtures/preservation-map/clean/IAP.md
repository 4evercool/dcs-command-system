<!--
Fixture -- see 202-OBJECTIVES.md's header comment in this same directory.
-->

# IAP -- widget-sync-fixture (Period 1, fixture)

## Partition

| Tasking | Territory |
|---|---|
| S1 | src/catalog/sync.py, src/catalog/config.py, docs/sync-guide.md, docs/rollout.md, tests/test_sync.py |
| S2 | src/catalog/sync.py |

## Criterion coverage

### Criterion 1
Anchor: the retry loop wraps each attempt in exponential backoff capped by `max_retries`.

### Criterion 2
Anchor: the retry policy section spells out the backoff schedule for operators.

### Criterion 3
Anchor: `test_timeout_path` exercises the sync worker's timeout branch.

### Criterion 4
Anchor: `max_retries` is exposed as a configurable integer default of 5.

### Criterion 5
Anchor: the rollout checklist enumerates every launch step end to end.

### Criterion 6
(amended this period -- see 204-TASKING/S2.md)
