---
tags: [dcs, metrics, incidents]
updated: 2026-07-27
---

# Incident metrics

**Regenerate before citing** — every number below is a derived fact with
a lifetime (doctrine principle 15):

```bash
python vault/_scripts/incident_metrics.py <project-root> [<worktree>...]
```

> **The script's `halts` column is not trustworthy today, in both directions**
> (measured 2026-07-26 during `safety-halt-functional-scope`'s stem; queued as
> register row `halt-enumeration-grammar-drift`). It counts with an unanchored
> whole-file substring search — `vault/_scripts/incident_metrics.py:52`,
> `halts=len(re.findall(r"SAFETY: halt", log))` — so narrative that quotes the
> sentinel back counts as a verdict: it reports 10 halts for
> `energy-cost-model-rework` where `grep -n "^\[.*\] SAFETY: halt"` finds 4
> real verdicts. And the same regex cannot see the `SAFETY-HALT:` grammar
> v0.6.9 introduced, so it reports **0** halts for `schema-citation-guard`,
> which had one. No enumeration command currently spans both grammars —
> anchor the pattern and check which grammar a log uses before citing any halt
> count from this file.

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

**This metric now has a stable definition, and did not before.** Until
`hot-path-budget-eol-sensitivity` (2026-07-25) the guard read raw on-disk bytes,
so the same commit measured differently depending on which files a given
checkout had rewritten — the merged tree at one point held `doctrine.md` as CRLF
and `schemas.md` as LF simultaneously. The check now **normalises CRLF to LF
before counting**, and `.gitattributes` pins the tree to LF as well, so every row
from v0.6.8 onward is comparable with the git-blob history above it without a
caveat.

Rows before that fix are **git-blob bytes (LF)** where taken from history, and
**raw on-disk bytes** where measured live — which is why the two 2026-07-25 rows
below carry the tree they were measured in.

| when | bytes | kB (÷1024) | note |
|---|---|---|---|
| before the v0.5.0 diet | 42,219 | 41.2 | war stories inline with every rule |
| after the diet (`d5d8106`) | 31,723 | 31.0 | provenance moved to `doctrine-appendix.md` |
| 2026-07-25, v0.6.4 (`51dd073`) | 41,444 | 40.5 | twelve versions of additions since |
| 2026-07-25, v0.6.6 (`0428ac4`) | 42,623 | 41.6 | `schemas.md` +1,189 B in `6a57b97`; 385 B under the 42 kB budget |
| 2026-07-25, v0.6.7 | 37,734 | 36.9 | after `doctrine-hot-path-trim` merged; **−4,889 B**. Raw on-disk, mixed-EOL tree — the last figure this table has to qualify |
| 2026-07-25, v0.6.8 | 37,579 | 36.7 | after `hot-path-budget-eol-sensitivity`. **Normalised — identical in any checkout** |
| 2026-07-26, v0.6.9 (`532b809`) | 38,878 | 38.0 | after `halt-loop-unbounded`. `doctrine.md` **+1,299 B** for principle 13's ceiling clause; **34 B of slack** under the 38 kB ratchet — the tightest this table has recorded |
| **2026-07-26 (`08f75f0`)** | **36,561** | **35.7** | after `schemas-md-trim`. `schemas.md` −2,317 B; ratchet re-seated **38 → 37**, so slack is **1,327 B** against a *lower* ceiling |
| 2026-07-26 (`9830af5`) | 36,582 | 35.7 | after `schema-citation-guard`. `doctrine.md` **+21 B** for check 13's anchor. Row added retroactively at the next incident's close — that incident did not record one, which is why the step from 36,561 looked unexplained |
| **2026-07-27 (`c0fea95`)** | **36,683** | **35.8** | after `safety-halt-functional-scope`. `doctrine.md` **+101 B**: principle 15 now names the advisory default and cites the charter step instead of "checklist". Provenance went to `doctrine-appendix.md`, which is outside the pair. **1,205 B of slack** against the 37 kB ratchet |

Regenerate the two current rows — note this uses the **normalised** measure
the guard itself applies (`CRLF → LF` before counting), not `os.path.getsize`,
which the earlier version of this line used and which disagrees with the
guard in a CRLF checkout:

```bash
python -c "import pathlib; d=pathlib.Path('dcs/references/doctrine.md').read_bytes().replace(b'\r\n',b'\n'); s=pathlib.Path('dcs/references/schemas.md').read_bytes().replace(b'\r\n',b'\n'); print(len(d), len(s), len(d)+len(s))"
```

**Read the 2026-07-26 pair together or not at all.** `halt-loop-unbounded`
spent almost the entire margin on one clause and left 34 B; `schemas-md-trim`
then took 2,317 B back out of the file that had *not* grown and lowered the
ceiling with it. Neither row means much alone: the first looks like
negligence, the second like a windfall, and what actually happened is that
the budget worked — it made the cost of the clause visible immediately.

**The 1,189 B in the v0.6.6 row belongs to `schemas.md`, and its basis is
raw CRLF.** Normalised the same growth is **1,179 B** (14,434 → 15,613 at
`6a57b97`); `doctrine.md` did not change in that commit at all. Six artifacts
carried "1,189" without naming a basis, and during `schemas-md-trim` that
unlabelled number produced three separate errors — a wrong file attribution
in an IAP, a broken arithmetic sentence in the guard's own comment, and a
misdirected tasking prompt. Regenerate:

```bash
python -c "import subprocess; f=lambda r: len(subprocess.run(['git','show',r+':dcs/references/schemas.md'],capture_output=True).stdout.replace(b'\r\n',b'\n')); print(f('6a57b97')-f('6a57b97^'))"
```

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

The trim recovered roughly half the regrowth: **42,623 → 37,734 B**, against a
post-diet 31,723 B. The remainder is a queued follow-up, not an oversight —
see [[Backlog]] items 7 and 8.

**The two middle rows are the lesson, not just bookkeeping.** The incident
measured its result at **36,717 B** and derived a 37 kB ratchet from it. That
number was correct when taken and wrong when merged: `6a57b97` added 1,189 B to
`schemas.md` while the incident was open, so the merged pair came out **above**
the budget the incident had just set — the guard would have landed red on main
by 18 B. `close.md` step 1a caught it before the merge, which is the entire
argument for running a merge-time guard on the *merge result* rather than
trusting two green branches. Budget re-derived from the merge:
`ceil(37906/1024) + 1 = 38`.

Budget enforced by `HOT_PATH_BUDGET_KB` in `tests/test_doctrine_integrity.py`,
re-seated **42 → 38 kB**. Still a ratchet — it bites ~1.2 kB sooner than the
budget it replaced — with **1,178 B** of headroom as merged. Candidate re-seat
to 37 or 36 kB after a period of stability.

**A caveat on all of these numbers.** The merged tree holds `doctrine.md` with
CRLF and `schemas.md` with LF at the same time, because git rewrote one and not
the other. On-disk size therefore depends on which files were last touched,
which means this metric currently has no stable definition — see [[Backlog]]
item 8.
