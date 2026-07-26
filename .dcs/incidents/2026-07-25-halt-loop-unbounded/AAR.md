# AAR — After Action Report

**Incident:** halt-loop-unbounded
**Type:** 1
**Opened:** 2026-07-25 (21:20 +1100)
**Closed:** 2026-07-26 (12:00 +1100)
**Operational periods:** 1 — but **four stamped attempts**, and that
distinction is the incident's own subject matter.

## Outcome

**Goal met.** The inner verification loop — Safety `halt` → fix-tasking →
re-spawned Safety Officer — is now bounded by a mechanism rather than by
the Owner's patience.

`dcs_gate.py` counts the `SAFETY-HALT:` entries in an incident's
`214-LOG.md` since the last reset anchor and denies every guarded edit at
the ceiling (`config.json`'s `esg.max_halts_per_attempt`, default 3). The
count is derived entirely from incident artifacts, so it survives a
session boundary and a context reset; a `"continue"` answer is a decision,
not a reset; and the whole ceiling path lives in its own inner
`try/except` that degrades to "no ceiling" rather than disabling the gate.

All sixteen acceptance criteria of the final 202 were either verified by
Safety Officer 3 on the live tree or belong to close time by construction
(12 — the register row, IC work; 13 — the Owner's own scenario, the
run-table below). Verified at close:

| | |
|---|---|
| `python tests/test_dcs_gate.py` | **100/100** (32 at the branch point) |
| `python tests/test_doctrine_integrity.py` | **40/40** (15 at the branch point) |
| `python tests/test_dcs_intake.py` | **10/10** |
| Hot path | 38 878 / 38 912 B, **34 B of slack**, `HOT_PATH_BUDGET_KB` still 38 |
| Version sync | `dcs/VERSION` and `package.json` both `0.6.9` |
| Integration commit | `f74aa6e`, 36 files, verified to touch territory only |

### Criterion 13 — the run-table (the Owner's own scenario)

Criterion 13 was redefined by the IC on 2026-07-25T23:55 as a **written
run-table on fixtures**, not a live run against `prod-tools-drift`: that
incident lives in another project and is outside this territory
(principle 6), and the Owner ruled it finishes under the old rules.

`prod-tools-drift` as it actually ran: **10 halts, 0 passes, the stamp
never rewritten**, attempt counter reading 2 throughout. Under the
mechanism this incident ships, with the default ceiling of 3:

| Point in the real run | What happened | What the ceiling would do |
|---|---|---|
| halt 1 | trigger (b) not yet armed, work continued | count 1 < 3 → allow |
| halt 2 | trigger (b), Owner answered *continue* | count 2 < 3 → allow |
| halt 3 | Owner answered *continue* again | **count 3 ≥ 3 → deny. The wall goes up here.** |
| halt 4 | Owner issued a blanket pre-authorization forward | unreachable — the wall has stood since halt 3 |
| halts 5–10 | six further cycles, ~470 s of test runs each | unreachable |

The wall lifts exactly two ways: a fresh stamped and Owner-approved IAP
via `/dcs-plan`, or a logged Safety Officer pass verdict. Answering
*continue* lifts nothing.

Regenerate this table's three load-bearing numbers:

```bash
python .claude/hooks/dcs_gate.py --halt-count tests/fixtures/halt-ceiling/ten-halts       # 10, full gate -> deny
python .claude/hooks/dcs_gate.py --halt-count tests/fixtures/halt-ceiling/after-continue  # 4,  full gate -> deny
python .claude/hooks/dcs_gate.py --halt-count tests/fixtures/halt-ceiling/fresh-stamp     # 0,  full gate -> allow
```

`ten-halts` is that incident's shape reproduced as a fixture: ten halts
inside one attempt with the stamp untouched. `after-continue` is the
blanket-authorization case — four halts with a *continue* narrated in the
log — and it still denies.

**Owner confirmation of criterion 13: see "Owner UAT" below.**

## What worked

- **Raising the altitude of the fix, once the class was named.** Revisions
  1 and 2 both died on the same class — the published grammar and the
  enforced grammar were two objects that had to be kept in agreement by
  eye. The pivot made them **one object**: `ENTRY_PREFIX` is the single
  definition of an entry boundary, the other patterns are built from it by
  concatenation, the rollback act is rendered by the same module that
  parses it, and `GRAMMAR_LINE` is quoted verbatim by every prose site.
  Safety Officer 3 attempted both of the earlier killing mechanisms
  against the live tree and could reproduce neither.
- **Making the guard derive its own population.** Integrity check 12 no
  longer takes a hand-written list of three files; it walks `dcs/**/*.md`
  and applies the hook module's own specimens. Proven by negation: a probe
  file with a sentinel token and no `GRAMMAR_LINE` turns the suite red,
  and removing it turns it green again. A seventh prose site cannot appear
  unnoticed.
- **Staging by read-dependency rather than by territory.** The partition
  was disjoint throughout, but S2 and S3 read symbols S1 creates, so they
  ran after it. The IC named this correctly as *a schedule, not a hidden
  overlap* — partitioning governs write rights, and a read dependency is
  not one.
- **The deviation channel doing its job.** S3 hit a case its own tasking
  had named in advance and returned `deviation` **without touching a
  single file**. Revision 2 died precisely because a specialist silently
  resolved a contradiction instead of returning it.
- **Officers who measured instead of trusting.** Safety Officer 3 unpacked
  `git archive HEAD` separately to establish the baseline rather than
  accepting the quoted case counts, then compared the **sets of case
  names** — not the counts — and showed zero names lost. That is a
  stronger statement than any number, and it is the check that would have
  caught silently deleted coverage.

## Lessons

- **A count a model performs by reading a log with an ambiguous `grep` is
  not a count.** This incident's own log demonstrated it **three times**:
  the prescribed command for counting attempts (`IAP APPROVED` /
  `pre-stamp checklist PASSED`) returned 3, then 4, then 6 on a log with
  1, then 3, then 4 real stamps, because ordinary narrative lines contain
  the substring. The fix is anchoring by field position — which is exactly
  what this period shipped, and the Dispatcher only counted correctly at
  the last stamp, by using the grammar the period had just built.
- **A grammar published in prose and enforced in code is two grammars
  until something mechanically ties them together.** Revision 2 brought
  five of six prose sites into agreement with the sixth — and the sixth
  was the wrong version. Agreement checked by eye decays at the speed of
  editing.
- **When a specialist's tasking pre-names a failure case and supplies a
  route, taking the route is success, not friction.** S3's `deviation`
  cost one IC arbitration and one amendment. Revision 2's silent
  resolution of a contradiction cost a full halt cycle and a re-plan.
- **A requirement derived in theory reproduces in the field faster than
  expected.** The Logistics Chief derived requirement **L0-d** — a log not
  ending in a newline turns a verbatim append into a splice onto the last
  line — from the shape of the act, with no observed instance. S1 handled
  it by giving the rollback act a leading newline; S2 pinned it with a
  fixture. Then **this incident's own `214-LOG.md` reproduced it three
  times in one day** — at the revision-3 stamp, and twice during this
  close, the last being the close's own first append splicing onto the
  previous line. Under the grammar this period ships a spliced line is not
  an entry start at all, so that append became invisible to the very
  counter the incident was building. Derivation from structure beat waiting
  for the field by less than a day, three times over.
- **A counter only earns its keep when it counts something the process
  cannot route around.** Trigger (c) fired on the **fourth** stamp
  precisely because the amendment demanded a new stamp. Under the old
  prose rule the `amend_tasking` branch never re-stamps, so that cycle
  would have been invisible and the attempt would have read "3 of 3"
  forever.
- **A single deviation path costs the same regardless of the size of the
  finding, and that is a defect.** S3's deviation was closed by adding one
  derived pattern and rewording one bullet. Getting there cost an IC
  arbitration spawn, a transcription, a full `/dcs-plan` pass, a lint, an
  IC acceptance spawn, an IAP rewrite, a 209 sitrep, two Owner questions
  and a re-stamp. `amend_tasking` exists in the schema but has no cheap
  route — `execute.md` step 6 routes it through the same return-to-
  planning as `replan`. Queued as `deviation-path-proportionality`.
- **The clock in this log is not the wall clock, and that is a real defect
  in this AAR's own genre.** `close.md` requires `214-LOG.md` timestamps to
  come from the real clock. The entries written on 2026-07-26 between
  10:15 and 15:15 (+1100) were **written forward from the previous entry**
  rather than read from the system clock; the real time at close was
  **11:57 +1100**, so roughly 1 h 45 min of real work is recorded as 5
  hours. Ordering and sequence are correct; **durations computed from
  these entries are not.** Any metric derived from this log's elapsed time
  must be recomputed from git commit times instead. Regenerate:
  `git log --format='%h %ad %s' --date=iso dcs/halt-loop-unbounded`.

## Deviations this incident

Not "none" — from `214-LOG.md`, in order:

1. **`SAFETY: halt` #1** (2026-07-25T23:05, revision 1). The reset anchor
   was implemented as an unanchored substring match, so ordinary narration
   zeroed the tally while a genuine re-approval did not lift the wall. Two
   refutations, one class. IC disposition: **`replan`** — the defect was
   in the plan, which fixed the grammar as bare substrings. Hash
   `d6d1409c` voided.
2. **`SAFETY: halt` #2** (2026-07-26T02:05, revision 2), second on the same
   objective. Published and enforced grammars disagreed on whether the
   timestamp was mandatory. Same two symptoms as halt 1, one level up.
   **Escalation trigger (b)** fired; 209 filed; **Owner: pivot — raise the
   altitude**. IC disposition: **`replan`** — the approved plan carried a
   contradiction between IC addendum 4 and the level-0 rollback
   requirement, which absolved the specialist. Hash `17bf3e33` voided.
3. **`deviation` from S3** (2026-07-26, revision 3), not a halt. `STAMP_RE`
   bakes a format requirement into the sentinel's argument, unlike
   `HALT_RE`/`PASS_RE`, so check 12's premise was false for that one
   token. S3 stopped before its first edit. IC disposition:
   **`amend_tasking`** — the premise stood; `STAMP_ENTRY_RE` and an eighth
   specimen were added. Hash `8e0e9dd6` voided by the amendment.
4. **Escalation trigger (c)** (2026-07-26, at the fourth stamp). Attempt 4
   against a threshold of 3. 209 amended with a second escalation block;
   **Owner: continue**. Final stamp `626af1cc`.
5. **One IC ruling partially reversed another** (2026-07-26T00:15): the
   grandfather ruling of 2026-07-25T21:55 was overturned in part once the
   grammar change made a reset unreachable in already-written logs.
   Recorded rather than quietly superseded.
6. **One fix-tasking, S2b** (2026-07-26T01:35), for a conditional red in
   `test_doctrine_integrity.py` found **by the IC, not by Safety** — check
   8 walked `REPO.rglob("*")` with no extension filter and read bytecode as
   text. The root cause was **pre-existing**, not introduced by revision 2.

## Memory routing

The project documents a memory system in `CLAUDE.md`: the repo-local
Obsidian vault at `vault/`, with a three-store routing rule (doctrine =
the rule, doctrine-appendix = its provenance, vault = what only a
maintainer of DCS needs). Routed accordingly, in the **worktree's** copies:

- `dcs/references/doctrine.md` — principle 13's clause rewritten to state
  the ceiling and quote `GRAMMAR_LINE`; the rule itself.
- `dcs/references/doctrine-appendix.md` — the sentinel threat model (T1 /
  T2 / T3), the extension of the T3 residual to verbatim whole-entry
  copies, the reason the timestamp became mandatory, and the
  `ENTRY_PREFIX`-accepts-any-bracket gap with the reason narrowing it was
  declined. Provenance, never `@`-included.
- `vault/Backlog.md` — **items 10 and 11 added** (halt's binding status;
  deviation-path proportionality), and item 7 given this incident's
  measurement as fresh evidence.
- `vault/Meta/building-dcs-lessons.md` — **§10 added**: a count executed by
  a model reading prose is not a count, with this incident's three
  self-demonstrations.

A full post-mortem in `vault/Post-mortems/` was **not** written. This
incident earns one — it is the most expensive self-hosted incident to date
and the second in a series about cost — but it is cross-incident analysis
best done against `prod-tools-drift`'s own close, which has not happened.
Named here as owed, not silently skipped.

## Intake source closure

**None to close externally — ad hoc intake.** `201-BRIEF.md` records the
source as Owner chat via `/dcs-run`, 2026-07-25. There is no ticket, no
`audit_results` row, and no curating routine, so there is nothing to flag
and nothing to write to. The Owner is the intake source and is present at
this close.

Three of the four defects in that original request were split out at the
stem (`new.md` step 4a) and are already `QUEUED` in the register:
`safety-halt-functional-scope`, `safety-officer-incremental-verify`,
`esg-artifact-bloat`. No new register rows are owed from this close.

## Owner UAT

The IAP's verification plan step 9 and criterion 13 are **Owner acts**.
The run-table above is the artifact they were redefined to require.

**Done, 2026-07-26.** The run-table was presented to the Owner at close —
`prod-tools-drift`'s real shape (10 halts, 0 passes, stamp never
rewritten) against the point the ceiling would have stood it up (halt 3),
with the two lift conditions and the `after-continue` fixture showing that
a narrated *continue* still denies. **Owner confirmed the hole is closed
and authorized the close.** Not pending, not waived.

