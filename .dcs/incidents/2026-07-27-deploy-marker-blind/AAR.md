# AAR — deploy-marker-blind

**Incident:** deploy-marker-blind · **Type:** 1
**Opened:** 2026-07-27 09:09 (+1100) · **Closed:** 2026-07-27 (+1100)
**Operational periods:** 1 · **Stamped attempts:** 2 · **Safety Officer spawns:** 5
**Driven by:** `/dcs-run deploy-marker-blind` (attended auto-chain)

## Outcome

**Goal met.** `/dcs-deploy` can now tell a shipped payload from an
unshipped one by evidence that changes when the content changes. Every
acceptance criterion is met on a Safety Officer's independent evidence,
criterion 11 as amended by the Owner at the third-halt escalation, and
criterion 9 (Owner UAT) approved at close.

Delivered, in `916bebc`:

- **`tests/payload_check.py`** — the witness that had been rebuilt by hand
  three times, now a command. Per-file sha256 against the installed tree;
  four classes with exits `0`/`1`/`3`/`2`. **Its payload set is derived by
  walking**, not listed — proven by injecting files it had never seen and
  watching all three surface as repo-only. Exit 3 exists because neither
  installer deletes, so stale extras are debris rather than a failed ship;
  exit 2 keeps *"cannot check"* distinct from *"differs"*.
- **`dcs/workflows/deploy.md`** — steps 4 and 7 rewritten shape-aware, with
  step 7 the **single source of every disposition**. A marker that did not
  move is explicitly not a stop condition. The step-4 / step-7 asymmetry
  for the cannot-check case is deliberate and now says so.
- **Checks 15 and 16** — suite **73 → 82**, read from its own line.
- **`CLAUDE.md`'s Deploy table** — states the contract step 7 actually
  enforces, all four exit classes.

**Not delivered, deliberately, and recorded as unmet rather than dropped:**
check 15 does **not** verify disposition *content*, and **cannot reach
`CLAUDE.md`** (which contains zero `DEPLOYED` tokens). IC directive (iii)
aimed to hold rule C over `CLAUDE.md` and that aim is unmet.

## The number that matters: 5 officers, 4 halts, 3 of them one class

This incident cost far more than its diff suggests, and the reason is
legible.

| Halt | Refutation | Class |
|---|---|---|
| 1 | Step 7 lost the shape-awareness step 4 kept; `CLAUDE.md:40` vs step 7 on exit 2 | two statements of one contract disagreeing |
| 2 | `REGISTER.md`'s definition vs its facts-only block 13 lines below | **same** |
| 3 | The **guard built to end the class** was defeated by markup; four forgeries stayed green | **same, one level in** |
| 4 | `CHANGELOG.md` still claimed the withdrawn rule B | **different** — a seam |
| 5 | — | **pass**, 11 attacks survived |

**Each detector was defeated by a narrower surface assumption than the
last: vocabulary → token → markup.** That is the single most valuable
thing this incident learned, and it was only visible because the
convergence read was performed honestly three times.

## What worked

- **The convergence read did its job, and it is why this never rotated.**
  Doctrine principle 13 (v0.5.9) requires it from the second halt. Twice it
  came out *same class* and forced an altitude raise rather than another
  site fix; once it came out *different class* and correctly permitted a
  plain continue. **The Owner took the leading option at first offer all
  three times**, so a rotation that the field lesson behind v0.5.9 records
  running to four halts on one objective stopped at three.
- **The measurement, not the argument.** At halt 2 the recurrence mechanism
  was not asserted — it was measured: the binding enumerator returned **4**
  hits where a role-shaped sweep returned **22**, and the halting line
  matched none of its patterns. That number is what made "raise the
  altitude" concrete instead of aspirational.
- **The negative control (criterion 5a) earned its place.** It was added
  because *"this incident has already shipped one thing that looked like
  new capability and was a relabel."* Every officer ran it, and every
  officer confirmed the new enumerator reaches `REGISTER.md`'s facts-only
  region where the old one does not.
- **One prose owner.** Revision 1 split the contract surfaces across two
  specialists and **halt 2 landed exactly on that seam**. Revision 2 gave
  all six declaring files to one hand and the seam did not recur.
- **The read-only fourth specialist.** The Planning Chief argued the only
  credible fourth was a second prose owner — the measured cause of halt 2.
  The IC used the slot for a **read-only** reconciliation pass instead, and
  it earned it: it re-implemented the declaring predicate itself to
  enumerate the nine paragraphs the tightening excluded, and reproduced the
  `ba6019e` red rather than reading about it.
- **Specialists reporting against themselves.** S1-CONTRACT flagged that
  its own `SKILL.md` wording might redden rule C, and handed it to S2-GUARD
  as a named test case. S2-FIX2 reported that `CLAUDE.md` still could not
  enter the population **and refused to bend the predicate to force it**.
  S3-RECORD caught a false disposition claim in a draft it inherited by
  reading the actual diff.
