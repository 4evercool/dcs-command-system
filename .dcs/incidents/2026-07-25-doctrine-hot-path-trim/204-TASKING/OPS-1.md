# 204 — Tasking OPS-1

**Incident:** doctrine-hot-path-trim
**Period:** 1
**Specialist:** dcs-ops-specialist (OPS-1)

## Task

Execute the doctrine hot-path trim end to end, **in this order**.

### (1) LAND FIRST — write the destinations into `dcs/references/doctrine-appendix.md`

Before cutting anything, write into the appendix every destination passage named
in the tactics below:

- A new sub-paragraph under the **existing** `## Transfer of command` (after
  line 44) carrying the model-availability rationale **and** the 2026-07-24
  command-point field lesson in full. It **must** contain the words `quota` and
  `transcript` — criterion 7 probes for exactly those — plus the 2026-07-24
  dating, both halves of the lesson (a real quota-exhaustion kill correctly
  re-spawned on `opus`; a live spawn misdiagnosed as dead from a zero-byte
  transcript that had in fact returned a complete `reject`), and the principle-15
  point that acting on the misdiagnosis would have written a fabricated failure
  into an append-only 214.
- An addition under the **existing** `## The working principles` (after line 89)
  for: principle 4's over-scope cost, principle 6's one-session-one-project
  elaboration, principle 9b's two structural reasons, principle 13's
  four-revisions / 31-hour story, and principle 15's branch-collision
  test-inversion lesson.
- An addition under the **existing** `## Relationship to project-specific
  protocols` (after line 114) for the charter-defect field lesson.
- A **new** `## The lifecycle (Planning P mapped to software)` section for the
  unmerged-proven-work rationale. New appendix headings are safe — the guard's
  check 6 reads headings from `doctrine.md` only.

Preserve the appendix's existing voice and its heading-mirrors-the-core convention.

### (2) THEN CUT from `dcs/references/doctrine.md`

Cut exactly the spans enumerated in T2, T3 and T4 below, keeping every KEEP-listed
rule sentence verbatim or in a strictly shorter kernel that still states the
instruction.

**Use the Edit tool for surgical edits. Never rewrite either file wholesale** — a
whole-file Write flips CRLF to LF, books a ~157 B phantom win against this
period's stated measurement basis, and produces an all-lines diff no Safety
Officer can review.

### (3) MEASURE

If `doctrine.md` is still above **22,268 B**, work the T5 reserve list in priority
order. The reserve is **pre-authorized** (IC ruling, command point 2) — draw on it
without asking, and log each draw in the ledger exactly like a tier-1 cut.

If the reserve is exhausted and it is *still* above: **STOP and return
`status: "deviation"`** with the measured shortfall. Do not cut into any
MUST / NEVER / definition / threshold to make a number. Do not renumber. Do not
rename a heading. Do not touch `schemas.md`.

### (4) RATCHET — last, measured, never guessed

Per T6. Set `HOT_PATH_BUDGET_KB` at `tests/test_doctrine_integrity.py:40` to
`math.ceil(total/1024) + 1` from the **actual post-trim measurement**, and rewrite
the comment block at lines 34–39 to state the derivation, the measured bytes, the
CRLF-worktree caveat, the incident slug, and the regenerating command. **Nothing
else in that file may change.**

### (5) VERSION — atomic

`dcs/VERSION` and the `version` field of `package.json` both to `0.6.5`, in the
same edit sequence, so the guard's check 1 is never left red.

### (6) RETURN THE ROUTING LEDGER

This is criterion 6's artifact and a **required structured field** of your return
(IC ruling, command point 2 — it gets transcribed verbatim into `214-LOG.md` and
carried into the AAR, and the Safety Officer refutes against it row by row).

One row per removed passage:

```
doctrine.md:<baseline line> "<first ~6 words>" (<gross B>) -> doctrine-appendix.md `## <section>` <new|append>
doctrine.md:<baseline line> "<first ~6 words>" (<gross B>) -> redundant with doctrine-appendix.md:NN-NN
```

plus the net byte delta on each row, and reserve draws included. **Every deletion
visible in `git diff dcs/references/doctrine.md` must appear as a row.** A cut with
no row fails criterion 6 even if the byte target is met.

Satisfies criteria 1–9 and 11. Criteria 10 (Owner-UAT) and 12 (deploy) are
explicitly **not yours**.

---

## The cuts, enumerated

### T1 — arithmetic

`schemas.md` is out of scope and fixed at 14,596 B, so `doctrine.md` must land at
**≤ 22,268 B**, i.e. **−4,899 B** from 27,167 B. Every byte figure below was
measured by extracting the span and taking `len(span.encode('utf-8'))`, and was
independently re-verified by the IC to the byte. "gross" = bytes of the span as it
stands; "net" = gross minus the replacement kernel that stays in the core.

### T2 — `## Transfer of command` (net ~1,596 B) → appendix `## Transfer of command`

