# 201 — Incident Brief

**Incident:** trim-content-loss-restoration
**Opened:** 2026-08-01
**Type:** 1

## Symptom

Two prior DCS self-hosted incidents' commits — `bca0b56` (workflow-file-trim-grandfathered, a line-count trim of `dcs/workflows/plan.md` and `execute.md`, among others) and `e3d4bcc` (hot-path-budget-emergency-trim, a byte-budget trim of `dcs/references/doctrine.md` and `tests/test_doctrine_integrity.py`) — dropped operative content beyond what their own stated objective (reducing line/byte count) required. An external period review (`vault/Post-mortems/deepseek-period-review.md` §B) found this; two independent situation analysts in this stem reproduced every claim against git history and current file content, and found the true scope is larger than the review's own five-item list.

## Evidence

- CONFIRMED: `dcs/workflows/plan.md`'s no-DELEGATION fallback lost the sentence stating the `guarded_paths` auto-approval condition (`git show bca0b56 -- dcs/workflows/plan.md`, old lines ~340-350). Current `plan.md:127-129` now reads as an internally incoherent fragment: it says "No DELEGATION.md -> fallback to config.json (conservative, no per-bound audit)" but never states what that fallback's own `guarded_paths` condition actually is. `grep -rn guarded_paths` across `dcs/workflows/**` `dcs/references/**` returns zero hits — the term survives only in code (`dcs/hooks/dcs_gate.py:319-320`) and the config schema (`dcs/templates/config.json:3-4`), never in the prose that tells the IC when/how to apply it. This is a live safety-relevant gap, not pure prose loss.
- CONFIRMED: `dcs/workflows/execute.md` lost its explicit `escalate_owner` handling instruction ("use AskUserQuestion if the disposition is escalate_owner — the right call is genuinely the Owner's judgment, not just a mechanical correction"), `git show bca0b56 -- dcs/workflows/execute.md` old lines ~239-240. Current `execute.md:115` names the disposition enum but gives no handling instruction for it; no duplicate exists elsewhere.
- CONFIRMED, undercounted by the intake's "three": `bca0b56` deleted at least FOUR field-lesson provenance stories outright, not routed to `doctrine-appendix.md` per `CLAUDE.md`'s "Where lessons go" convention: 2026-07-22 (`close.md` step 5, "routine owns creates a race and duplicates its write"), 2026-07-23 (`plan.md` 4a lint, "an entire IAP review cycle... consumed by defects in this list"), 2026-07-24 (`plan.md`, "four Safety halts... on one objective"), 2026-07-24 (`execute.md`, "that fix then sat in a branch. A fix that is not shipped fixes nothing"). Two more possible losses flagged by an analyst (2026-07-26 version-bump-waiver story, 2026-07-24 IAP.md-edit-criterion story) need confirmation at planning time.
- CONFIRMED with a nuance: `e3d4bcc` dropped doctrine.md hard-rule-3's "notify if a tool is available" clause for unattended `/dcs-loop` operation. However `dcs/workflows/loop.md:92-100` independently carries an equivalent, more detailed instruction since commit `a3fb60b` (v0.2) — predating both trims by weeks. The behavior was never actually lost from the shipped package; only doctrine.md's own canonical restatement is missing it. Restoration should touch `doctrine.md` only, not `loop.md`.
- CONFIRMED: `tests/test_doctrine_integrity.py`'s budget-history comment chain is corrupted. `e3d4bcc` rewrote the 2026-07-26 (schemas-md-trim) paragraph's trailing figure in place to the 2026-07-30 incident's own figure (36539/36) instead of appending a new paragraph, and that new paragraph then duplicates the same figure. The corruption for this paragraph actually started one commit earlier, at `2e15682` (2026-07-29, unrelated incident worktree-removal-self-conflict), which overwrote the true 2026-07-26 figure (36547, budget 37) to a wrong intermediate figure (38361/38) and deleted an explanatory sentence. Fixing this requires reconstructing the true 2026-07-26 provenance line across both corrupting commits, not just reverting `e3d4bcc`'s diff.
- ADDITIONAL FINDING (present in the source review's own text but not in the intake's five-item list; same root commit, same root cause): `bca0b56` also over-broadened `execute.md`'s worktree-isolation clause from a scoped instruction into a blanket "set up the worktree per new.md step 7b before spawning" (current `execute.md:89`).
- `python tests/test_doctrine_integrity.py` currently passes 123/123 — none of these six losses are mechanically detectable; they are semantic content losses the merge-time guard's structural/citation checks do not reach. A guard against this *class* of defect is explicitly OUT of this incident's scope (a different root cause from restoring this instance's damage).

## Reproduction path

Not a runtime repro — a documentation/content-integrity defect. Verify via `git show bca0b56 -- dcs/workflows/plan.md dcs/workflows/execute.md dcs/workflows/close.md` and `git show e3d4bcc -- dcs/references/doctrine.md tests/test_doctrine_integrity.py`, diffed against current file content at each evidence bullet above.

## Blast radius (best guess at intake, refined by two situation analysts)

- `dcs/workflows/plan.md` — restore `guarded_paths` auto-approval condition prose; restore/relocate field-lesson stories (2026-07-23, 2026-07-24, and possibly 2026-07-26)
- `dcs/workflows/execute.md` — restore `escalate_owner` handling instruction; restore 1 field-lesson story (2026-07-24); narrow the over-broadened worktree-isolation clause back to its original scope
- `dcs/workflows/close.md` — restore 1 field-lesson story (2026-07-22)
- `dcs/references/doctrine.md` — restore "notify if a tool is available" to hard rule 3's canonical text
- `dcs/references/doctrine-appendix.md` — candidate destination for restored field-lesson stories per CLAUDE.md's "Where lessons go" convention — exact placement (inline in the workflow file vs. appendix) is a planning-time call; `new.md` itself still carries one inline field-lesson exemplar (lines 108-118), so both patterns coexist in the shipped package today
- `tests/test_doctrine_integrity.py` — repair the budget-history comment chain for the 2026-07-26 paragraph, reconstructing across both corrupting commits (`2e15682` then `e3d4bcc`)
- `dcs/workflows/loop.md` — EXCLUDED from territory on evidence: no actual defect: the equivalent instruction already exists there independently and predates both trims

Total: 6 files in scope.

**Budget constraint measured by the IC at typing (command point 1):** `dcs/workflows/execute.md` is at 250/250 lines (WORKFLOW_BUDGET_LINES hard ceiling, zero headroom); `dcs/workflows/plan.md` has 4 lines of headroom; `dcs/workflows/close.md` has 7; the hot path (doctrine.md + schemas.md) has 433 bytes of headroom against HOT_PATH_BUDGET_KB. Restored content cannot simply be reverted verbatim — it must be relocated (to `doctrine-appendix.md`) or compressed to fit. **Owner ruling (typing confirmation, 2026-08-01): the budget is inviolable — relocate or compress, never raise the budget constants as a side effect of this restoration.**

## Prior art

`vault/Post-mortems/deepseek-period-review.md` §B is the sole prior documentation (external review, 2026-08-01). No DCS incident has attempted this fix yet — `REGISTER.md` row `trim-content-loss-restoration` was QUEUED, rank 1 (fifteenth `/dcs-esg`, 2026-08-01), the row this stem opens. The two source incidents (`workflow-file-trim-grandfathered`, `hot-path-budget-emergency-trim`) are both DEPLOYED and are the origin of the regression, not just similarly-named prior art.

## Type + rationale

**Proposed type:** 1
**Rationale:** Six files including the constitution (`doctrine.md`) and the merge-time enforcement mechanism itself (`tests/test_doctrine_integrity.py`), with the restoration targets measured at zero line headroom (`execute.md` 250/250), 4 lines (`plan.md`), and 433 bytes of hot-path budget — the deleted content cannot be restored as previously-reviewed text and must be re-authored or relocated under the very budgets that caused its deletion, which is a structural/logistics call, not a mechanical revert. Typed by `dcs-commander` (IC, model opus/fable-tier) standing in for the main session, which is not running Fable this turn.
**Owner confirmation:** confirmed as proposed (Type 1), via `AskUserQuestion`, 2026-08-01. Owner also ruled on the IC's open question: the workflow-line and hot-path-byte budgets are inviolable for this incident — restored content must be relocated (to `doctrine-appendix.md`) or compressed to fit; raising `WORKFLOW_BUDGET_LINES` / `HOT_PATH_BUDGET_KB` is explicitly out of scope, not a side effect of this restoration.

## Intake source (for /dcs-close to route back to)

`vault/Post-mortems/deepseek-period-review.md` §B, Owner-directed queue 2026-08-01 (see `.dcs/esg/REGISTER.md` row `trim-content-loss-restoration`, ranked 1 at the fifteenth `/dcs-esg`, 2026-08-01).
