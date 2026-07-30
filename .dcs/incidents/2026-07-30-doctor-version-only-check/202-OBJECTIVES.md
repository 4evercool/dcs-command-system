# 202 — Objectives (Operational Period 1)

**Incident:** doctor-version-only-check
**Period:** 1

## Goal

`dcs doctor` проверяет установленную копию DCS по содержимому (вызовом `tests/payload_check.py` или эквивалентной логики сравнения sha256), а не по строковому равенству номеров версий. Команда `dcs bump <version>` атомарно редактирует `dcs/VERSION` и `package.json` в одной операции, устраняя риск перекодировки (UTF-8 BOM) при ручном редактировании через PowerShell.

## Acceptance criteria (the Definition of Done)

1. `dcs doctor` выполняет content-aware проверку: сравнивает установленные файлы payload с эталонными из репозитория (через `tests/payload_check.py` или эквивалентную логику) и сообщает о расхождениях, а не только о различии строк версий.
2. `dcs doctor` без аргументов (или с аргументами, не затрагивающими новый режим) сохраняет обратную совместимость — существующее поведение `doctor` не ломается.
3. `dcs bump <version>` атомарно обновляет `dcs/VERSION` и `package.json` (поле `version`) — оба файла меняются в одной операции, и ни один не остаётся в рассогласованном состоянии при ошибке.
4. `dcs bump` без аргументов показывает текущую версию и инструкцию по использованию.
5. `docs/publishing.md` и `README.md` обновлены: `dcs doctor` описан как content-aware проверка, `dcs bump` задокументирован как способ смены версии.
6. Все существующие тесты проходят: `npm test` — зелёный. [IC]

## Out of scope this period

- Изолированный запуск `test_doctrine_integrity.py` только для проверки версий (check 1) — это отдельная задача, не входящая в данный инцидент.
- Публикация пакета (`npm publish`) — остаётся отдельной операцией Owner.

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

{{objectives_feedback}}
