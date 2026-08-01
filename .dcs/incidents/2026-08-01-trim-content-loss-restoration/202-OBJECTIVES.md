# 202 — Objectives (Operational Period 1)

**Incident:** trim-content-loss-restoration
**Period:** 1

## Goal

Content dropped by two prior trim commits (`bca0b56`, `e3d4bcc`) is restored to the shipped package — verbatim where it fits, relocated per the core/appendix convention where it doesn't — without exceeding the current `WORKFLOW_BUDGET_LINES` or `HOT_PATH_BUDGET_KB` ceilings, and the corrupted test budget-history comment chain reflects true provenance.

## Acceptance criteria (the Definition of Done)

1. `dcs/workflows/plan.md`'s no-DELEGATION fallback states the `guarded_paths` auto-approval condition explicitly, not just the term in code/config — `grep -c guarded_paths dcs/workflows/plan.md` returns ≥1 and the surrounding sentence names the actual condition (files outside the ordinary source tree void the fallback).
2. `dcs/workflows/execute.md`'s deviation-arbitration step (step 6) states the `escalate_owner` handling instruction (use `AskUserQuestion` when the disposition is `escalate_owner`, because the call is genuinely the Owner's) — `grep -n "escalate_owner" dcs/workflows/execute.md` shows handling text, not only the enum name.
3. `dcs/workflows/execute.md`'s worktree-isolation clause is narrowed back to a scoped instruction, not the current blanket "set up the worktree per new.md step 7b before spawning" — read the line and confirm it is conditioned, not unconditional.
4. The 2026-07-22 field lesson ("routine owns creates a race and duplicates its write", originally `close.md` step 5) is present, verbatim or cited, in `close.md` or `doctrine-appendix.md` — `grep -rn "routine owns\|race and duplicates" dcs/workflows/close.md dcs/references/doctrine-appendix.md` returns ≥1 match.
5. The 2026-07-23 field lesson ("an entire IAP review cycle... consumed by defects", originally `plan.md` 4a lint) is present, verbatim or cited, in `plan.md` or `doctrine-appendix.md` — same grep pattern against the distinctive text.
6. The 2026-07-24 field lesson ("four Safety halts... on one objective", originally `plan.md`) is present, verbatim or cited, in `plan.md` or `doctrine-appendix.md`.
7. The 2026-07-24 field lesson ("that fix then sat in a branch... fixes nothing", originally `execute.md`) is present, verbatim or cited, in `execute.md` or `doctrine-appendix.md`.
8. `dcs/references/doctrine.md`'s unattended hard-rule 3 states the "notify if a tool is available" clause — `grep -n "notify" dcs/references/doctrine.md` inside the hard-rules block returns ≥1 match.
9. `tests/test_doctrine_integrity.py`'s budget-history comment chain no longer duplicates one figure across the 2026-07-26 and 2026-07-30 paragraphs — the 2026-07-26 paragraph states its own true, reconstructed figure, distinct from 2026-07-30's.
10. [IC] Neither `WORKFLOW_BUDGET_LINES` nor `HOT_PATH_BUDGET_KB` constant value changes anywhere in `tests/test_doctrine_integrity.py` — `git diff main -- tests/test_doctrine_integrity.py` shows no change to those two assignment lines (Owner ruling at typing: budgets are inviolable for this incident).
11. [IC] `dcs/workflows/loop.md` is unchanged this period — `git diff main -- dcs/workflows/loop.md` is empty (no defect found there at the stem; explicitly out of scope).
12. `python tests/test_doctrine_integrity.py` passes (all cases green) after all restorations — named test run, independently re-run by the Safety Officer.
13. Every edited workflow file (`plan.md`, `execute.md`, `close.md`) stays at or under `WORKFLOW_BUDGET_LINES` (currently 250) — `wc -l dcs/workflows/plan.md dcs/workflows/execute.md dcs/workflows/close.md`, each ≤ 250.
14. `doctrine.md` + `schemas.md` combined stay at or under `HOT_PATH_BUDGET_KB` (currently 37 KiB) — regenerate per STRATEGY.md objective 1's documented measurement command.

## Out of scope this period

A new automated guard that catches semantic content loss in future trims (the defect *class*, not this instance's damage) — candidate for a separate future incident, not this one. Raising `WORKFLOW_BUDGET_LINES` or `HOT_PATH_BUDGET_KB` — Owner ruled these budgets inviolable for this restoration (typing confirmation, 2026-08-01). Two possible additional field-lesson losses flagged by only one of two situation analysts (2026-07-26 version-bump-waiver story, 2026-07-24 IAP.md-edit-criterion story) — the Planning Chief should confirm or deny their status during tactics; if confirmed real, they are a follow-up, not silently folded into this period's criteria without a fresh gate.

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

{{filled in after chiefs return}}
