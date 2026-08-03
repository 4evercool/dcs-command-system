### `/dcs-deploy`, 2026-08-03 — three-row train, portfolio-clean

Worktree audit clean: one worktree (main checkout only), zero orphans,
zero stale actives. One unmerged `dcs/*` branch is expected debris, not
a dangling-branch finding: `dcs/revision-preservation-map-abandoned-2026-07-31`,
a deliberately kept evidence branch from an abandoned early attempt (its
own register row: "kept... not a mergeable state") — not backed by a
`MERGED` row, did not ship. Payload (scoped to `dcs/**`, `agents/dcs-*.md`,
`skills/dcs-*/` per `install.ps1`) was clean before the run — whole tree
clean, not merely the payload subset.

**Content-witness reconciliation (`python tests/payload_check.py`),
before/after, both against integration-branch tip `9a9abee` (unchanged
across the run):** before — **44 identical, 6 differing** (`dcs/README.md`,
`dcs/VERSION`, `dcs/references/doctrine-appendix.md`,
`dcs/references/doctrine.md`, `dcs/references/forms.md`,
`dcs/workflows/close.md`), **1 repo-only** (`dcs/tools/record_integrity.py`).
Per `deploy.md` step 4, a differing/repo-only witness can't be attributed
to individual rows, so all 3 `MERGED` rows shipped together rather than
any reconciling away — including `record-integrity-corrections`, whose
own payload footprint was independently confirmed inert
(`git show a62ffad --stat`: `.dcs/incidents/**` + `vault/` only, nothing
under `dcs/`/`agents/`/`skills/`). After — **51 identical, 0 differing,
0 repo-only, 0 installed-only** → `DEPLOYED` per `deploy.md` step 7's
identical disposition.

**Shipped under Delegation v6 deploy authority** (`auto: true`, no row's
territory hit `forbidden_globs` — `dcs/hooks/**`, `install.ps1`,
`install.sh`, `bin/**` — none migration-bearing, 3 rows == `max_rows_per_train`
3) — announced in one visible line rather than a click-through, per
doctrine principle 12:

- `record-integrity-corrections`: `MERGED`→`DEPLOYED` (merge `a62ffad`,
  2026-08-02 → this train, 2026-08-03). `dcs/record-integrity-corrections`
  branch deleted.
- `close-integrity-guard-bundle`: `MERGED`→`DEPLOYED` (merge `779773b`,
  2026-08-03 → this train, same day). `dcs/close-integrity-guard-bundle`
  branch deleted. Ships `dcs/tools/record_integrity.py` (new) and the
  rewritten `close.md` — the unconditional close-time record-integrity
  gate is now live for every future close, including this deploy
  session's own eventual account of itself.
- `spawn-effort-control`: `MERGED`→`DEPLOYED` (merge `fd8740d`,
  2026-08-03 → this train, same day). `dcs/spawn-effort-control` branch
  deleted. The new "Capability tier" doctrine rule (per-spawn model-tier
  selection by availability and complexity) is now live in
  `~/.claude/dcs/references/doctrine.md` for the first session that
  starts after this install — not this deploying session itself, which
  already read the pre-deploy doctrine at its own start.

Portfolio counts, regenerated with the table-row-anchored pattern
(`grep -cE '^\| [a-z][a-z0-9-]* \|.*\| <STATE> \|' .dcs/esg/REGISTER.md`,
state word swapped per row, `QUEUED` dropping the `**` wrapping): 31
`DEPLOYED`, 20 `QUEUED`, 1 `PARKED`, 10 `KILLED`, 0 `ACTIVE`, 0
`MERGED (deploy pending)`, 1 plain `RESOLVED` — this hand-count does not
attempt to also match qualified variants like `RESOLVED (field repair)`,
so it is a lower bound on total rows, not a claimed total; regenerate
per-state rather than trusting this sum.

**ESG note carried forward, not acted on here:** the register's last
full re-rank (seventeenth `/dcs-esg`, 2026-08-02) had `close-integrity-guard-bundle`
at rank 1; it has now closed and shipped, so the portfolio's top slot is
open pending the next `/dcs-esg`. Two new rows exist since that ranking
and are both unranked: `spawn-effort-control` (Owner chat report) and
`spawn-effort-control-d5-corrections` (follow-up, queued at that
incident's own close).
