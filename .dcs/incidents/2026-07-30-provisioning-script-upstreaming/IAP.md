# IAP — Incident Action Plan

**Incident:** provisioning-script-upstreaming
**Type:** 1
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `203-ORG.md` · `204-TASKING/*.md` · logistics plan below

## Objectives (summary of 202)

**Goal:** The worktree provisioning question has a recorded, reasoned disposition: DCS either generalizes the bread_bot pattern into a project-agnostic mechanism, or formally declines to — and the two-day silent drift that motivated this register row is closed either way.

**Acceptance criteria:**
1. A disposition is made and recorded: **upstream** (a generalized provisioning mechanism is designed and shipped) **or** **decline** (a formal decision document states why DCS should not carry this mechanism, with reasoning that would hold for any onboarded project, not only bread_bot).
2. **If upstream:** DCS ships a worktree-provisioning mechanism that is project-agnostic — no hardcoded bread_bot paths, configurable per-project — integrated into the worktree-creation step(s) in `dcs/workflows/new.md` (and `dcs/workflows/execute.md` if applicable). The mechanism is documented in doctrine (or a workflow). *(The bread_bot script's "LOCAL — candidate for upstreaming" marker resolution is cross-project — DCS cannot touch bread_bot files; tracked as a follow-up act in bread_bot's own repo.)*
3. **If decline:** a decision document lives at `vault/Decisions/provisioning-script-upstreaming.md` with the reasoning. The register row `provisioning-script-upstreaming` transitions to `RESOLVED` with the decision summarized in its Outcome cell. The bread_bot script's "LOCAL" marker is preserved, and the fable-review-roadmap's Phase 3 rec-6 residue is marked discharged. [IC]
4. `python tests/test_doctrine_integrity.py` passes (no regression). If upstream code is shipped, `python tests/test_dcs_gate.py && python tests/test_dcs_intake.py` also pass.
5. The register row is updated to reflect the terminal state (RESOLVED or MERGED, depending on disposition). [IC]
6. The disposition is Owner-confirmed. [Owner]

## Tactics (from the Planning Chief)

1. Generalize bread_bot's provisioning pattern into a DCS convention: a project-supplied executable or script at `<project>/.dcs/provision` that DCS runs after any `git worktree add` — both `new.md` step 7b's primary worktree creation and `execute.md` step 4's worktree-isolated specialist clause. DCS provides only the hook point and invocation contract; the project owns the content entirely. No new shipped files, no hardcoded paths, no cross-platform script to maintain.
2. Document the convention in `doctrine.md` (new subsection under "Parallel operation": path, invocation args, exit-code contract, idempotency expectation, DCS's no-content guarantee) with provenance in `doctrine-appendix.md` tracing to bread_bot's field script, the three motivating incidents, and the review-to-register chain.
3. If the IC decides DECLINE: bypass all code taskings below. The IC writes a decision document at `vault/Decisions/provisioning-script-upstreaming.md` and resolves the register row directly — vault is unguarded, no specialist needed, tests pass as baseline.

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | `dcs/workflows/new.md`, `dcs/workflows/execute.md` | `dcs/references/**`, `tests/**` |
| S2 | `dcs/references/doctrine.md`, `dcs/references/doctrine-appendix.md`, `tests/test_doctrine_integrity.py` | `dcs/workflows/**` |

**Partition status:** disjoint — parallel execution

## Deploy / environment plan (Type 1, from the Logistics Chief)

**Deploy path:** Two-branch disposition. UPSTREAM: full deploy via `install.ps1` / `install.sh` (channel 1 — copies `dcs/`, `agents/`, `skills/` into `~/.claude`); `bin/dcs.js` is not touched by this plan. DECLINE: no deploy — vault decision doc (not shipped) + register row update (gitignored).

**Environment dependencies:**
- UPSTREAM: No new env vars. Config-driven (`.dcs/provision` convention), not env-var-driven.
- UPSTREAM: No new npm/pip dependencies. Standalone script convention with no runtime deps.
- UPSTREAM: No cross-platform risk — the convention is an invocation point in prose; projects supply their own platform-appropriate script.
- DECLINE: No environment or dependency changes.

**Migration ordering:** No migration. DCS is file-based — no database, no schema, no persistent state. All changes are additive (new workflow step, new doctrine text). Workflows are read fresh on every invocation — a new provisioning step takes effect immediately after `install.ps1` / `install.sh` runs, with no service restart needed.

**Rollback plan:** UPSTREAM: All changes are additive — redeploy the prior commit via `install.ps1` / `install.sh`. No destructive operations to undo. A worktree created with the provisioning step is fine after rollback — the step is idempotent by design, and a post-rollback workflow that omits provisioning leaves the worktree in a working state.
DECLINE: None needed — nothing was deployed.

## Risks

1. Workflow line-count budgets are extremely tight: `new.md` currently 255/260 (5 lines headroom), `execute.md` 450/450 (0 headroom). S1 must keep each addition to single-digit line counts. S2 adjusts ceilings (new.md: 270, execute.md: 460) to provide headroom, but if S1 produces significantly more text than expected, the integrated test will still fail.
2. Hot-path budget headroom is 301 bytes (36,563/36,864). S2's doctrine additions of ~12 lines (~720 bytes) will almost certainly exceed it, requiring `HOT_PATH_BUDGET_KB` to bump from 36 to 37. This is a known and accounted-for adjustment.
3. The DECLINE path voids both taskings. If the IC decides DECLINE at IAP review, no specialist spawn is needed — the IC writes `vault/Decisions/provisioning-script-upstreaming.md` directly (vault is unguarded) and resolves the register row.
4. Criterion 2's bread_bot marker resolution is cross-project — scoped out of this incident per doctrine principle 6 (v0.6.2).
5. The 201 blast radius lists `bin/dcs.js`, `install.ps1`, `install.sh`, `package.json` — this plan touches none of them. Territory is `dcs/workflows/`, `dcs/references/`, and `tests/` only.
6. `forbidden_globs` in Delegation v4 includes `install.ps1`, `install.sh`, `bin/**` — neither S1 nor S2 touches any of these, but the Delegation check at step 6 will still fire because Type 1 is never auto-approved.
7. Self-hosting: `install.ps1` must not run during an active DCS incident (CLAUDE.md hard rule). Deploy happens after `/dcs-close`.
8. `npm publish` is out of scope this period — `bin/dcs.js` is not touched by this plan.

## Verification plan

1. Run `python tests/test_doctrine_integrity.py` from repo root — all checks pass: workflow budgets within adjusted ceilings, hot path within adjusted budget, principle numbering contiguous, version sync, encoding clean, schema citations resolve.
2. Run `python tests/test_dcs_gate.py` — all checks pass.
3. Run `python tests/test_dcs_intake.py` — all checks pass.
4. Read `dcs/workflows/new.md` step 7b end-to-end: `git worktree add` → `.dcs/provision` check → incident directory creation. The three form a coherent sequence.
5. Read `dcs/workflows/execute.md` step 4's worktree-isolated clause: now references both `git worktree add` and the provisioning convention.
6. Read `dcs/references/doctrine.md` "Parallel operation" → new provisioning subsection: path, invocation args, exit-code contract, idempotency expectation, DCS's no-content guarantee all stated.
7. Read `dcs/references/doctrine-appendix.md` → provenance paragraph citing bread_bot's script by commit, the three incidents by slug, and the review-to-register chain.
8. If DECLINE: tests pass as baseline; `vault/Decisions/provisioning-script-upstreaming.md` exists with dated decision, rationale, and register-row resolution note; register row shows `RESOLVED`.

## Deviation history (this period)

None — first IAP for this incident.
