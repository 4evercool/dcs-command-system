<!--
201-BRIEF.md — written by the IC from dcs-situation-analyst findings, once,
at the stem (/dcs-new). Never edited after typing is confirmed except to
append a note if a later period's assessment reveals the original blast
radius was wrong (append, don't rewrite — 214-LOG.md is the append-only
one, but this file's Symptom/Evidence should stay a true record of what was
known at intake).
-->

# 201 — Incident Brief

**Incident:** prompt-vs-schema-drift
**Opened:** 2026-07-29
**Type:** 1

## Symptom

Диспетчер DCS при формировании вводной (prompt) подчинённому агенту называет
поля, отсутствующие в объявленной схеме возврата этого агента, — inbound-дрейф.
Агент при возврате отдаёт форму, не соответствующую контракту его устава, —
outbound-дрейф. Оба направления невидимы сторожу над деревом: вводная — не файл,
возврат — не файл. On-disk половина (формат контрактов, проверки 18/19) закрыта
в v0.6.14 (d23111e). Off-disk половина — валидация вводных при отправке и
возвратов при приёмке — остаётся определяющим механизмом версии 0.7.0.

## Evidence

### Inbound: Диспетчер использует имена полей не из схемы

- `checks_run` вместо `checked` — промпт Диспетчера офицеру Safety, зафиксирован
  в трёх из четырёх артефактов SAFETY.md: `halt-loop-unbounded/SAFETY.md:52`,
  `hot-path-budget-eol-sensitivity/SAFETY.md:24`,
  `doctrine-hot-path-trim/SAFETY.md:16`. Источник:
  `schema-citation-guard/201-BRIEF.md:151-156` и
  `schemas-md-trim/SAFETY.md:73-79` (офицер сам зафиксировал расхождение).
- `findings[]` вместо `evidence[]` — промпт Диспетчера обоим situation analyst'ам
  в стеме schema-citation-guard. Источник:
  `schema-citation-guard/201-BRIEF.md:158-162`.
- `open_questions` затребован от situation analyst — поле есть в схеме #6
  (commander, `typing`) но отсутствует в #1 (analyst). Тот же стем. Источник:
  `schema-citation-guard/201-BRIEF.md:159`.
- Частота: 5 inbound экземпляров за один инцидент (schema-citation-guard), включая
  2 в собственных вводных той же сессии. Источник:
  `schema-citation-guard/AAR.md:127-130`.

### Outbound: агент возвращает форму не по контракту

- S1-FIX1 (schema-citation-guard) вернулся без структурного JSON-блока — нет
  `status`, `files_touched`, `deviation`. Последствие: границу территории
  устанавливал офицер по `find -newermt`, а не исполнитель. Источник:
  `vault/Backlog.md:559-598` (item 14) и `schema-citation-guard/AAR.md:158-163`.
- S2 (schema-citation-guard) доложил семантическое расхождение в `evidence`, тогда
  как задание требовало `status: "deviation"`. Источник:
  `vault/Backlog.md:566-571` (item 14).
- S1 (schemas-contract-format) вернулся структурированной прозой без литерального
  JSON-блока схемы #4. Источник:
  `schemas-contract-format/AAR.md:71-73`.

### On-disk: примеры командира расходятся с собственной контрактной таблицей

- `agents/dcs-commander.md` — четыре JSON-примера в `<command_points>` (строки
  29-31 typing, 40-42 iap_review, 51-53 deviation, 80-82 verdict_disposition) не
  содержат поле `esg_activation`. Таблица `output_contract` (строка 138)
  объявляет `esg_activation` как «rides with any decision».
  `schemas.md:122-126` — пример deviation *с* `esg_activation` присутствует в
  схеме, но отсутствует в уставе командира. Расхождение зафиксировано ещё в
  schema-citation-guard (`201-BRIEF.md:120-121`), не исправлено до сих пор.

### Механический сторож отсутствует

- Проверка 18 (`test_doctrine_integrity.py`) сверяет поля схемы с уставами —
  направление схема→устав, on-disk. Docstring явно говорит: «deliberately NOT
  checked» про обратное направление.
- Проверка 19 разбирает `<output_contract>` JSON-блоки — on-disk.
- Ни та, ни другая не видят ни промпт Диспетчера, ни возврат агента. Источник:
  `vault/Backlog.md:588-591` («a prompt is not a file, and neither is a return»).
