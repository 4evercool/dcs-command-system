<!--
202-OBJECTIVES.md -- written by the IC together with the Owner, at the
start of EACH operational period (/dcs-plan). Re-drafted (new file content,
same filename) each time the incident re-enters the P-loop for another
period -- the prior period's 202 is preserved in 214-LOG.md's phase-
transition history and, once complete, in AAR.md's summary, not in this
file itself.
-->

# 202 — Objectives (Operational Period 1)

**Incident:** prompt-vs-schema-drift
**Period:** 1

## Goal

Вводные Диспетчера (prompt) и возвраты агентов (return) механически
валидируются на соответствие объявленной схеме в точке использования:
вводная сверяется при отправке агента, возврат — при получении. Off-disk
половина канала дрейфа, оставленная v0.6.14 открытой, закрыта.

## Acceptance criteria (the Definition of Done)

1. Каждый workflow (new.md, plan.md, execute.md), формирующий вводную
   агенту, передаёт в ней секцию `schemas.md`, соответствующую роли этого
   агента — агент видит контракт, которому должен соответствовать его
   возврат. [IC]

2. Каждый workflow, принимающий возврат агента, валидирует его на
   соответствие объявленной схеме — отсутствие структурного JSON-блока,
   отсутствие обязательного поля или поле не из схемы считается
   отклонением (deviation), а не молча принимается. [IC]

3. Четыре JSON-примера в `<command_points>` устава командира
   (`agents/dcs-commander.md`) содержат поле `esg_activation` там, где
   его объявляет `<output_contract>` таблица — расхождение,
   зафиксированное ещё в schema-citation-guard, устранено.

4. `python tests/test_doctrine_integrity.py` — все проверки зелёные
   (115/115 сегодня, без регресса). Новые проверки, добавленные этим
   инцидентом, также зелёные.

5. Добавлена как минимум одна новая механическая проверка (в
   `tests/test_doctrine_integrity.py` или в `dcs/hooks/`), которая
   ловит: (a) workflow, ссылающийся на имя поля не из схемы (inbound);
   (b) агентский возврат с отсутствующими обязательными полями
   (outbound, на исторических артефактах `.dcs/incidents/`).

6. Ни один существующий артефакт инцидентов (`.dcs/incidents/*/SAFETY.md`,
   `214-LOG.md`, etc.) не сломан новым механизмом — валидация outbound
   на исторических возвратах либо проходит, либо явно документирует
   расхождения как ожидаемые (pre-existing drift), не блокируя чтение.

## Out of scope this period

- Runtime-валидация через хук PreToolUse/Stop (требует механизма,
  которого нет в сегодняшнем DCS — хук не видит текст промпта до
  отправки агенту и не видит возврат агента до записи на диск).
  Механизм этого периода — workflow-уровневая: валидация внутри процесса
  workflow, не перехват на уровне harness.
- Исправление всех исторических экземпляров дрейфа (checks_run, findings[]
  и т.д.) в существующих артефактах инцидентов — они остаются
  свидетельствами, новый механизм предотвращает будущие.

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

{{objectives_feedback from the chief-plan schema -- if the Chief flagged a
criterion as untestable, note the resolution here: revised criterion, or
Owner accepted the risk}}