**[a] `doctrine.md:31`, the model-availability paragraph (1,294 B total).**
Cut the span from `A tier that failed earlier in this session or incident tells
you nothing about now:` through `...cited as a standing condition by every later
attempt.` (**429 B**, gross=net), and the clause `and if it fails again the cost
is one wasted spawn ... than the Owner is paying for` (**165 B**).

*KEEP verbatim in the core:* the Fable=strongest-tier definition; the
`opus` → `sonnet` fallback order; the log format; **"Availability is per-spawn and
MUST be re-tested at every command point (v0.6.1)"**; **"Never cache the fallback,
and never let one failed spawn demote the seat for the rest of the incident"**;
**"try the preferred tier first every single time"**; and the NEVER-acceptable
Dispatcher-decides-itself clause.

**[b] `doctrine.md:38`, the empty-return bullet (1,452 B).**
Cut from `Transcript size and file mtimes are harness artifacts` through
`...a fabricated failed-attempt entry into the 214.` (**689 B** — this span
contains the literal string `Field lesson` and is therefore **mandatory for
criterion 2**), and the sentence `A spawn is dead only if it ended without a
decision block - not because its transcript file looks empty, not because no files
changed, not because it has been quiet.` (**167 B**). Replace both with **one
clause of at most ~90 B** keeping the proxy list, e.g.
`— not transcript size, not file mtimes, not silence, all harness artifacts.`

*KEEP verbatim:* **"An empty or errored return is a FAILED spawn, not a slow
one"**; the no-decision-block definition of dead; re-spawn on the next tier; log
**both** attempts; never wait on a corpse; never resume it (principle 9b); never
let a dead spawn become the reason the Dispatcher decides alone; **"Liveness is
measured by the decision, never by a proxy"**; **"Ask the session what the agent
returned; never infer it from the filesystem."**

**[c] `doctrine.md:37`** — cut the trailing rationale `a command-point agent
writes nothing by design (single-writer rule), so its working time is
indistinguishable from a hang unless it was announced` with its leading em-dash
separator (**~150 B**). The announce instruction itself stays.

**[d] `doctrine.md:35`** — delete the lead-in line
`**(v0.5.10)** Two rules, both about making the pause legible instead of
ambiguous:` and its blank line (**86 B**). The two bullets follow the `###`
heading directly.

**THE WRITE-THEN-CUT (criterion 7):** the appendix has **no** Transfer-of-command
counterpart for any of this, so [a]+[b]+[c] must be **written into the appendix
first**, per step (1) above.

### T3 — `## The working principles` (net ~2,273 B)

Destinations: appendix `## The working principles` (after line 89), **except**
where marked redundant.

**Principle 4** (line 57) — cut `and nothing downstream can undo an over-scoped
201: the halts, rejects and escalations all fire correctly and all of them cost
hours` (**132 B**) and the example `("rethink how X is accounted")` (**30 B**).
The sentence must still end at `Type 1 authorizes the full org, never unbounded
scope.`
*KEEP:* ceremony-never-size; one-incident-one-defect with its definition;
register-each-open-the-critical-path (`new.md` 4a); model-goal → STRATEGY item.

**Principle 6** (line 59, 1,086 B) — cut from `so a session rooted in repo A opens
A's incidents` through `...rather than leaving it to be discovered.` (**445 B**),
replaced by a **≤ 155 B** kernel keeping the consequence *and* the enforcement,
e.g. `A cross-project territory is silently ungated (the gate cannot judge a tree
it has no `.dcs/` for), so `plan.md` lint check 8 refuses it at plan time.`; also
cut `keeps their `git merge --no-ff` into main trivially clean` (**57 B**).
*KEEP:* disjoint territories; IC rejects a partition-less IAP; portfolio-wide rule
+ REGISTER territory column; **"territory never leaves its own project: one
session, one project"**; every-artifact-resolved-from-the-project-root-that-holds-`.dcs/`.

