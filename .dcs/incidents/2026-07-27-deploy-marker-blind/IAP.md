# IAP — Incident Action Plan (**revision 2**)

**Incident:** deploy-marker-blind
**Type:** 1
**Operational period:** 1 · **Revision:** 2 (attempt 2)
**Links:** `202-OBJECTIVES.md` (rev 2) · `203-ORG.md` (rev 2) ·
`204-TASKING/S1-CONTRACT.md`, `S2-GUARD.md`, `S3-RECORD.md`,
`S4-RECONCILE.md` · Logistics plan below (Type 1)

> **This IAP supersedes revision 1 and voids its approval by hash.**
> Revision 1's *work* stays on disk and is Safety-proven for criteria 1-4
> and 6-8 — what is voided is the plan's authority, not the diff.

## Why revision 2 exists

Two Safety halts. **Convergence read: SAME CLASS** — three refutations of
one form, *two statements of one contract disagreeing*: `deploy.md` step 4
vs step 7; `CLAUDE.md:40` vs step 7; `REGISTER.md`'s `DEPLOYED` definition
vs its facts-only block thirteen lines below. Halt 1's two are closed and
verified; halt 2's is open.

**The mechanism was measured, not guessed.** Revision 1's criterion 5
defined its population by **vocabulary** while the defect is defined by
**role**. The halting line reads *"DEPLOYED only after the project's
deployed marker was read"* and matched none of its four patterns — so
criterion 5 was **met at both halts** while the class kept shipping. Old
enumerator: **4** hits. New: **18 in 6 files**. Only the new one returns
`REGISTER.md:59-60`.

Per doctrine principle 13 (v0.5.9) the answer to a same-class recurrence is
to **raise the altitude**, and the Owner took that at first offer — so the
rotation stopped at two halts rather than four.

**Halt count is 2 of 3.** Stamping this IAP resets it. That reset is a real
cost of this route, stated in the 209 and accepted by the Owner; it is not
a free retry. Plan for an officer with nothing left to find.

## Objectives (summary of 202 rev 2)

**Goal.** `/dcs-deploy` can tell a shipped payload from an unshipped one
using evidence that changes when the **content** changes — so a correct
ship that deliberately did not bump the version verifies as shipped, an
unshipped `MERGED` row is never recorded live, and the witness exists as a
runnable command in the repo. **Extended:** and every site in the package
that states that contract says the **same** thing, held there by a
**mechanism** rather than by a criterion in one incident's 202.

**Carried unchanged, Safety-proven, not re-litigated:** 1 witness exists,
payload set derived by walking · 2 witness proven RED on a scratch copy, no
install · 3 step 7's stop condition content-shaped · 4 step 4 defined for a
readable non-commit-ish marker · 6 `CLAUDE.md`'s Deploy table states what
step 7 enforces, all four exit classes · 7 CHANGELOG in the existing
unpublished 0.6.10 section · 8 three suites green from their own
`N/M passed` lines. **Criteria 1 and 2 are tagged `[already delivered — no
tasking]`:** `tests/payload_check.py` is forbidden to every tasking, and
criterion 12 asks for a check that its constants *stay* aligned, not for an
edit.

**5 (revised).** No surviving site in the population presents the version
marker as sufficient proof of a ship, population defined by **role**:

```bash
grep -rniE 'deployed[- ]?(version )?marker|deployed_sha|marker (actually )?advanc|VERSION.*after deploy|DEPLOYED only after|deploy(ed|-)?[ -]evidence|deployed[- ]content|content witness|payload witness' dcs/ agents/ skills/ CLAUDE.md README.md docs/
```

**18 hits in 6 files** at plan time — `deploy.md` 10,
`dcs/templates/REGISTER.md` 3, `skills/dcs-deploy/SKILL.md` 2,
`dcs/workflows/close.md` 1, `CLAUDE.md` 1, `docs/spec-v0.3-parallel.md` 1.
The command's **live output** is the population, not this list. `bin/**` is
outside it and is not a refutation.

**5a.** Negative control — the new enumerator must be **shown** to return
`REGISTER.md:59-60` where the old does not. *This incident has already
shipped one thing that looked like new capability and was a relabel.*

**10 (new).** No file states the contract two ways.
**11 (new).** A durable guard binds contract-declaring sites to step 7's
live text.
**12 (new).** The two copies of `EXCLUDED_DIRS` / `BYTECODE_SUFFIXES` held
together by reading source text, never by import.
**9 [Owner]** UAT — scheduled explicitly after Safety, per the IC's open
question, so the guard's self-referential PASS is not read as covering
correctness.

## Tactics (from the Planning Chief)

1. **Raise the altitude the way the measurement points.** The guard's
   population predicate keys on **role and nothing else** — `DEPLOYED`
   co-occurring with proof language. **No marker vocabulary appears in the
   predicate at all, because vocabulary is precisely what failed.**
