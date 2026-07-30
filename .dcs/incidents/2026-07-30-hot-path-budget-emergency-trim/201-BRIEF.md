<!--
201-BRIEF.md — written by the IC from dcs-situation-analyst findings, once,
at the stem (/dcs-new). Never edited after typing is confirmed except to
append a note if a later period's assessment reveals the original blast
radius was wrong (append, don't rewrite — 214-LOG.md is the append-only
one, but this file's Symptom/Evidence should stay a true record of what was
known at intake).
-->

# 201 — Incident Brief

**Incident:** 2026-07-30-hot-path-budget-emergency-trim
**Opened:** 2026-07-30
**Type:** 3

## Symptom

Строка регистра ESG `hot-path-budget-emergency-trim` (открыта на 13-м ESG 2026-07-30) утверждает нарушение бюджета горячего пути: «38 419 B against 37 888 B ceiling (HOT_PATH_BUDGET_KB=37) … budget violated». Это утверждение ошибочно — константа `HOT_PATH_BUDGET_KB` была поднята с 37 до 38 инцидентом `worktree-removal-self-conflict` (слит 2026-07-29, за день до ESG). Фактический запас: 38 419 байт при бюджете 38 912 байт = **493 байта**. Guard зелёный (122/122 passed). Однако запас критически мал — меньше одного абзаца прозы. Следующее изменение `doctrine.md` или `schemas.md` более чем на 493 байта зажжёт проверку слияния красным. Ситуация с workflow-файлами ещё острее: `deploy.md` (282/282) и `execute.md` (450/450) имеют нулевой запас, но это отдельный дефект, уже зарегистрированный как `workflow-file-trim-grandfathered` (QUEUED, M, rank 8).

## Evidence

- `tests/test_doctrine_integrity.py:184` — `HOT_PATH_BUDGET_KB = 38`; проверка 7 (строки 305-314) сравнивает нормализованную сумму `doctrine.md + schemas.md` с `HOT_PATH_BUDGET_KB * 1024`. Источник: чтение кода.
- Измерение горячего пути: `doctrine.md` = 24 623 B, `schemas.md` = 13 796 B, итого 38 419 B при бюджете 38 912 B, запас 493 B. Команда: `python -c "d=open('dcs/references/doctrine.md','rb').read().replace(b'\r\n',b'\n'); s=open('dcs/references/schemas.md','rb').read().replace(b'\r\n',b'\n'); print(len(d)+len(s), 'of', 38*1024)"`. Источник: прямое измерение.
- `.dcs/esg/REGISTER.md:139` — строка регистра ссылается на `HOT_PATH_BUDGET_KB=37` и заявляет дефицит -531 B. Константа была поднята до 38 инцидентом `worktree-removal-self-conflict` (AAR: «S2 deviation: hot-path budget exceeded … Commander: amend_tasking → S1 bump HOT_PATH_BUDGET_KB 37→38»), слитым 2026-07-29. Источник: чтение регистра + AAR.
- `tests/test_doctrine_integrity.py` check 17 + `WORKFLOW_GRANDFATHERED_LINES`: `deploy.md` = 282/282 (ноль запаса), `execute.md` = 450/450 (ноль запаса), `close.md` = 282/283 (1 строка), `new.md` = 255/260 (5 строк), `plan.md` = 682/687 (5 строк). Источник: чтение кода + `wc -l`.
- `vault/Metrics/incident-metrics.md:88-99` — полная история размера hot path от v0.5.0 diet (31 723 B) до worktree-removal-self-conflict (38 419 B при бюджете 38 kB). Источник: vault.

## Reproduction path

1. `cd C:\dcs`
2. Измерить горячий путь: `python -c "d=open('dcs/references/doctrine.md','rb').read().replace(b'\r\n',b'\n'); s=open('dcs/references/schemas.md','rb').read().replace(b'\r\n',b'\n'); print(f'hot-path: {len(d)+len(s)} bytes of {38*1024} budget, headroom={38*1024-(len(d)+len(s))} bytes')"` → `hot-path: 38419 bytes of 38912 budget, headroom=493 bytes`
3. Измерить строки workflow: `wc -l dcs/workflows/*.md` → `deploy.md=282, execute.md=450, close.md=282, new.md=255, plan.md=682`
4. `python tests/test_doctrine_integrity.py` → 122/122 passed (check 7 и check 17 зелёные)
5. Вывод: нарушения нет, но запас опасно мал

## Blast radius (best guess at intake)

- `dcs/references/doctrine.md` — основной кандидат на обрезку (24 623 B, ~60% горячего пути)
- `dcs/references/schemas.md` — вторичный кандидат (13 796 B, ~35% горячего пути)
- `tests/test_doctrine_integrity.py` — возможно, коррекция константы `HOT_PATH_BUDGET_KB` после обрезки (ratchet act)
- `CLAUDE.md` — может ссылаться на устаревшие цифры бюджета
- `.dcs/esg/REGISTER.md` — исправить устаревшую ссылку на `HOT_PATH_BUDGET_KB=37` → `38`
- `vault/Metrics/incident-metrics.md` — обновить метрики размера горячего пути

## Prior art

Пять предшествующих инцидентов касались этого же бюджетного механизма:

1. **doctrine-hot-path-trim** (2026-07-25, Type 3) — перенёс provenance из `doctrine.md` в `doctrine-appendix.md`, обрезал 4 889 B, переустановил ratchet 42→38 kB. Два Safety halt из-за параллельного роста `schemas.md`.
2. **hot-path-budget-eol-sensitivity** (2026-07-25, Type 1) — нормализовал измерение (CRLF→LF), чтобы бюджет не зависел от платформы.
3. **schemas-md-trim** (2026-07-26, Type 3) — обрезал `schemas.md` на 2 317 B, переустановил ratchet 38→37 kB. Модель pay-as-you-go: удалил избыточный абзац, чтобы оплатить собственные таблицы.
4. **workflow-budget-enforcement** (2026-07-28, Type 1) — добавил проверку 17 (строки workflow), grandfathering для четырёх файлов. Явно отложил обрезку grandfathered файлов → `workflow-file-trim-grandfathered` (QUEUED).
5. **worktree-removal-self-conflict** (2026-07-29) — S2 deviation поднял `HOT_PATH_BUDGET_KB` 37→38.

Общий шаблон (vault §24): бюджет, заявленный только в прозе, дрейфует. Механическая проверка держит, но запас сейчас нулевой для двух файлов. Предыдущие обрезки доказали, что направленные сокращения работают: `doctrine-hot-path-trim` убрал provenance, `schemas-md-trim` убрал избыточный абзац.

**Decomposition note:** Workflow-часть (deploy.md, execute.md, close.md, new.md, plan.md) — это отдельный дефект, уже зарегистрированный как `workflow-file-trim-grandfathered` (QUEUED, M, rank 8). Данный инцидент занимается только горячим путём.

## Type + rationale

**Proposed type:** 3
**Rationale:** Проблема понятна, паттерн сокращения прозы отработан пятью предшествующими инцидентами (doctrine-hot-path-trim Type 3, schemas-md-trim Type 3), набор файлов ограничен (doctrine.md, schemas.md, test_doctrine_integrity.py, REGISTER.md, vault), архитектурных изменений нет — только ratchet-действие константы, уже выполнявшееся в Type 3.
**Owner confirmation:** confirmed as proposed (Type 3)

## Intake source (for /dcs-close to route back to)

ESG register row `hot-path-budget-emergency-trim` (13-е ESG, 2026-07-30)