**Principle 9b** (line 63, 925 B) — cut `Two reasons, both structural: ... a
partition violation invisible to the gate, because each edit looks in-bounds for
the tasking the agent remembers.` (**488 B**), replaced by a **≤ 175 B**
parenthetical preserving the operative warning, e.g. `(a resumed specialist still
holds its OLD tasking — a partition violation the gate cannot see; and its
reasoning lives in a transcript no artifact records, breaking principle 5)`; also
cut `this was prose twice before it was a mechanism, and prose did not hold either
time` (**85 B** incl. separator).
*KEEP:* single-shot; a revision is always a **fresh spawn** carrying corrected
inputs verbatim, never a resumed agent; enforced by `dcs_gate.py` denying
`SendMessage` while an incident is active.

**Principle 13** (line 67, 1,648 B) — cut the four-revisions story `Counting
periods alone is a loophole the field walked straight through: ... never tripped
the cap that exists to catch exactly that;` (**308 B**), the cost clause `each
further pass buys one instance at the cost of a full execute+verify cycle`
(**~100 B** net), and (f)'s rationale `three rejects means the objectives, the
chief's information diet, or the incident's size is wrong, not that the plan needs
one more pass;` (**137 B**).
*KEEP:* all of (a)(b)(c)(d)(f) as triggers; the convergence-read requirement
including same-class vs different-class and **"must lead with raising the fix's
altitude — a guard that makes the class unrepresentable — never with an unqualified
continue"**; the attempt definition **"an attempt is any stamped-and-executed IAP,
so a re-planned revision of the same period counts"**; (f)'s three offers;
Owner-decides continue/pivot/demobilize.

**Principle 15** (line 69, measured **1,901 B** — the single most bloated line in
the file) — cut `Two independent forces make this mechanical rather than
stylistic: ... with no memory of having been a guess.` (**406 B**; replace with a
**≤ 50 B** pointer such as `Derived facts rot, and they travel.`) → route as
**REDUNDANT**, already carried by `doctrine-appendix.md:48-55`. Cut `in the
incident that produced this principle, every seat including the IC and the
Dispatcher shipped one, and the corrective for the surviving instance was to
delete the number, not to fix it` (**196 B**) → **REDUNDANT** with
`doctrine-appendix.md:52-55` and `57-61`. Cut `A test asserting that two live
branches still collide is green only while the defect survives: ... instead
punishes the repair.` (**269 B**) → **NOT** in the appendix (appendix:48-52 names
the migration-number incident but never the test-inversion lesson), so this is a
**second small write-then-cut**.
*KEEP in the core:* the whole rule; **"Write the derivation, not the result"**;
the `as of <ref> — it moves` fallback; **"enforced by the Safety Officer's
checklist (principle 7), not by discipline"**; and the v0.5.4 rule **"a regression
test must pin immutable evidence — a fixture, a frozen blob, a commit SHA — never a
moving ref"** plus **"assert the invariant, never the instance"**.

### T4 — elsewhere in the core (net ~1,160 B)

- **`doctrine.md:104`** (lifecycle) — cut `a Safety-passed period holds proven
  work, and holding it open keeps that work unmerged and unshipped - fixing
  nothing - until the rest of the scope catches up.` (**165 B**) → **new**
  appendix `## The lifecycle (Planning P mapped to software)` section.
  *KEEP the rule:* default at a pass is close / merge / ship and register the
  remainder as a follow-up incident whose 201 evidence is this AAR; keep it open
  only when the delivered part cannot ship alone; say which in the log.
