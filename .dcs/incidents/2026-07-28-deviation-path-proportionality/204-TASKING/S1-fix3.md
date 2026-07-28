# 204 — Fix-tasking S1-fix3 (repair of Safety Halt 3, structural)

**Incident:** deviation-path-proportionality
**Period:** 1
**Specialist:** dcs-ops-specialist (fresh spawn — do not resume any
prior S1 agent, per doctrine principle 9b)
**Triggered by:** `SAFETY.md` verdict 3 (halt), refutation 1; command
point 4 disposition `fix_taskings` (dcs-commander); escalation triggers
(b)/(c)/(e) folded into one 209 update
(`.dcs/esg/SITREPS/deviation-path-proportionality-p1.md`), Owner
decision: **continue, structural fix**, decided inline,
2026-07-28T12:21:19+11:00.

## Why this tasking is different again

Three fix-taskings in a row have each closed the specific hole a halt
named and opened or re-exposed a different one in the same boundary
(`## 6c.`'s condition 1), because the fix's author also authored its own
validation cases. **This tasking removes the recurring class by
construction, not by another guess at wording**: the "skip lint checks
1/4/8, they're provably unneeded" optimization is DELETED — those checks
now always run, so there is no skip-claim left to be wrong. This costs
nothing under this incident's own ceremony metric (criterion 1 counts
only agent spawns and Owner round-trips; running a lint check costs
zero of either). **The validation fixture set below is IC-authored, not
yours to invent** — you may add cases, you may not substitute, weaken, or
drop any of them.

## Task

**(1) Delete the checks-1/4/8 degeneracy paragraph entirely.** Remove
the claim that lint checks 1, 4, and 8 are "degenerate under boundary
condition 3" and therefore skippable. Add checks 1, 4, and 8 to `## 6c.`'s
"still run" list (alongside 2, 3/3a/3b, 5, 6, 7 — confirm the existing
list's exact membership by reading it, don't guess). State explicitly
that these three now run over the **complete post-amendment
`204-TASKING/*.md` set** — every tasking file as it would stand after the
amendment, including any file the amendment itself creates — and that
this costs 0 additional agent spawns and 0 additional Owner round-trips
under criterion 1's own ceremony accounting (the session already runs
lint itself; this is not a new spawn).

