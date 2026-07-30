# 202 — Objectives (Operational Period 1)

**Incident:** worktree-path-propagation
**Period:** 1

## Goal

Обеспечить, что DCS ops-специалисты ВСЕГДА редактируют файлы в worktree
инцидента, а не в основном checkout. Механизм: добавить параметр
`worktree_root` в контракт специалиста и инструкцию по его передаче в
execute.md, чтобы разрыв между созданием worktree (new.md) и спавном
специалиста (execute.md) был закрыт.

## Acceptance criteria (the Definition of Done)

1. `agents/dcs-ops-specialist.md` — секция `<inputs>` содержит
   `worktree_root` (опциональный — если не передан, используется
   `project_root`); секция `<process>` требует разрешать territory-глобы
   относительно `worktree_root`, а не `project_root`
2. `dcs/workflows/execute.md` шаг 4 — для каждого специалиста (не только
   worktree-isolated) инструкция явно требует передавать `worktree_root`
   (путь к worktree инцидента) в промпт специалиста; путь вычисляется
   из `git worktree list --porcelain` по имени ветки `dcs/<slug>`
3. `dcs/templates/204-TASKING.md` — шаблон содержит поле `worktree_root`
   (опциональное, с пометкой «если не указан — используется project root»)
4. `python tests/test_dcs_gate.py && python tests/test_dcs_intake.py && python tests/test_doctrine_integrity.py` — все тесты проходят [IC]

## Out of scope this period

- Другие agent charters (dcs-safety-officer, dcs-situation-analyst,
  dcs-planning-chief, dcs-logistics-chief) — они read-only, для них
  worktree путь менее критичен; завести отдельным инцидентом при
  необходимости
- Исправление docs/spec-v0.3-parallel.md (неверное предположение о
  «наследовании» worktree) — prose fix, не влияет на поведение
- Механическое принуждение на уровне gate hook — гейт не имеет доступа
  к контексту агента; это остаётся процедурной гарантией, выполняемой
  IC при спавне

## Chief feedback

(заполняется после spawn Planning Chief)
