# IAP — Incident Action Plan

**Incident:** doctrine-hot-path-trim
**Type:** 3
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `204-TASKING/OPS-1.md` — *203-ORG.md skipped: default Type 3 activation (IC + Planning Chief + 1 specialist matching the 1 tasking, plain execution); the partition table below carries the same information.*

## Objectives (summary of 202)

**Goal.** The doctrine hot path costs materially less to read on every invocation
and every command-point spawn, **without any rule changing, moving, or
disappearing.** Every version-tagged war story, field lesson and worked example
accumulated since the v0.5.0 diet relocates to `doctrine-appendix.md` (which ships
but is never `@`-included), leaving the core carrying the operative rule and only
the rationale a reader needs at the moment of applying it. The budget ratchet is
re-seated behind the result so the win cannot silently erode again.

The success condition is a byte count, but the **risk** is a rule quietly lost in
the editing — which is why criteria 3–5 and 9 exist and why the Owner reads the
result.

**Measurement convention.** Raw on-disk bytes of `doctrine.md` + `schemas.md`,
measured **inside this worktree** by the guard's own method. This tree reads
319 B larger than the LF main checkout at the same commit (`core.autocrlf=true`,
no `.gitattributes`), which makes it the conservative basis. Baseline
27,167 + 14,596 = **41,763 B**.

**Acceptance criteria:**

1. Combined hot path **≤ 36,864 B** ⇒ `doctrine.md` ≤ 22,268 B, i.e. **−4,899 B**.
2. `grep -n "Field lesson" dcs/references/doctrine.md` returns **empty** (baseline:
   lines 38, 120). Line 3's lowercase routing pointer must survive.
3. `grep -noE "^[0-9]+b?\." dcs/references/doctrine.md` yields the same **28-label**
   sequence, including `9b`. No renumbering.
4. `grep -n "^## "` yields the **12 baseline headings** unchanged in text and order.
5. `python tests/test_doctrine_integrity.py` all green.
6. **Nothing deleted without a home** — a routing line per removed passage naming
   the appendix destination, or the existing appendix text that already covers it,
   cited by line.
7. `grep -n "quota\|transcript" dcs/references/doctrine-appendix.md` **non-empty**
   (baseline: empty) — a write-then-cut, not a relocation.
8. `HOT_PATH_BUDGET_KB` re-seated to `math.ceil(total/1024) + 1`, strictly < 42,
   comment stating the derivation. **Only** that constant and its comment change in
   that file.
9. Every named rule still stated **as a rule** in the core: model-availability
   re-test-per-spawn; announce-before-spawn and empty-return-is-a-failed-spawn;
   principle 4 ceremony-not-size; principle 6 territory-never-leaves-its-project;
   principle 9b fresh-spawn; principle 13 convergence-read and attempt-counting;
   principle 15 write-the-derivation and tests-pin-immutable-evidence.
10. **[Owner]** Owner reads the trimmed `doctrine.md` end to end at close and
    confirms no rule was lost or weakened.
11. `dcs/VERSION` and `package.json` both to **0.6.5**.
12. **[deploy period]** `~/.claude/dcs/VERSION` equals `dcs/VERSION` after install.

## Tactics (from the Planning Chief)

**T0 — one seat, deliberately.** `doctrine.md` and `doctrine-appendix.md` are the
two ends of one edit. Despite being trivially disjoint files, they are **not**
split across two specialists: criterion 6's routing ledger needs one seat holding
both the cut and its landing; the byte margin is thin enough that the reserve will
likely be drawn, and every extra cut needs a matching appendix landing a parallel
writer could not anticipate — *"the split deadlocks exactly when it is needed"*;
and criterion 8's ratchet must be measured after the trim lands, which serializes
anyway. Internal sequence: **land appendix destinations → cut → measure → ratchet
→ version bump**.

**Method is mandatory: surgical `Edit` operations only.** A wholesale `Write` of
either file converts CRLF→LF, books a ~157 B phantom win against the stated
measurement basis, and produces an all-lines diff no Safety Officer can review.

**T1 — arithmetic.** `schemas.md` fixed at 14,596 B ⇒ `doctrine.md` ≤ 22,268 B
(−4,899 B). Every span measured, not estimated (`len(span.encode('utf-8'))`), and
**independently re-verified by the IC at command point 2 to the byte** across the
seven largest spans; the single discrepancy found (principle 15's line measures
1,901 B vs 1,868 claimed) favours the plan.

**T2 — `## Transfer of command`, net ~1,596 B** → appendix `## Transfer of
command`. Cuts at `doctrine.md:31` (429 B + 165 B of model-availability
rationale), `:38` (689 B — contains the literal `Field lesson`, mandatory for
criterion 2 — plus a 167 B sentence, replaced by a ≤90 B clause keeping the proxy
list), `:37` (~150 B), `:35` (86 B lead-in). **Write-then-cut:** the appendix has
no Transfer-of-command counterpart, so this text is written there *before* it is
removed, retaining `quota` and `transcript`, the 2026-07-24 dating, and both
halves of the lesson.

