---
tags: [dcs, metrics, incidents]
updated: 2026-07-25
---

# Incident metrics

**Regenerate before citing** — every number below is a derived fact with
a lifetime (doctrine principle 15):

```bash
python vault/_scripts/incident_metrics.py <project-root> [<worktree>...]
```

## Snapshot — 2026-07-25, bread_bot (first eight incidents)

| incident | 201 kB | log kB | entries | halts | passes | rejects | escal | taskings |
|---|---|---|---|---|---|---|---|---|
| analytics-patterns-dynamics-mismatch | 9 | 6 | 23 | 0 | 1 | 0 | 0 | 2 |
| fix-audit-287-292 | 9 | 8 | 0 | 0 | 0 | 0 | 0 | 4 |
| nan-guard-admin-forms | 10 | 5 | 13 | 0 | 1 | 0 | 0 | 3 |
| shift-overview-rework | 7 | 30 | 50 | 0 | 3 | 0 | 0 | 6 |
| analytics-order-date-tz-sweep | 11 | 10 | 29 | 0 | 1 | 0 | 0 | 3 |
| **energy-cost-model-rework** | **32** | **285** | **257** | **10** | 3 | **5** | **3** | **8** |
| migration-number-allocation | 15 | 23 | 23 | 0 | 1 | 1 | 0 | 2 |
| subscription-refund-cluster | 27 | 26 | 42 | 0 | 1 | 0 | 1 | 3 |

## What the numbers say

**Brief size is the leading indicator.** Incidents that ran clean have
201 briefs of 7–15 kB. The two with any escalation at all are the two
largest briefs (32 kB and 27 kB). Nothing else at intake predicts trouble
as well — not type, not tasking count. This is the evidence behind
`new.md` step 4a and the "~7–11 kB is normal" smell test.

**The outlier is an outlier on process, not on subject.** Energy's brief
is 3× the median; its log is ~10×, its entries ~5×, and it is the only
incident with double-digit halts. Difficulty alone does not produce that
shape — [[Post-mortems/energy-cost-model-rework|absorbed scope]] does.

**Zero halts is the norm.** Six of eight incidents never had a Safety
refutation. That matters for reading the outlier: halts are not routine
friction to be endured, they are a signal, and ten of them in one
incident was ten opportunities to stop.

**A `?` in the timestamps column** (fix-audit-287-292) means the 214 log
has no parseable entries — an early incident written before the log
format settled. Left visible rather than cleaned: it is honest evidence
about when the convention took hold.

## Hot-path size (the other metric worth tracking)

`doctrine.md` + `schemas.md` are read on **every** workflow invocation and
**every** command-point spawn, so their size is a continuously-paid tax.

| when | size | note |
|---|---|---|
| before the v0.5.0 diet | 42.2 kB | war stories inline with every rule |
| after the diet | 31.7 kB | provenance moved to `doctrine-appendix.md` |
| 2026-07-25 (v0.6.3) | 40.5 kB | twelve versions of additions since |

Budget enforced at 42 kB by `tests/test_doctrine_integrity.py` — set as a
ratchet just above current usage, not a comfortable ceiling. See
[[Backlog]].
