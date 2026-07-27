# AAR — After Action Report

**Incident:** direct-resolution-lane
**Type:** 1
**Opened:** 2026-07-27
**Closed:** 2026-07-27
**Operational periods:** 1 (one stamped attempt — `grep -cE "^\[[^]]+\] IAP-APPROVED:" 214-LOG.md` → 1)

## Outcome

**All ten acceptance criteria met.** The register now has a terminal state for
work resolved without a worktree, and the express lane writes it.

`dcs/templates/REGISTER.md`'s enum went from six values to seven, the seventh
being `RESOLVED` — defined **scenario-neutrally**, as terminal for an incident
whose work completed inline with no worktree ever opened and never entering the
deploy lifecycle. `dcs/workflows/new.md` step 7a gained a substep that writes it,
**update-only and silent** when there is no register or no matching row, so a
Type 5 with nothing tracking it acquires no register ceremony. `forms.md:22` and
`close.md` were brought into agreement, and `close.md`'s pre-v0.3 fallback —
which told a never-worktreed incident to move its row `ACTIVE → CLOSED`, a state
the enum never contained — now names `RESOLVED` instead.

Criterion-by-criterion, each verified independently by the Safety Officer:
1 (seven values, counted by command) · 2 (scenario-neutral, greped **and read**)
· 3 (every in-territory carrier names the same seven values) · 4 (7a writes the
register; the block greps non-empty where it returned 0 at HEAD) · 5
(`close.md:239` true beside the new state; the phantom `CLOSED` reconciled) · 6
(`82/82`, check 15 still one declaring paragraph in
`dcs/templates/REGISTER.md`) · 7 (`100/100`, `10/10`) · 8 (hot path `36683 1205`,
ratchet `37`, both untouched) · 9 (entry in the existing `0.6.10` section, no
bump) · 10 (**Owner-UAT approved 2026-07-27**, against the question of whether
`RESOLVED` is the shape wanted in the portfolio's state machine, given it is the
first state added since v0.3 established all six together).

**Scope was narrowed before execution, not delivered as filed.** The brief
carried three manifestations under one asserted root cause; the IC ruled that
root cause is a **model, not a defect** (principle 4) and split it. This period
delivered manifestation (a) only.

## What worked

- **Re-verifying a parked stem instead of re-deriving it.** The brief had been
  worked by a third-party review and parked on a territory conflict. Two analysts
  were spent only on the queue note's own reopen condition (*"unless the blast
  radius changed"*), which had been met. Every original claim held but two — and
  one of those two was the whole reason the period needed care.
- **Reading a guard's source rather than its documentation.** The IC found that
  check 15's arrow rule shape is `chr(0x2192)`, not ASCII `->`
  (`tests/test_doctrine_integrity.py:922`). That single fact reclassified
  `REGISTER.md`'s header paragraph — **the one S1 was tasked to edit** — as one
  character from becoming a second declaring paragraph. Neither chief found it.
- **Making the hot path forbidden rather than conditional.** Both chiefs pushed
  for it and the IC ruled it. It cost nothing (no doctrine rule changed) and
  bought two things: criterion 8 became structurally unbreakable, and the
  territory shrank enough to free three queued rows.
- **Sequential execution over a disjoint partition.** The territories *were*
  disjoint, so parallelism was available; the IC declined it because the
  *verification surface* was shared and the state literal was a cross-tasking
  contract nothing enforced. S2 read S1's landed literal instead of trusting the
  plan's copy of it. Cost: one round.
- **Fixing the plan's own defects at lint time rather than at Safety time.** Four
  lint defects were found and **all four were the Dispatcher's, not the chiefs'.**
  The sharpest — criterion 3's word *"agrees"* — would have gone **red before a
  single edit**, because the three enumeration carriers already disagreed
  textually at HEAD. Caught by the Planning Chief, confirmed mechanically, and
  rewritten before any specialist saw it.

## Lessons

- **A guard's predicate is not what its prose says it is; read the source.** The
  difference between ASCII `->` and U+2192 decided whether an ordinary tidy-up
  would silently break Rule C. Prose describing a mechanism is a summary of it,
  and this period twice found the summary insufficient — once for the arrow, once
  for which paragraph actually declares.
