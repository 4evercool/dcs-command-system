# 202 — Objectives (Operational Period 1)

**Incident:** spawn-effort-control
**Period:** 1

## Goal

The IC's choice of which tier answers a spawn tracks that spawn's actual
complexity every time, not a value fixed once when the seat was defined —
using the mechanism that genuinely works today (the Agent tool's existing
per-call `model` override, since no per-call effort parameter exists),
phrased so it never assumes a specific provider's effort vocabulary is
universal.

## Acceptance criteria (the Definition of Done)

1. `dcs/references/doctrine.md` states a rule for selecting a spawn's
   capability tier by that spawn's own complexity, grounded in the real
   per-call `model` override that already exists today — not an
   unverified `effort:` parameter (verified: read the new/extended text
   directly and confirm it names the mechanism it actually relies on).
2. That rule and the existing availability-fallback rule ("Model
   availability," doctrine.md's current tier-fallback text) are ONE
   mechanism, not two separate/competing principles — `doctrine.md`
   contains exactly one place governing per-spawn tier selection after
   this incident (verified: read the full "Transfer of command" section
   and confirm no duplicate or conflicting rule was added elsewhere).
3. The rule's vocabulary is provider-agnostic: it selects "the strongest
   tier the complexity warrants, from what's available for that seat's
   provider," never mandating Claude's specific low/medium/high/xhigh/max
   scale as the only shape a tier can take (verified: read the new/
   extended text directly — no unconditional Claude-specific vocabulary
   asserted as universal).
4. The existing Fable availability-fallback behavior for the four command
   points is unchanged in substance — re-testing availability per spawn,
   never caching the fallback, still holds exactly as before (verified:
   diff each workflow's command-point spawn instructions against their
   pre-incident text; every change is additive, never a removal of the
   existing guarantee).
5. `python tests/test_doctrine_integrity.py` passes in full, including
   its hot-path budget check (`doctrine.md` + `schemas.md` ≤
   `HOT_PATH_BUDGET_KB`, currently 37) — the Owner's ruling that the
   ceiling stays fixed holds, satisfied by an offsetting trim if the
   addition needs one, never a ceiling increase.
6. `python tests/test_dcs_gate.py` and `python tests/test_dcs_intake.py`
   stay green — no regression to the gate or intake mechanics this
   incident doesn't intend to touch.
7. `dcs/references/doctrine-appendix.md` gains a field-lesson entry
   recording the platform-capability finding (the interactive Agent tool
   has no per-call effort parameter, only `model`) and why the design
   reuses tier-substitution rather than waiting on or assuming a
   parameter that doesn't exist — citing how it was verified.
8. The rule ships with at least 2 concrete worked examples distinguishing
   a default-tier spawn from a deliberately stronger-tier spawn, grounded
   in real DCS work (e.g. a one-line prose fix vs. a multi-file
   architectural tactic) — not left as an unguided judgment call with
   zero worked examples (verified: the examples are findable and
   concrete, whether they live in doctrine.md itself or a paired
   reference it points to).

## Out of scope this period

- New per-effort-tier agent-charter file variants (multiplies the
  charter count against Type 1's own blast-radius discipline; unnecessary
  given the tier-substitution design).
- Changing any of the six `agents/dcs-*.md` charters' existing static
  `model:` defaults.
- Algorithmic or scripted complexity scoring — this stays an IC judgment
  call, the same way typing and every other command-point decision does;
  no scoring formula, heuristic script, or automation is in scope.
- Actually spawning any DCS seat on a non-Claude provider — no such spawn
  has ever happened in this project (verified at the stem); the design
  must not preclude it, but making it happen is not this incident's job.
- Waiting on, or assuming the arrival of, a native per-call effort
  parameter for the interactive Agent tool — not DCS's to build; the
  design must work with today's real tool surface.

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

{{objectives_feedback from the chief-plan schema -- if the Chief flagged a
criterion as untestable, note the resolution here: revised criterion, or
Owner accepted the risk}}
