# AAR — After Action Report

**Incident:** revision-preservation-map
**Type:** 1
**Opened:** 2026-08-01
**Closed:** 2026-08-01
**Operational periods:** 1

## Outcome

All 8 acceptance criteria from `202-OBJECTIVES.md` (period 1) were met,
Safety-verified with 0 refutations (`SAFETY.md`). `dcs/workflows/plan.md`'s
`## 6c.` bounded-amendment path now requires a preservation map — proven
by content, re-derived from disk every time — before it will re-stamp,
closing the gap that let `register-field-repair-path` silently drop a
Safety-verified criterion while fixing an unrelated one. The mechanism
(`dcs/tools/preservation_map.py`), its documentation (`schemas.md` #9),
its provenance (`doctrine-appendix.md` W4), and its regression proof
(three frozen fixtures plus a mechanical test-suite section) are all
committed on `dcs/revision-preservation-map` at integration commit
`76976f3`, merged in step 5a below.

## What worked

- Building the mechanism as an executable (`dcs/tools/preservation_map.py`)
  rather than a prose instruction plus a phrase-grep — the exact shape
  the abandoned 2026-07-31 attempt tried and that shape's own vacuity
  (validating that words were said, not that any map was real) is what
  motivated this design from the stem onward.
- The dual-comparator contrast (`prefix_coverage()` vs `verify()` on one
  frozen `dropped-criterion` fixture) proved criterion 4 without touching
  any git ref — survived Safety Officer's independent re-derivation
  unchanged.
- Three disjoint specialist territories (tool+tests, workflow, schema+
  appendix) with two deliberately shared literals (the invocation string,
  the `schemas.md` #9 heading) pinned verbatim on both sides — both
  "expected red until the counterpart lands" carrier cases resolved green
  once all three specialists' work was in the same worktree, exactly as
  planned.
- Renaming (not deleting) the abandoned attempt's branch to
  `dcs/revision-preservation-map-abandoned-2026-07-31` preserved its
  evidence commit (`497dcd4`) while cleanly freeing the branch name for
  the restart — no information lost, no confusion about which branch is
  live.

## Lessons

- **A discipline-only fix for "a check wasn't run" fails the same way
  the missing check did.** The abandoned attempt's own check 23 only
  verified that `plan.md`'s prose said the words "preservation map" — it
  never verified any incident actually produced or verified a real one.
  When the defect class is "an assertion stood in for a checked fact,"
  the fix must itself avoid becoming a second unchecked assertion.
- **A tight byte/line budget should be treated as load-bearing input to
  planning, not an afterthought at review.** The Planning Chief measured
  the hot-path headroom (402 B) and the `plan.md` line headroom (3
  lines) at plan time and bounded each specialist's tasking to fit —
  which is why both landed inside budget without a deviation. See
  `vault/Backlog.md` item 7 for the fresh headroom figure (50 B) this
  incident leaves for the next.
- **Word-diffing a compression claim is stronger evidence than reading
  the ledger prose.** The Safety Officer's `git diff --word-diff` check
  on `plan.md` (zero removed-word runs) and its row-count comparison of
  `schemas.md`'s field tables (identical counts across sections 1-7)
  turned "the specialist says nothing was lost" into an independently
  checked fact — exactly the standard this incident's own fix holds
  future amendments to.
- **A section-number citation to another file's internal structure has
  a known expiry when that file is contested territory.** Two "check
  18(f)" citations (in `preservation_map.py` and the new test section)
  were replaced with name/regenerating-command citations because
  `field-lesson-guard-vacuity` (REGISTER.md rank 4) will renumber
  `test_doctrine_integrity.py`'s sections — a citation by number would
  have gone stale the moment that incident lands.

## Deviations this incident

None — executed as planned. Zero Safety halts, zero deviation reports,
one operational period, one stamped IAP.

## Memory routing

`CLAUDE.md`'s documented memory system for this project is the three-store
split: `dcs/references/doctrine.md` (rule, hot path), `doctrine-appendix.md`
(provenance, never shipped in the hot path), and `vault/` (maintainer-only).
This incident's own rule change and provenance story are its primary
deliverable, not separate memory routing — `dcs/references/schemas.md` #9
and `dcs/references/doctrine-appendix.md`'s new W4 entry (both landed in
the integration commit `76976f3` per `202-OBJECTIVES.md` criteria 2 and 5).
Separately, two vault writes for what only a DCS maintainer needs going
forward:
- `vault/Backlog.md` item 19 marked ✅ DONE with closure details and a
  pointer to this AAR.
- `vault/Backlog.md` item 7 gained a "Fresh evidence, 2026-08-01" note
  recording the hot-path headroom this incident leaves (50 B) for the
  next doctrine/schemas-touching incident to plan against (Safety
  advisory 5, not actioned this period per the IC's disposition).

## Intake source closure

Register row `revision-preservation-map` in `.dcs/esg/REGISTER.md` —
`vault/Backlog.md` item 19, originally queued at the eighth `/dcs-esg`
(2026-07-27), restarted at the fifteenth `/dcs-esg` (2026-08-01) after
the prior attempt's mid-execution abandonment. This close moves the row
`ACTIVE` → `MERGED (deploy pending)` at step 5a.3 below — no external
ticket or audit-row reference exists; the register row itself is the
intake source and this AAR is its closure record.

## Safety Officer's final verdict (verbatim, from SAFETY.md)

```json
{
  "verdict": "pass",
  "refutations": [],
  "advisories": [
    {
      "finding": "dcs/tools/preservation_map.py:4 — the module docstring cites 'incident revision-preservation-path'; the actual slug is 'revision-preservation-map'. Only occurrence of that string in the repo, resolves to no incident directory, no branch and no register row.",
      "fix": "s/revision-preservation-path/revision-preservation-map/ in the docstring at line 4. Fold into the integration commit."
    },
    {
      "finding": "The incident's 214-LOG.md carries no specialist return entries at all — all three S1/S2/S3 returns are absent from the log. No verification depended on them (Safety Officer re-derived everything from the repo), but the log is what a fresh session reads to resume losslessly.",
      "fix": "IC appends the three specialist return entries (and the command-point-3 verdict entry) before close, per execute.md's logging steps."
    },
    {
      "finding": "preservation_map.py's output-disagreement branch — the false-fidelity defect the module docstring twice claims to close — has no named test case. Section 22's in-memory forgery proof deletes the anchor line, exercising only the anchor-missing branch. Safety Officer hand-verified the branch works correctly, so the capability is real, just uncovered.",
      "fix": "Add one more forgery case in section 22 mutating the victim entry's output rather than the artifact text — same comparator, no new fixture, ~6 lines."
    },
    {
      "finding": "preservation_map.py and tests/test_doctrine_integrity.py both cite 'check 18(f)' by section number; that numbering is exactly what the queued field-lesson-guard-vacuity incident will renumber, so these citations have a known expiry with no regenerating command beside them.",
      "fix": "Cite the idiom by test name rather than section number, or add the regenerating grep beside the citation."
    },
    {
      "finding": "Hot-path headroom is now 50 B, not the 402 B the IAP planned against — S3 spent 352 of the 402 B. In band, criterion 6 met, but the next hot-path sentence anyone adds anywhere breaches the budget.",
      "fix": "No action this period — worth a note in the AAR so the next incident touching doctrine.md/schemas.md knows it must fund its own trim from the first byte."
    }
  ],
  "checked": ["see .dcs/incidents/2026-08-01-revision-preservation-map/SAFETY.md for the full 23-item checked[] list — git diff/status forbidden-zone sweep, all 8 acceptance criteria independently re-derived (word-diff audits, field-table row counts, byte-level insert-only proof of the new test section, all three fixtures re-run personally, hot-path byte count re-derived, all four suites re-run), plus a hand-built adversarial probe of the false-fidelity branch"]
}
```

Post-verdict disposition: **close** (command point 4, `dcs-commander`,
model fable). Advisories 1/3/4 folded into the integration commit
(`76976f3`); all four suites re-run green afterward (133/133 integrity,
100/100 gate, 18/18 intake, 14/14 cli). Advisory 2 resolved by appending
the missing log entries before this close. Advisory 5 recorded above and
in `vault/Backlog.md` item 7, not actioned this period.