- **`doctrine.md:120`** (charter defect, 1,089 B) — cut `Field lesson 2026-07-24:
  a project made call-graph queries mandatory before cross-file edits, ... rather
  than silently claiming the step.` (**270 B** — **mandatory for criterion 2**) →
  appendix `## Relationship to project-specific protocols`, appended after line
  114 (its lines 106–109 already describe the codegraph-protocol example but not
  this incident's specifics, so this is an **append**, not a redundancy); and
  compress `An agent that reports "the protocol's tool isn't in my toolset, here
  is what I used instead" is behaving exactly right; the defect is upstream, in
  whoever granted the tools.` (**173 B**) to **≤ 90 B** keeping *"the defect is
  upstream, in whoever granted the tools"*.
  *KEEP:* charter-defect-not-agent-failure; must be granted in `agents/dcs-*.md`;
  widen the charter, never let the substitution stand unremarked; `/dcs-init`
  surfaces it; missing tools are environment-dependent.
- **`doctrine.md:124`** — cut `neither changes who holds command judgment or what
  counts as approval, they only remove the Owner's need to type each phase command
  by hand` (**140 B**) → **REDUNDANT** with `doctrine-appendix.md:116-135`.
- **`doctrine.md:127`** — cut `Legitimate only *because* the Delegation defines
  "routine" in writing` (**69 B**) → **REDUNDANT** with
  `doctrine-appendix.md:128-135`. *KEEP* `without one, it still runs but pauses at
  every IAP approval`.
- **`doctrine.md:139-141`**, the three ICS-analogy bullets (**573 B**) — compress
  to **≤ 330 B** keeping ONLY the operative rules: one incident per worktree on
  its own git worktree + branch; the main checkout is where merged, Safety-passed
  work marshals and only Type 5 express fixes and portfolio bookkeeping happen
  there; `/dcs-deploy` ships only what is already merged to main, runs only from
  staging, never reaches into a worktree early. The ICS imagery itself is
  **REDUNDANT** with `doctrine-appendix.md:158-171`.
  **Preserve the bolded lead-ins** — *"A worktree is a division of the fire
  line"*, *"The main checkout is the staging area"*, *"The deploy train
  (`/dcs-deploy`) is demobilization to the line"* — `docs/spec-v0.3-parallel.md:184`
  refers to them (IC-verified), and they are cheap.
- **`doctrine.md:149`** — cut the example list `(harness worktrees, a deploy
  script's own, a human's personal one)` (**66 B**) → **REDUNDANT** with
  `doctrine-appendix.md:139-156`. The DCS-owned/foreign test and the three NEVERs
  stay.
- **`doctrine.md:17`** — cut the ICS framing `regardless of who first reported the
  incident (ICS)` from its first sentence (**90 B**) → **REDUNDANT** with
  `doctrine-appendix.md:31-44`.
- **`doctrine.md:114`** — cut `which fails and confuses the Owner` (**34 B**).

### T5 — RESERVE (pre-authorized, ~491 B)

Use **only** if T2+T3+T4 land short of 22,268 B. Log each draw in the routing
ledger exactly like a tier-1 cut. Priority order:

- **(r1)** `doctrine.md:13` — compress the `## Why phases, not nesting` body from
  347 B to ≤ 170 B (net **~177 B**). Principle 1 already states *"chiefs plan (A),
  IC approves, specialists execute (B), Safety Officer reviews (C); the pipeline
  is the hierarchy"* and `doctrine-appendix.md:14-27` carries the reasoning. The
  heading and the no-nested-subagents constraint must survive.
- **(r2)** `doctrine.md:9` — cut `subagents start blank and even the IC's context
  can reset, ... and every phase transition leaves a paper trail there` down to
  `the directory is the only channel that survives a reset` (net **~130 B**) —
  restated in full by principle 5.
- **(r3)** `doctrine.md:110` — cut the illustration `a 201-BRIEF.md written
  mid-Russian-conversation is written in Russian, because the Owner has to read
  it` (**104 B**) → appendix, **new** `## v0.1 constraints` section. The rule
  *"incident artifacts inherit the conversation language"* stays.
- **(r4)** `doctrine.md:155` — compress the three-surfaces sentence by **~80 B**,
  keeping all three surfaces, *"parking always removes the worktree"*, and the
  `.dcs/CLOSED` fail-closed exception.

Tier 1 + reserve ≈ **5,520 B** against a **4,899 B** requirement (12.7% margin).

### T6 — the ratchet

After the trim is final, run the measurement command, then compute
`budget = math.ceil(total/1024) + 1` and **paste the arithmetic**. Edit **only**
`HOT_PATH_BUDGET_KB` at `tests/test_doctrine_integrity.py:40` and the comment
block at lines 34–39. The comment must state (principle 15): the derivation, the
measured post-trim total in bytes, that it was measured in the incident worktree
where CRLF makes the pair ~319 B **larger** than the LF main checkout (so the
ratchet is conservative for main), the incident slug, and the regenerating command
verbatim. **Do not touch the check-7 logic at lines 146–150** or anything else in
that file — out of territory, and a deviation.

### T7 — invariants you must not break

- All 12 `##` headings unchanged in text and order, **and** the `### A command
  point is never a silent wait` sub-heading at line 33 — it is cited by name from
  `dcs/workflows/plan.md:206` and `agents/dcs-commander.md:113`, and the guard's
  check 6 matches against `^#{2,3}` headings.
- All 28 numbered labels unchanged and in order, including `9b.` and including the
  four command points, the three unattended hard rules and the five worktree-audit
  steps. The guard's principle regex keys on `^(\d+)([a-z]?)\.\s+\*\*`, so every
  principle line must keep its `N. **Bold lead-in**` shape.
- `doctrine.md:3`'s routing pointer — *"Provenance, field lessons, and extended
  rationale live in doctrine-appendix.md"* — **must survive**. It is the routing
  rule and it does not match criterion 2's grep.
- Line endings stay **CRLF** in both files.
- `schemas.md` is not to be opened for editing at all.

## File territory (may edit only within these globs)

- `dcs/references/doctrine.md`
- `dcs/references/doctrine-appendix.md`
- `tests/test_doctrine_integrity.py` — **only** `HOT_PATH_BUDGET_KB` (line 40) and
  its comment block (lines 34–39)
- `dcs/VERSION`
- `package.json` — only the `version` field

## Forbidden zones (explicitly, even if it seems related)

- `dcs/references/schemas.md`, `dcs/references/typing.md`, `dcs/references/forms.md`
- `dcs/workflows/**`, `dcs/templates/**`, `dcs/hooks/**`
- `agents/**`, `skills/**`
- `tests/test_dcs_gate.py`, `tests/test_dcs_intake.py`
- `bin/**`, `install.ps1`, `install.sh`
- `docs/**`, `vault/**`, `CLAUDE.md`, `README.md`
- `.dcs/**`

## Evidence required in the return

Paste each command's **real output**, not a description of it.

- `python -c "import os; d=os.path.getsize('dcs/references/doctrine.md'); s=os.path.getsize('dcs/references/schemas.md'); print(d, s, d+s)"` — criterion 1: third number ≤ 36864; baseline was `27167 14596 41763`
- `grep -n "Field lesson" dcs/references/doctrine.md; echo "exit=$?"` — criterion 2: must print nothing, `exit=1`
- `grep -noE "20[0-9]{2}-[0-9]{2}-[0-9]{2}" dcs/references/doctrine.md; echo "exit=$?"` — dated-war-story superset: must print nothing (baseline: 38 and 120)
- `grep -noE "^[0-9]+b?\." dcs/references/doctrine.md | tr '\n' ' '` — criterion 3: 28 labels, same sequence
- `grep -n "^## " dcs/references/doctrine.md` — criterion 4: exactly the 12 baseline headings, same text and order
- `grep -n "^#\{2,3\} " dcs/references/doctrine.md` — criterion 4 superset: 13 headings, i.e. the 12 plus `### A command point is never a silent wait`
- `grep -n "quota\|transcript" dcs/references/doctrine-appendix.md` — criterion 7: must be non-empty (baseline: empty); paste enough context to show it sits under `## Transfer of command`
- `python tests/test_doctrine_integrity.py` — criteria 5, 8, 11: all checks passing
- `python tests/test_dcs_gate.py | tail -3 && python tests/test_dcs_intake.py | tail -3` — CLAUDE.md requires all three suites green
- `git diff -U0 tests/test_doctrine_integrity.py` — proves only `HOT_PATH_BUDGET_KB` and its comment changed
- `python -c "import math; total=<paste the measured total>; print(total, total/1024, math.ceil(total/1024)+1)"` — criterion 8: the derivation pasted, not the answer asserted
- `git diff --numstat` — exactly 5 files, and `doctrine.md` must **not** show every line changed (that would mean a wholesale rewrite / EOL flip)
- `python -c "d=open('dcs/references/doctrine.md','rb').read(); a=open('dcs/references/doctrine-appendix.md','rb').read(); print(d.count(b'\r\n'), d.count(b'\n'), a.count(b'\r\n'), a.count(b'\n'))"` — line endings still 100% CRLF in both files
- `git diff dcs/VERSION package.json` — criterion 11: both at 0.6.5, atomically

## On discovering the plan doesn't fit reality

STOP. Do not improvise a different fix. Return `status: "deviation"` per
`references/schemas.md` #4, with `found`, `why_plan_wrong`, and a `proposal` (a
recommendation, not an action). The IC will re-enter planning around your finding.

**Specifically:** if tier-1 *and* the T5 reserve are both exhausted and
`doctrine.md` is still above 22,268 B, that is a deviation — **not** a licence to
cut into rule text. The IC ruled at command point 2 that a replan cycle is cheaper
than a rule silently weakened past criterion 10.