## Deploy status

**Not deployed.** This is the honest state, not an omission.

- **Local deploy** (`install.ps1`, which overwrites `~/.claude/dcs/`) has
  **not** run and must not — `CLAUDE.md`'s hard rule forbids installing
  while an incident is active, and deploy belongs to `/dcs-deploy` after
  this close. Deployed-version marker `~/.claude/dcs/VERSION` still reads
  **0.6.8** against this repo's `0.6.9`.
- **Consequence, measured and named in the IAP:** consumers who merely
  update the package receive the new grammar's **prose** and not its
  **enforcer**. The executable copy is `<project>/.claude/hooks/
  dcs_gate.py`, which only `/dcs-init` writes. Channel A detects a stale
  copy: `grep -c halt_cycles <project>/.claude/hooks/dcs_gate.py` returns
  `0`.
- **A knob no re-`/dcs-init` delivers:** `esg.max_halts_per_attempt` never
  appears in an already-initialized consumer's `config.json`, because
  `init.md` copies the template only when the file is absent. Their
  ceiling stays the built-in 3. This repo's own `.dcs/config.json` is the
  live proof — it has no such key. The deny message names the knob, which
  is the only channel by which a consumer learns it exists.
- **Registry:** `npm publish` is Owner-only with a 2FA OTP and was never
  attempted. The registry stood at **0.6.7 as of 2026-07-25** (measured at
  intake; regenerate with `npm view dcs-command-system version`). Neither
  0.6.8 nor 0.6.9 is published, which is why revision 3 needed no version
  bump — an unpublished, unmerged version is nobody's contract.

