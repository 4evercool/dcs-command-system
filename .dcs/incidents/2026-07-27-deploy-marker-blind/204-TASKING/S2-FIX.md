# 204 — Tasking S2-FIX (fix round, after Safety halt 1)

**Incident:** deploy-marker-blind
**Period:** 1 · **Fix round:** 1 (halt count 1 of 3)
**Specialist:** dcs-ops-specialist (S2-FIX) — a **fresh** spawn, not the
original S2 resumed (doctrine principle 9b).

## Task — closes Safety refutation 1 and advisory 4

### 1. Step 7 must be shape-aware, mirroring step 4's own trichotomy

**This is the refutation, and it is a defect the fix introduced.** Step 4
(lines 86-115) enumerates four marker shapes and preserves the commit-ish
ancestry check. Step 7 (lines 188-218) mandates **one** mechanism — "Run
the project's deployed-content witness" — and its outcomes are literally
one witness implementation's four classes. `repo-only` and
`installed-only` are meaningless for a `.deployed_sha` file or a
`/version` endpoint, and the shape-agnostic text that named both was
deleted with no replacement path.

`deploy.md` is a **shipped deliverable**, and neither installer copies
`tests/` into a consuming project — they copy `dcs/`, `agents/dcs-*.md`,
`skills/dcs-*/` only. So as written, this period converts a
previously-working verification into a hard stop for every project that is
not this one: a project with a `.deployed_sha` marker passes step 4's
commit-ish branch, runs step 6, then reaches a step 7 with no applicable
branch and falls into "Witness errors → stop".

Give step 7 the same trichotomy step 4 has:

- **Commit-ish marker** → `git merge-base --is-ancestor` of the shipped
  merge commits against the recorded post-deploy marker sha.
- **Content witness** → the four classes exactly as you currently have
  them. No change to that branch.
- **Readable but neither shape** → say so and stop; nothing is marked
  `DEPLOYED`.

### 2. Step 7's cross-reference to step 4 is false — remove it

Step 7's "Witness errors" bullet grounds its stop in *"step 4's same
'cannot check' treatment"*. **Step 4's cannot-check treatment is not a
stop** — lines 110-113 say skip the reconciliation, say so plainly, treat
every `MERGED` row as unshipped, and flag the re-ship risk. Remove the
false cross-reference and state the real rule: **after** a deploy an
unverifiable payload stops the train, because nothing may resolve to
`DEPLOYED` unproven. Say plainly that this is **deliberately stricter than
step 4** — before the deploy, over-shipping is the safe direction; after
it, recording an unproven ship is not.

### 3. Advisory 4 — `close.md`'s retired vocabulary

**Reassigned to S3-FIX** (`close.md` is S3's territory in the approved
partition; the IC's directive labelled it S2, which would have put one
file in two territories). **Not yours. Do not touch `close.md`.**

## IC ruling on the line budget — binding

`deploy.md` sits at exactly **250** lines, the `CLAUDE.md` ≤ ~250 ceiling.
The Safety Officer proved clause by clause that the current 250 lines lost
**no rule** to the earlier compression, so there is no safe fat to trim.

> **Exceeding the budget by up to 15 lines is authorised** for step 7's
> trichotomy. The budget is approximate ("≤ ~250") and no suite enforces
> it. **Prefer prose trims that cost no normative clause; deleting a
> clause to fit is forbidden.** Report the final line count in your return.

## File territory (may edit ONLY this)

- `dcs/workflows/deploy.md`

## Forbidden zones

Unchanged from `204-TASKING/S2.md`. Note especially: `dcs/workflows/close.md`
(S3's), `CLAUDE.md` (S3's), `tests/**` (S1's), and `install.ps1`,
`install.sh`, `package.json`, `dcs/VERSION`, `bin/**` — in no territory and
in every forbidden list.

## Hard constraints (unchanged, and still binding)

1. **`deploy.md` stays project-agnostic** — never name
   `tests/payload_check.py`, `~/.claude`, or `dcs/VERSION`. This is the
   whole point of refutation 1: the shipped workflow must work for a
   project that has neither.
2. **Preserve step numbering 1-10 and step 5's identity.**
3. **Preserve the `schemas.md #7, delegation bounds` citation** (currently
   line 135) — integrity check 13.

## Evidence required in the return

1. `wc -l dcs/workflows/deploy.md` — the real number, whatever it is.
2. `grep -n '^## ' dcs/workflows/deploy.md` — steps 1-10 intact, step 5
   still the Owner/Delegation gate.
3. `grep -n 'schemas.md #7' dcs/workflows/deploy.md`.
4. **The refutation-1 trace, on paper, in your return.** Walk a consuming
   project whose `CLAUDE.md` documents a `.deployed_sha` marker through the
   new step 7 and show which branch it lands in and what happens. Then walk
   this repo (content witness) through it. Both must reach a definite
   outcome; neither may fall into an error branch for want of an
   applicable one.
5. Paste the new step 7 text in full.
6. `grep -rniE 'deployed[- ]version marker|deployed_sha|marker (actually )?advanc|VERSION.*after deploy' dcs/workflows/deploy.md`
   — full output, with a per-hit disposition. The commit-ish worked example
   is expected to remain and is correct; say so.
7. `python tests/test_doctrine_integrity.py`, `python tests/test_dcs_gate.py`,
   `python tests/test_dcs_intake.py` — each suite's own `N/M passed` line.

## On discovering the plan doesn't fit reality

STOP. Return `status: "deviation"` per `schemas.md` #4 with `found`,
`why_plan_wrong`, `proposal`.
