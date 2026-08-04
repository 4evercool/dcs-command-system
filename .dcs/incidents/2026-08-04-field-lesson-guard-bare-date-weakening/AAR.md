<!--
AAR.md -- After Action Report, written by the IC during /dcs-close. Requires
a green (pass) Safety Officer verdict to exist before this file is written
-- close.md enforces this, do not write an AAR to paper over a halt.
-->

# AAR — After Action Report

**Incident:** field-lesson-guard-bare-date-weakening
**Type:** 3 (IC proposed 1; Owner overrode at the typing gate — see 201)
**Opened:** 2026-08-04
**Closed:** 2026-08-04
**Operational periods:** 1 (two attempts: halt → fix-tasking F1 → pass)

## Outcome

All 8 acceptance criteria of the period-1 202 verified by the Safety
Officer's independent re-derivation (SAFETY.md, attempt 2, 0 refutations):

1. Check 20a flags a same-line bare-date-only claim — fixture
   `tests/fixtures/field-lesson-guard/bare-date-claim.md` + self-test;
   the officer re-ran OLD vs NEW regex over the fixture (OLD accepts,
   NEW flags).
2. `multiline-claim.md` / `undated-claim.md` byte-identical
   (hash-compared to their main blobs) with unchanged outcomes.
3. Strict rule holds package-wide, enumerated by the guard's own loop
   (`python tests/test_doctrine_integrity.py` green) — and the shipped
   `_FL_ID_RE` source line read directly: three alternatives, no date
   branch (the anti-re-widening check).
4. Check 20a's docstring now matches the enforced rule, including both
   named exemptions with reasons.
5. `bcf9468`'s identifier stuffing removed at all enumerated sites.
   **Recorded disposition at `doctrine-appendix.md:670`:** criterion 5
   is met there as *stuffing-removed*, not *identifier-erased* — the
   in-sentence `v0.6.9` is TRUE (the section quotes the original v0.6.9
   ceiling text) and grammatical, and it stays by explicit IC decision
   (214-LOG command point 4). A later reader should not re-open that
   question.
6. `_SENTINEL_TOKENS` names all four sentinels; the fourth
   (`RECORD-CORRECTION:`) documented truthfully in `forms.md` (parsed by
   `record_integrity.py`, NOT classified by `sentinel_of()`, no fourth
   `--sentinel` choice) and named in `doctrine.md` principle 13's
   running prose; no fenced occurrence anywhere in `dcs/**/*.md`;
   `dcs/hooks/**` untouched.
7. Hot-path budget green with **25 B of slack** (as of the integration
   commit `54d5b41` — it moves; regenerate with
   `python -c "import os;p='dcs/references/';a=os.path.getsize(p+'doctrine.md');b=os.path.getsize(p+'schemas.md');print(a,b,a+b,37*1024-(a+b))"`).
   The next doctrine.md addition requires a paired trim — the budget
   check is fail-closed at merge time.
8. Suites at close, each read from its own run: 268/268 (was 266 — +2
   named cases, the exemption-staleness check and the bare-date
   self-test), 100/100, 18/18.

**Deploy status:** NOT deployed. The merge rides the same **held** train
as its parent `field-lesson-guard-vacuity` (deploy held by Owner
direction pending exactly this fix); `/dcs-deploy` is the next act, and
`~/.claude/dcs/` still runs the pre-fix copy until then.

**Owner-UAT:** none defined in the IAP — not applicable.

## What worked

- **The strict-regex-plus-named-allowlist design (tactics T1/T3)**
  survived adversarial review intact: the officer's mutation test
  confirmed the 2-entry allowlist is load-bearing for exactly the two
  named heading lines and grants nothing else, and the staleness case
  makes a stale exemption fail loudly.
- **Criterion 3's anti-re-widening pairing** (fixture + Safety reading
  the shipped regex source directly) — designed at plan time against
  the exact failure mode of the parent incident — was executed as
  specified.
- **Criterion 5 as an invariant** ("every identifier `bcf9468`
  inserted", enumerated by `git show`) instead of the intake's
  three-line census: the chief's reading surfaced a fourth site (the
  title line) the census missed, and the officer surfaced a fifth
  (:414) already covered by S2's rewording.
- **The disjoint 3-way partition** produced no territory violation and
  a trivially clean integration; peer-caused mid-flight reds were
  named, never cross-repaired.

## Lessons

- **Relocate-instead-of-remove is the failure mode of "remove the
  identifier" taskings.** S2 moved `v0.5.0` from a parenthetical into a
  load-bearing sentence — and the sentence was false. The guard cannot
  distinguish a true identifier from a false one; only provenance
  checking can (`git log -S` on the phrase the claim dates). Caught by
  the Safety Officer doing exactly that, pre-merge — the same class the
  parent shipped undetected.
- **A "since vX.Y.Z" claim is a measured claim about history** — verify
  with `git log -S` + `git show <commit>:dcs/VERSION` before writing it,
  the same discipline 202 criteria already require for out-of-tree
  facts.
- **Folding two defects into one incident worked here** (same file, same
  train, ESG-decided) but consumed the hot-path slack down to 25 B —
  the byte cost of the second defect's documentation landed on the
  first defect's budget.

## Deviations this incident

From `214-LOG.md` (the full record): no specialist deviation returns; no
202/IAP amendment; one tasking-lint defect fixed pre-review (S1's
pseudo-glob, logged 17:14); one Safety **halt** (attempt 1, 17:51 — the
false `Since v0.5.0` claim at `doctrine-appendix.md:13`) resolved via
fix-tasking F1 (fresh spawn) and a re-spawned Safety Officer's pass
(18:06). Command points 1 (typing, Owner override to Type 3), 2 (IAP
accept), 4 twice (halt → fix_taskings; pass → close) all logged; command
point 3 never fired (no deviation).

## Memory routing

Per CLAUDE.md's three-store rule (doctrine / appendix / vault): nothing
here changes a DCS rule (the rule change IS the shipped fix), so no
doctrine or appendix lesson. Vault (maintainer store), written in the
worktree and carried by the merge:

- `vault/Post-mortems/field-lesson-guard-bare-date-weakening.md` — the
  relocate-instead-of-remove pattern, the provenance-check lesson, and
  the hot-path spend, with citations into this incident's artifacts.
- `vault/Backlog.md` item 31 banner — one line appended recording the
  fold is discharged by this incident (shipped with `54d5b41`).

## Intake source closure

Register row `field-lesson-guard-bare-date-weakening`
(`.dcs/esg/REGISTER.md`) — internal, updated mechanically at close
(`ACTIVE` → `MERGED (deploy pending)`); no external system to flag.
`vault/Backlog.md` item 31 was already marked FOLDED at the eighteenth
`/dcs-esg`; its discharge is recorded in the banner (memory routing
above) — the item's final strike-through belongs to the next `/dcs-esg`
sweep, not to this close. The parent's held deploy is now unblocked:
flagged for the Owner — run `/dcs-deploy` to ship both rows on one
train.

## Safety Officer's final verdict (verbatim, from SAFETY.md)

See `SAFETY.md` "Attempt 2 — PASS (2026-08-04, re-spawn
a53c777d0eee51324, after fix-tasking F1)" — copied there verbatim at
verdict time (0 refutations, 4 advisories, 17 `checked` entries); this
AAR's Outcome section restates its criterion-by-criterion findings and
the two advisory duties it assigned this AAR (the 25 B figure with its
regenerating command, and the criterion-5-at-:670 disposition), both
discharged above.