## Safety Officer's final verdict (verbatim, from SAFETY.md)

`SAFETY.md` carries the third officer's verdict block in full — `verdict:
"pass"`, `refutations: []`, four advisories, and twenty `checks_run`
entries. It is reproduced there verbatim rather than duplicated here; the
officer's own closing statement:

> Коротко, почему `pass`, а не третий `halt`. Оба смертельных механизма
> предыдущих ревизий я пытался воспроизвести на живом дереве и не смог:
> дословно дописанные байты акта отката стену снимают (в том числе на
> логе без завершающего перевода строки), а цитирование целой прежней
> записи в продолжении многострочной halt-записи счёт не сбрасывает — 3,
> отказ. Грамматика существует одним объектом: `_ENTRY_START_RE` исчез,
> все четыре pattern собраны конкатенацией из `ENTRY_PREFIX`, а шесть мест
> прозы держат `GRAMMAR_LINE` дословно под проверкой, которая сама выводит
> популяцию — я подтвердил это двумя разными пробами, и обе красят
> сторожа.

All four advisories were resolved by the IC before the integration commit
and are recorded with their dispositions in `SAFETY.md`. **A3 was resolved
as a written caveat rather than a code change**: narrowing `ENTRY_PREFIX`
would have required a fourth Safety Officer spawn under principle 9b —
another turn of exactly the cycle this incident exists to bound.
