### `/dcs-deploy`, 2026-07-29 — one row shipped, portfolio-clean train

Worktree audit clean: one worktree (main checkout only), zero unmerged
`dcs/*` branches, zero orphans, zero stale actives, zero dangling
branches. Payload (scoped to `dcs/**`, `agents/dcs-*.md`,
`skills/dcs-*/` per `install.ps1`) was clean before the run — whole
tree clean, not merely the payload subset.

**Content-witness reconciliation (`python tests/payload_check.py`),
before/after, both against integration-branch tip `729959b`
(unchanged across the run — nothing wrote into payload paths
mid-deploy):** before — **42 identical, 5 differing** (`dcs/VERSION`,
`dcs/references/doctrine-appendix.md`, `dcs/references/doctrine.md`,
`dcs/workflows/esg.md`, `dcs/workflows/new.md` — exactly
`decomposition-backlog-routing`'s own delivered set, expected input to
the ship, not a stop condition). After — **47 identical, 0 differing,
0 repo-only, 0 installed-only** → `DEPLOYED` per `deploy.md` step 7's
identical disposition.

**Shipped under Delegation v4 deploy authority** (`auto: true`,
`frontend_only` irrelevant here, no `forbidden_globs` hit, 1 row <=
`max_rows_per_train` 3) — announced in one visible line rather than a
click-through, per doctrine principle 12. `decomposition-backlog-routing`:
`ACTIVE`→`MERGED` (`close.md`, 2026-07-29) → `DEPLOYED` (this train,
same day). `dcs/decomposition-backlog-routing` branch deleted, its rollback
job done. Portfolio now: 14 DEPLOYED, 17 QUEUED, 2 PARKED, 8 KILLED,
0 ACTIVE, nothing deploy-pending. **Regenerate with a table-row-anchored
pattern, not a bare state-word match** — the latter also matches prose
narrating a past state (found live, this same edit: the `token-economy`
note below reads "**ACTIVE**, mid-execution as of this writing", a
stale 2026-07-28 sentence, not a current row, which the naive form
silently counts as one):
`grep -cE '^\| [a-z][a-z0-9-]* \|.*\| \*\*DEPLOYED\*\* \|' .dcs/esg/REGISTER.md`
(swap the state word for PARKED/KILLED/ACTIVE; QUEUED has no `**`
wrapping, so its own pattern drops the asterisks:
`'^\| [a-z][a-z0-9-]* \|.*\| QUEUED \|'`).