- Фактический контракт недетерминирован: ни один устав не `@`-включает
  `schemas.md`; `new.md` шаг 3 схему субагенту не передаёт. Контракт есть
  «перечень устава плюс схема как арбитр, разрешаемый решением агента на бегу».
  Источник: `schema-citation-guard/201-BRIEF.md:164-168`.

### On-disk состояние (отправная точка)

- `python tests/test_doctrine_integrity.py` → 115/115 passed (HEAD cf76ce7).
  Все 6 уставов несут `<output_contract>` блоки. Все разделы схемы имеют
  `Returned by` строки. `advisories` восстановлен в контракте Safety Officer.

## Reproduction path

1. Убедиться, что on-disk чисто: `python tests/test_doctrine_integrity.py` → 115/115.
2. Убедиться, что inbound не проверяется: `grep -n 'prompt\|dispatch' tests/test_doctrine_integrity.py` — механики валидации вводных нет.
3. Убедиться, что outbound не проверяется: `grep -rn 'status.*done\|files_touched\|deviation' tests/` — поля возврата упоминаются только в данных фикстур, не в коде сторожа.
4. Найти исторические экземпляры inbound-дрейфа: `grep -rn 'checks_run' .dcs/incidents/` → три SAFETY.md с именем поля, отсутствующим в любой схеме.
5. Найти исторические экземпляры outbound-дрейфа: `grep -rn 'find -newermt' .dcs/incidents/` → SAFETY.md с обходным путём определения территории.
6. Сверить примеры командира с таблицей контракта: `grep -n 'esg_activation' agents/dcs-commander.md` — поле есть только в `output_contract`, отсутствует во всех четырёх JSON-примерах `<command_points>`.

## Blast radius (best guess at intake)

- `dcs/references/schemas.md` — центральный артефакт: схема, с которой всё сверяется
- `agents/dcs-commander.md` — примеры в `<command_points>` (esg_activation)
- `agents/dcs-situation-analyst.md` — устав аналитика (контракт, вводная)
- `agents/dcs-ops-specialist.md` — устав специалиста (контракт, вводная)
- `agents/dcs-safety-officer.md` — устав офицера (контракт, вводная)
- `agents/dcs-planning-chief.md` — устав планировщика (контракт, вводная)
- `agents/dcs-logistics-chief.md` — устав логиста (контракт, вводная)
- `dcs/workflows/new.md` — шаг 3: формирование вводной аналитикам
- `dcs/workflows/plan.md` — формирование вводной планировщику
- `dcs/workflows/execute.md` — формирование вводной специалистам и офицеру
- `tests/test_doctrine_integrity.py` — добавление inbound/outbound проверок
- `dcs/hooks/` — возможный новый хук (PreToolUse/Stop) для runtime-валидации

## Prior art

- **schema-citation-guard** (2026-07-26, Тип 1) — первый систематический аудит:
  обнаружил 5 inbound экземпляров за один инцидент, отсутствие `esg_activation` в
  примерах командира, отсутствие `advisories` в контракте офицера. Породил 4
  строки реестра, включая данную (prompt-vs-schema-drift, rank 6).
- **schemas-contract-format** (2026-07-29, Тип 1, d23111e) — исправил on-disk
  половину: машиночитаемый формат контрактов, проверки 18/19. Осознанно оставил
  off-disk половину для prompt-vs-schema-drift. Записал улику о возврате S1 без
  JSON-блока.
- **vault/Backlog.md item 14** (Return-form drift) — два экземпляра расхождения
  возврата за один период, с конкретным последствием (территорию устанавливал
  проверяющий по `find -newermt`).
- **vault/Decisions/v0.7-scope.md** — решение Owner: метка 0.7.0 принадлежит
  механизму валидации вводных при dispatch и возвратов при получении.
- **safety-halt-functional-scope** (2026-07-26, 6a57b97) — инцидент, добавивший
  `advisories` в схему #5, но не обновивший контракт офицера (дрейф, исправленный
  только в d23111e).

## Type + rationale

**Proposed type:** 1
**Rationale:** off-disk runtime-валидация вводных Диспетчера и возвратов агентов — новый сквозной архитектурный механизм, затрагивающий 6 уставов агентов, 3 dispatch workflow, schemas.md и файлы механизма принуждения (tests, hooks). Определён как класс механизмов версии 0.7.0 решением v0.7-scope, принятым на одиннадцатой /dcs-esg. (IC=dcs-commander, Fable)
**Owner confirmation:** подтверждён как Type 1

## Intake source

`.dcs/esg/REGISTER.md` — строка prompt-vs-schema-drift (rank 6, приоритет H,
повышен на одиннадцатой /dcs-esg, v0.7-scope).
