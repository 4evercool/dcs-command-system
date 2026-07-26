# SAFETY — Safety Officer verdicts, period 1

**Incident:** schema-citation-guard
**Period:** 1
**Officer:** `dcs-safety-officer` (opus), two runs

Оба вердикта приводятся **дословно**, включая тот, что остановил период.
Остановка не вычёркивается после исправления: она и есть доказательство, что
сторож проверялся, а не принимался на слово.

---

## Прогон 1 — `halt`

**verdict:** `halt`

**refutations** (одно):

> **claim:** «Criterion 8 is satisfied: the CHANGELOG.md line 'no longer
> carries an unreproducible number' — S1 rewrote it to a number-free wording
> that points at the new check.»
>
> **evidence:** «The 202 states that line is wrong TWICE: the count (20, not
> 19) AND that `dcs/references/doctrine.md` is absent from the surface list
> entirely; it then requires that the previous formulation 'must not survive
> in any form'. Only the first error was removed. `CHANGELOG.md:41-44` now
> reads: 'because `schemas.md #N` citations scattered across the package's
> charters, workflows and templates depend on positional numbering, and
> `tests/test_doctrine_integrity.py` now verifies each one against the
> section title it actually names.' The three-surface list survived unchanged
> in composition. I enumerated the population myself with the 202's own
> command: 20 citations in 14 files, and one of them is
> `dcs/references/doctrine.md`, which is neither a charter (`agents/`), a
> workflow (`dcs/workflows/`) nor a template (`dcs/templates/`). So the
> sentence is still a false census of the citing surfaces. It is worse than a
> stale number in a comment: the same sentence now cites the new check as the
> thing that 'verifies each one', while that check's own degeneracy guard
> (`_CITE_SURFACES`) names FOUR surfaces, the fourth being
> `dcs/references/doctrine.md` — I confirmed this by erasing doctrine.md's
> sole citation in an out-of-repo copy and getting 'FAIL schema citation: all
> four citing surfaces represented / missing:
> ['dcs/references/doctrine.md']'. A shipped changelog line that tells the
> reader the guarded population is three surfaces, while the guard it names
> guards four, is a citation pointing somewhere false — the exact defect class
> this incident opened over. This clears step-6 bar (c) (an acceptance
> criterion covers it explicitly, by file and by name) and bar (a) (the
> CHANGELOG edit is itself a delivered artifact of this period with its own
> criterion). A criterion named wrong twice and fixed once is not met.»

**Ремарка офицера IC:** «everything about the **code** holds up. The guard is
not vacuum — I attacked it four ways and it went red on three of them, went
red on both 201 forgeries, and the pre-incident tree proves the defect was
real. Criterion 1, 2, 3, 4, 5, 6, 7 all pass under my own hands, not the
specialists' reports. The halt is on one sentence.»

**Четыре зонда на вакуумность, прогон 1:**

| Зонд | Что делал | Результат |
|---|---|---|
| P1 | стереть единственную цитату `dcs/references/doctrine.md` | **красное**, `missing: ['dcs/references/doctrine.md']` |
| P2 | стереть единственную цитату `dcs/workflows/deploy.md` | зелёное 58/58 — закрытие держится на уровне поверхности, не файла |
| P3 | завести `docs/probe-new.md` с цитатой на поверхности вне четвёрки | **красное**, популяция и правда обходится |
| P4 | тихо переименовать заголовок §5 при неизменном номере | **красное**, снос смысла при стабильном номере ловится |

**Контрольный опыт, которого никто не просил:** `git archive c7e42aa` в
каталог вне репозитория → `40/40`; та же подделка §3 **в нём** → снова
`40/40`. Симптом 201 воспроизводится до работы периода и не воспроизводится
после — сторож есть новая способность, а не переименование старой.

---

## Прогон 2 — `pass`

**verdict:** `pass`
**refutations:** `[]` — пусто

**advisories** (шесть, дословно по существу):

1. **Область в отгружаемом тексте не оговорена.** `CHANGELOG.md:41-44`
   говорит, что проверка 13 «verifies every citing surface's references» без
   оговорки. Проверка обходит только `*.md` и исключает `.dcs/` и `vault/`
   (`tests/test_doctrine_integrity.py:534-536`), а `vault/Backlog.md:318`
   несёт живую цитату `schemas.md #6`, которую никто не сверяет. Верно для
   отгружаемого пакета, неверно для репозитория целиком.
   **→ Закрыто IC в интеграционном коммите.**

