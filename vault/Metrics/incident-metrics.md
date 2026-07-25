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

**All sizes below are in the guard's own units — bytes, and kB at 1024.**
An earlier version of this table mixed bases (1000-based "42.2 kB" and
"31.7 kB" beside a 1024-based "40.5 kB"), which made the diet look like it
recovered more than it did. Corrected 2026-07-25 during
`doctrine-hot-path-trim`.

Historical rows are **git-blob bytes (LF)**, the only thing recoverable from
history; the current row is **on-disk bytes**, which is what the guard actually
reads. On a Windows checkout with `core.autocrlf=true` those differ by one byte
per line — see the `hot-path-budget-eol-sensitivity` row in [[Backlog]].

| when | bytes | kB (÷1024) | note |
|---|---|---|---|
| before the v0.5.0 diet | 42,219 | 41.2 | war stories inline with every rule |
| after the diet (`d5d8106`) | 31,723 | 31.0 | provenance moved to `doctrine-appendix.md` |
| 2026-07-25, v0.6.4 (`51dd073`) | 41,444 | 40.5 | twelve versions of additions since |
| **2026-07-25, v0.6.5** | **36,717** | **35.9** | after `doctrine-hot-path-trim`; on-disk, CRLF worktree |

Regenerate the historical rows:

```bash
for ref in 4ea5026 d5d8106 51dd073; do
  d=$(git show $ref:dcs/references/doctrine.md | wc -c)
  s=$(git show $ref:dcs/references/schemas.md | wc -c)
  echo "$ref $d $s $((d+s))"
done
```

Regenerate the current row (from a checkout, matching what the guard reads):

```bash
python -c "import os; d=os.path.getsize('dcs/references/doctrine.md'); s=os.path.getsize('dcs/references/schemas.md'); print(d, s, d+s)"
```

The trim recovered roughly half the regrowth: 41,444 → 36,717 B, against a
post-diet equivalent of ~32,031 B in on-disk CRLF units. The remainder is a
queued follow-up, not an oversight — see [[Backlog]].

Budget enforced by `HOT_PATH_BUDGET_KB` in `tests/test_doctrine_integrity.py`,
re-seated **42 → 37 kB** by this incident per `ceil(36717/1024) + 1`. It is a
ratchet set just above current usage, not a comfortable ceiling — and note the
band it leaves: the incident's own acceptance bar was 36,864 B, so there is
**147 B** before that target is re-breached but **1,171 B** before the guard
turns red. Candidate re-seat to 36 kB after a period of stability. See
[[Backlog]].
