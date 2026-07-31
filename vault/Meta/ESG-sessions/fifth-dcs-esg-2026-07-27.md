### Fifth `/dcs-esg`, 2026-07-27 — rank 1 refilled, the queue fully ranked

Portfolio: **7 DEPLOYED, 15 QUEUED, 2 PARKED, 4 KILLED, nothing ACTIVE and
nothing awaiting deploy.** Regenerate by reading the State column.

**A stale-read correction, recorded because it is this repo's own recurring
defect class.** This session's sweep read `deploy-marker-blind` as `MERGED
(deploy pending)` with its branch kept, and reported to the Owner that the
row claimed a branch `git show-ref` could not find. Both readings were
**stale, not wrong-on-disk**: the deploy train transitioned the row and
deleted the branch between the sweep's read and its report. The register was
correct throughout; the audit's snapshot was not. A file read at the top of a
long session is a derived fact with a lifetime (principle 15), and the
`.dcs/esg/` artifacts are exactly the ones a parallel session writes.

**`deploy-marker-blind` shipped, and the row's own Outcome carries the
evidence** — the fourth consecutive blind ship and the last, red-then-green
against `tests/payload_check.py` (exit 1, 4 differing → exit 0, 47 identical).
**Rows it had sequenced behind it may now open:** `esg-artifact-bloat`
(rank 8, shared `dcs/templates/`) and the `tests/test_doctrine_integrity.py`
cluster — `check-14-hardening` (3), `schemas-contract-format` (4),
`json-examples-unparsed` (13) — which still collide with **each other** and
must open one at a time.

**Rank 1 is `direct-resolution-lane`** — the Owner's call. Its territory lock
cleared with the merge, and its stem is already worked (201 in
`.dcs/esg/QUEUED-201/`; typing Owner-confirmed as Type 1 and not to be
re-litigated), so it opens cheaper than anything else queued. The cost is
named rather than left to be discovered: at seven files including
`doctrine.md` and four workflows it is **the widest territory in the queue**,
and while `ACTIVE` it blocks ranks 5, 6, 7, 8, 9 and 12. **Corrected at this
incident's stem, 2026-07-27**, from the territory cells rather than from the
list this session first wrote: rank 6 (`prompt-vs-schema-drift`) claims
`dcs/workflows/**`, which covers four of this row's files and was **omitted**;
rank 10 (`doctor-version-only-check`) claims `bin/dcs.js` alone and was
**wrongly included**. Regenerate by parsing the Territory column and
intersecting with this row's.

**The three unranked rows were ranked**, discharging a gap left when the
previous session ranked only the rows its own incident produced.
`decomposition-backlog-routing` at 9 — blocked by rank 1 regardless, and
upstream prevention for `esg-artifact-bloat` at 8, so the pair stays adjacent.
`doctor-version-only-check` at 10 — its parent shipped a witness its
`doctor()` can call instead of reimplementing, and it shares `bin/dcs.js` with
`version-bump-command` at 11, so ranking it immediately ahead is deliberate:
folding the two gets weighed at its stem.

**`vault/Backlog.md` items 17 and 18 were NOT queued, and that is a decision.**
Both were left by the close as "an ESG act"; the Owner declined both with the
queue already at 15 rows. Recorded so the next sweep reads them as
considered-and-deferred, not missed. **Item 18 gained sharper evidence here and
still did not carry:** it was filed against `deploy.md` at 275 lines, and
`wc -l dcs/workflows/*.md` now shows **four** files over the ~250-line budget —
`plan.md` 403, `execute.md` 387, `deploy.md` 275, `close.md` 266.

**Worktree audit — one finding, unchanged and still owed.**
`C:\DCS-wt\schema-citation-guard` is on disk, empty (0 entries), absent from
`git worktree list`. `rmdir` returned *Device or resource busy* for the
**third** time (fourth ESG, `deploy-marker-blind`'s close, this session). This
session's shell is rooted in `C:\DCS`, so the holder is neither process
previously blamed. Zero loss, not forced, still a one-liner from a terminal
that does not hold it: `rmdir "C:\DCS-wt\schema-citation-guard"`.

**Delegation unchanged at v3 — on a date, not on caution.** v3's revisit
condition for the whole `deploy` object fired when this row closed, but the
evidence it was waiting for has not arrived: the content-shaped step 7 was
installed *by this very train*, so the first train to run under it is the next
one. Loosening `deploy.auto` now decides on expectation rather than
observation. Revisit at the session after that train.

The paragraph below is the record of the territory lock while it was held.

