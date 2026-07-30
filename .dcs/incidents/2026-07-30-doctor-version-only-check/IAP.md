# IAP — Incident Action Plan

**Incident:** doctor-version-only-check
**Period:** 1
**Type:** 3

## Linked artifacts

- [202-OBJECTIVES.md](202-OBJECTIVES.md)
- 203-ORG.md — skipped (default Type 3 activation: IC + Planning Chief + 2 specialists, plain parallel)
- [204-TASKING/S1.md](204-TASKING/S1.md) — `bin/dcs.js`: content-aware `doctor()` + `dcs bump <version>`
- [204-TASKING/S2.md](204-TASKING/S2.md) — `docs/publishing.md`, `README.md`: обновление документации

## Partition table

| Tasking | Territory | Forbidden | Execution |
|---------|-----------|-----------|-----------|
| S1 | `bin/dcs.js` | `docs/**`, `dcs/**`, `tests/**`, `agents/**`, `skills/**` | parallel |
| S2 | `docs/publishing.md`, `README.md` | `bin/**`, `dcs/**`, `tests/**`, `agents/**`, `skills/**` | parallel |

**Partition status:** disjoint — территории не пересекаются. S1 и S2 могут выполняться параллельно.

## Tactics

1. **doctor() content-aware:** заменить строковое сравнение `dcs/VERSION` на вызов `tests/payload_check.py` через `spawnSync('python', [...])`. Ключи `--repo <PKG_ROOT> --installed <CLAUDE_DIR>`. Маппинг exit-кодов: 0 → content identical, 3 → identical + stale extras (warning), 1 → список differing/repo-only файлов + предложение переустановки, 2 → env error — fallback на строковое сравнение как degraded mode. Проверка Python остаётся.
2. **bump <version>:** новая команда в switch/case. Без аргументов — вывод `pkgVersion()` и usage. С аргументом: валидация semver → запись `package.json` (parse → замена поля version → JSON.stringify с отступом 2 + финальный перевод строки) → запись `dcs/VERSION`. При ошибке на втором шаге — восстановление `package.json`. Node `writeFileSync` с utf8 не добавляет BOM.
3. **Документация:** `docs/publishing.md` — заменить ручную инструкцию «bump dcs/VERSION and package.json together» на `dcs bump <version>`; обновить описание doctor. `README.md` — обновить таблицу команд CLI.

## Risks

- S1 и S2 меняют принципиально разные классы файлов (код vs документация) — параллельное выполнение безопасно.
- Единственный файл исходного кода, который меняется — `bin/dcs.js` (~200 строк). Обе функции (doctor и bump) в рамках S1.
- `tests/payload_check.py` не редактируется — переиспользуется как внешний процесс.
- `dcs/VERSION` и `package.json` — runtime-цели команды bump, не коммитятся в инциденте.

## Verification plan

1. `npm test` — все три набора зелёные.
2. `node bin/dcs.js doctor` — вывод содержит результат content-aware сравнения (identical/differing/repo-only/installed-only), проверка Python на месте.
3. `node bin/dcs.js bump` — текущая версия + usage.
4. Цикл: `node bin/dcs.js bump 0.7.0-test` → grep `0.7.0-test` в обоих файлах → `node bin/dcs.js bump 0.7.0` → grep `0.7.0` в обоих файлах.
5. `grep -c 'content-aware' docs/publishing.md README.md` — не ноль. `grep -c 'dcs bump' docs/publishing.md README.md` — не ноль.
6. `bin/dcs.js` не содержит вызовов `Set-Content` / `Out-File` / PowerShell для редактирования версий.
7. Оригинальный 201 repro: `dcs doctor` при одинаковой версионной строке, но разном payload должен показать расхождение.
