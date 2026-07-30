<!--
IAP.md -- the Integrated Action Plan, written by the IC during /dcs-plan.
This is the ONLY document specialists execute against once approved -- the
single source of truth doctrine principle 3 insists on. Editing this file
after approval voids IAP-APPROVED automatically (hash mismatch) -- that is
deliberate, not a bug to route around.
-->

# IAP — Incident Action Plan

**Incident:** 2026-07-30-hot-path-budget-emergency-trim
**Type:** 3
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `204-TASKING/S1.md` (203 skipped — default Type 3 activation: 1 specialist, plain parallel)

## Objectives (summary of 202)

**Goal:** Запас горячего пути (doctrine.md + schemas.md) увеличен с 493 байт до ≥2 000 байт путём сокращения прозы, без потери нормативного содержания. Проверка 7 (`test_doctrine_integrity.py`) остаётся зелёной, ratchet-константа `HOT_PATH_BUDGET_KB` пересчитана под новый размер.

1. Суммарный нормализованный (CRLF→LF) размер `dcs/references/doctrine.md` + `dcs/references/schemas.md` ≤ 36 864 байт (36 * 1024), сокращение ≥1 555 байт от текущих 38 419 байт. Команда: `python -c "d=open('dcs/references/doctrine.md','rb').read().replace(b'\r\n',b'\n'); s=open('dcs/references/schemas.md','rb').read().replace(b'\r\n',b'\n'); print(len(d)+len(s), 'bytes')"`.
2. Константа `HOT_PATH_BUDGET_KB` в `tests/test_doctrine_integrity.py` пересчитана: `math.ceil(<новый_размер> / 1024)` — ratchet act. [IC]
3. `python tests/test_doctrine_integrity.py` — все проверки проходят (check 7 зелёный), без изменения логики проверок. [IC]
4. В `CLAUDE.md` нет устаревших ссылок на старые значения бюджета. [IC]
5. Строка регистра `hot-path-budget-emergency-trim` в `.dcs/esg/REGISTER.md` исправлена: устаревшая ссылка на `HOT_PATH_BUDGET_KB=37` заменена на актуальную. [IC]
6. `vault/Metrics/incident-metrics.md` — запись о размере горячего пути обновлена под новый размер.

## Tactics (from the Planning Chief)

- Cut-registry approach: enumerate exact spans to trim, measure 'before' for each, attach KEEP constraint, specialist executes the ledger rather than exercising fresh editorial judgment. Reserve positions pre-authorised for shortfall, taken in strict order without deviation.
- Primary donor is doctrine.md (24,623 B) — it carries the growth that consumed the headroom and holds the largest blocks of compressible prose. schemas.md (13,796 B) contributes smaller, targeted savings.
- Tighten in place where the rule is the substance and the surrounding prose is the fat. Move to appendix where the passage is provenance/implementation-detail that deserves preservation but not hot-path residency. Reference live primary source where another file already carries the same rule (never duplicate).
- One specialist because the ratchet is a function of final combined size — one hand produces the size, the IC derives the constant.
- IC re-seats the ratchet after S1 returns: read S1's reported final combined size, compute math.ceil(new_size / 1024), update HOT_PATH_BUDGET_KB and its deriving comment, run the full suite. IC also corrects the REGISTER.md Notes stale reference and verifies CLAUDE.md has no stale budget numbers.

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | dcs/references/doctrine.md, dcs/references/schemas.md, dcs/references/doctrine-appendix.md, vault/Metrics/incident-metrics.md | dcs/workflows/**, dcs/templates/**, dcs/hooks/**, dcs/**, agents/**, skills/**, tests/**, bin/**, install.ps1, install.sh, package.json, dcs/VERSION, .dcs/**, CLAUDE.md, docs/**, vault/Post-mortems/**, vault/Decisions/**, vault/Meta/**, vault/Backlog.md, vault/00-Navigation.md, vault/_scripts/** |

**Partition status:** disjoint — parallel execution (single specialist)

## Risks

- Sequential dependency (not a partition conflict): the IC cannot re-seat HOT_PATH_BUDGET_KB until S1 reports the final combined size. This is normal P-loop behavior — disjoint territories make the dependency safe.
- doctrine-appendix.md append at end of file is the only write-path that could conflict if a second specialist existed — with one specialist, no conflict.
- Cut-registry estimate uncertainty: D2 (principle 13 implementation-detail migration) carries the largest single reduction (~868 B estimated) and the most editorial judgment. The specialist must parse the v0.6.9 sub-clause boundary correctly.
- Gap between specialist return and IC ratchet re-seat: test_doctrine_integrity.py check 7 uses HOT_PATH_BUDGET_KB=38 until the IC changes it. The specialist measures combined size directly, so evidence is valid regardless of the constant's state.
- The REGISTER.md Notes carry stale ceiling reference — IC must correct this (outside specialist territory).
- CLAUDE.md lines 56-57 and 146 mention 'hot-path budget' but carry no explicit kB value — low risk, but IC should grep for any number near 37/38/36 in the file.

## Verification plan

1. Combined size gate: run the normalised measurement command — doctrine.md + schemas.md ≤ 36,864 B.
2. All three test suites green with their own N/M counts: `python tests/test_doctrine_integrity.py`, `python tests/test_dcs_gate.py`, `python tests/test_dcs_intake.py`.
3. Schema contract intact: section numbers 1-8 preserved, all JSON blocks parseable, all 19 live citations to 'schemas.md #N' still resolve.
4. No normative content lost: for each moved-to-appendix position, confirm the full original text is present. For each compress-in-place position, diff confirms KEEP constraint held.
5. Stale references eliminated: REGISTER.md Notes corrected; CLAUDE.md grep clean; vault metrics updated with regeneration command.
6. The original 201 symptom (493 B headroom) is reversed — combined hot path now has ≥2,000 B of measured headroom.

## Deviation history (this period)

none (first IAP for period 1)
