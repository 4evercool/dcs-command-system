# 201 — Incident Brief

**Incident:** provisioning-script-upstreaming
**Opened:** 2026-07-30
**Type:** 1

## Symptom

The bread_bot project has a worktree provisioning script (`.dcs/provision-worktree.ps1`, 216 lines) that copies four gitignored payload targets (`.env`, local database, `node_modules` via `npm ci`, `dist`) from the main checkout into a freshly-created DCS worktree. Three prior bread_bot incidents burned Safety Officer cycles on worktrees missing these files. The script shipped as a Phase 0 field repair on 2026-07-27 with its register row explicitly marked "LOCAL — candidate for upstreaming." For two days, no register row, backlog item, or decision document in DCS carried the upstreaming question — it silently drifted until the fable-review-roadmap's 2026-07-29 amendment flagged the gap. The tenth `/dcs-esg` (2026-07-29) queued it as a register row (the Owner chose queue over the Chief of Staff's below-the-bar backlog-line recommendation); the thirteenth (2026-07-30) raised it to rank 3. DCS itself has no worktree provisioning mechanism — `install.ps1`/`install.sh`/`bin/dcs.js` only copy the DCS package payload into `~/.claude`, and `dcs/workflows/new.md` creates worktrees via bare `git worktree add` with no provisioning step.

The central question: should DCS generalize this pattern (a config-driven or convention-based provisioning hook), or formally decline and leave it project-local? The disposition — upstream, backlog-line, or recorded decline — is the deliverable; silent drift is the defect.

## Evidence

- Bread_bot provisioning script (C:\bread_bot\.dcs\provision-worktree.ps1): 216 lines, PowerShell, 4 hardcoded bread_bot-specific paths (Copilot\.env, Copilot\bread_orders.db, Copilot\frontend\node_modules, Copilot\frontend\dist). Idempotent (every target skipped with `[skip]` if already present), junction-guarded (stale junction detection + removal before `npm ci`), resolves main root via `git worktree list --porcelain` rather than `$PSScriptRoot` (a fix applied 2026-07-28 after the original PSScriptRoot-based resolution broke when invoked from inside the worktree). Smoke-tested on a throwaway worktree — all 4 targets provisioned, re-run produced `[skip]` on all. — source: situation-analyst direct file read + bread_bot REGISTER.md row `dcs-worktree-provisioning-local`
- Three prior bread_bot incidents motivated its creation: `cost-dynamics-labor-toggle`, `cost-dynamics-per-product`, `tools-prod-db-guards` — all burned Safety Officer cycles on worktrees missing payload files (the app would not start, or `npm run build` failed cold). — source: provision-worktree.ps1 header comment, lines 9-12
- DCS `dcs/workflows/new.md` line 197: sole `git worktree add` invocation — bare command, no post-worktree provisioning step exists between worktree creation and incident-file writes. — source: situation-analyst grep of dcs/workflows/
- DCS `dcs/workflows/execute.md` line 135: second `git worktree add` site (worktree-isolated specialists) — also lacks any provisioning step. — source: situation-analyst grep
- DCS `bin/dcs.js`: supports `install`, `uninstall`, `doctor`, `bump`, `version`, `postinstall` — no `provision` or `worktree` command. `install` copies DCS payload only (dcs/, agents/, skills/ into ~/.claude). — source: situation-analyst file read
- DCS has no `.env`, no database, no `node_modules`, no `dist` — the generalization problem is real: all 4 bread_bot targets are project-specific, and DCS itself needs none of them for its own operation. — source: situation-analyst file-system inspection + .gitignore
- Register row territory estimate: `install.ps1`, `install.sh`, `bin/**` — all three inside Delegation v4 `forbidden_globs`, so any IAP needs Owner approval regardless of typing. — source: REGISTER.md row 140, DELEGATION.md lines 342-348
- `vault/Decisions/fable-review-roadmap.md` Phase 3 (lines 304-314): the upstreaming question had "silently lost its carrier" until the 2026-07-29 amendment — no register row, backlog item, or vault decision carried it for two days. — source: situation-analyst file read
- Related bread_bot incident `worktree-junction-node-modules-wipe` (bread_bot REGISTER.md row 116, DEPLOYED): independently fixed a destructive junction bug — the script being considered for upstreaming is already the post-fix version using `npm ci` instead of junctions. — source: situation-analyst cross-reference

## Reproduction path

Not reproducible as a defect — this is an upstreaming/disposition decision. The bread_bot script is verified correct (live smoke on a throwaway worktree, re-run idempotent). The question is whether DCS should generalize this pattern or formally decline.

## Blast radius (best guess at intake)

- `dcs/workflows/new.md` — the `git worktree add` step (natural insertion point for a provisioning hook)
- `dcs/workflows/execute.md` — second worktree-add site for isolated specialists
- `bin/dcs.js` — if a `dcs provision` command is added
- `dcs/references/doctrine.md` — if provisioning becomes a doctrine-level concept
- `dcs/references/doctrine-appendix.md` — provenance of any new provisioning rule
- `install.ps1`, `install.sh` — if the provisioning script itself rides the installer payload
- `package.json` — if `bin/` or `files` whitelist changes

## Prior art

Full provenance chain in `vault/Decisions/fable-review-roadmap.md`: rec 6 of the 2026-07-27 third-party fable review ("Provision worktrees — .env, node_modules, dist, test DB; a ~20-line setup script at worktree creation") → Phase 0 item 2 shipped bread_bot-local with register row marked "LOCAL — candidate for upstreaming" (commit `4ae52377`) → two-day silent drift with no carrier in any DCS surface → 2026-07-29 roadmap amendment flags the gap → tenth `/dcs-esg` (2026-07-29) queues it as register row `provisioning-script-upstreaming` at rank 10 (Owner overrides Chief of Staff's below-the-bar backlog-line recommendation) → thirteenth `/dcs-esg` (2026-07-30) re-ranks to rank 3. A related bread_bot incident `worktree-junction-node-modules-wipe` independently fixed a destructive junction bug in the script.

## Type + rationale

**Proposed type:** 1
**Rationale:** Territory estimate includes `install.ps1`, `install.sh`, `bin/**` — all inside Delegation `forbidden_globs` — and `CLAUDE.md` classifies installer changes as Type 1. Even if the incident resolves to a recorded decline, the scope includes the upstreaming path and the rule is type-up-not-down; a provisioning hook would be a new cross-cutting architectural pattern touching the enforcement mechanism itself. (IC=dcs-commander, opus — fable unavailable at spawn time)
**Owner confirmation:** confirmed as proposed (Type 1)

## Intake source

`vault/Decisions/fable-review-roadmap.md` Phase 3, rec-6 residue; surfaced at the tenth `/dcs-esg`, 2026-07-29; queued as register row `provisioning-script-upstreaming`
