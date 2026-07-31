### Tenth `/dcs-esg`, 2026-07-29 — rank 1 refilled by Owner pick, one new row, a lock-holder identified

Portfolio: **14 DEPLOYED, 18 QUEUED (ranked 1–18, contiguous), 2 PARKED,
8 KILLED, nothing ACTIVE, nothing deploy-pending.** All sitrep decisions
filled — cluster (d) empty. Regenerate counts with the table-row-anchored
patterns in the `/dcs-deploy` note below.

**Rank 1 is `schemas-contract-format`** — the Owner's pick, promoted from
rank 4 over the Chief of Staff's recommendation of
`worktree-removal-self-conflict` (which stays rank 2; the two are
territory-disjoint and could open together). Three previously-unranked
rows entered at ranks 5 / 8 / 18 (`esg-intake-writeback-gap`,
`workflow-file-trim-grandfathered`, `strategy-compaction-loses-history`);
one new row `provisioning-script-upstreaming` entered at rank 10 (see its
own Intake source cell). `vault/Backlog.md` item 25 (new Owner intake,
2026-07-29) confirmed as a backlog line under the v0.6.13 priority bar,
folded into `esg-intake-writeback-gap` — the first live application of
that bar. Everything else kept its relative order, renumbered
contiguously; ranked list rewritten in `STRATEGY.md` accordingly.

**Worktree hygiene: the husk's lock-holder has a face now.** Git-side
audit clean (one worktree — the main checkout; zero unmerged `dcs/*`
branches; no orphans, stale actives, or dangling branches). The
`C:\DCS-wt\token-economy` husk again refused removal from an external cwd
via two API paths a full day later — falsifying the transient-hold
theory — and an orphaned `claude` process (PID 40876) was found whose
start time matches the husk's mtime **to the minute**. Working
hypothesis: the closing session's own never-exited process holds the
handle. **Owner decision: keep the process+husk pair as the live specimen
for `worktree-removal-self-conflict`'s stem** rather than kill-and-clean.
Full chain: `vault/Decisions/orphan-worktree-husk.md` (updated this
session).

**Both PARKED rows stay parked** — neither's revisit condition fired
(`halt-binding-status`: no genuinely arguable halt yet;
`type5-express-lane-tuning`: typing decisions not looking systematically
conservative). **Delegation unchanged at v4** — no new evidence on any
untested bound: no Type 3 has halted since the `max_specialists`
fix-tasking ambiguity was flagged, `auto_approve_type3` still has exactly
one clean fire, and `deploy.auto: true` ran its second clean train
(2026-07-29, one row, no substitution).