- **When a criterion's population is enumerable, the criterion must be the
  command's output, never a hand-listed set — and the enumeration must be run
  before the criterion is written, not after.** Running it at plan time surfaced
  a carrier nobody had named (`dcs/templates/REGISTER.md:71`, the row template's
  own state cell), and the officer later showed the 202 *still* undercounted the
  full population (7 hits, not 4).
- **A criterion asserting agreement between sites must say what "agree" means.**
  Three carriers of one enum already differed in separator and in spelling of
  `MERGED` before this incident existed. "Agrees" read strictly is red on arrival;
  "the same set of values, each site in its own style" is checkable and true.
- **Splitting on principle 4 does not multiply the edits — it orders them.** The
  argument against splitting was that three incidents would each edit the same
  enum. They will not: one creates the state, the others consume it. That holds
  *only* because the definition was made scenario-neutral as a hard bound, which
  is what converted a scope argument into a design constraint.
- **The verifier must be told what the IC already found.** The false CHANGELOG
  sentence was found at step 5 and deliberately **not** fixed before the officer
  saw it. It re-derived the predicate rather than accepting the IC's word, and
  then found three further things the IC had missed — including that S1's own
  arrow evidence reported the post-state as its own baseline. Handing a verifier
  a pre-cleaned tree buys a cheaper verdict and a worse one.

## Deviations this incident

**None.** Read from `214-LOG.md`, not from memory: zero `deviation reported by`
entries, zero `SAFETY-HALT:` sentinels, one stamped `IAP-APPROVED:`, one
`SAFETY-PASS:`. Four command points logged (`typed`, `iap_review ACCEPT`,
`verdict -> close`, plus the advisory triage), and **one escalation** —
trigger **(e)**, an IC-requested ESG activation raised at command point 1, filed
as `.dcs/esg/SITREPS/direct-resolution-lane-p0.md` and answered `continue` by the
Owner, who declined to convene a sixth ESG the same day.

Two specialists, two spawns, both returning `status: done` with schema blocks on
the first attempt. **The fourth clean self-hosted incident**, and the first whose
scope was narrowed by a command-point ruling before any specialist ran.

## Advisory dispositions

Five advisories on a `pass`, per the v0.6.5 default. Dispositions ruled by the IC
at command point 4:

| # | Finding | Disposition |
|---|---|---|
| 1 | `CHANGELOG.md` named the wrong paragraph as check 15's declaring one | **Fixed** in `13f557d`, with the regenerating command added beside it |
| 2 | S1's ASCII-arrow evidence reported the post-state as its own baseline (`4 → 4`; genuine count went `3 → 4`) | **Commit-message note** — the arrow was added on purpose, U+2192 stayed 0 |
| 3 | Criterion 3's census undercounts its own population | **Recorded here** — see below |
| 4 | `REGISTER.md`'s header writer-map omits `/dcs-close` as a `RESOLVED` writer | **Deferred** to register row `register-writer-map-completeness` |
| 5 | `new.md` 7a substep 5's claim about the row template was loose for the Worktree column | **Fixed** in `13f557d` |

**Advisory 3, recorded with its command rather than as a number.** The census
returns **7 hits**, not the 4 the 202 accounted for. Regenerate:

```bash
grep -rnE "QUEUED" dcs/ agents/ skills/ CLAUDE.md README.md --include=*.md | grep -E "ACTIVE|DEPLOYED|PARKED|KILLED"
```

Of those 7: **4 are enumeration carriers** — `dcs/references/forms.md:22`,
`dcs/templates/REGISTER.md`'s value list and row-template cell, plus
`dcs/workflows/status.md:102` which is out of territory and already its own row
(`status-md-enum-drift`). The other **3 are transition prose, not enumerations**
— `dcs/templates/REGISTER.md:8`, `dcs/workflows/loop.md:121`,
`dcs/workflows/new.md:208` — and all three matched at HEAD, before any edit.

## Memory routing

`CLAUDE.md` documents `vault/` (Obsidian, repo-local, never shipped) with a
routing rule: doctrine changes to `doctrine.md`, provenance to
`doctrine-appendix.md`, and maintainer-only knowledge to the vault. **No doctrine
rule changed this period** (a bookkeeping substep is not a rule, and
`doctrine.md` was forbidden territory by IC ruling), so nothing was routed to
either reference file. That is the routing rule working, not a gap.