**T3 — `## The working principles`, net ~2,273 B** → appendix `## The working
principles`, except where redundant. Principle 4 (132 + 30 B); principle 6 (445 B
→ ≤155 B kernel, plus 57 B); principle 9b (488 B → ≤175 B parenthetical, plus
85 B); principle 13 (308 + ~100 + 137 B); principle 15 (406 B **redundant** with
appendix:48-55; 196 B **redundant** with appendix:52-55 and 57-61; 269 B
test-inversion lesson = a second write-then-cut). Each cut carries an explicit
KEEP-list of rule sentences that stay verbatim or in a strictly shorter kernel.

**T4 — elsewhere, net ~1,160 B.** `:104` (165 B → **new** appendix `## The
lifecycle` section); `:120` (270 B field lesson → appendix `## Relationship to
project-specific protocols`, plus a 173→≤90 B compression); `:124` (140 B
redundant); `:127` (69 B redundant); `:139-141` (573 B → ≤330 B, imagery redundant
with appendix:158-171, **the three bolded lead-ins preserved** because
`docs/spec-v0.3-parallel.md:184` cites them — IC-verified); `:149` (66 B
redundant); `:17` (90 B redundant); `:114` (34 B).

**T5 — reserve, ~491 B, PRE-AUTHORIZED** (IC ruling A below). Drawn without asking
if tier 1 lands short, each draw logged in the ledger identically: (r1) compress
`## Why phases, not nesting` body (~177 B); (r2) `:9` (~130 B); (r3) `:110`
Russian-201 illustration (104 B → new appendix `## v0.1 constraints`); (r4) `:155`
(~80 B). **Tier 1 + reserve ≈ 5,520 B against 4,899 B required — a 12.7% margin.**

**T6 — the ratchet, last and measured.** `budget = math.ceil(total/1024) + 1`,
arithmetic pasted. Comment states the derivation, measured bytes, the
CRLF-worktree caveat, the incident slug, and the regenerating command.

**T7 — invariants.** 12 `##` headings **and** the `### A command point is never a
silent wait` sub-heading (cited by name from `plan.md:206` and
`dcs-commander.md:113`); 28 numbered labels including `9b` and the three
non-principle lists; the guard's `^(\d+)([a-z]?)\.\s+\*\*` shape on every
principle; `doctrine.md:3`'s routing pointer; CRLF preserved; `schemas.md` not
opened.

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| OPS-1 | `dcs/references/doctrine.md`, `dcs/references/doctrine-appendix.md`, `tests/test_doctrine_integrity.py` (**only** `HOT_PATH_BUDGET_KB` + its comment), `dcs/VERSION`, `package.json` (**only** the `version` field) | `dcs/references/schemas.md`, `typing.md`, `forms.md`, `dcs/workflows/**`, `dcs/templates/**`, `dcs/hooks/**`, `agents/**`, `skills/**`, `tests/test_dcs_gate.py`, `tests/test_dcs_intake.py`, `bin/**`, `install.ps1`, `install.sh`, `docs/**`, `vault/**`, `CLAUDE.md`, `README.md`, `.dcs/**` |

**Partition status:** disjoint — trivially, a single seat. `partition_ok: true`.
The one-seat choice is a deliberate tactic (T0), not an absence of partitioning;
the Dispatcher removed a catch-all `**/*` from the forbidden list at lint, which
had matched every entry of the tasking's own territory.

## IC rulings — binding on execution (command point 2)

**(A) Feasibility.** Option (a): the **tier-2 reserve is pre-authorized**, drawn
only if tier 1 lands short, each draw logged in the ledger identically to a tier-1
cut. **Criterion 1 is NOT relaxed** — 36,864 B stands, because the 202 is the
Owner-facing contract and the reserve makes it feasible at 12.7% without touching
rule text. If tier 1 **and** the reserve are exhausted and the total is still
over, the specialist **files a deviation** with the measured shortfall; it must
never invent cuts into MUST / NEVER / definition / threshold text. **The ratchet's
+1 kB margin is reserved for criterion-10 Owner-UAT rebound repairs and must not
be spent to reach criterion 1.**

**(B) Criterion 6's artifact.** The **routing ledger** is accepted as criterion 6's
artifact: a required structured field of the specialist's return (one row per
removed passage — baseline line + first words → appendix destination section, or
`redundant with doctrine-appendix.md:NN-NN`, plus the measured byte delta, reserve
draws included). The Dispatcher transcribes it **verbatim into `214-LOG.md`** so
criterion 6's literal text is satisfied, it is carried into the AAR, and the
Safety Officer refutes against it **row by row** — verifying that every
`redundant with` citation genuinely covers the cut substance and that every
write-then-cut actually landed.

**(C) Criterion 8's formula** is pinned to `budget = math.ceil(total/1024) + 1`,
so an exact 1024-multiple gains only the +1 margin. The arithmetic is pasted into
the comment (measured bytes, the command, the CRLF caveat, the slug); the constant
is never merely asserted. Result must be strictly < 42.

## Risks