2. **Один неохраняемый позиционный указатель заменён другим в том же
   файле:** «check 13» — номер, который ничем не сторожится, ровно тот класс
   дефекта, который инцидент закрывает. Критерий 8 такую ссылку разрешал,
   поэтому соответствие есть, но перенумерация проверок тихо сгноила бы
   строку. Fix: назвать проверку вместе с номером.
   **→ Закрыто IC в интеграционном коммите.**

3. **`REGISTER.md` строка 68: число 19 встречается дважды.** Ячейка
   Territory помечена, ячейка Outcome — нет; в однострочной ячейке ~5 КБ
   читатель Outcome пометку в Territory не увидит.
   **→ На закрытие.**

4. **Причинное утверждение в самой пометке неверно.** «The surface list is
   short by one for the same reason» — перенос **не** причина: построчный
   `grep` предшественника `doctrine.md` **находил** (`SAFETY.md:45`
   перечисляет `doctrine.md:22`). Из перечня он выпал потому, что не
   подходит ни под одну из трёх категорий. У двух дефектов старой строки две
   разные причины, и это различие и есть смысл пометки.
   **→ На закрытие. Ошибка внесена Диспетчером по директиве IC; IC назвал
   исправление обязательным независимо от того, что `.dcs/esg/` не
   отгружается.**

5. **`vault/Backlog.md:135`** несёт старую перепись во второй форме: «19
   citations pointed at the wrong sections». Неверно дважды: цитат 20, и
   снесло 14 из 20 при 6 сохранивших смысл и 0 повисших. Вне критериев 8 и 9.
   **→ На закрытие, числом вместе с командой восстановления.**

6. **S1-FIX1 не вернул блок схемы #4**, поэтому заявления `files_touched` не
   существовало вовсе. IC записал отклонение в журнал, а не спрятал, но
   гарантию территории дал **офицер**: он установил её по mtime и дифу, а не
   по возврату. Второе отклонение формы возврата за период.
   **→ Действий по поставке нет; материал в строку очереди
   `prompt-vs-schema-drift`.**

**Зонды прогона 2:** тихое переименование заголовка §5 при неизменном номере
→ `57/59`, падение по `agents/dcs-safety-officer.md`. Путь воспроизведения
201 (удалить `## 3.`, сдвинуть `## 4.`–`## 8.`) → **`48/59` с одиннадцатью
именованными падениями**, при этом `test_dcs_gate` `100/100` и
`test_dcs_intake` `10/10` остаются зелёными: конфигурация, которая в 201 была
«все три набора зелёные», теперь падает, и падает **только** в новой
проверке.

**Границы S1-FIX1, которые специалист не подтвердил сам:** офицер установил
их по `find -newermt`: после времени задания изменились ровно три файла —
само задание, `214-LOG.md` и `CHANGELOG.md`.

**Пометки критерия 9 офицер проверил первоисточниками, а не по тексту
пометки:** `SAFETY.md:44` предшественника действительно несёт построчный
`grep -rnoE ... -> 19`; `SAFETY.md:45` действительно перечисляет 13 файлов
без устава командира; `agents/dcs-commander.md:101-102` действительно
разорвана переносом. Строку реестра офицер **смог** прочитать и подтвердил
пометку.

---

## Как разошлись рекомендации

| № | Куда | Состояние |
|---|---|---|
| 1 | интеграционный коммит | закрыто |
| 2 | интеграционный коммит | закрыто |
| 3 | `/dcs-close` | открыто |
| 4 | `/dcs-close` | открыто, IC назвал обязательным |
| 5 | `/dcs-close` | открыто |
| 6 | строка очереди `prompt-vs-schema-drift` | улика, не работа |

Дополнительно IC распорядился записать `vault/Backlog.md:318` **принятой
границей**, а не недостачей: `vault/` исключён из обхода сознательно, он не
отгружается. С уликой: цитата там записана как `` `schemas.md` #6 `` —
обратная кавычка разрывает шаблон, и такую форму не берёт даже наивный
`grep`. Грамматика цитат в соседних популяциях шире, чем ловит нынешний
сравниватель.
