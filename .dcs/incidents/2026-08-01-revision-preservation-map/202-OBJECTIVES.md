# 202 — Objectives (Operational Period 1)

**Incident:** revision-preservation-map
**Period:** 1

## Goal

A narrow IAP revision taken under `dcs/workflows/plan.md`'s `## 6c.`
bounded-amendment path can no longer silently drop an already-satisfied
202 acceptance criterion's content — the amendment path mechanically
proves every criterion untouched by the amendment still holds in the
artifact as it now stands, before it re-stamps the approval marker. This
closes the exact gap that let `register-field-repair-path` (2026-07-27)
lose a Safety-verified criterion's answer while repairing an unrelated
halt.

## Acceptance criteria (the Definition of Done)

1. `dcs/workflows/plan.md`'s `## 6c.` boundary conditions (or an added
   step in that path) require, before the marker is re-stamped, a
   preservation map: every 202 acceptance criterion NOT named by the
   triggering amendment is paired with the section of the current
   artifact that satisfies it, with that section's actual content (or a
   command whose output shows it is present) cited beside the pairing —
   never a bare assertion of coverage (doctrine principle 15).
2. `dcs/references/schemas.md` documents the preservation map's shape (a
   new numbered section, or a documented extension of an existing one) so
   the field is not invented ad hoc per incident. Verify:
   `grep -n "preservation" dcs/references/schemas.md` returns a match
   describing the shape.
3. `tests/test_doctrine_integrity.py` gains a new mechanical check that
   verifies a preservation map exists AND cites real, checkable content
   for a `## 6c.` amendment — not merely that the phrase "preservation
   map" appears (the exact vacuity the abandoned 2026-07-31 attempt's
   check 23 had: it only greped `plan.md`'s own prose for the phrase and
   a provenance string, never checking any incident's actual map). The
   new check is appended **after** the current highest-numbered
   `# --- N.` section — regenerate the correct next number at tasking
   time with `grep -n '^# --- [0-9]' tests/test_doctrine_integrity.py`,
   never hardcode a number in this document — and does **not** renumber,
   edit, or otherwise touch any existing section. The pre-existing
   duplicate-`20`/mislabeled-`21` numbering defect (two sections both
   headed `# --- 20.`, outbound guard mislabeled `21` instead of `22`) is
   left exactly as found, for `field-lesson-guard-vacuity` (REGISTER.md
   rank 4) to fix independently.
4. A regression test reproduces the `register-field-repair-path` defect
   shape (a narrow amendment that edits one criterion's content while
   silently dropping a different, previously-satisfied criterion's
   section) and demonstrates: it fails against the pre-fix mechanism, and
   passes once the new check/mechanism is in place. Per principle 15 the
   test pins immutable evidence (a fixture or frozen artifact snapshot),
   never a moving ref (branch name, `HEAD`, "the integration tip").
5. `dcs/references/doctrine-appendix.md` gains a provenance entry for this
   defect class, citing `register-field-repair-path`'s `AAR.md` and
   `vault/Meta/building-dcs-lessons.md` §18 — rule stays in the core
   (`plan.md`/`doctrine.md`), story goes here, per this project's own
   rule/story split (`CLAUDE.md`, "Where lessons go").
6. If `dcs/references/doctrine.md` needs a pointer to the new mechanical
   requirement (e.g. near principle 8), any added bytes are checked
   against `HOT_PATH_BUDGET_KB` — regenerate with
   `wc -c dcs/references/doctrine.md dcs/references/schemas.md`. If the
   hot path would exceed budget, the fix funds its own trim rather than
   shipping over budget (pay-as-you-go, the v0.6.14 precedent).
7. `npm test` (`test_dcs_gate.py` + `test_dcs_intake.py`) and
   `python tests/test_doctrine_integrity.py` all report every case
   passing, including the new check from criterion 3 and the regression
   test from criterion 4.
8. [IC] The register's territory cell for this incident is refined to the
   union of the actual `204-TASKING/*.md` territories at `/dcs-plan` step
   5a, and the row is updated at close per `REGISTER.md`'s own
   conventions.

## Out of scope this period

- Renumbering or otherwise fixing the pre-existing duplicate `# --- 20.`
  / mislabeled `# --- 21.` sections in `tests/test_doctrine_integrity.py`
  — owned by the already-queued `field-lesson-guard-vacuity` (rank 4).
  This incident's own new check must not disturb that numbering (see
  criterion 3).
- `semantic-content-loss-guard`'s broader, class-level trim-content-loss
  guard (a general test-preserves-semantic-content check across any
  budget trim) — a separate, unranked, queued incident.
- Widening `dcs_gate.py`'s hash-stamp coverage beyond `IAP.md` to other
  `.dcs/**` artifacts — a materially larger mechanism change than this
  incident's scope. If the Planning Chief concludes this is the only
  viable fix, that is a scope question for the IC/Owner (deviation or
  `esg_activation`), never a silent expansion of this period's taskings.
- Any sequencing decision among this incident, `field-lesson-guard-vacuity`,
  and `semantic-content-loss-guard` over their shared
  `tests/test_doctrine_integrity.py` territory — `REGISTER.md` itself
  defers that decision to the next `/dcs-esg`; this period only has to
  avoid worsening the collision (criterion 3's append-only constraint).

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

(pending)