2. **One statement per file, one source per package.** Not "reconcile them
   harder": only `deploy.md`'s step 7 states dispositions, every other site
   cites it in a fixed form, and no non-source file carries more than one
   declaring paragraph. **That last rule is what catches halt 2
   phrasing-independently** — the second paragraph is red for *existing*,
   whatever it says. Agreement checking alone would not have caught it,
   because *"only after … an ancestor of it"* is a **necessary condition,
   not a per-class disposition**, and a comparator reads straight past it.
3. **One hand owns all the prose.** Revision 1 split the surfaces and the
   halt landed exactly on that seam. Re-splitting recreates it.
4. **The guard is built from checks 13 and 14, minus their two known
   gaps** (`check-14-hardening`, rank 3): a declaring site that drops its
   citation entirely is RED here, and the one-per-file rule is tree-wide.
5. **Teach the guard the source's deliberate asymmetry without
   special-casing.** Step 4's shape branches state **pre-deploy**
   dispositions and never say `DEPLOYED`, so they are simply not
   declaring. Step 4's out-of-band paragraph *does* move rows to
   `DEPLOYED` — so it is in the population and must cite step 7, which is
   criterion 10's second known instance.
6. **Prove everything in scratch copies; mutate nothing.**

## IC rulings at command point 2 — binding

**(i) Criterion 11's literal rule takes the NARROW reading.** S2 may pin
**exactly one** named anti-erasure floor — `dcs/templates/REGISTER.md`, the
halt-2 site — as a *"population must include"* assertion. Shipped
precedent: `tests/test_doctrine_integrity.py:549-555`, check 13, does
exactly this with `agents/dcs-commander.md`. **The pin is a floor on a
walked population, not a population source**; the hazard the no-literal
rule guards against is a *fitted list*, which a floor is not.

**(ii) The 265-line ceiling holds as the target, with a bounded band.**
Compressing step 4's shape branches into citations of step 7 is the
intended payment — and it *is* the one-statement-per-file fix, not a tax.
If honest compression cannot fit the three step-7 additions, S1 is
pre-authorised to overrun to **at most 275 lines, every line past 265
inside step 7's disposition section**, with the count and justification in
its return. **The step-4 / step-7 asymmetry is a protected element.** Any
pressure to delete it, or any need beyond 275, is a **deviation to the
IC**. Rejected: raising the ceiling wholesale (loosening a binding on no
evidence) and holding it hard (a specialist squeezing under a hard ceiling
deletes the asymmetry silently).

**(iii) Rule C holds TREE-WIDE.** `CLAUDE.md`'s table row and the paragraph
beneath it collapse to one; `SKILL.md`'s frontmatter and objective carry
dispositions in one place; `docs/spec-v0.3-parallel.md` is made
**non-declaring**, never path-exempted. The chief's fallback — scoping to
`dcs/` and `skills/` — was **rejected because it drops `CLAUDE.md`**, both
a halt-1 refutation site and where the flawed contract was normatively
stated.

**(iv) The fourth specialist slot is USED, read-only.** S4-RECONCILE runs
after S1-S3 and before Safety: the officer's own manual read, performed
early. No write access, no territory; findings route as fix-taskings to the
owning specialist. This is the one fourth use that **cannot recreate the
seam**.

**(v) The self-blocking-guard escape is written into this IAP now, in
advance.** A future incident fixing a **too-strict** check 15/16 is
otherwise red by construction — the guard is the merge gate, so the fixing
incident must pass close step 1a while running the broken guard. The path:
**escalation trigger (a), plus an Owner-authorised, logged, one-time bypass
of close step 1a for that fixing incident only.** Pre-defining it removes
the need to invent it under a red gate; it remains an **Owner act** at
exercise time.

**(vi) P3's non-emptiness condition is BINDING.** The `ba6019e` proof is
valid **only if** check 15 **prints** its derived population size and
parsed token set on that tree and **both are non-empty**. Green without the
printed counts is not evidence — the old step 7 enumerates **no** exit
classes, so an empty population would pass by finding nothing. The baseline
is `git archive` of the **literal sha `ba6019e`, never `HEAD`** — verified:
HEAD currently **equals** it and will silently diverge at the first commit.

## File-territory partition

| Specialist | Territory | Order |
|---|---|---|
| **S1-CONTRACT** | `dcs/workflows/deploy.md`, `dcs/workflows/close.md`, `dcs/templates/REGISTER.md`, `skills/dcs-deploy/SKILL.md`, `CLAUDE.md`, `docs/spec-v0.3-parallel.md` | 1st |
| **S2-GUARD** | `tests/test_doctrine_integrity.py` | 2nd |
| **S3-RECORD** | `CHANGELOG.md` | 3rd |
| **S4-RECONCILE** | **none — read-only** | 4th |

