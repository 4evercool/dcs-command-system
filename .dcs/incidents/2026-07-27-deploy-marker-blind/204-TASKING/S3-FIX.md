# 204 — Tasking S3-FIX (fix round, after Safety halt 1)

**Incident:** deploy-marker-blind
**Period:** 1 · **Fix round:** 1 (halt count 1 of 3)
**Specialist:** dcs-ops-specialist (S3-FIX) — a **fresh** spawn, not the
original S3 resumed (doctrine principle 9b).

## Task

### 1. `CLAUDE.md` line 40 — closes Safety refutation 2 (criterion 6)

`CLAUDE.md` and `deploy.md` state **opposite dispositions of the same exit
class**, and the disagreement runs in the dangerous direction:

- `CLAUDE.md:40` — *"Exit `2` is an environment error, not a verdict, and
  **blocks nothing it can't explain**."*
- `deploy.md:217-218` — *"**Witness errors** (before or after): **report it
  and stop**."*

`deploy.md` steps 6 and 7 both tell the agent to discover the mechanism
from `CLAUDE.md`, so `CLAUDE.md` is what a deploy agent reads **first**. An
exit 2 (say, `~/.claude` absent on a fresh machine) read as "blocks
nothing" resolves rows to `DEPLOYED` with **zero verification performed** —
the mirror image of the defect this incident exists to fix. Criterion 6
requires the table to state the contract step 7 actually enforces, and
three of four exit classes matching is not four.

Replace line 40's clause with, in substance:

> Exit `2` is an environment error, not a payload verdict: the train stops
> and reports it, and nothing is marked `DEPLOYED`.

Match `deploy.md` step 7's stop disposition **exactly**. Read step 7 as it
now stands before you write — S2-FIX is rewriting it in parallel to add a
marker-shape trichotomy, so check the file rather than this paragraph for
its final wording, and make the two agree.

### 2. `CHANGELOG.md` — advisory 2

The entry says *"Step 7 now runs `tests/payload_check.py` and reads its
four classes"*. Step 7 **never names the script** — it says "the project's
deployed-content witness (discovered from `CLAUDE.md`, same discipline as
step 6)". As written the CHANGELOG tells a DCS user in another project that
the shipped workflow invokes a script their repo does not have. Correct to,
in substance: *"Step 7 now runs the project's own deployed-content witness
(this repo's is `tests/payload_check.py`) and reads its four classes."*

**Also fold in refutation 1's outcome** once you can see S2-FIX's final
step 7: the shipped step 7 is shape-aware (commit-ish / content witness /
neither), not witness-only. An entry describing a witness-only step 7 would
be stale the moment it lands.

### 3. `dcs/templates/REGISTER.md` — advisory 3

Two things:

- The new `DEPLOYED` definition requires *"a green witness run against the
  integration tip"*, which is **narrower than step 7 allows** — step 7 also
  grants `DEPLOYED` on the installed-only-only class, which the witness
  reports with exit **3**, not green. Widen to "a green (or
  stale-extras-only) witness run".
- The sentence now reads *"`/dcs-deploy` verified … that this incident
  shipped … and that its `dcs/<slug>` branch has been deleted"*, which
  makes branch deletion something the deploy **verified** rather than
  **did**. Reword.

### 4. `dcs/workflows/close.md:76-77` — advisory 4 (reassigned to you)

*"verify the project's deployed-version marker (e.g. a `.deployed_sha`)"*.
Your earlier disposition was factually right — it is generic advice and its
worked example is content-based, so criterion 5 was met and this was
correctly not a refutation. But **in this repo** the "deployed-version
marker" is now documented as explicitly *not* proof, so a closer following
`close.md` literally would read `~/.claude/dcs/VERSION` and write a deploy
status this incident just declared insufficient. One-line fix:

> verify the project's documented deploy evidence (`deploy.md` step 7's
> mechanism)

**The IC's directive labelled this S2's; it is yours** — `close.md` is in
your approved territory, and giving it to S2 would put one file in two
territories.

### Not in this round

`docs/spec-v0.3-parallel.md`'s optional "superseded" note (advisory 8) is
left for the IC's integration commit. **Do not touch it.**

## File territory (may edit ONLY these)

- `CLAUDE.md`
- `CHANGELOG.md`
- `dcs/templates/REGISTER.md`
- `dcs/workflows/close.md`

## Forbidden zones

Unchanged from `204-TASKING/S3.md`, and note especially:
`dcs/workflows/deploy.md` (S2-FIX's — **read it, do not edit it**),
`tests/**` (S1-FIX's), `docs/spec-v0.3-parallel.md` (out of this round),
`dcs/VERSION`, `package.json`, `install.ps1`, `install.sh`, `bin/**`.

## Evidence required in the return

1. `sed -n '25,45p' CLAUDE.md` — the corrected table and sentence.
2. **Side-by-side proof that `CLAUDE.md` and `deploy.md` step 7 now agree
   on all four exit classes.** Quote both, class by class. This is the
   refutation; a partial match is what failed last round.
3. `git diff CHANGELOG.md dcs/templates/REGISTER.md dcs/workflows/close.md`
   — the real diff.
4. `grep -n '^## ' CHANGELOG.md | head -3` — no new version heading.
5. `git diff --stat` — `dcs/VERSION` and `package.json` still untouched.
6. `python tests/test_doctrine_integrity.py`, `python tests/test_dcs_gate.py`,
   `python tests/test_dcs_intake.py` — each suite's own `N/M passed` line.

## On discovering the plan doesn't fit reality

STOP. Return `status: "deviation"` per `schemas.md` #4 with `found`,
`why_plan_wrong`, `proposal`.