1. **Byte margin — the dominant risk.** Tier-1 inventory nets ~5,029 B against
   4,899 B required (**2.7%**), reaching 12.7% only by consuming the reserve.
   Essentially every one of the ~25 measured spans must actually come out; if the
   specialist judges even two or three of the mid-sized spans (principle 6's
   445 B, 9b's 488 B, 15's 406 B) too rule-adjacent, criterion 1 fails. Mitigated
   by naming each span verbatim with its KEEP-list so the judgment is pre-made and
   IC-reviewed, plus the pre-authorized reserve, plus an explicit deviation
   instruction instead of improvised cuts into rule text.
2. **Substance loss is invisible to the guard.** A passage cut but never written
   into the appendix passes all 12 checks. Only the routing ledger plus a human
   read catches it — which is why the cut and the landing are one seat and the
   ledger is a required return field.
3. **CRLF/LF measurement basis.** This worktree reads 319 B larger than main at
   the same commit. A wholesale rewrite that flips line endings books a ~157 B
   phantom win; and the ratchet derived here is conservative when the guard later
   runs in the LF main checkout — the safe direction, but the comment must say so
   or the next reader re-derives it wrong.
4. **Owner-UAT rebound (criterion 10).** If the Owner's read finds a rule
   weakened, the repair restores text **into** the core against a by-then-tightened
   ratchet. Criterion 8's +1 kB margin is exactly what absorbs that (ruling A).
5. **Criterion 7's probe is loose** — it greps the whole appendix, so it would
   pass on an incidental match or text landed in the wrong section. Tasked and
   verified to the stricter bar (under `## Transfer of command`).
6. **Appendix growth is unbudgeted** (~3–4 kB). It ships but is never
   `@`-included and is not part of check 7 — no latency cost, no check to trip,
   but nothing constrains it either. Worth a vault note at close, not a control
   this period.
7. **Single-specialist workload** — ~25 surgical edits across two files plus three
   one-line edits, against a hard byte target. Mitigated by the plan pre-deciding
   every cut boundary and KEEP-list. **If it deviates on volume rather than bytes,
   the correct amendment is to split by core SECTION across two sequential
   periods — not to split the two files across two parallel seats** (T0).

## Verification plan

What the Safety Officer checks, all in `C:\DCS-wt\doctrine-hot-path-trim`:

1. **Re-measure independently** — do not trust the specialist's paste. Confirm
   combined ≤ 36,864 B; confirm `HOT_PATH_BUDGET_KB == math.ceil(total/1024) + 1`,
   strictly < 42, and that its comment states the derivation, the measured bytes
   and the regenerating command (principle 15 applies to the guard's own comment).
2. **Re-run every criterion command verbatim** from the 202: size; `grep -n
   "Field lesson"` empty; the 28-label sequence incl. `9b`; the 12 headings in
   order; guard all-green. Plus the dated-narrative superset `grep -noE
   "20[0-9]{2}-[0-9]{2}-[0-9]{2}"` (must be empty) and `grep -n "quota\|transcript"`
   on the appendix (non-empty **and**, read in context, sitting under `## Transfer
   of command`).
3. **Verify the guard now bites.** The 201's repro path is a measurement, so
   confirm check 7's remaining headroom is on the order of ≤ ~1 kB — the next
   elaboration should trip it. That is the whole point of the incident and no
   other check covers it.
4. **Rule-survival sweep (criterion 9)** — one grep per named rule, each returning
   a line that still reads as an **instruction**, not a memory: `re-tested at every
   command point` / `per-spawn`; `Announce before spawning`; `FAILED spawn`;
   `ceremony, never size`; `one session, one project`; `fresh spawn` /
   `single-shot`; `convergence read` and `an attempt is any stamped`; `Write the
   derivation` and `immutable`. Confirm `doctrine.md:3`'s routing pointer survives.
5. **Ledger reconciliation — the check no command replaces.** Read `git diff
   dcs/references/doctrine.md` end to end against the routing ledger. Every
   deletion hunk must have a row; every row claiming a destination must be findable
   in `git diff dcs/references/doctrine-appendix.md`; every row claiming redundancy
   must cite appendix lines that genuinely cover it (spot-check at minimum the
   principle-15 rows against appendix:48-68 and the parallel-operation rows against
   139-171). **A deletion with no row is a criterion 6 failure regardless of the
   byte count.**
6. **Territory** — `git diff --numstat` shows exactly five files; `git diff -U0
   tests/test_doctrine_integrity.py` shows only the constant and its comment. Any
   touch to the check logic at lines 146–150 is out of territory and a halt.
7. **Regression** — `python tests/test_dcs_gate.py` and `python
   tests/test_dcs_intake.py` both green (CLAUDE.md requires all three suites before
   close); `git diff --stat dcs/references/schemas.md` empty.
8. **The manual check that matters, and is not automatable** — read the trimmed
   `## The working principles` as a first-time reader would. *A principle reduced
   to a slogan with its operative clause amputated will pass every grep above.*
   Anything reading as weakened goes into the verdict for the Owner's criterion-10
   read rather than being silently accepted.
9. **Not verifiable this period** — criterion 10 (Owner-UAT at close) and criterion
   12 (`~/.claude/dcs/VERSION` after `/dcs-deploy`). Do not mark them either way.

## Deviation history (this period)

none
