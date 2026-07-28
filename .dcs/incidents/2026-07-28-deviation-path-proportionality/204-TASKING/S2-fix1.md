# 204 — Fix-tasking S2-fix1 (repair of Safety Halt 1)

**Incident:** deviation-path-proportionality
**Period:** 1
**Specialist:** dcs-ops-specialist (fresh spawn — do not resume the
original S2 agent, per doctrine principle 9b)
**Triggered by:** `SAFETY.md` verdict 1 (halt), refutation 3; command
point 4 disposition `fix_taskings` (dcs-commander), `214-LOG.md`
2026-07-28T10:34:21+11:00.

## Task

One attribution fix to `dcs/references/doctrine-appendix.md`'s new
principle-15 provenance paragraph (which you authored in the prior
pass), plus one advisory fold. No criterion changes, no territory
changes, no premise change.

**Refutation 3 — fix the misattribution.** The paragraph (around lines
221-231) currently opens with wording like "This incident's own review
of the seat most exposed to that pattern... named it the dominant defect
source." That is false: the finding — "9 of `prod-tools-drift`'s 10
halts were not about the code" — was NOT made by this incident. It comes
from `vault/Decisions/fable-review-roadmap.md:55-56`, a third-party
review of DCS recorded in a DIFFERENT project's (`bread_bot`'s) session,
decided 2026-07-27 — the day BEFORE this incident even opened
(2026-07-28). This incident's 202 criterion 6 already states the correct
provenance ("still comes from `vault/Decisions/fable-review-roadmap.md`")
— the criterion was right; the prior pass's execution deviated from it.

Rewrite the paragraph's opening to attribute the finding correctly: to
the third-party review of DCS recorded 2026-07-27 (name it as such — a
third-party review, the day before this incident opened — do not cite a
`vault/` path per criterion 6's standing constraint, `vault/` still does
not ship). Keep everything else that was already verified sound: the
quoted parenthetical stays verbatim-accurate, the "as of the incident's
own close — it moves" annotation stays (principle 15's own discipline),
and the reconciliation against the adjacent "eight of ten" figure stays
(confirmed independently by the Safety Officer as accurate — do not
touch that part).

**Advisory fold 3 — add the missing version token.** The paragraph's
header parenthetical is currently the only one of five provenance
headers in this file with no version. Match the file's own idiom
(`(field lesson <date>, v<version>)`, confirmed by census of the other
four): change it to read `(field lesson 2026-07-28, v0.6.11, incident
deviation-path-proportionality)`.

## File territory (may edit only within these globs — unchanged from
your original tasking)

- `dcs/references/doctrine.md`
- `dcs/references/doctrine-appendix.md`
- `dcs/references/forms.md`

## Forbidden zones (unchanged from your original tasking)

- `dcs/references/schemas.md`
- `dcs/references/typing.md`
- `dcs/workflows/**`
- `agents/**`
- `skills/**`
- `dcs/hooks/**`
- `tests/**`
- `dcs/templates/**`
- `dcs/VERSION`
- `package.json`
- `CHANGELOG.md`
- `.dcs/**`
- `vault/**`

## Evidence required in the return

- `python tests/test_doctrine_integrity.py` — full tail + every FAIL
  line. Current baseline: 83/83 (from the original pass — note this
  suite's total may include cases discovered from sibling S1's
  concurrent fix-tasking too, if run while both are in flight; compare
  named cases, not the raw count, exactly as the original pass's
  evidence discipline required).
- `python tests/test_dcs_gate.py` — baseline 100/100, INCLUDING
  confirming the `--halt-count` line is still first, unchanged, at line
  209 (you must not have touched it — re-confirm).
- `python tests/test_dcs_intake.py` — baseline 10/10.
- **CRITERION 8 re-check:** re-run the byte-budget one-liner
  (`doctrine.md` + `schemas.md`, LF-normalised) and confirm headroom is
  still positive — your edit here is a small rewording, not expected to
  meaningfully change the count, but confirm rather than assume.
- `git diff --stat -- dcs/references/schemas.md dcs/hooks/dcs_gate.py
  tests/` — must print nothing.
- 0 Cyrillic characters in your edited region (re-run the scan) — the
  rewritten attribution must stay in English.
- Confirm no new `vault/` path citation was introduced:
  `grep -rn "vault/" --include=*.md dcs/references/doctrine-appendix.md`
  should show only generic mentions, never a citation into a specific
  file.

## On discovering the plan doesn't fit reality

STOP. Do not improvise a different fix. Return `status: "deviation"` per
`references/schemas.md` #4 (ops-specialist return), with `found`,
`why_plan_wrong`, and a `proposal`. The IC will re-enter planning around
your finding.