**Partition status: disjoint, executed SEQUENTIALLY** — and the sequencing
is the fix, not a performance compromise. S2's population, citation form
and live step number all come from S1's finished prose; running them
together would have S2 writing a comparator against text that is still
moving, and *"two artefacts built against different snapshots of one
contract"* is the exact failure this incident is at halt 2 over. The IC
verified disjointness by inspecting the explicit file lists rather than
accepting `partition_ok: true`.

**In no territory, in every forbidden list:** `install.ps1`, `install.sh`,
`package.json`, `dcs/VERSION`, `bin/**`, and — deliberately —
`tests/payload_check.py`, which is Safety-proven and whose constants
criterion 12 asks to *hold*, not to edit. Touching any of them is a
deviation and an IAP re-approval.

## Deploy / environment plan (Type 1, Logistics Chief)

**Reach split, measured** (`npm pack --dry-run` → 75 files):
**(a) reaches a consuming project via `install`** — `deploy.md`,
`close.md`, `templates/REGISTER.md`, `SKILL.md`: these four and nothing
else. **(b) registry only, via `npm publish`** (an Owner act with an OTP no
session performs) — `CHANGELOG.md` and everything under `tests/`, which
ride the tarball but are **never copied into `~/.claude`**. **(c) guards
only this repo's merges, reaches nobody** — `test_doctrine_integrity.py`
as merge gate, and **`CLAUDE.md`, absent from BOTH the installer payload
AND `package.json`'s `files`**, so criterion 6's edit ships to no user by
any route. That is correct under ship-no-project-facts.

**Environment.** No new env vars, no new dependencies, **no `package.json`
change and none permitted** — `tests/` is already whitelisted, verified.
Stdlib-only Python throughout.

**Version.** No bump. `npm view dcs-command-system version` → `0.6.9`,
repo `0.6.10` — unpublished. **Re-measure at close**; it is external
volatile state.

**Ordering — three runs at close step 1a, in order.**
**R1** the suite in the worktree (ordinary signal).
**R2 — the merge-content run, and the one that matters:**
`git archive <branch tip>` extracted **outside both checkouts**, suite run
from there. `tests/payload_check.py` and the incident directory are
currently **untracked**, so R1 sees files the merge would not carry unless
`git add`ed.
**R3** after `git merge --no-ff`, on the merge result, before flipping the
register row. `close.md` step 1a positions the guard *before* the merge
while describing it as a merge-result check; that gap is harmless only
while main is still at `ba6019e` — confirm `git rev-parse main` first, and
if main advanced, R3 is mandatory. **R3 red is escalation trigger (a).**

**Deploy-time.** Revision 1's verdict stands and is now evidenced: this
train runs the **OLD** step 7 (loaded from `~/.claude` at step 0; the new
text lands at step 6) and will report "did not advance". **Sharpened: the
substitution is no longer a by-hand sha256 comparison — the merged tree
carries the witness.** Evidence is `python C:\DCS\tests\payload_check.py`
from the main checkout **before** step 6 (expect exit 1, differing: 4,
naming the four payload files) and **after** (expect exit 0, or exit 3 if
pre-existing debris shows as installed-only, which is not a stop). Record
both full outputs, not exit codes alone. **The Owner's pre-authorisation is
single-use:** if the before-run returns exit 0, its premise is broken and
the correct action is stop-and-report, never substitute again.

**Rollback — three surfaces, two corrections from revision 1.**
**(A) Payload:** `git checkout ba6019e` in `C:\DCS` and re-run the same
install; idempotent overwrite. Revision 1's "no residue" **holds, but for a
narrower reason than stated**: neither installer deletes, so a re-install
can never remove what a forward install added — no residue is true here
**only because this period adds zero new payload files.** If execution adds
one, the claim dies and rollback needs an explicit delete list.
**(B) Guard: cannot be rolled back by re-installing** — `tests/` was never
copied. **Too strict is self-blocking** (ruling (v)). **Green-when-it-should-be-red
has NO rollback**, because nothing visibly breaks — it simply stops
protecting, silently, *exactly as the deployed-version marker did for three
consecutive ships*. That asymmetry is why criterion 11's degeneracy guard,
criterion 5a's control and the forged-input self-tests are load-bearing
rather than decorative.
**(C) Merge:** R3 red → no push has occurred, `git reset --hard ba6019e`
restores the tip — the Owner's call, not authorisation.

## Risks

- **S2 may find S1's prose non-compliant. That is the mechanism working**,
  not a plan failure — the first time anything has been able to detect this
  class. S2 must **not** edit prose; it raises a deviation naming file,
  paragraph and failed rule.
