# 201 — Incident Brief

**Incident:** schemas-contract-format
**Opened:** 2026-07-29
**Type:** 1

## Symptom

Контракты агентов объявлены в `dcs/references/schemas.md` в форме, которую
машина разобрать не может, и ни одна проверка не сверяет список полей
устава агента с его же разделом схемы. Наблюдаемые следствия на HEAD
(793e01c, v0.6.13): §3 (Logistics Chief) — только заголовок и JSON-пример,
без таблицы полей и без строки `Returned by`; §6 связывает три имени поля
в одну ячейку `type` / `verdict` / `disposition`, не привязывая поле к
командной точке; `agents/dcs-commander.md` вовсе не имеет блока
`<output_contract>`, хотя таблица §6 отсылает за привязкой именно к нему;
и одно настоящее расхождение уже живёт в пакете — `advisories` есть в
схеме №5 и в теле процесса Safety Officer, но отсутствует в его
`<output_contract>` с коммита `6a57b97` (v0.6.5). Дополнительно (влито
решением Владельца на этом стеме): JSON-примеры `schemas.md` не разбирает
ни один тест — проверка разбора из diet-коммита осталась ручной.

## Evidence

- §3 состоит из заголовка и огороженного JSON — ни таблицы полей, ни
  `Returned by` (у §1/§2/§4/§5/§6 строка есть). Источник:
  `dcs/references/schemas.md:50-54`; regenerate:
  `grep -n '^Returned by' dcs/references/schemas.md`.
- §6, строка таблицы `` `type` / `verdict` / `disposition` | enum per
  point `` — три имени поля в одной ячейке без привязки к командной
  точке; извлекатель аналитика прежнего стема прочёл ячейку как одно имя
  поля и сообщил самопротиворечие, которое IC опроверг чтением файла.
  Источник: `dcs/references/schemas.md:120-127`;
  `.dcs/incidents/2026-07-26-schema-citation-guard/201-BRIEF.md:129-149`.
- `agents/dcs-commander.md` — 0 вхождений `output_contract`; решения
  объявлены четырьмя JSON-примерами внутри `<command_points>`; поле
  `esg_activation`, которое читает `dcs/workflows/execute.md:319`, не
  встречается ни в одном примере. Regenerate:
  `grep -c "output_contract" agents/*.md`.
- `agents/dcs-safety-officer.md:143-150` — `<output_contract>` перечисляет
  `verdict`, `refutations[]`, `checked[]`; поля `advisories` нет, хотя
  `schemas.md:101` определяет его в контракте №5, а шаги 6-8 самого устава
  им пользуются. Пробел с `6a57b97` (v0.6.5); regenerate:
  `git show 6a57b97 -- agents/dcs-safety-officer.md` + чтение HEAD.
- Ни одна проверка не сравнивает поля устава со схемой: проверка 13
  сверяет только номер цитаты `schemas.md #N` с заголовком раздела
  (`tests/test_doctrine_integrity.py:508-536`), проверка 14 — одну пару
  полей принципа 15 в уставе Safety Officer (докстрока, строки 49-52).
  Regenerate: `grep -n 'output_contract\|schemas\.md'
  tests/test_doctrine_integrity.py`.
- Прецедент машиночитаемого формата уже в пакете: огороженный блок
  ```delegation-bounds``` — «the only part of that file workflows parse»
  (`dcs/references/schemas.md:131`; `dcs/workflows/plan.md:291-294`);
  разбирает его сам workflow-текст, не Python-скрипт (`grep -rn
  'delegation-bounds' dcs/hooks` — пусто).
- Влитая строка `json-examples-unparsed`: JSON-примеры схемы не парсит ни
  один тест; число примеров в артефактах не фиксировать — прежнее «11» не
  соответствовало ни одной ревизии (10 на HEAD прежнего стема, 12 до
  `08f75f0`). Regenerate население: разбор всех огороженных JSON-блоков
  `schemas.md` во время прогона. Источник: `.dcs/esg/REGISTER.md`, строка
  `json-examples-unparsed`;
  `.dcs/incidents/2026-07-26-schema-citation-guard/201-BRIEF.md:235-238`.
- ОПРОВЕРГНУТО на HEAD: пункт заявки «§8 обещает цитаты, которых нет» —
  `schemas-md-trim` (2026-07-26) перенёс §8 в
  `templates/209-SITREP.md`, и текст раздела теперь сам объясняет
  резервирование номера. Из объёма работ выпадает. Источник:
  `dcs/references/schemas.md:150-156`.
- Асимметрия направлений сверки измерена, не предположена: направление
  «поле схемы отсутствует в уставе» — 0 ложных срабатываний, 1 настоящая
  находка (`advisories`); обратное — пусто у командира и 4 ложных имени на
  двух других уставах. Источник:
  `.dcs/incidents/2026-07-26-schema-citation-guard/201-BRIEF.md:170-186`;
  `.dcs/esg/REGISTER.md`, строка `schemas-contract-format`, ячейка Intake
  source.

