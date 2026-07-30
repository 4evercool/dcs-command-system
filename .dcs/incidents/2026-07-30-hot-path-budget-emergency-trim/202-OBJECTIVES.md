<!--
202-OBJECTIVES.md -- written by the IC together with the Owner, at the
start of EACH operational period (/dcs-plan). Re-drafted (new file content,
same filename) each time the incident re-enters the P-loop for another
period -- the prior period's 202 is preserved in 214-LOG.md's phase-
transition history and, once complete, in AAR.md's summary, not in this
file itself.
-->

# 202 — Objectives (Operational Period 1)

**Incident:** 2026-07-30-hot-path-budget-emergency-trim
**Period:** 1

## Goal

Запас горячего пути (doctrine.md + schemas.md) увеличен с 493 байт до ≥2 000 байт путём сокращения прозы, без потери нормативного содержания. Проверка 7 (`test_doctrine_integrity.py`) остаётся зелёной, ratchet-константа `HOT_PATH_BUDGET_KB` пересчитана под новый размер.

## Acceptance criteria (the Definition of Done)

1. Суммарный нормализованный (CRLF→LF) размер `dcs/references/doctrine.md` + `dcs/references/schemas.md` ≤ 36 864 байт (36 * 1024), то есть сокращение минимум на 1 555 байт от текущих 38 419 байт, с запасом ≥2 000 байт до потолка 38 912. Команда: `python -c "d=open('dcs/references/doctrine.md','rb').read().replace(b'\r\n',b'\n'); s=open('dcs/references/schemas.md','rb').read().replace(b'\r\n',b'\n'); print(len(d)+len(s), 'bytes')"`.
2. Константа `HOT_PATH_BUDGET_KB` в `tests/test_doctrine_integrity.py` пересчитана: `math.ceil(<новый_размер> / 1024)` — ratchet act. Команда: `grep -n "HOT_PATH_BUDGET_KB" tests/test_doctrine_integrity.py`.
3. `python tests/test_doctrine_integrity.py` — все проверки проходят (check 7 зелёный), без изменения логики проверок. [IC] — `tests/test_doctrine_integrity.py` под guard.
4. В `CLAUDE.md` нет устаревших ссылок на старые значения бюджета (если есть — обновлены). Команда: `grep -in "hot.path\|budget.*kb\|hot_path" CLAUDE.md` → ни одна ссылка не содержит устаревшего числа.
5. Строка регистра `hot-path-budget-emergency-trim` в `.dcs/esg/REGISTER.md` исправлена: устаревшая ссылка на `HOT_PATH_BUDGET_KB=37` заменена на актуальную. [IC]
6. `vault/Metrics/incident-metrics.md` — запись о размере горячего пути обновлена под новый размер. Команда: `grep -A2 "hot path" vault/Metrics/incident-metrics.md` показывает актуальные цифры.

## Out of scope this period

- Workflow-файлы (deploy.md, execute.md, close.md, new.md, plan.md) — это отдельный инцидент `workflow-file-trim-grandfathered` (QUEUED, M, rank 5).
- Изменение логики проверок `test_doctrine_integrity.py` — только коррекция константы.
- `doctrine-appendix.md` — перемещение контента из doctrine.md допустимо, но не обязательно; приоритет — сокращение, а не реорганизация.

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

(будет заполнено после возврата Planning Chief)