- **The IAP predicted halt 4 and prescribed its own mitigation.** Its risk
  list said the CHANGELOG *"is written in parallel with the changes it
  describes… stale by construction"* and directed the officer to diff it
  against the real diff rather than the IAP. Officer 4 did exactly that and
  caught it.

## What did not work

- **Three attempts to build a role-shaped detector inside a regex suite.**
  The honest lesson is not "try harder" — it is that a recognizer keyed on
  surface form cannot enumerate a population defined by role, and each
  narrowing looks like progress from inside. The resolution was the Owner's:
  **narrow the claim to what the check demonstrably enforces.** A guard that
  under-claims truthfully beats one that over-claims greenly.
- **`deploy.md`'s line budget was hit twice** and needed an IC ruling both
  times (265, then a pre-authorised band to 275, landing at 275). The
  budget is a `CLAUDE.md` rule that **no suite enforces** — the hot-path
  check covers `doctrine.md` + `schemas.md` only — so it can only be held
  by someone remembering to measure.
- **Five officer spawns re-derived every criterion from scratch each time.**
  The queued row `safety-officer-incremental-verify` exists for exactly
  this and its evidence just got much stronger.

## Deviation history

**No specialist deviations, none blocked** — ten Ops Specialist spawns
across two attempts, every one returning `done`. Every re-tasking was a
fresh spawn (principle 9b).

Four Safety halts and three escalations, all recorded above and in
`214-LOG.md`. One re-plan (attempt 1 → attempt 2), which voided
`IAP-APPROVED` `b27f7200e4cd` by hash exactly as the deviation doctrine
intends and stamped `215939852854`.

Two IC transcription corrections were caught by the Dispatcher's own lint
rather than by an officer: a directive that would have put `close.md` in
two territories, and one that would have widened a specialist into the
guard validating its own file.

## Safety Officer's final verdict

`pass`, **zero refutations**, five advisories — all fixed by the IC before
the integration commit. Verbatim in `SAFETY.md`, with all five verdicts of
the period tabled. The officer's own note on its closest call:

> *"The one finding I weighed hardest for a halt is advisory 1 — the
> population PASS line survived deleting both named root files. It stays an
> advisory because on the tree under review the line is measurably true,
> the degeneracy condition criterion 11 actually names I proved red in both
> directions, and reaching the false green requires deleting the repo's own
> `CLAUDE.md`."*

That advisory's fix is **proven, not asserted**: deleting `README.md` in a
scratch copy now reddens the population check where it stayed green at
82/82 before.

## Owner-UAT status

**Done.** The Owner approved at close, against the question *"is this the
shape you were reaching for when you authorised the substituted check three
times by hand?"* The check offered was
`python tests/payload_check.py --repo C:/DCS` plus `deploy.md` steps 4
and 7.

## Deploy status

**Not deployed — and the marker cannot witness this ship either.** Verified
rather than assumed at close: `npm view dcs-command-system version` →
`0.6.9` while `dcs/VERSION` and `package.json` read `0.6.10`, so 0.6.10 is
unpublished, no bump was made, and `~/.claude/dcs/VERSION` will read
`0.6.10` both before and after. **This is the fourth consecutive ship the
version marker is blind to — and the last**, because this incident's own
train installs the content-shaped step 7 that every later train reads.

The Owner **authorised that fourth substitution in advance, in writing in
the IAP**, before approval. The substituted evidence is sharper than the
three that preceded it: the merged tree now **carries the witness**, so it
is `python C:\DCS\tests\payload_check.py` before the install (expect exit
1, four differing files) and after (expect exit 0, or exit 3 for
pre-existing debris, which is not a stop). Record both full outputs, not
exit codes. **The authorisation is single-use:** if the before-run returns
exit 0, its premise is broken and the correct action is stop-and-report.

Regenerate the deploy state with `python tests/payload_check.py --repo C:/DCS`.

## Memory routing

Written at close — see the "Memory routing" entries in `vault/`:

- `vault/Meta/building-dcs-lessons.md` — the surface-form detector lesson
  and the one-prose-owner lesson.
- `vault/Backlog.md` — item 12 closed; new items registered.

## Intake source

`vault/Backlog.md` item 12, queued at the 2026-07-26 `/dcs-esg` as register
row `deploy-marker-blind` (rank 1, H). **No external routine owns closure**
— `CLAUDE.md` documents the vault as a maintainer-facing store with no
auto-curating pipeline, so item 12 is marked closed directly at this close
and the register row is transitioned by `/dcs-close` itself.

## Follow-ups registered

- **`doctor-version-only-check`** — split at the stem; `bin/dcs.js`'s
  `doctor()` has the same blind spot in a different consumer.
- **`check-15-role-coverage`** — the two things this incident could not
  make a mechanism hold: disposition-content agreement, and `CLAUDE.md`,
  which states dispositions in exit-code vocabulary and so contains no
  `DEPLOYED` token for any predicate to key on.
- **`deploy-md-line-budget-unenforced`** — the ~250-line workflow budget is
  a `CLAUDE.md` rule no suite checks; it needed an IC ruling twice in one
  incident.