## Reproduction path

Не падение программы, а измеримое состояние текста; воспроизводится
чтением и grep: (1) `grep -n '^Returned by' dcs/references/schemas.md` —
§3 в списке отсутствует; (2) `grep -n 'output_contract'
agents/dcs-commander.md` — 0 совпадений; (3) сравнить
`agents/dcs-safety-officer.md:143-150` со `schemas.md:101` — `advisories`
в уставе нет; (4) `python tests/test_doctrine_integrity.py` — зелёный
(свой счёт печатает сам), при этом ни одна проверка не заявляет сверку
полей устава со схемой.

## Blast radius (best guess at intake)

- `dcs/references/schemas.md` — формат объявления контрактов (§3, §6;
  примеры всех разделов, если сторож будет их разбирать)
- `agents/dcs-commander.md` — блок `<output_contract>` появляется впервые
- `agents/dcs-safety-officer.md` — `advisories` в `<output_contract>`
- `agents/dcs-planning-chief.md`, `agents/dcs-logistics-chief.md`,
  `agents/dcs-ops-specialist.md`, `agents/dcs-situation-analyst.md` —
  выравнивание блоков контрактов под новый формат
- `tests/test_doctrine_integrity.py` — новый сторож (сверка полей + разбор
  JSON-примеров); не регрессировать проверки 13/14

## Prior art

- Стем `schema-citation-guard` (закрыт 2026-07-26, Type 1, DEPLOYED) —
  прямой предшественник: измерил асимметрию направлений и назвал
  прецедент `delegation-bounds`. Его 201, раздел «Механизируемость».
- Строки `charter-schema-agreement` и `commander-output-contract` — KILLED
  и влиты в эту 2026-07-26; их улики — часть этой работы, повторно не
  собирать.
- `vault/Meta/building-dcs-lessons.md` §15 — один контракт, разбитый на
  две изолированные руки, даёт дефект на шве: прозу контракта и сторож над
  ней не поручать двум специалистам без сверки; §8 — цитировать по
  содержательному якорю, не по номеру: сторож обязан разбирать схему и
  уставы на лету, без литералов имён и счётов (принцип 15 доктрины).
- Дисциплина для нового сторожа — по образцу проверок 13/14: население
  обходом дерева, разбор на лету, страховка от вырождения, именованный
  случай на файл, отрицательное доказательство подделкой. Известные
  слабости проверки 14 (`vault/Backlog.md` item 16) чинит своя строка
  `check-14-hardening` (ранг 3) — не здесь, но и не регрессировать.

## Decomposition (new.md step 4a)

Дефект один: контракт объявлен прозой и примерами, поэтому производителя
и потребителя нельзя сверить машиной; «сделать машиночитаемым» и
«сторожить» ESG признал неразделимыми ещё при слиянии трёх строк
(2026-07-26). Решения этого стема:

1. **Открыт этот инцидент** — формат контракта + сторож + починка живого
   расхождения `advisories`.
2. **Влита `json-examples-unparsed` (ранг 13)** — решением Владельца на
   командной точке 1 (вопрос ESG оставил стему): разбор всех огороженных
   JSON-блоков — почти тот же акт, что разбор контрактных таблиц;
   отдельный инцидент унаследовал бы только что переписанный тест (шов из
   урока §15). Строка помечена FOLDED, улики переезжают.
3. **Не втянуто:** `prompt-vs-schema-drift` (ранг 7) — тот же корень, но
   сторож над деревом не видит ни вводную, ни возврат — нужен другой
   механизм; `check-14-hardening` (ранг 3) — своя строка, свой корень.
4. **Выпало из заявки:** пункт про §8 — опровергнут на HEAD (уже устранён
   `schemas-md-trim`).

## Type + rationale

**Proposed type:** 1
**Rationale:** вводится новый сквозной формат объявления контрактов
(`schemas.md` + шесть уставов — ~9 файлов, за пределами «до ~4» Type 3) и
расширяется механизм слияния-сторожа `tests/test_doctrine_integrity.py`;
прецеденты той же формы (`schema-citation-guard`,
`workflow-budget-enforcement`) типизированы 1.
**Owner confirmation:** confirmed as proposed (AskUserQuestion,
2026-07-29); туда же — решение влить `json-examples-unparsed`.

## Intake source (for /dcs-close to route back to)

`.dcs/esg/REGISTER.md`, строка `schemas-contract-format` — ранг 1, выбор
Владельца на десятой `/dcs-esg` (2026-07-29); передана через
`/dcs-run schemas-contract-format`. Влитая строка: `json-examples-unparsed`
(решение Владельца на этом стеме).
