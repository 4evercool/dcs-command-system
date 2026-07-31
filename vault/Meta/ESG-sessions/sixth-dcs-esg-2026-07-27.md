### Sixth `/dcs-esg`, 2026-07-27 — the queue is ranked, rank 1 is deliberately empty

Portfolio: **7 DEPLOYED, 1 MERGED (deploy pending), 17 QUEUED (all ranked),
2 PARKED, 5 KILLED, nothing ACTIVE.** Regenerate from the State column.

**Rank 1 is vacant on purpose, not by omission.** The Owner declined to refill it
until `direct-resolution-lane` ships, because that train is the **first to run
under the content-shaped step 7** and its outcome is the one piece of evidence
Delegation v3's `deploy` revisit has been waiting two sessions for. Ranks run
**2–18**, contiguous.

**All four rows owed to this sweep by the p0 sitrep are discharged.**
`register-field-repair-path` → 10, `register-writer-map-completeness` → 15,
`status-md-enum-drift` → 17, and the `trivial-work-inline-lane` question was
**decided rather than deferred a second time**.

**The fold, and why it does not violate principle 4.** `trivial-work-inline-lane`
is `KILLED (folded)` into `decomposition-backlog-routing` (rank 9). Both edited
`new.md` step 4a and `esg.md`'s sweep for the same complaint, differing only in
the axis of the bar — triviality versus priority. Principle 4 asks for one
*defect* per incident, and there is one: **step 4a has no bar at all.** Two
readings of one missing bar are not two defects. Two incidents over one pair of
files would have meant a second planning pass to settle a single routing
question, with the second inheriting a step 4a the first had just rewritten —
the seam failure `vault/Meta/building-dcs-lessons.md` §15 names.

**`vault/Backlog.md` 17 and 18 declined for the SECOND time, and recorded as a
decision so a third sweep does not reopen it cold.** The queue went 15 → 17
since they were first declined, so the reason for declining got stronger, not
weaker. Item 18 arrived with sharper evidence again — `new.md` grew 234 → 242
lines this incident and stayed under the ceiling **only because the ceiling was
written into the tasking by hand.** Both remain accounted for in the backlog;
neither is lost.

**Delegation unchanged at v3 — third session running, and still on a date.** The
`deploy` revisit condition fired when `deploy-marker-blind` closed, but the
evidence it waits on is the first train under the new step 7, which has still not
run. `max_files`/`max_specialists` got no new evidence either: the incident that
closed was Type 1, which no `auto_approve_type3` bound reaches. Across **seven**
closed incidents the grant has never once fired. The Owner was offered the honest
alternative of dropping it and kept v3.

**Two measurements this session that belong in front of `esg-artifact-bloat`
(rank 8) rather than inside it.** These files grew **+24 KB in a single
incident** — `REGISTER.md` 71,362 → 88,376 B, `STRATEGY.md` 32,663 → 40,392 B,
total **128,768 B**, which is 77 % of the 167 KB in the other project that
motivated the row. And the widest row in the queue is
**`prompt-vs-schema-drift` (rank 6)**: its `dcs/workflows/**` + `agents/**`
territory intersects **8 of the 13** collision clusters, so it stalls most of the
queue while `ACTIVE`. Regenerate both with
`wc -c .dcs/esg/REGISTER.md .dcs/esg/STRATEGY.md` and by intersecting the
Territory column pairwise.

**Worktree audit — one worktree (`C:/DCS`, `main`), one `dcs/*` branch
(`dcs/direct-resolution-lane`, merged into HEAD, kept as the rollback reference
until the deploy), no dangling branches, no stale actives, all five 209 sitreps
carrying filled decisions.** One finding, and it is now the **fifth** consecutive
failure: `C:\DCS-wt\schema-citation-guard` is on disk, empty, absent from
`git worktree list`. Zero loss, never forced. Owed:
`rmdir "C:\DCS-wt\schema-citation-guard"` from a terminal that does not hold it.
Also spent and removable: `.dcs/esg/QUEUED-201/2026-07-27-direct-resolution-lane.md`,
whose incident has opened and closed — kept for now as the stem's archive.

