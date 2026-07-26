# 204 — Tasking S1-FIX1 (исправляющее, после остановки Safety)

**Incident:** schema-citation-guard
**Period:** 1
**Specialist:** dcs-ops-specialist (S1-FIX1) — свежий спавн, не продолжение S1

## Почему это задание существует

Safety Officer остановил период **одним** опровержением. Критерий 8 назвал в
строке `CHANGELOG.md` **две** ошибки, а правка сняла одну.

Что стоит сейчас (`CHANGELOG.md:41-44`):

> because `schemas.md #N` citations scattered across the package's charters,
> workflows and templates depend on positional numbering, and
> `tests/test_doctrine_integrity.py` now verifies each one against the
> section title it actually names.

Число 19 убрано — это сделано верно. Но перепись поверхностей уцелела по
составу: «charters, workflows and templates», три штуки. Между тем цитата
есть и в `dcs/references/doctrine.md`, который не относится ни к одной из
трёх. Отягчающее обстоятельство, названное и офицером, и IC: **та же фраза
теперь ссылается на новую проверку как на сверяющую «each one», а страховка
самой этой проверки** (`_CITE_SURFACES` в `tests/test_doctrine_integrity.py`)
**поимённо охраняет четыре поверхности, четвёртая — `doctrine.md`.** То есть
отгружаемый текст говорит читателю то, чему сам названный им код
противоречит, — ровно тот класс дефекта, ради которого инцидент открыт.

## Task

Закрывает критерий 202 **№8 целиком, обе исходные ошибки фразы**.

Переписать предложение `CHANGELOG.md:41-44` одним из двух способов:

1. **Перепись становится верной.** Состав поверхностей прочитать **из
   `_CITE_SURFACES` в `tests/test_doctrine_integrity.py` на момент правки**,
   а не по памяти и не из этого задания. Файл `tests/**` тебе запрещён к
   правке, но читать его ты обязан.
2. **Переписи не остаётся вовсе** — формулировка без перечня поверхностей и
   без числа, со ссылкой на проверку 13 как на то, что теперь эту привязку
   сторожит.

Второй способ предпочтительнее по принципу 15: перепись — производный факт,
и именно потому, что она стояла в прозе без способа пересчёта, число 19
уехало в три места. Но выбор за тобой, оба удовлетворяют критерий.

**Прежняя формулировка не должна выжить ни в каком виде** — это требование
критерия 8 дословно, и относится оно к перечню поверхностей так же, как
относилось к числу.

После правки прогнать поиск по всем `*.md` области на любых потомков старой
формулировки — перечень из трёх поверхностей в любом составе и порядке — и
включить вывод в возврат.

## File territory (may edit only within these globs)

- `CHANGELOG.md`

## Forbidden zones (explicitly, even if it seems related)

- `tests/**` — читать обязан, править нельзя
- `dcs/**`, `agents/**` — работа S1 принята, повторно её не трогать
- `skills/**`, `bin/**`, `install.ps1`, `install.sh`, `package.json`
- `.dcs/**`, `vault/**`, `README.md`

**Отдельно запрещено:** трогать якоря, поставленные S1, и вообще что-либо
кроме этого предложения. Твоя правка не должна породить новую неякорёванную
ссылку вида `schemas.md #<цифра>` — буквальное `schemas.md #N` с буквой N в
популяцию не попадает, шаблон требует цифр. Только Write/Edit, не
`Set-Content`/`Out-File`. Английский, LF, без BOM.

## Evidence required in the return

1. `git diff -- CHANGELOG.md` — приложить целиком.

2. **Состав поверхностей прочитан из кода, а не из памяти** — приложить
   команду, которой ты его прочитал, и её вывод:

```bash
grep -n -A8 "_CITE_SURFACES" tests/test_doctrine_integrity.py
```

3. **Потомков старой формулировки не осталось:**

```bash
python - <<'PY'
import re, pathlib
EX = {".git", "node_modules", "__pycache__", ".dcs", "vault"}
pat = re.compile(r"charters?.{0,40}workflows?.{0,40}templates?", re.I)
hits = 0
for p in sorted(pathlib.Path(".").rglob("*.md")):
    if any(x in p.parts for x in EX):
        continue
    t = re.sub(r"\s+", " ", p.read_text(encoding="utf-8"))
    for m in pat.finditer(t):
        hits += 1
        print(f"{p.as_posix()}: {t[max(0,m.start()-60):m.end()+60]!r}")
print("hits:", hits)
PY
```

   Ожидается `hits: 0`. Если попадание осталось — объясни, почему оно не
   является потомком той же переписи, а не убирай его молча.

4. **Команда-перечислитель из 202** — вывод обязан остаться пустым (твоя
   правка не должна была породить новую неякорёванную ссылку):

```bash
python - <<'PY'
import re, pathlib
EX = {".git", "node_modules", "__pycache__", ".dcs", "vault"}
REPO = pathlib.Path(".")
schemas = (REPO / "dcs/references/schemas.md").read_text(encoding="utf-8")
KEY = {int(n): re.split(r"\s*[(—]", t.strip())[0].strip().lower()
       for n, t in re.findall(r"^##\s+(\d+)\.\s+(.+)$", schemas, re.M)}
pat = re.compile(r"schemas\.md`?\s*#\s*(\d+)")
for p in sorted(REPO.rglob("*.md")):
    if any(x in p.parts for x in EX):
        continue
    t = re.sub(r"\s+", " ", p.read_text(encoding="utf-8"))
    for m in pat.finditer(t):
        n = int(m.group(1))
        if KEY.get(n) and KEY[n] in t[m.end():m.end() + 80].lower():
            continue
        print(f"MISSING {p.as_posix()} #{n} (expect {KEY.get(n)!r})")
PY
```

5. `python tests/test_doctrine_integrity.py` — напечатанная `N/M passed` и
   код возврата; зелёный.

6. **Границы территории:** `git status --porcelain` — по сравнению с
   состоянием до тебя изменился **только** `CHANGELOG.md`.

7. **Кодировка:** `CHANGELOG.md` — `LF`, без BOM (он не входит в набор
   проверки 10, поэтому смотрим явно).

## On discovering the plan doesn't fit reality

STOP. Do not improvise a different fix. Return `status: "deviation"` per
`references/schemas.md` #4 (ops-specialist return), with `found`,
`why_plan_wrong`, and a `proposal` (a recommendation, not an action). The IC
will re-enter planning around your finding.
