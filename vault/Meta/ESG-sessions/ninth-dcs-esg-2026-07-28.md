### Ninth `/dcs-esg`, 2026-07-28 — three ships since the eighth session, two new rows, one reopened decision

Portfolio: **12 DEPLOYED, 16 QUEUED, 2 PARKED, 8 KILLED, nothing ACTIVE.**
Regenerate: `grep -oE '\*\*(DEPLOYED|PARKED|KILLED|ACTIVE)\*\*|\| QUEUED \|' .dcs/esg/REGISTER.md | sort | uniq -c`.
`criterion-unmeasured-fact`, `deviation-path-proportionality` and `token-economy`
shipped since the eighth session, all today. Deploy witness re-verified fresh
rather than trusted: `python tests/payload_check.py` → 47 identical, 0
differing.

**Rank 1 is `workflow-budget-enforcement`, new this sweep** (`vault/Backlog.md`
item 18) — the Owner's call. Fresh measurement made the case: `plan.md` is now
666 lines against the `CLAUDE.md` ~250-line budget nothing enforces, up from
422 two incidents ago. **Rank 2 is `worktree-removal-self-conflict`, also new**
— see the worktree-hygiene paragraph below. Ranks 3–16 are the prior queue
(ranks 2,3,5,6,9–17 before this session) shifted down by the two insertions,
renumbered contiguously; `token-economy-advisory-fixes` (left unranked at
close) filled rank 5. No row's territory or premise was invalidated by the
three ships — checked directly against each one's delivered partition, not
assumed: `token-economy` kept `doctrine.md` out of every tasking and never
touched `tests/test_doctrine_integrity.py`, so those two clusters only lost
members (the ones that shipped or were folded), they did not gain new
collisions.

**`esg-artifact-bloat`'s own objective is being met, not just its row closed.**
`REGISTER.md` + `STRATEGY.md` are **108,510 B** (`wc -c`), down from 158,542 B
three sessions ago — `token-economy`'s pointer-not-copy mechanism plus the
Owner-directed retroactive compaction actually worked.

**Backlog items 15 and 20/24 need no register row — recorded as resolved
here so neither is rediscovered cold.** #15 (check 13's `vault/` exclusion) is
an already-accepted boundary. #20/#24 (doctrine.md's per-phase reread) turned
out to be **closed as infeasible with today's tools** inside `token-economy`
itself — the automation-path share was fixed for free (`run.md`/`loop.md`
never re-resolve a nested `@`-include via `Read`), and the hand-typed-lifecycle
share has no safe mechanism (tested three ways, all fail). Reopen only if the
tool surface changes. Backlog items #17 (check 15 content guard) and #22+#23
(verification methodology, from `deviation-path-proportionality`'s own
IC-requested ESG activation) were surfaced this sweep and **declined for
queueing** — left as backlog candidates, not register rows.

**The Owner-raised SQLite migration for `REGISTER.md` (backlog #21) was
declined and recorded** at
[`vault/Decisions/sqlite-migration-register.md`](../../vault/Decisions/sqlite-migration-register.md)
rather than queued.

**Worktree hygiene: `vault/Decisions/orphan-worktree-husk.md`'s own reopen
trigger fired.** `C:\DCS-wt\token-economy` is a second orphaned husk, same
shape as `schema-citation-guard` — both empty, both git-forgotten, both
diagnosed by their own closing session as `Permission denied`/`used by
another process` because the closing session's cwd sits inside the worktree
it is asked to remove. Two occurrences of the identical failure reads as a
structural property of `close.md` step 5a.4, not two coincidences — queued as
`worktree-removal-self-conflict` (rank 2) rather than re-affirming the
accepted-boundary treatment. **Disk cleanup attempted this session from
`C:\DCS` (not rooted in either husk), with a mixed and informative result:**
`schema-citation-guard` finally removed cleanly (first success in seven
attempts across five sessions) — `rmdir` from outside it just worked.
`token-economy` did **not**: `Device or resource busy`, from a cwd outside
the worktree, with `.git/worktrees/` not even present to hold a lock. That
falsifies "the closing session's cwd is inside it" as a *complete*
explanation — it may explain schema-citation-guard's first two attempts, but
not this one. Full account: `vault/Decisions/orphan-worktree-husk.md`.

**Mechanical hygiene, no Owner judgment needed:** `register-field-repair-path`
was the only `DEPLOYED` row never collapsed to `— (removed)`/`— (deleted)`
after the retroactive compaction (verified by scanning every `DEPLOYED` row's
Worktree/Branch cells, not sampled) — corrected. This file's own state-values
comment was stale against `dcs/templates/REGISTER.md` (missing `RESOLVED`,
the field-repair qualifier, and the shape-dependent `DEPLOYED` definition,
none of which were back-ported here when `direct-resolution-lane` and
`deploy-marker-blind` shipped them to the template) — synced.

**Delegation unchanged at v4.** Worth recording: `criterion-unmeasured-fact`
is the **first-ever clean `auto_approve_type3` fire** after 8+ sessions of
"never once" — all bounds held (`max_files` 4/4), no forbidden glob/topic hit
(its 201/202 were written in Russian, so the English topic-screen substrings
could not match by construction). One clean fire is not the three-close
pattern that would justify loosening a bound, so no amendment proposed.

