### Eighth `/dcs-esg`, 2026-07-27 — rank 1 refilled from the queue, one new row from the closing incident's own halts

Portfolio: **8 DEPLOYED, 1 MERGED (deploy pending), 17 QUEUED (ranks 1–17,
contiguous), 2 PARKED, 5 KILLED, nothing ACTIVE.** Audit clean: one worktree,
one `dcs/*` branch (`dcs/register-field-repair-path`, merged, kept as the
rollback reference until deploy), no orphans, no dangling branches, no stale
actives, all seven 209 sitreps carrying filled decisions.

**Rank 1 is `criterion-unmeasured-fact`**, filled from rank 2, not from new
intake — third field measurement of the same failure class (an acceptance
criterion resting on an unmeasured external fact), the second one supplied by
the incident that just closed. Ranks 2–4 shifted up one each; 6–17 unchanged
in number.

**One new row, `revision-preservation-map` at rank 5**: `vault/Backlog.md`
item 19, a second and sharper measurement for `deviation-path-proportionality`
(rank 4) — a narrow IAP revision has no required check that it preserved
every other acceptance criterion, and the closing incident's own repair
proved it by dropping one.

**Territory clusters recomputed from delivered territory** — `register-field-
repair-path`'s 201 estimate (`doctrine.md`, `esg.md`, `REGISTER.md`) did not
match what it actually shipped (`REGISTER.md`, `esg.md`, `CHANGELOG.md`, no
`doctrine.md`), so the `doctrine.md` cluster lost a member it never actually
held. Full pairwise re-derivation across all 17 rows not claimed; see
`STRATEGY.md` for what was and wasn't checked.

**`esg-artifact-bloat` (rank 8) measured a third time (158,542 B, ~95% of the
167 KB benchmark, up from 77% two sessions ago) and deferred a third time** —
put to the Owner directly this session; the call was to defer again rather
than reorder. Flagged as a pattern worth the ninth session's attention.

**Delegation v4 unchanged.** Topic screen ("version bump") reconsidered on a
fourth consecutive false positive (three from this session's closing incident
alone) and kept as-is, same reasoning as v2/v3.

**One self-corrected slip**: an edit to this file's own row 94 briefly wrapped
a table cell across six physical lines via embedded newlines; caught before
this sweep and collapsed back to one line. No content lost. Full account in
`STRATEGY.md`'s Sessions log.

