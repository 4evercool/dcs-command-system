<!--
IAP.md -- the Integrated Action Plan, written by the IC during /dcs-plan.
This is the ONLY document specialists execute against once approved -- the
single source of truth doctrine principle 3 insists on. Editing this file
after approval voids IAP-APPROVED automatically (hash mismatch) -- that is
deliberate, not a bug to route around.
-->

# IAP — Incident Action Plan

**Incident:** prompt-vs-schema-drift
**Type:** 1
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `203-ORG.md` · `204-TASKING/*.md` · logistics plan below

## Objectives (summary of 202)

**Goal:** Вводные Диспетчера (prompt) и возвраты агентов (return) механически валидируются на соответствие объявленной схеме в точке использования: вводная сверяется при отправке агента, возврат — при получении. Off-disk половина канала дрейфа, оставленная v0.6.14 открытой, закрыта.

**Acceptance criteria:**
1. Каждый workflow (new.md, plan.md, execute.md), формирующий вводную агенту, передаёт в ней секцию `schemas.md`, соответствующую роли этого агента. [IC]
2. Каждый workflow, принимающий возврат агента, валидирует его на соответствие объявленной схеме — отсутствие структурного JSON-блока, отсутствие обязательного поля или поле не из схемы считается deviation. [IC]
3. Четыре JSON-примера в `<command_points>` устава командира содержат поле `esg_activation` там, где его объявляет `<output_contract>` таблица.
4. `python tests/test_doctrine_integrity.py` — все проверки зелёные, без регресса. Новые проверки также зелёные.
5. Добавлена минимум одна новая механическая проверка, которая ловит: (a) workflow, ссылающийся на имя поля не из схемы (inbound); (b) агентский возврат с отсутствующими обязательными полями (outbound, на исторических артефактах).
6. Ни один существующий артефакт инцидентов не сломан новым механизмом — валидация outbound на исторических возвратах либо проходит, либо явно документирует расхождения как ожидаемые (pre-existing drift), не блокируя чтение.

**Out of scope:** Runtime-валидация через хук PreToolUse/Stop. Исправление исторических экземпляров дрейфа.

## Tactics (from the Planning Chief)