**(2) New-partition-line clamp.** Add: an amendment whose touched set
includes any `204-TASKING/*.md` file that did **not** exist at the
`IAP-APPROVED` stamp currently in force never auto-approves under the
Delegation delta-screen (halt 1's fix) — it always takes `## 6c.`'s
existing lightweight Owner approve/reject round-trip (still within
criterion 1's "at most 1"), because a new territory/forbidden pair is
planning-shaped content the Owner has never seen. The requirement that
the triggering logged decision must *name* the file stays unchanged.

**(3) Fold verdict-3 advisory 4 (halt-ceiling reset).** Add one sentence:
`## 6c.` may not be used to re-stamp while the halt tally
(`dcs_gate.py --halt-count`) stands at `esg.max_halts_per_attempt` — at
the ceiling, the route is trigger (b)/(c) escalation, never a cheap
re-stamp.

**(4) Fold verdict-3 advisory 2 (false justification).** Delete the
sentence claiming the delta-scoped Delegation re-check "already
re-evaluates `forbidden_topics` in full." Keep the actual, verified-sound
argument for why `forbidden_topics` is excluded from the failed-bound
inheritance clause: boundary conditions 2, 3, and 4 guarantee the rest of
the 201/202 text is identical to what the last full approval already
ruled on, failed bound or not — so a delta-clean `forbidden_topics` means
the amendment introduced no *new* forbidden topic, not that the standing
plan trips none. State the residual explicitly in those terms.

**(5) Fold verdict-3 advisory 1 (bookkeeping writes).** Add one clause:
mandatory bookkeeping the path itself performs — `214-LOG.md` appends,
the `IAP-APPROVED` rewrite, and a register **status** transition an
escalation trigger performs — is not part of condition 1's screened set.
A **content** edit to `.dcs/esg/**` (e.g. editing `DELEGATION.md`'s
bounds, or `REGISTER.md`'s territory/title fields) remains excluded, as
condition 1 already states.

**(6) Fold verdict-3 advisory 5 (phase-transition line).** Add to step
8's instruction: on a `## 6c.` amendment the phase does not change — the
log line reads `re-stamp, no phase transition (still execution, period
<N>)` in place of the `phase: planning -> execution` transition clause.

## MANDATORY validation — IC-authored fixture population

Run every case below yourself, with real commands, and report real
output. You may add cases. You may **not** substitute, weaken, or drop
any of the following. If any MUST-ADMIT case fails to admit, or any
MUST-REJECT / MUST-CATCH-BY-EXECUTION case fails to reject/fail, your
rewrite is wrong — revise and re-validate before returning `done`.

**MUST-ADMIT (re-derive both real savings from the raw logs):**

(i) Field measurement 1's exact 4-artifact set
(`204-TASKING/S1.md` + `S3.md` + `IAP.md` + `203-ORG.md`,
`.dcs/incidents/2026-07-25-halt-loop-unbounded/214-LOG.md:118`) — 1 agent
spawn saved.

(ii) Field measurement 2's single-tasking-plus-`IAP.md` advisory
correction (`.dcs/incidents/2026-07-27-register-field-repair-path/214-LOG.md`,
the 22:22:57 event) — 1 Owner round-trip saved, unregressed.

(iii) A fix-tasking re-stamp whose touched set includes a **newly
created** tasking file named by the logged verdict decision — admitted,
but via the lightweight Owner round-trip (per fix 2), with checks 1, 4,
and 8 demonstrably executed against that file's fresh
territory/forbidden content (show the check actually running against a
real or constructed example — do not just assert it would).

**MUST-REJECT:**

(iv) A new tasking file named by **no** logged commander decision.

(v) An acceptance-criterion substance change, in either
`202-OBJECTIVES.md` or `IAP.md`'s own summary.

(vi) Any `.dcs/esg/**` or `.dcs/config.json` **content** edit (distinct
from the bookkeeping writes fix (5) exempts).

(vii) A citation of a commander decision entry predating the
`IAP-APPROVED` stamp currently in force.

(viii) A re-stamp attempted while the halt tally is at the ceiling (per
fix (3)).

**MUST-CATCH-BY-EXECUTION, not by prose claim (construct or point to a
real case where each check actually fires red):**

(ix) A new tasking whose territory overlaps a sibling's — check 4 must
fail it.

(x) A new tasking whose `forbidden` list intersects its own
`territory` — check 1 must fail it.

(xi) A new tasking carrying a `../` or absolute-path glob — check 8 must
fail it.

## File territory (may edit only within these globs — unchanged)

- `dcs/workflows/execute.md`
- `dcs/workflows/plan.md`
- `agents/dcs-commander.md`

(Expected to land entirely in `plan.md`'s `## 6c.` section again — name
any consequential exception explicitly if your validation reveals one.)

## Forbidden zones (unchanged)

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
  line. Current baseline: 83/83.
- `python tests/test_dcs_gate.py` — baseline 100/100. `python
  tests/test_dcs_intake.py` — baseline 10/10.
- `git diff --stat -- dcs/hooks/dcs_gate.py tests/` — must print nothing.
- All 11 fixture-population results (i-xi), each with real command
  output, not a paraphrase or an assertion of confidence.
- Confirm `git diff --stat` shows only `plan.md` (or name the
  consequential exception).

## On discovering the plan doesn't fit reality

STOP. Do not improvise. Return `status: "deviation"` per
`references/schemas.md` #4, with `found`, `why_plan_wrong`, `proposal`.
Given this is the incident's third fix-tasking after three halts, a
`deviation` return here is highly significant — say so plainly.
