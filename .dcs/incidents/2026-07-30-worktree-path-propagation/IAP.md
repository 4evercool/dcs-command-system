# IAP — Incident Action Plan

**Incident:** worktree-path-propagation
**Period:** 1
**Type:** 3

## Links

- [202-OBJECTIVES.md](202-OBJECTIVES.md)
- 203-ORG.md: skipped (default Type 3 activation: 3 specialists, plain parallel, no Logistics Chief)
- [204-TASKING/S1.md](204-TASKING/S1.md) — agents/dcs-ops-specialist.md
- [204-TASKING/S2.md](204-TASKING/S2.md) — dcs/workflows/execute.md
- [204-TASKING/S3.md](204-TASKING/S3.md) — dcs/templates/204-TASKING.md

## Objectives summary

Goal: обеспечить, что ops-специалисты всегда редактируют файлы в worktree
инцидента. Механизм: параметр `worktree_root` в контракте специалиста +
инструкция по его передаче в execute.md.

Acceptance criteria:
1. agents/dcs-ops-specialist.md — `worktree_root` в inputs + правило разрешения в process
2. dcs/workflows/execute.md шаг 4 — передача `worktree_root` каждому специалисту
3. dcs/templates/204-TASKING.md — поле `worktree_root`
4. Все тесты проходят [IC]

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | agents/dcs-ops-specialist.md | dcs/workflows/**, dcs/templates/**, dcs/references/**, tests/** |
| S2 | dcs/workflows/execute.md | agents/**, dcs/templates/**, dcs/references/**, tests/** |
| S3 | dcs/templates/204-TASKING.md | agents/**, dcs/workflows/**, dcs/references/**, tests/** |

**Partition status:** disjoint — parallel execution

## Risks

- execute.md is 445/450 lines (grandfathered ceiling). S2 must stay within 5 net new lines.
- `worktree_root` is entirely net-new (0 matches in tree) — no regression risk, but the wiring must be unambiguous
- The specialist's territory-resolution rule must be clear enough that an LLM agent applies it — ambiguity would silently reintroduce the original defect

## Verification plan

1. Test suite: `python tests/test_dcs_gate.py && python tests/test_dcs_intake.py && python tests/test_doctrine_integrity.py` — 122/122 or better, zero new failures
2. grep -rn 'worktree_root' across all three target files — at least one match each
3. execute.md line count ≤ 450
4. `git worktree list --porcelain` referenced in execute.md step 4
5. Manual read: specialist charter inputs + process, template field coherence
