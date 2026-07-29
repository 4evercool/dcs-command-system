# AAR — After Action Review

**Incident:** prompt-vs-schema-drift
**Type:** 1
**Opened:** 2026-07-29
**Closed:** 2026-07-29
**Periods:** 1
**Merge commit:** `6d3d08e` (pending — not yet merged at time of writing; see step 5a below)

## Outcome

**Goal:** Вводные Диспетчера (prompt) и возвраты агентов (return) механически валидируются на соответствие объявленной схеме в точке использования — inbound при отправке, outbound при получении.

**Result:** Все 6 критериев приёмки выполнены, проверены Safety Officer независимо (0 рефутаций, 0 advisories). 120/120 тестов, 100/100 gate, 10/10 intake.

**Delivered:**
- Три workflow-файла (new.md, plan.md, execute.md) теперь передают inline-контракт схемы в каждый spawn-промпт агента и валидируют каждый возврат на соответствие схеме (критерии 1-2)
- Четыре JSON-примера командира теперь содержат поле `esg_activation` (критерий 3)
- Новые проверки: check 20 (inbound field-presence guard, 5 случаев) и check 21 (outbound missing-required-fields guard, informational mode для исторических артефактов) (критерии 5-6)
- WORKFLOW_GRANDFATHERED_LINES обновлены: new.md 260, plan.md 687, execute.md 450 (от criteria 4)

## What worked

- **Inline-контракт в workflow-прозе** — самый простой и прямой способ закрыть inbound-дрейф: поле схемы появляется в тексте workflow как backtick-терм, и check 20 механически сверяет его наличие. Никакого нового механизма не потребовалось.
- **Валидация возврата как prose-инструкция Диспетчеру** — вместо runtime-хука (который невозможен в сегодняшнем DCS), инструкция в workflow предписывает Диспетчеру проверить возврат агента перед тем, как писать артефакты на диск. Эффективно для предотвращения будущего outbound-дрейфа.
- **Check 21 в informational mode** — правильное решение для исторических артефактов: дрейф задокументирован, но не блокирует suite. 2 finding'а (отсутствие `checked` в старых SAFETY.md/AAR.md) — это pre-existing drift до появления поля `checked` в схеме #5 (v0.6.5, 6a57b97).

## Lessons

1. **Citation anchors чувствительны к переформатированию.** S1 изменил формат ссылок `schemas.md #N` (убрал префикс `references/`, заменил запятую на скобку), и проверка 13 перестала находить полные названия секций в пределах окна. S1-FIX восстановил anchors добавлением краткого названия секции сразу после номера. Урок: любой edit, меняющий текст рядом с `schemas.md #N`, должен проверять `grep citation` в тестах.

2. **Line-count ceilings достигаются быстрее, чем ожидается.** new.md был на 248/250 (2 строки запаса) — добавление 5-строчного контракта и 3-строчной валидации дало +7 строк (255). plan.md +16, execute.md +21. Все три файла пересекли потолки. S3 должен обновлять WORKFLOW_GRANDFATHERED_LINES после каждого S1 — sequential execution оказался правильным решением.

3. **Первая версия S1 упала на API-ошибке, но частичные правки сохранились на диске.** Второй spawn обнаружил, что new.md и plan.md уже содержат контракты — и дополнил только execute.md. Частичный fs-эффект упавшего агента — это и риск (незавершённая работа выглядит как завершённая), и экономия (не пришлось переделывать). Check 20 механически подтвердил, что все поля на месте.

## Deviation history

Одна неформальная девиация: S1 потребовал fix-таскинг (S1-FIX) для восстановления citation anchors, сломанных при добавлении inline-контрактов. Не было зафиксировано как `status: "deviation"` — S1-FIX был запущен IC напрямую после обнаружения 3 красных тестов на этапе сбора returns.

## Safety Officer's final verdict (verbatim from SAFETY.md)

```json
{
  "verdict": "pass",
  "refutations": [],
  "advisories": [],
  "checked": [
    "120/120 tests passed",
    "100/100 gate, 10/10 intake — no regression",
    "5 files modified exactly matching specialists' claims",
    "All schema contracts verified in all 3 workflows",
    "All 4 commander JSON examples parse OK with esg_activation",
    "Check 20: 5/5 PASS, Check 21: 2 informational findings",
    "WORKFLOW_GRANDFATHERED_LINES verified at measured values"
  ]
}
```

## Owner-UAT

Не требовался IAP — критерии были чисто механическими (тесты + grep). Утверждение IAP Owner'ом на шаге 6b покрыло приёмку.

## Deploy status

Не развёрнуто. Строка реестра — `MERGED (deploy pending)`. Развёртывание — через `/dcs-deploy`: `powershell -ExecutionPolicy Bypass -File C:\DCS\install.ps1`, свидетель `python tests/payload_check.py`.

## Memory routing

Уроки записаны в `vault/Post-mortems/prompt-vs-schema-drift.md` согласно протоколу, описанному в `CLAUDE.md` ("write to it after").
