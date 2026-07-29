# AAR — After Action Report

**Incident:** worktree-path-propagation
**Type:** 3
**Opened:** 2026-07-30
**Closed:** 2026-07-30
**Operational periods:** 1

## Outcome

Все четыре критерия приёмки выполнены:

1. `agents/dcs-ops-specialist.md` — `worktree_root` добавлен в `<inputs>` как опциональный абсолютный путь (строка 31), правило разрешения territory/forbidden глобов относительно `worktree_root` добавлено в `<process>` шаг 3 (строки 47-49), с fallback на `project_root` при отсутствии
2. `dcs/workflows/execute.md` шаг 4 — инструкция вычисления `worktree_root` из `git worktree list --porcelain` добавлена (строки 117-119), с явным правилом выбора нужного worktree по имени ветки `refs/heads/dcs/<slug>` (исправлено по advisory Safety Officer)
3. `dcs/templates/204-TASKING.md` — секция `## Worktree root` с плейсхолдером `{{worktree_root}}` добавлена (строки 30-32), между Forbidden zones и Evidence required
4. Тесты: 100/100 + 10/10 + 122/122 — все зелёные (проверено Safety Officer независимо)

Цель достигнута: ops-специалисты при следующем инциденте получат `worktree_root` в задании, а чартер специалиста предписывает разрешать territory-глобы относительно него.

## What worked

- Разбиение на трёх специалистов по одному критерию на каждого — чистое, без пересечений, каждый закрыл ровно свой файл
- Параллельный спавн — все три специалиста отработали независимо, без отклонений
- Safety Officer обнаружил реальную неоднозначность в execute.md (выбор worktree при нескольких в `git worktree list --porcelain`), исправленную до закрытия — advisory сработал как задумано, предотвратив ambiguity в production

## Lessons

- **`git worktree list --porcelain` требует явного правила выбора.** Формулировка «the worktree line is the absolute path» неоднозначна при нескольких worktree. Правильная: «match the branch line `refs/heads/dcs/<slug>`, then take the preceding `worktree` line». Уже внесено в execute.md.
- **execute.md на пределе строк (450/450).** Любое следующее изменение execute.md потребует либо сокращения существующего текста, либо повышения потолка. Это не doctrinal change, а maintenance note — записано в vault.

## Deviations this incident

Одно отклонение на фазе планирования: Commander дважды отклонил IAP (REJECT) — первый раз из-за неверного прочтения плана (дублирование schema-contract работы), второй раз из-за чтения 202-OBJECTIVES.md из основного checkout вместо worktree. Третья попытка — ACCEPT. Ирония в том, что второй REJECT был вызван ровно тем дефектом, который этот инцидент исправляет.

На фазе выполнения отклонений не было: все три специалиста — `done`, Safety Officer — `pass`.

## Memory routing

- **vault/Meta/building-dcs-lessons.md** — урок #25 обновлён: дефект исправлен, указан коммит `16e4307`
- Других записей не требуется: doctrinal changes нет, новый behavioural pattern не выявлен (исправление — аддитивное, существующих правил не меняет)

## Intake source closure

Ad hoc (Owner chat report) — внешней ссылки нет, закрывать нечего.

## Safety Officer's final verdict (verbatim, from SAFETY.md)

```json
{
  "verdict": "pass",
  "refutations": [],
  "advisories": [
    {
      "finding": "execute.md line 117 says 'the worktree line is the absolute path' but git worktree list --porcelain can produce multiple worktree lines. In this repo there are two worktrees (main at C:/DCS and the incident at C:/DCS-wt/worktree-path-propagation). Without specifying how to select the right one — by matching the branch line to refs/heads/dcs/<slug>, or by matching the worktree line to the current directory — the instruction is formally ambiguous.",
      "fix": "Append to line 118: 'Match the branch line refs/heads/dcs/<slug> to the slug, then take the preceding worktree line for that entry.'"
    }
  ],
  "checked": [
    "git diff --stat: confirmed only 3 files touched",
    "Full unified diff: 12 insertions, 1 deletion across 3 files",
    "tests/test_dcs_gate.py: 100/100 passed",
    "tests/test_dcs_intake.py: 10/10 passed",
    "tests/test_doctrine_integrity.py: 122/122 passed",
    "grep -rn 'worktree_root': confirmed at least one match in each target file",
    "wc -l dcs/workflows/execute.md: 449, under 450 ceiling",
    "grep 'git worktree list --porcelain' execute.md: confirmed",
    "Manual read agents/dcs-ops-specialist.md: inputs + process confirmed",
    "Manual read dcs/templates/204-TASKING.md: ## Worktree root section confirmed",
    "Manual read dcs/workflows/execute.md: computation + pass-to-specialist confirmed",
    "No BOM, CRLF, or NUL bytes",
    "No principle-15 durable claims added"
  ]
}
```
