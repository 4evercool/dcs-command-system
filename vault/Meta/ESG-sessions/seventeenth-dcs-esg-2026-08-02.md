# Seventeenth `/dcs-esg`, 2026-08-02 — the convened session: v6, ranks shifted

Chair: Owner. Chief of Staff: main session (Fable). Convened per the
Owner's decision on `record-integrity-corrections`'s escalation
trigger (e) sitrep (close now, convene ESG separately) — the convening
obligation named exactly two acts, both done here.

## Portfolio at close of session

32 DEPLOYED, 1 MERGED (deploy pending — `record-integrity-corrections`,
branch kept as rollback ref until the train), 20 QUEUED (ranked 1–20,
contiguous), 1 PARKED, 10 KILLED, 4 RESOLVED, nothing ACTIVE, no pending
sitreps (all Decision fields filled, including the two new ones).
Regenerate from the State column:
`awk -F'|' '/^\| [a-z][a-z0-9-]* \|/ {s=$6; gsub(/^ +| +$/,"",s); sub(/ \(.*/,"",s); print s}' .dcs/esg/REGISTER.md | sort | uniq -c`.

## Decisions

1. **Delegation v6 — `auto_approve_type3` reinstated (`false` → `true`),
   everything else byte-identical to v5.** The written condition was met
   verbatim: `record-integrity-corrections` closed 2026-08-02 with a
   green Safety verdict (pass, 0 refutations, 3 advisories; merge
   `a62ffad`), corrections applied append-only per its own convention.
   The alternative (hold `false` until the model floor lands) was
   offered and declined: a met condition left unhonored teaches future
   sessions that written conditions are decorative. The model floor
   (rank 2) supersedes the blanket switch by its own IAP when it lands.
2. **Ranks 2–20 shifted up to 1–19, order unchanged; new row
   `record-verbatim-attribution-followup` at rank 20** (likely Type 5:
   two sibling-`CORRECTION-<date>.md` annotations per the established
   convention — Safety advisories 2+3 of the closing incident). Rank 1
   is now `close-integrity-guard-bundle`, whose precondition (corrected
   archives for the SHA-existence sweep) was delivered by the very close
   that convened this session.

## Process note (recorded against myself)

While appending the v6 block, the Chief of Staff first renamed the v5
block's fence (`delegation-bounds` → a superseded marker) — an edit to a
past version block, which the file's own audit-trail rule forbids —
and reverted it within the same session, byte-identical, before any
consumer read it. A "v5-prelude note" between the v4 and v5 blocks
remains (new text between blocks, no past block edited). Recorded here
because the record-integrity arc is exactly about not silently patching
one's own slips.

## Hygiene

Worktree audit clean: one worktree (main checkout), no orphans, no
husks. Two `dcs/*` branches, both accounted for:
`dcs/record-integrity-corrections` (rollback ref until deploy) and
`dcs/revision-preservation-map-abandoned-2026-07-31` (kept by the
sixteenth session's decision). One MERGED row awaits `/dcs-deploy` —
an Owner-invoked act, not started by this session.
