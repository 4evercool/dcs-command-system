<!--
Fixture -- THE REGRESSION FIXTURE, reproducing register-field-repair-path's
defect shape: the amendment below names only criterion 6, and its
preservation map still claims criterion 5 preserved (with a plausible
self-reported output, carried over unchanged from before the drop), but
this IAP.md's own "Criterion 5" section has been removed. verify() on
this directory must return a finding naming criterion 5; prefix_coverage()
on this same directory must return [] (every criterion still maps to a
204-TASKING/*.md tasking id -- the pre-fix comparator's blind spot).
-->

# IAP -- widget-sync-fixture (Period 1, fixture, criterion 5 dropped)

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

### Criterion 6
(amended this period -- see 204-TASKING/S2.md)