- **The guard is narrower than criterion 5, deliberately.** It holds
  **disposition-stating** sites; `close.md:66`'s exemplar phrasing states
  none, so criterion 5's human walk catches it. Widening the predicate
  would mean returning to vocabulary matching, **which just failed twice.**
  Honest statement for the AAR: *the mechanism holds the contract's
  dispositions forever; its vocabulary still needs a walk.*
- **The guard grades its own incident's merge.** Three named modes:
  *self-referential green* (it proves the sites **agree**, never
  agreement-on-**right** — only Owner UAT and Safety cover correctness, so
  its PASS line must not be read as closing that); *fitted to the data* (it
  will be iterated against this tree until green — `ba6019e` is the sole
  out-of-sample datum); *truncated run read as pass* (the module
  `sys.exit()`s at file scope with no runner, so an exception mid-file
  prints accumulated PASS lines then a traceback — **every suite result in
  evidence carries its final `N/M` line AND its exit code**).
- **Vacuous green on P3** — addressed by binding ruling (vi).
- **Extracting an archive inside either checkout would poison the suite** —
  check 8 walks `REPO.rglob('*')` filtered only by
  `{.git, node_modules, __pycache__}`.
- **Untracked files absent from the merge** — R2 is the cheap detector.
- **Hot path: 1,205 B spare** (36,683 of 37,888). Criterion 5's role-shaped
  population could reach into `doctrine.md` / `schemas.md`, which would
  turn the merge gate red at close. **A scope change to escalate at
  proposal time, not an edit** — carried verbatim from the Logistics risks
  as the IC directed.
- **Encoding tripwires:** check 8 walks the whole repo **including
  `.dcs/incidents/`**, so one BOM in an incident artifact reds the merge
  gate; checks 9/10 scope to `SHIPPED_DIRS`, which **includes `tests/`**.
  `.gitattributes` protects the git object, not the working-tree bytes the
  check reads.
- **Forbidden-list drift under pressure.** `payload_check.py`'s header
  cites installer line numbers, currently accurate. A specialist finding
  them stale fixes the **comment**, never the installer.
- **Ceremony mismatch, unchanged and still correct.** The delivered
  territory is workflow + tests + prose, Type-3-shaped, while the incident
  is typed 1. Typing is fixed at the stem. **Do not re-type mid-incident.**

## Verification plan

1. **Re-derive the 201 path at end state.**
   `git merge-base --is-ancestor aab9f06 0.6.10` still exits 128 — **the
   world is unchanged and that is correct**; what must have changed is that
   `deploy.md` now has a defined non-stopping branch for a
   readable-but-not-commit-ish marker (step 4) and a content-shaped stop
   condition (step 7). Confirm the three field instances would each resolve
   **without** an Owner authorising a substituted check.
2. **The contract is stated once.** Walk criterion 5's output asking the
   **role** question of every hit, not the vocabulary question. **If the
   tree is green and two declaring paragraphs are found in one file by eye,
   the GUARD is the defect, not just the prose.**
3. **The mechanism actually binds — verify it, don't read about it.**
   Independently reproduce at least P1 and P2 in a fresh scratch copy, and
   confirm the anti-erasure direction (delete a declaring paragraph
   outright → not green by subtraction). *A guard that only goes red on the
   forgeries its own author chose is not a guard.*
4. **The new population reaches further than the old** — both enumerators;
   and check 15's own population is derived by walking, with only the two
   authorised file literals.
5. **Both rulings survived:** `wc -l deploy.md` ≤ 265 (or ≤ 275 justified),
   no `payload_check` / `~/.claude` / `dcs/VERSION` literal, and the
   step-4 / step-7 asymmetry intact.
6. **Three suites**, each from its own `N/M passed` line **and exit code**.
   The integrity total will have moved past 73 — read the live line.
7. **Nothing shipped that should not have.**
8. **Manual, and it matters more than any command here.** Read
   `REGISTER.md` end to end as a maintainer instantiating it; read
   `deploy.md` steps 4 and 7 back to back as an operator. Looking for the
   same thing that halted this incident twice: two places in one document
   answering one question differently. The commands catch that only where a
   disposition token is present.
9. **Criterion 9 is the Owner's** and is not closable by the Safety
   Officer — scheduled explicitly after Safety.

## Deviation history (this period)

- **Halt 1** (2 refutations, both closed): step 7 not shape-aware while
  step 4 was; `CLAUDE.md:40` vs step 7 on exit 2. IC disposition:
  fix-taskings. See `214-LOG.md`.
- **Halt 2** (1 refutation, open — the reason for this revision):
  `REGISTER.md`'s definition vs its facts-only block. Escalation trigger
  (b), convergence read **same class**, 209 filed, Owner chose **pivot —
  raise the altitude**. See
  `<esg_root>/.dcs/esg/SITREPS/deploy-marker-blind-p1.md`.
- No specialist deviations. Six specialist spawns so far, all returning
  `done`.
