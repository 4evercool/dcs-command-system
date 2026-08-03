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

### GitHub release, same day (`docs/publishing.md` steps 1/5/6/9, Owner-directed)

CHANGELOG.md's `0.8.0` entry was found incomplete during release prep —
documented `close-integrity-guard-bundle` but not `spawn-effort-control`,
even though both shipped in this same train — fixed and committed
(`f13c791`), verified against the merge (`fd8740d`), not restated from
memory, per the 0.7.2 lesson. `npm pack --dry-run`: 165 files, 283.7 kB,
clean. Owner authorized the GitHub side explicitly; `npm publish` stays
Owner-only (2FA), not attempted here.

Ordered: `git push origin main` (`e25dc75..f13c791`) → tip gate confirmed
(`git rev-parse HEAD origin/main` identical) → `git tag v0.8.0` → `git
push --tags` → tag-at-HEAD confirmed → `python
tests/release_provenance_check.py` now exits 0 (was: `no git tag v0.8.0
exists`) → `gh release create v0.8.0` from the notes drafted during prep.
Release: https://github.com/4evercool/dcs-command-system/releases/tag/v0.8.0.
Registry still shows `0.7.2` as latest (`npm view dcs-command-system
version`) — `npm publish` is the one remaining step, and it is the
Owner's.

### `/dcs-deploy`, 2026-08-03 (second train, same day) — one-row train

Ran after `independence-fail-closed-and-model-floor` closed (merge
`f67f6d0`) via a same-day `/dcs-run --next`. Worktree audit clean: one
worktree (main checkout only), zero orphans, zero stale actives. Same
`dcs/revision-preservation-map-abandoned-2026-07-31` debris noted again
— unchanged, still not backed by a `MERGED` row, still did not ship.
Payload clean both scoped and whole-tree before the run.

**Content-witness reconciliation (`python tests/payload_check.py`),
both against integration-branch tip `783c4b9` (unchanged across the
run):** before — **38 identical, 13 differing** (the incident's 13
modified package files: `agents/dcs-safety-officer.md`,
`dcs/references/doctrine.md`/`schemas.md`/`doctrine-appendix.md`,
`dcs/templates/DELEGATION.md`, and 8 `dcs/workflows/*.md` files), **1
repo-only** (`dcs/tools/verdict_rerun.py`, new). Only one `MERGED` row
existed, so no reconciliation-away question arose — it shipped. After —
**52 identical, 0 differing, 0 repo-only, 0 installed-only** →
`DEPLOYED` per `deploy.md` step 7's identical disposition.

**Shipped under Delegation v6 deploy authority** (`auto: true`, the
row's 17-item territory hit no `forbidden_globs`, not migration-bearing,
1 row well under `max_rows_per_train` 3) — announced in one visible
line, per doctrine principle 12:

- `independence-fail-closed-and-model-floor`: `MERGED`→`DEPLOYED` (merge
  `f67f6d0`, 2026-08-03 → this train, same day). `dcs/independence-fail-closed-and-model-floor`
  branch deleted. Ships the Safety-Officer-independence fail-closed gate
  (`execute.md` step 8 spawn-liveness fallback, `close.md`'s unattended-close
  refusal, new `dcs/tools/verdict_rerun.py`) and the Delegation model
  floor (`approved_models` in `schemas.md` #7 and `templates/DELEGATION.md`,
  gated at all 9 real bound-read sites across 6 workflows) — both now
  live in `~/.claude/dcs/` for the next session that starts. This
  deploying session itself already read the pre-deploy `doctrine.md`/
  workflows at its own start, so the new independence/model-floor rules
  govern sessions from here forward, not retroactively.

Intake source (`vault/Decisions/non-anthropic-hardening.md` packaging
item 3) updated from `MERGED (deploy pending)` to `DEPLOYED` at this
step — the flag `close.md` raised became actionable exactly here, per
`deploy.md` step 8's intake-closure linkage note.

No GitHub release or npm publish this train — Owner did not direct
either; both remain separate, Owner-gated acts per `docs/publishing.md`.
