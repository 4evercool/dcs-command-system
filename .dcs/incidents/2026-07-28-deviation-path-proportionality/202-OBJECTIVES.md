# 202 — Objectives (Operational Period 1)

**Incident:** deviation-path-proportionality
**Period:** 1

## Goal

A narrow, no-premise-change amendment to an approved plan — reached via
any of the three deviation dispositions (`replan` / `amend_tasking` /
`escalate_owner`) or a Safety-verdict fix-tasking — costs ceremony
proportional to its own size instead of a full replanning cycle, while
remaining fully counted by the existing attempt/halt machinery; and a
fact a prior DCS seat already established moves into a later artifact by
reference to its source, not by the Dispatcher retyping it from memory.

## Acceptance criteria (the Definition of Done)

1. `dcs/workflows/execute.md` and/or `dcs/workflows/plan.md` define at
   least one amendment path — usable for a narrow, no-premise-change fix
   regardless of which of the three deviation dispositions, which
   Safety-verdict fix-tasking, **or which post-pass advisory correction
   that touches `IAP.md` content (`execute.md` step 9) triggered it**
   (widened by Planning Chief ruling — see Chief feedback) — whose total
   ceremony (agent spawns + Owner `AskUserQuestion` round-trips) is
   documented as strictly less than a full `plan.md` steps-1-9 pass,
   while the path still produces a stamp that satisfies `dcs_gate.py`'s
   existing `marker_valid()` check unchanged, and that trigger (c)'s
   attempt count (the `IAP-APPROVED:` sentinel tally in `214-LOG.md`)
   still captures with no bypass.

2. The new path's boundary is explicit in the workflow text: it states
   the conditions under which it applies (e.g. single-tasking scope, no
   territory/premise change) and, symmetrically, that anything outside
   those conditions falls back to the existing full-replan path
   unchanged — so the cheap route cannot be reached for a genuine
   re-plan.