1. Внедрить inline-контракт схемы в каждый spawn-промпт workflow: вставить перечень обязательных полей из соответствующей секции schemas.md непосредственно в текст промпта, который Dispatcher передаёт агенту при spawn.
2. Добавить валидацию возврата в workflow после получения JSON от агента: проверить наличие структурного JSON-блока, обязательных полей, и отсутствие полей не из схемы. Отсутствие обязательного поля — deviation.
3. Исправить четыре JSON-примера командира — добавить поле `esg_activation` в каждый.
4. Добавить механическую проверку inbound-дрейфа (check 20): для каждого workflow, spawn'ящего агента, проверить, что все обязательные поля из схемы этого агента присутствуют в тексте workflow.
5. Добавить механическую проверку outbound-дрейфа (check 21): обойти `.dcs/incidents/*/` в поисках JSON-возвратов агентов, сверить с объявленной схемой, задокументировать найденные расхождения как informational (не failing).

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | dcs/workflows/new.md, dcs/workflows/plan.md, dcs/workflows/execute.md | agents/**, tests/**, dcs/references/**, dcs/hooks/** |
| S2 | agents/dcs-commander.md | dcs/workflows/**, tests/**, dcs/references/**, agents/dcs-{situation-analyst,ops-specialist,safety-officer,planning-chief,logistics-chief}.md |
| S3 | tests/test_doctrine_integrity.py | dcs/workflows/**, agents/**, dcs/references/**, dcs/hooks/** |

**Partition status:** disjoint — sequential execution (S1 first, then S2 ∥ S3). S3 measures S1's line counts for WORKFLOW_GRANDFATHERED_LINES ceiling updates; S2 is independent. Territories are in three separate directory trees — no write conflicts.

## Deploy / environment plan (Type 1, from the Logistics Chief)

- **Deploy path:** full — все три корня полезной нагрузки (dcs/ через robocopy, agents/dcs-*.md через Copy-Item, skills/dcs-*/ не затронуты но копируются при полном deploy). Команда: `powershell -ExecutionPolicy Bypass -File C:\DCS\install.ps1`, свидетель: `python tests/payload_check.py`.
- **Env deps:** нет новых переменных окружения, нет новых зависимостей (pip, npm). Изменения — prose и stdlib-only Python (test additions). Без изменений конфигурации (.dcs/config.json, DELEGATION.md, REGISTER.md не меняются).
- **Migration ordering:** нет миграции — zero schema changes, zero database involvement, zero service restarts. Изменения чисто файловые (prose workflow, косметика устава агента, stdlib-only test additions), развёртываются как копии файлов без ограничений порядка.
- **Rollback plan:** откат — переразвёртывание предыдущего коммита (checkout родителя merge-коммита и перезапуск install.ps1). Все изменения аддитивны (новые проверки, новый язык валидации, косметические примеры) — без деструктивных операций, без состояния БД для отмены.
- **Risks:**
  1. Hook propagation gap: если dcs/hooks/dcs_gate.py модифицирован, install.ps1 развёртывает хук в ~/.claude/dcs/hooks/ но НЕ в копию хука каждого проекта. Проекты должны перезапустить /dcs-init.
  2. Workflow line-count budget: plan.md (666) и execute.md (424) уже на потолке. S1 добавит код → оба файла пересекут ceiling. S3 должен обновить WORKFLOW_GRANDFATHERED_LINES.
  3. Test-schema coupling: новые проверки парсят schemas.md в runtime — при разработке редактирование одного без другого вызовет локальное падение теста (правильное поведение для сторожа).
  4. Agent charter glob fragility: install.ps1 копирует agents/dcs-*.md одним glob. Если glob не совпадёт с файлом, развёрнутый набор агентов будет неполным (pre-existing risk инсталлятора).

## Risks

- **Line-count ceiling:** plan.md (666, ceiling 666) и execute.md (424, ceiling 424) на потолке. S1 гарантированно пересечёт оба. S3 должен обновить WORKFLOW_GRANDFATHERED_LINES после S1. new.md (248, ceiling 250) — 2 строки запаса.
- **Check 21 informational mode:** `.dcs/incidents/` содержит задокументированный pre-existing drift. Check 21 должен классифицировать расхождения как informational, не как failures — иначе criterion 6 нарушен.
- **Commander JSON examples:** три из четырёх примеров — однострочные JSON. S2 должен проверить, что все блоки остаются валидным JSON после правки.
- **Inline-контракт дублирует schemas.md:** при будущем изменении схемы workflow нужно обновлять вручную. Принятый риск для v0.7.0 — check 20 механически ловит расхождение на merge time.
- **S1→S3 ordering:** территории disjoint, но S3 измеряет line counts, которые S1 меняет. Если запустить параллельно, S3 может прочитать старые значения и check 17 упадёт.

## Verification plan

1. `python tests/test_doctrine_integrity.py` — все проверки зелёные (включая новые check 20/21 и check 17 с обновлёнными ceiling).
2. `python tests/test_dcs_gate.py && python tests/test_dcs_intake.py` — без регресса.
3. Ручная проверка каждого workflow: grep на наличие всех обязательных полей схемы в точке spawn, grep на код валидации возврата.
4. Проверка agents/dcs-commander.md: все 4 JSON-примера содержат `esg_activation`, все парсятся json.loads.
5. Проход по reproduction path из 201-BRIEF.md: (a) grep на prompt/dispatch в тестах находит check 20; (b) grep на поля возврата в тестах находит check 21; (c) исторические экземпляры дрейфа документированы, не блокируют; (d) esg_activation есть в примерах командира.

## Deviation history (this period)

none
