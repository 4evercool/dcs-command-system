# 202 — Objectives (Operational Period 1)

**Incident:** provisioning-script-upstreaming
**Period:** 1

## Goal

The worktree provisioning question has a recorded, reasoned disposition: DCS either generalizes the bread_bot pattern into a project-agnostic mechanism, or formally declines to — and the two-day silent drift that motivated this register row is closed either way.

## Acceptance criteria (the Definition of Done)

1. A disposition is made and recorded: **upstream** (a generalized provisioning mechanism is designed and shipped) **or** **decline** (a formal decision document states why DCS should not carry this mechanism, with reasoning that would hold for any onboarded project, not only bread_bot).
2. **If upstream:** DCS ships a worktree-provisioning mechanism that is project-agnostic — no hardcoded bread_bot paths, configurable per-project — integrated into the worktree-creation step(s) in `dcs/workflows/new.md` (and `dcs/workflows/execute.md` if applicable). The mechanism is documented in doctrine (or a workflow). *(The bread_bot script's "LOCAL — candidate for upstreaming" marker resolution is cross-project — DCS cannot touch bread_bot files; tracked as a follow-up act in bread_bot's own repo.)*
3. **If decline:** a decision document lives at `vault/Decisions/provisioning-script-upstreaming.md` with the reasoning. The register row `provisioning-script-upstreaming` transitions to `RESOLVED` with the decision summarized in its Outcome cell. The bread_bot script's "LOCAL" marker is preserved, and the fable-review-roadmap's Phase 3 rec-6 residue is marked discharged. [IC]
4. `python tests/test_doctrine_integrity.py` passes (no regression). If upstream code is shipped, `python tests/test_dcs_gate.py && python tests/test_dcs_intake.py` also pass.
5. The register row is updated to reflect the terminal state (RESOLVED or MERGED, depending on disposition). [IC]
6. The disposition is Owner-confirmed. [Owner]

## Out of scope this period

- A full npm publish cycle (if upstreaming produces shippable code, the deploy is a separate `/dcs-deploy` act — the incident delivers the mechanism, not the ship)
- Porting the bread_bot script to POSIX shell (the generalization design decides whether a cross-platform provision command belongs in `bin/dcs.js` or as a template script; a POSIX equivalent is a separate concern unless the design explicitly includes it)

## Chief feedback

(filled in after Planning Chief returns)