**Written to the vault** (repo-local, never shipped; verified present by reading
the file back after the write):

- `vault/Meta/building-dcs-lessons.md` **§16** — *"Narrowing scope at the stem
  widened what could run beside it."* Why the anti-split argument (three
  incidents, three enum edits) does not follow, and how it only fails to follow
  because the scenario-neutrality bound was made hard; plus the finding that
  territory width is a **portfolio** cost invisible unless the collision is
  recomputed after the IAP narrows — this session got that list wrong by hand
  twice, once in each direction.
- `vault/Meta/building-dcs-lessons.md` **§17** — *"Hand the verifier what you
  already found."* The IC found a false CHANGELOG claim at step 5 and passed it
  to the Safety Officer unfixed; the officer re-derived it independently and then
  found three further defects the IC had missed. The charter's rule that a
  self-report is a claim rather than a check should extend to the IC's own
  findings.

Nothing was written to `vault/Backlog.md`: the four items this incident produced
are **register rows**, not backlog items, and ranking them is an ESG act.

## Intake source closure

**Register row, not an external system.** `201-BRIEF.md` names the intake as a
third-party DCS review (2026-07-27, bread_bot main session, Fable, Owner-directed
"Phase 1"), reaching this incident via `REGISTER.md` **rank 1**. Closure is the
register's own transition, performed at close step 5a.3 — `ACTIVE` → `MERGED
(deploy pending)`. Nothing external to flag, and no production system was
touched.

Three rows this incident's own stem created (`register-field-repair-path`,
`trivial-work-inline-lane`, `status-md-enum-drift`) plus one its close created
(`register-writer-map-completeness`) are `QUEUED` and **unranked** — ranking them
is an ESG act, and they are recorded as owed to the next sweep in both
`REGISTER.md`'s Notes and the p0 sitrep.

## Deploy status

**Not deployed.** The fix ships by `install.ps1` — every changed file except
`CHANGELOG.md` sits under `dcs/` and is in the installer payload; `CHANGELOG.md`
is in `package.json`'s `files` whitelist only, so it reaches users on a future
`npm publish`, an Owner act with a 2FA OTP that no session performs.

**The version marker will be blind to this ship**, as it has been for the last
four: `dcs/VERSION` and `~/.claude/dcs/VERSION` both read `0.6.10`. This is the
**first train that reads the content-shaped step 7** installed by
`deploy-marker-blind`, so no Owner-authorised substitution is needed — the
witness is `python tests/payload_check.py`, resolved per `deploy.md` step 7.

**No version bump, on a fact measured at close rather than carried from plan
time** — which is the whole reason criterion 9 was written to carry its command:
`npm view dcs-command-system version` → **0.6.9** against `dcs/VERSION`
**0.6.10**, so 0.6.10 is genuinely unpublished and the entry belongs in that open
section. That re-measurement is the exact discipline register row
`criterion-unmeasured-fact` (rank 2) exists to make routine, and it cost one
command.

## Owner-UAT

**Done, 2026-07-27.** Approved against the concrete question of whether
`RESOLVED` is the shape wanted in the portfolio's state machine, with the state's
full definition, the enum line and the new 7a substep shown. The Owner accepted
without qualification.

## Safety Officer's final verdict (verbatim, from SAFETY.md)

`verdict: "pass"`, `refutations: []`, five advisories, `checked[]` of 26 items.
The full block is transcribed verbatim in `SAFETY.md`; its two non-mechanical
reads, which the IAP's verification plan said a green suite could not supply:

> **Scenario-neutrality, read not grepped.** *"Yes, both split-out incidents
> consume it unchanged … `register-field-repair-path` is served too, and I want
> to name the one place I thought it might not be: a field repair to a live
> system could be read as having 'entered the deploy lifecycle.' It has not, in
> the sense this enum uses — the neighbouring `MERGED` and `DEPLOYED`
> descriptions define the deploy lifecycle as the `/dcs-deploy` train over a
> merge commit, and a worktree-less field repair has no merge commit to carry."*

> **The Rule-B hole.** *"Intact. `REGISTER.md`'s `DEPLOYED` bullet is
> byte-identical to HEAD, `deploy.md`'s step 7 is still numbered 7 … S1's
> insertion landed after `KILLED` and inside the same unbroken paragraph, so it
> neither split the declaring paragraph nor created a second one."*
