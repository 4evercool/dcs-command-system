# AAR — After Action Report

**Incident:** provisioning-script-upstreaming
**Type:** 1
**Opened:** 2026-07-30
**Closed:** 2026-07-30
**Operational periods:** 1

## Outcome

The UPSTREAM disposition was chosen and delivered: DCS now has a generalized worktree provisioning convention. A project places an executable or script at `<project>/.dcs/provision`; DCS runs it after every `git worktree add` with the worktree path and main checkout root as arguments. Exit 0 = success, non-zero = warn-and-proceed, absent file = skip silently. DCS provides only the execution point — the project owns the provisioning content entirely.

All six 202 acceptance criteria are met:
1. ✅ UPSTREAM disposition made and recorded
2. ✅ Project-agnostic `.dcs/provision` mechanism integrated into `new.md` step 7b and `execute.md` step 4, documented in `doctrine.md` + `doctrine-appendix.md`
3. N/A — decline path not taken
4. ✅ All three test suites pass: 122/122 doctrine integrity, 100/100 gate, 10/10 intake
5. ✅ Register row updated to `MERGED (deploy pending)` — this AAR section; terminal state reached at merge
6. ✅ Owner confirmed disposition at IAP approval

The two-day silent drift that motivated the register row is closed: the fable-review-roadmap's Phase 3 rec-6 residue now has a recorded, shipped disposition.

**Deploy status:** pending — `/dcs-deploy` is the next step. The merge commit is `bf21a1f` on `dcs/provisioning-script-upstreaming`, merged into `main` via `--no-ff`.

**Owner-UAT status:** not defined in IAP — the IAP's verification plan covers automated checks only.

## What worked

- **Planning Chief's two-path design:** accommodating both UPSTREAM and DECLINE in the same plan was correct — it let the IC decide the disposition at IAP time rather than pre-committing, and the DECLINE path required zero specialist spawns.
- **Logistics Chief's budget analysis:** flagging `execute.md` at 450/450 (0 headroom), `new.md` at 255/260 (5 lines headroom), and doctrine hot-path at 301 bytes headroom was precise — all three constraints bound, and S2's ceiling adjustments (new.md 270, execute.md 460, hot-path 37 KB) absorbed S1's additions exactly.
- **Safety Officer's version-tag catch:** the advisory on `v0.7` vs `v0.7.1` mismatch was correct — the IC had overlooked the inconsistency.

## Lessons

- **`worktree-path-propagation` fix is incomplete.** S1 (dcs-ops-specialist) edited the main checkout (`C:\DCS`) instead of the worktree (`C:\DCS-wt\provisioning-script-upstreaming`) despite the worktree root being stated in its 204 tasking. The incident `worktree-path-propagation` (DEPLOYED at rank H, 2026-07-30) was supposed to fix this, but the defect manifested again in the very next incident. S2 correctly edited the worktree — the bug is intermittent. Worth measuring: under what conditions does a specialist ignore the stated worktree root? The tasking format was identical for both specialists.

## Deviations this incident

- **S1 wrong-location edit:** S1 returned `status: "done"` but `files_touched` pointed to the main checkout, not the worktree. The IC applied S1's changes to the worktree manually via the Edit tool, then reverted the main checkout with `git checkout`. This was a process deviation — the specialist's return was truthful about what it touched, but the location was wrong. No command-point deviation arbitration was needed because the fix was mechanical (copy changes, revert wrong location).

## Memory routing

- `vault/Meta/building-dcs-lessons.md` — recorded the incomplete `worktree-path-propagation` fix observation (S1 edited main checkout despite worktree root in tasking)
- Deploy pending — `/dcs-deploy` will mark the register row `DEPLOYED` and delete the branch

## Intake source closure

Intake source: `vault/Decisions/fable-review-roadmap.md` Phase 3, rec-6 residue. The roadmap's Phase 3 now has its rec-6 residue discharged — the disposition is recorded, the mechanism ships. No external system to close; the register row itself carries the terminal state.

## Safety Officer's final verdict (verbatim, from SAFETY.md)

```json
{
  "verdict": "pass",
  "refutations": [],
  "advisories": [
    {
      "finding": "Version tag mismatch between new.md and doctrine.md. dcs/workflows/new.md:203 labels the feature '(v0.7)' while dcs/references/doctrine.md:157 labels it '(v0.7.1)'.",
      "fix": "Pick one version label (likely v0.7.1) and use it consistently."
    }
  ],
  "checked": [
    "Read full git diff of all 5 files in worktree — diff confirms only the claimed provisioning-hook additions and budget-ceiling adjustments",
    "Ran `python tests/test_doctrine_integrity.py` independently — 122/122 passed",
    "Ran `python tests/test_dcs_gate.py` independently — 100/100 passed",
    "Ran `python tests/test_dcs_intake.py` independently — 10/10 passed",
    "Verified hot-path byte budget: 37455 B, ceil(37455/1024) = 37 — matches HOT_PATH_BUDGET_KB",
    "Verified new.md line count: 263 — within adjusted ceiling 270",
    "Verified execute.md line count: 451 — within adjusted ceiling 460",
    "Verified IAP-APPROVED hash matches",
    "Verified main checkout has zero guarded-file changes",
    "Read all insertion sites — flow is correct, contracts stated, provenance cited"
  ]
}
```

Advisory resolved by IC: changed `(v0.7)` to `(v0.7.1)` in `new.md` line 203.
