# 201 — Incident Brief

**Incident:** worktree-path-propagation
**Opened:** 2026-07-30
**Type:** 3

## Symptom

DCS ops-специалисты (порождаемые /dcs-execute) редактируют файлы в основном
checkout (C:\DCS), а не в worktree инцидента (C:\DCS-wt\<slug>). Owner
вынужден вручную копировать изменения из основного checkout в worktree и
коммитить там. Дефект воспроизводится при каждом инциденте, где сессия IC
находится в основном checkout.

## Evidence

- agents/dcs-ops-specialist.md:30 — специалист получает «project root path»
  без какого-либо упоминания worktree; слово «worktree» отсутствует в файле
  целиком
- dcs/workflows/execute.md:109-115 — шаг 4 (Fan out Ops Specialists) не
  говорит IC передавать worktree путь; специалисту передаются только
  204-TASKING и выдержка IAP
- dcs/workflows/execute.md:129-132 — даже в worktree-isolated режиме
  инструкция «set up the worktree (e.g. git worktree add) before spawning
  it» не говорит ПЕРЕДАТЬ путь специалисту
- dcs/templates/204-TASKING.md — шаблон (46 строк) не содержит поля
  worktree_root или Project root
- docs/spec-v0.3-parallel.md:93-95 — предположение «Specialists spawned from
  a worktree session inherit it naturally (their edits are absolute paths
  under the worktree)» не выполняется, когда сессия IC в основном checkout
- dcs/hooks/dcs_gate.py:281-295 — find_project_root() разрешает .dcs/ от
  целевого файла; правка в C:\DCS находит основной .dcs/ без ACTIVE (ACTIVE
  только в worktree) и пропускается молча
- .dcs/incidents/2026-07-30-token-economy-advisory-fixes/AAR.md:34 — прямое
  подтверждение: «Specialists were given C:\dcs (main checkout) as project
  root, causing edits to land in the main checkout instead of the worktree
  (C:\DCS-wt\token-economy-advisory-fixes). The Dispatcher copied files into
  the worktree before committing»
- vault/Meta/building-dcs-lessons.md:1016-1050 (урок #25) — тот же дефект
  задокументирован 2026-07-30, предписанное исправление («the Dispatcher
  must pass the worktree path as the project root in every specialist's
  tasking prompt») не применено к коду
- dcs/workflows/close.md:147-149 — v0.3.3 field lesson: «a session in the
  field routed vault lessons into the main checkout's copies by reflex and
  had to revert» — тот же класс ошибки (запись не в тот checkout)

## Reproduction path

1. Открыть Type 3 инцидент через /dcs-new из сессии в C:\DCS
2. Worktree создаётся в C:\DCS-wt\<slug>, но сессия остаётся в C:\DCS
3. Пройти /dcs-plan, затем /dcs-execute
4. При спавне специалиста IC передаёт C:\DCS как project root (поведение
   по умолчанию — ни один workflow не говорит иного)
5. Специалист редактирует файлы в C:\DCS; git status в worktree пуст
6. Подтверждено в AAR token-economy-advisory-fixes

## Blast radius (best guess at intake)

- agents/dcs-ops-specialist.md — основной файл: добавить worktree_root в inputs
- dcs/workflows/execute.md — шаг 4: добавить инструкцию передавать worktree путь
- dcs/templates/204-TASKING.md — добавить поле worktree_root
- agents/dcs-safety-officer.md, agents/dcs-situation-analyst.md,
  agents/dcs-planning-chief.md, agents/dcs-logistics-chief.md — все
  получают «project root path», для согласованности тоже добавить
  worktree_root (но они read-only, поэтому менее критично)
- dcs/workflows/new.md, dcs/workflows/plan.md — шаги спавна аналитиков и
  chief'ов, аналогичная проблема с project root
- docs/spec-v0.3-parallel.md — исправить неверное предположение о
  наследовании worktree (строки 93-95)

## Prior art

- vault/Meta/building-dcs-lessons.md, урок #25 (2026-07-30): тот же дефект
  в инциденте token-economy-advisory-fixes. Предписанное исправление: «the
  Dispatcher must pass the worktree path as the project root in every
  specialist's tasking prompt» — не применено
- dcs/workflows/close.md:147-149 — v0.3.3 field lesson о том же классе
  ошибки (запись в основной checkout «by reflex»)

## Type + rationale

**Proposed type:** 3
**Rationale:** Well-scoped bug fix (missing worktree path parameter in
dispatch prompt) touching 3-4 files with a clear root cause, additive changes
following existing prompt-template patterns, no architectural change or
contract modification. (IC=dcs-commander, opus — fable unavailable at this
attempt)
**Owner confirmation:** confirmed as proposed

## Intake source

Owner chat report