3. Re-tracing both field measurements this incident's 201 cites —
   `halt-loop-unbounded`'s S3 `amend_tasking` deviation
   (`.dcs/incidents/2026-07-25-halt-loop-unbounded/214-LOG.md:96-127`)
   and `register-field-repair-path`'s Halt-2 `fix_taskings` repair
   (`.dcs/incidents/2026-07-27-register-field-repair-path/214-LOG.md:31-44`)
   — against the new path's documented steps shows measurably fewer
   agent spawns and/or fewer Owner round-trips than what actually
   happened. **[S1 derives the count as evidence, using an anchored
   grep against each log, not a bare substring count; IC records the
   finished side-by-side table into the IAP's verification plan]** —
   split ownership per Planning Chief ruling, see Chief feedback.

4. `dcs/hooks/dcs_gate.py` and `tests/test_dcs_gate.py` are untouched by
   this incident (`git diff --stat` shows zero lines against both) — the
   standing constraint from command point 1 typing. [IC]

5. At least two of this incident's own in-territory command-point spawn
   instructions (candidates: `execute.md`'s deviation-arbitration and/or
   verdict-disposition spawn prompts; `plan.md`'s `iap_review` spawn
   prompt) are rewritten to instruct citing the source artifact (file
   path + line, or a regenerating command) for a fact a prior seat
   already established, rather than instructing the Dispatcher to
   summarize or retype it — demonstrated by the rewritten text itself,
   not merely a new abstract rule. (Backlog Rec 2, folded in at typing,
   2026-07-28.)

6. `dcs/references/doctrine.md` states the by-reference-not-retype
   principle generally (new principle, or an amendment to an existing
   one — chief's tactics decide placement), with
   `dcs/references/doctrine-appendix.md` carrying the provenance in the
   file's own established idiom (a `**Principle N — <topic> (field
   lesson <date>, v<version>).**` paragraph naming **this incident**,
   per Planning Chief ruling — **not** a `vault/` path: `vault/` is
   absent from `package.json`'s `files` whitelist, confirmed directly
   (`['bin/', 'dcs/', 'agents/', 'skills/', 'docs/', 'tests/',
   'install.ps1', 'install.sh', 'README.md', 'CHANGELOG.md']`), so a
   citation into it would be a dead pointer in every downstream install
   and collides with `CLAUDE.md`'s "ship no project facts" rule. The
   underlying field evidence — "9 of `prod-tools-drift`'s 10 halts were
   not about the code" — still comes from
   `vault/Decisions/fable-review-roadmap.md`; only the shipped citation's
   form changes, see Chief feedback).

7. `tests/test_doctrine_integrity.py`, `tests/test_dcs_gate.py`, and
   `tests/test_dcs_intake.py` all still pass after the change — `npm
   test` plus `python tests/test_doctrine_integrity.py`, per `CLAUDE.md`'s
   Verification suite, with real output recorded as evidence.

8. The hot-path budget guard (`test_doctrine_integrity.py`'s byte-count
   check over the doctrine/schemas hot-path pair) still passes at
   whatever ratchet is currently in force. **MEASURED CLAIM:** run the
   guard and record the actual before/after byte counts as evidence — do
   not carry forward a byte count from any prior incident's register row.

9. **MEASURED CLAIM**, established now: `npm view dcs-command-system
   version` → `0.6.10` (run 2026-07-28T08:5x+11:00, this incident's own
   stem), matching both `dcs/VERSION` and `package.json` (also read
   directly, both `0.6.10`) — tree and registry are in sync, so this is
   an ordinary next release, not a fill-in of an already-ahead tree.
   `dcs/VERSION` and `package.json` are bumped together, atomically (same
   commit, per `CLAUDE.md`'s version-sync rule), to `0.6.11` — the next
   minor, per the Owner-approved roadmap's "Channel 1, minor version" —
   with a `CHANGELOG.md` entry under a new dated section.

## Out of scope this period

- **Actually running `npm publish`** — Owner-only, requires a 2FA OTP,
  never attempted by a session (`CLAUDE.md`'s Deploy table). This
  incident prepares the release (criterion 9) and stops there; `npm pack
  --dry-run` review before close, not a publish.
- **`revision-preservation-map`** (`vault/Backlog.md` item 19, register
  rank 5) — a related but disjoint candidate fix (a required preservation
  map before re-stamping a narrow revision). Explicitly out of this
  incident's scope per the 201's decomposition check.
- **Any change to `dcs/hooks/dcs_gate.py` or `tests/test_dcs_gate.py`**,
  including generalizing `halt_cycles()` into a code-level attempt/stamp
  counter (`vault/Meta/building-dcs-lessons.md` §10) — standing
  constraint from command point 1 typing. A future Type 1 incident's
  scope if ever pursued.
- **The roadmap's un-sourced "one-line export crossing `max_files`"
  example** and Delegation-bound-crossing (escalation trigger (d))
  ceremony proportionality generally — a different mechanism, not
  measured in this repo. Excluded per the 201's decomposition check.
- **The full breadth of Rec 2** ("the Dispatcher never re-types values
  anywhere in DCS") beyond this incident's own in-territory
  command-point spawn instructions — criterion 5 scopes it to a concrete
  minimum inside `execute.md`/`plan.md`. A fuller sweep across
  `new.md`/other workflows, if warranted, is the next `/dcs-esg`'s call
  to queue, not this incident's to absorb.
- **`decomposition-backlog-routing`** (register rank 9) — explicitly the
  next incident per the roadmap, not part of this one.

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

Eight of nine criteria verifiable as written; four points needed an IC
ruling, all resolved here (criteria 1/3/6 revised above; criterion 8
below is acknowledgment only, no text change):

1. **Criterion 6's `vault/` citation was a dead pointer.** `vault/` ships
   in no install (`package.json`'s `files` whitelist confirmed directly,
   see criterion 6). **Ruling: accepted the Chief's substitution** — the
   appendix names the incident, in its own established provenance idiom,
   not a `vault/` path. Criterion 6 revised above.
2. **Criterion 1's trigger list didn't cover the case criterion 3 itself
   requires re-tracing.** Field measurement 2's *second* re-stamp was a
   post-pass advisory correction inside `IAP.md` (`execute.md` step 9),
   not one of the three deviation dispositions or a fix-tasking — the
   best-evidenced, cheapest case in the whole incident, excluded by the
   letter of the original wording. **Ruling: widened.** Criterion 1
   revised above.
3. **Criterion 3's recording site (verification plan / `SAFETY.md`) is
   not something a specialist may write** (IC- and Safety-Officer-owned
   artifacts respectively; lint check 6). **Ruling: split ownership** —
   S1 derives the count as evidence (anchored grep, not a bare substring
   count), IC transcribes the finished table into `IAP.md`'s verification
   plan. Criterion 3 revised above.
4. **Criterion 8 is tighter than its wording suggests** (1,205 B of
   headroom for the whole incident, measured by the Chief before any
   edit: `doctrine.md` 23,387 B + `schemas.md` 13,296 B = 36,683 B
   against a 37,888 B ceiling — independently re-confirmed by the IC,
   identical numbers). This is why one specialist (S2) owns the entire
   hot path and why the tactics prefer amending principle 15 over adding
   a new principle 16. **Ruling: acknowledged, no criterion text change**
   — if the mandatory clause (criterion 6) doesn't fit, S2 reports a
   deviation rather than trimming unrelated doctrine prose; the optional
   principle-8 pointer (tactics, not a criterion) is dropped first if
   space runs out.

Also flagged, not requiring a ruling: `dcs/workflows/run.md`'s pause list
(escalation-gate enumeration) is a plausible follow-up home for
mentioning the new amendment path, but no criterion requires it and it's
out of every tasking's territory — left as a noted follow-up, not
absorbed into this period.
