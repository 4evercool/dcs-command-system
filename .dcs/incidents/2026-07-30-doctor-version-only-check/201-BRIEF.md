# 201 — Incident Brief

**Incident:** doctor-version-only-check
**Opened:** 2026-07-30
**Type:** 3

## Symptom

`dcs doctor` (CLI-команда `bin/dcs.js:121-146`) сообщает, что установленная версия DCS «current», на основе строкового равенства номеров версий (`~/.claude/dcs/VERSION` == `package.json` version). При одинаковом номере версии, но разном содержимом payload (same-version ship), пользователь получает ложное «current» и не знает, что нужна переустановка. Кроме того, в проекте нет команды `dcs bump <version>` — атомарное редактирование `dcs/VERSION` и `package.json` делается вручную через PowerShell, что несёт риск перекодировки (UTF-8 BOM).

## Evidence

- `bin/dcs.js:121-146` — `doctor()`: читает `~/.claude/dcs/VERSION`, сравнивает с `package.json` version строковым равенством. При совпадении строк молча сообщает об успехе, даже если payload изменился без смены версии. Источник: прямое чтение файла.
- `tests/payload_check.py` — уже существует и делает content-aware сравнение (sha256) установленной копии с репозиторием. Именно то, что `doctor()` должна вызывать вместо строкового сравнения версий. Источник: прямое чтение файла.
- `tests/test_doctrine_integrity.py:225-229` — проверка синхронизации версий (dcs/VERSION == package.json) встроена в набор из 21 проверки, изолированного запуска нет. Источник: прямое чтение файла.
- `.dcs/esg/REGISTER.md:108` — строка `doctor-version-only-check`, QUEUED, rank 1. Территория: `bin/dcs.js`, `dcs/VERSION`, `package.json`. Поглотила `version-bump-command` (KILLED). Источник: прямое чтение.
- `vault/Decisions/v0.7-scope.md:59-61,93-97` — решение ESG: один инцидент на `bin/dcs.js` — content-aware `doctor()` + `dcs bump`. Источник: прямое чтение.
- `.dcs/incidents/2026-07-27-deploy-marker-blind/201-BRIEF.md:173-181` — первоисточник дефекта: выделен из `deploy-marker-blind` на фазе stem. Источник: прямое чтение.
- Текущие версии синхронизированы (0.7.0 == 0.7.0). Источник: `python tests/test_doctrine_integrity.py` — PASS.

## Reproduction path

1. Убедиться, что текущая установка != содержимому репозитория (внести payload-изменение без изменения версии, запустить install.ps1).
2. `node bin/dcs.js doctor` — сообщает «current», потому что `~/.claude/dcs/VERSION` == `package.json` version (строковое равенство).
3. `python tests/payload_check.py` — показывает расхождения (слепая зона: same-version, разное содержимое).
4. `node bin/dcs.js bump 0.7.1` — команда не существует (должна быть добавлена).

## Blast radius (best guess at intake)

`bin/dcs.js` (основной файл — doctor() + bump), `dcs/VERSION` и `package.json` (редактируются командой bump), `tests/payload_check.py` (переиспользуется, не меняется), `docs/publishing.md`, `README.md` (документация).

## Prior art

Выделено из инцидента `deploy-marker-blind` (2026-07-27, Type 1) на фазе stem (`new.md` step 4a): `bin/dcs.js:121-146`'s `doctor()` имеет ту же слепую зону, что и родительский инцидент — same-version ship не обнаруживается строковым сравнением версий. Самостоятельный потребитель (пользовательская проверка здоровья), самостоятельная поставка. Родительский инцидент доставил `tests/payload_check.py` как переиспользуемый свидетель именно для этого случая. `version-bump-command` поглощён на одиннадцатой сессии `/dcs-esg` (2026-07-29) согласно `vault/Decisions/v0.7-scope.md`: один инцидент на `bin/dcs.js` — content-aware `doctor()` + `dcs bump`. На тринадцатой сессии (2026-07-30) Owner установил rank 1 через дорожную карту Fable. Полный контекст: `.dcs/esg/REGISTER.md:108`, `.dcs/esg/STRATEGY.md:122,149-154`, `vault/Backlog.md:74-92`, `vault/Decisions/v0.7-scope.md:59-61,93-97`, `vault/Decisions/fable-review-roadmap.md:296-303`.

## Type + rationale

**Proposed type:** 3
**Rationale:** Bounded, understood feature + bugfix in 3 files following existing CLI patterns — не Type 5 (multi-file, multi-feature), не Type 1 (no structural consequences, no schema/migration/rollback, follows existing patterns).
**Owner confirmation:** confirmed as proposed (Type 3)

## Intake source (for /dcs-close to route back to)

`.dcs/esg/REGISTER.md` row `doctor-version-only-check` (QUEUED, rank 1), split out of `deploy-marker-blind` at its stem; absorbed `version-bump-command` at the eleventh `/dcs-esg`, 2026-07-29.
