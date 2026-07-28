# 204 — Fix-tasking S1-fix1 (repair of Safety Halt 1)

**Incident:** deviation-path-proportionality
**Period:** 1
**Specialist:** dcs-ops-specialist (fresh spawn — do not resume the
original S1 agent, per doctrine principle 9b)
**Triggered by:** `SAFETY.md` verdict 1 (halt), refutations 1 and 2;
command point 4 disposition `fix_taskings` (dcs-commander), `214-LOG.md`
2026-07-28T10:34:21+11:00.

## Task

Three fixes to `dcs/workflows/plan.md`'s new `## 6c.` section (which you
authored in the prior pass), plus two advisory folds. No criterion
changes, no territory changes, no premise change — this is a repair, not
a re-plan.

**(1) Refutation 1 — scope the Delegation re-check to the amendment's own
delta, not the whole plan.** Around line 409, `## 6c.` currently reuses
step 6's whole-201/202-text `forbidden_topics` screen. The Safety Officer
measured this against field measurement 2
(`.dcs/incidents/2026-07-27-register-field-repair-path/214-LOG.md:31-44`):
because that incident's 202 text contains "version bump," the
whole-plan screen re-trips every time, so the claimed Owner-round-trip
saving never materializes — a zero reduction, not partial. Rewrite the
clause so the amendment's Delegation re-check screens ONLY the
amendment's own delta: `forbidden_globs` against the file(s) the
amendment actually touches, `forbidden_topics` against the amendment's
own new/changed text — NOT the unchanged 201/202 body. State explicitly
why this is sound: boundary conditions 2, 3, and 4 (no criterion change,
no territory/forbidden change per fix (2) below, no premise change)
already guarantee the 201/202 text itself is unchanged from what the
last full approval already adjudicated — re-screening it again is pure
noise, not a second safety check.

Then **re-derive field measurement 2's row** with the same anchored
pattern you used before
(`grep -nE '^\[[^]]*\] (command:|ESCALATION:|IAP-APPROVED:|SAFETY-)' .dcs/incidents/2026-07-27-register-field-repair-path/214-LOG.md`),
applying your NEW delta-scoped clause instead of the old whole-plan one,
and report the corrected saving (spawns and/or round-trips) for the IC to
re-record into `IAP.md`'s verification plan (criterion 3's split
ownership: you derive, IC records).

**(2) Refutation 2 — widen boundary condition 3 to pin `forbidden`, not
just `territory`.** The Safety Officer found `plan.md`'s lint 4a checks 1
(`territory ∩ forbidden` empty) and 8 (territory + forbidden stay inside
the project) both read the tasking's `forbidden` list — but boundary
condition 3 (lines ~376-377) pins only `territory`, so `## 6c.`'s claim
that checks 1 and 8 are "degenerate" under that condition is false: an
amendment could edit a `forbidden` list unnoticed, newly intersecting an
unchanged territory or escaping the project. Widen condition 3 to "No
change to any `204-TASKING/*.md`'s territory OR forbidden list," and
correct the degenerate-checks sentence (lines ~395-399) to correctly
name checks 1, 4, AND 8 as degenerate now that both their inputs are
pinned — not just check 4.

**(3) Advisory fold 1 — make `## 6c.` reachable by a linear reader.** Add
one forward pointer in `plan.md` step 1's `phase == execution` branch
(lines ~21-27, which currently says "counts as a re-plan — proceed,"
routing straight into steps 2-4): if `214-LOG.md` holds a qualifying
command-point-3/4 entry AND `## 6c.`'s boundary conditions hold, go to
`## 6c.` instead of proceeding to step 2. This does not change step 1's
existing behavior for a genuine re-plan — only adds the missing branch.

**(4) Advisory fold 2 — scope boundary condition 1's second branch.**
Condition 1 currently reads "a single `204-TASKING/*.md` file, OR
`.dcs/**` content only" — but `204-TASKING/*.md` files live UNDER
`.dcs/**`, so the second branch swallows the first, and read literally
also reaches `.dcs/esg/DELEGATION.md`, `REGISTER.md`, and
`.dcs/config.json`. Scope the second branch explicitly to "this
incident's own `IAP.md` prose only" (the case the parenthetical already
intends), excluding `.dcs/esg/**` and `.dcs/config.json`. This also
closes the last route by which an amendment could reach 201/202 text,
making fix (1)'s delta-only screen airtight — do this fix in the SAME
pass as fix (1), they reinforce each other.

**(5) Advisory fold 4 — de-project-ify `execute.md:325`'s `vault/`
mention.** Your prior pass added prose mentioning "the close-time
`vault/` memory-routing write" — `vault/` is absent from `package.json`'s
`files` whitelist (confirmed: `['bin/', 'dcs/', 'agents/', 'skills/',
'docs/', 'tests/', 'install.ps1', 'install.sh', 'README.md',
'CHANGELOG.md']`), so this is a DCS-repo-specific project fact in shipped
prose. Rephrase to the project-neutral form already used elsewhere in the
package: "the close-time memory-routing write into whatever memory store
the project's `CLAUDE.md` documents."

## File territory (may edit only within these globs — unchanged from
your original tasking)

- `dcs/workflows/execute.md`
- `dcs/workflows/plan.md`
- `agents/dcs-commander.md`

## Forbidden zones (unchanged from your original tasking)

- `dcs/hooks/**`
- `tests/**`
- `dcs/references/**`
- `dcs/templates/**`
- every other `dcs/workflows/*.md`
- every other `agents/dcs-*.md`
- `skills/**`
- `dcs/VERSION`
- `package.json`
- `CHANGELOG.md`
- `.dcs/**`
- `vault/**`

## Evidence required in the return

- `python tests/test_doctrine_integrity.py` — full tail + every FAIL
  line. Current baseline (after the original S1/S2/S3 pass): 83/83.
- `python tests/test_dcs_gate.py` — baseline 100/100. `python
  tests/test_dcs_intake.py` — baseline 10/10.
- `git diff --stat -- dcs/hooks/dcs_gate.py tests/` — must print nothing.
- The corrected field-measurement-2 side-by-side row (fix 1), with the
  anchored grep output pasted, not paraphrased.
- Confirm boundary condition 3's new wording (fix 2) still reads
  coherently alongside conditions 1, 2, 4, and the degenerate-checks
  sentence names exactly checks 1, 4, 8.
- Confirm step 1's new forward pointer (fix 3) doesn't alter step 1's
  existing behavior for a genuine `/dcs-plan` re-invocation outside
  `## 6c.`'s conditions — trace one example by hand and report it.

## On discovering the plan doesn't fit reality

STOP. Do not improvise a different fix. Return `status: "deviation"` per
`references/schemas.md` #4 (ops-specialist return), with `found`,
`why_plan_wrong`, and a `proposal`. The IC will re-enter planning around
your finding.
