# IAP — Incident Action Plan

**Incident:** revision-preservation-map
**Type:** 1
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `203-ORG.md` · `204-TASKING/*.md` · logistics plan below

## Objectives (summary of 202)

**Goal:** A narrow IAP revision taken under `dcs/workflows/plan.md`'s
`## 6c.` bounded-amendment path can no longer silently drop an
already-satisfied 202 acceptance criterion's content — the amendment path
mechanically proves every criterion untouched by the amendment still
holds in the artifact as it now stands, before it re-stamps the approval
marker.

**Acceptance criteria:**
1. `## 6c.` requires a preservation map before re-stamping, with cited
   real content per pairing (never a bare assertion).
2. `schemas.md` documents the map's shape (`grep -n "preservation"
   dcs/references/schemas.md` returns a match).
3. `tests/test_doctrine_integrity.py` gains a new mechanical check (label
   22) that verifies the map cites real content, not just the phrase
   "preservation map" — appended after the current highest section,
   touching no existing section (the pre-existing duplicate-20/mislabeled-21
   defect is untouched, owned by `field-lesson-guard-vacuity`).
4. A regression test reproduces the `register-field-repair-path` defect
   shape and demonstrates the pre-fix comparator misses it while the new
   one catches it — resolved without any git ref: one frozen fixture
   (`dropped-criterion`) read through both `prefix_coverage()` (reports
   covered) and `verify()` (names criterion 5), as two separately named
   test cases.
5. `dcs/references/doctrine-appendix.md` gains a W4 provenance entry
   citing `register-field-repair-path`'s AAR and
   `vault/Meta/building-dcs-lessons.md` §18.
6. If `dcs/references/doctrine.md` needs a pointer, added bytes are
   checked against `HOT_PATH_BUDGET_KB` (band: 36865-37888 B); the fix
   funds its own trim rather than shipping over budget.
7. `npm test` (all three suites, since its script already runs
   `test_dcs_gate.py` + `test_dcs_intake.py` + `test_doctrine_integrity.py`)
   is green; the Safety Officer additionally runs `tests/test_dcs_cli.py`
   once since S1 adds a new payload path.
8. [IC] Register territory refined at step 5a below, row updated at
   close.

**Out of scope this period:** renumbering the pre-existing duplicate-20/
mislabeled-21 defect (owned by `field-lesson-guard-vacuity`, rank 4);
`semantic-content-loss-guard`'s broader class-level guard; widening
`dcs_gate.py`'s hash coverage beyond `IAP.md` (escalate as a deviation if
a specialist concludes it's the only fix); the sequencing decision among
this incident, `field-lesson-guard-vacuity`, and
`semantic-content-loss-guard` over shared `tests/test_doctrine_integrity.py`
territory (deferred to the next `/dcs-esg`).

## Tactics (from the Planning Chief)

- T1: put the mechanism in an executable (`dcs/tools/preservation_map.py`),
  not prose — the abandoned attempt's failure mode was prose-only plus a
  phrase-grep check.
- T2: the validator must distrust the map's self-reported `output` — it
  re-derives every pairing from the artifact's actual bytes, never trusts
  the pasted output field (the AAR's second, compounding defect).
- T3: coverage in both directions — criteria named by the amendment plus
  criteria in the preservation map must equal the full criterion set, and
  every preserved anchor must still occur in its named artifact.
- T4: prove non-vacuity with frozen fixtures plus an in-suite forgery (the
  idiom already used at check 18(f)) — `clean`/`dropped-criterion`/`no-map`
  fixtures, plus an in-memory anchor-deletion proof.
- T5: make the guard bite in the field going forward without retroactively
  failing history — walk `214-LOG.md` for `## 6c.` re-stamps on/after a
  pinned effective date (2026-08-02), not before.
- T6: one shape, documented once — new `schemas.md` #9, modeled on #7's
  precedent for a workflow-parsed (non-agent-return) shape, deliberately
  excluded from the "Returned by" contract population.
- T7: fund both budgets (hot-path 402 B headroom, `plan.md` 3-line
  headroom) from compression in place inside the same files being
  edited, with a before/after trim ledger.
- T8: no agent charter changes — confirms `dcs-commander.md` and
  `dcs-safety-officer.md` out of scope, as the 201 left unconfirmed.

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | `dcs/tools/**`, `tests/test_doctrine_integrity.py`, `tests/fixtures/preservation-map/**`, `dcs/README.md` | `dcs/workflows/**`, `dcs/references/**`, `dcs/hooks/**`, `dcs/templates/**`, `dcs/esg/**`, `dcs/VERSION`, `agents/**`, `skills/**`, `bin/**`, `tests/payload_check.py`, `tests/test_dcs_gate.py`, `tests/test_dcs_intake.py`, `tests/test_dcs_cli.py`, `tests/fixtures/halt-ceiling/**`, `package.json`, `install.ps1`, `install.sh`, `.dcs/**`, `vault/**` |
| S2 | `dcs/workflows/plan.md` | every other `dcs/workflows/*.md`, `dcs/references/**`, `dcs/tools/**`, `dcs/hooks/**`, `dcs/templates/**`, `dcs/esg/**`, `dcs/README.md`, `dcs/VERSION`, `tests/**`, `agents/**`, `skills/**`, `bin/**`, `package.json`, `install.ps1`, `install.sh`, `.dcs/**`, `vault/**` |
| S3 | `dcs/references/schemas.md`, `dcs/references/doctrine.md`, `dcs/references/doctrine-appendix.md` | `dcs/references/forms.md`, `dcs/references/typing.md`, `dcs/workflows/**`, `dcs/tools/**`, `dcs/hooks/**`, `dcs/templates/**`, `dcs/esg/**`, `dcs/README.md`, `dcs/VERSION`, `tests/**`, `agents/**`, `skills/**`, `bin/**`, `package.json`, `install.ps1`, `install.sh`, `.dcs/**`, `vault/**` |

**Partition status:** disjoint — parallel execution. Independently
verified pairwise by the IC at command point 2 (`214-LOG.md`), not merely
trusted from `partition_ok: true`.

## Deploy / environment plan (Type 1, from the Logistics Chief)

**Deploy path:** Scoped payload deploy, post-close only. Run
`powershell -ExecutionPolicy Bypass -File C:\DCS\install.ps1` (POSIX:
`./install.sh`) after `/dcs-close` merges to main, then the content
witness `python tests/payload_check.py`, resolving exit codes per
`dcs/workflows/deploy.md` step 7 (0 identical and 3 installed-only-only
are pass dispositions; 1 differing/repo-only and 2 environment error are
stop dispositions). Only the `dcs/` half of this change reaches the
installed copy: `install.ps1` copies `dcs/` recursively, plus
`agents/dcs-*.md` and `skills/dcs-*/`, and nothing else — so the
`plan.md`/`schemas.md`/`doctrine-appendix.md` edits deploy, while the new
check and regression test in `tests/test_doctrine_integrity.py` never
land in `~/.claude` (they act at merge time from the repo, and ship to the
registry only via `package.json`'s `files` whitelist, which does include
`tests/`). `npm publish` is Owner-only with a 2FA OTP and is not part of
this deploy — the session prepares the release (atomic version bump in
`dcs/VERSION` + `package.json` in one commit, CHANGELOG entry, `npm pack
--dry-run` review) and stops there.

**Env/deps:** No new environment variables. No new package dependencies —
stdlib-only Python like the rest of the suite. No config changes.
Existing prerequisites only (python on PATH, PowerShell+robocopy on
Windows). Version bump: baseline 0.7.2 in both `dcs/VERSION` and
`package.json`; recommend patch bump to 0.7.3 (new required artifact on
one workflow path plus one new guard check, no consumer-facing contract
removed) — decided by the IC in the integration commit, both files moving
together.

**Migration ordering:** None — no database, no running service, no
persisted state. Two ordering constraints stand in a migration's place:
(1) `CLAUDE.md`'s hard rule — `install.ps1` must not run while this
incident is active, and it bites hardest here because this incident edits
`plan.md`'s own bounded-amendment path; order is guard green → `/dcs-close`
→ merge → install → witness. (2) same-commit coupling: the new check and
the prose it validates must land in one commit, same as `dcs/VERSION` +
`package.json`'s existing coupling.

**Rollback plan:** Git revert of the merge commit, then re-run
`install.ps1` and `payload_check.py` to confirm match. Nothing here is
destructive — every payload edit is additive prose inside existing files,
and the guard change adds a check rather than removing one. Two caveats:
(a) `install.ps1`'s `robocopy /E` never purges, so a revert strands the
new `dcs/tools/preservation_map.py` in `~/.claude/dcs/` and
`payload_check` reports it installed-only (exit 3) until deleted by hand;
(b) rollback is trivial only before `npm publish` — after a publish the
only route is forward-fix (`npm deprecate` + a new patch).

## Risks

- Ordering coupling S1↔S2↔S3: disjoint files but shared literals (the
  invocation string, the section-9 heading) pinned verbatim on both sides
  so neither invents them; a red carrier case before its counterpart
  lands is expected and reported by name, not hidden.
- Check-number collision with REGISTER rank 4: `field-lesson-guard-vacuity`
  will need to renumber around label 22 when it fixes the duplicate-20
  defect. IC's call, resolved: append at 22 per criterion 3's literal
  rule; a visible gap at 22 would be worse than a renumber `field-lesson-guard-vacuity`
  has to do regardless.
- Two tight budgets (`plan.md` 3 lines, hot path 402 B) funded by
  compression in the same files specialists are already editing —
  mandatory trim ledgers so this incident about content-loss does not
  itself lose content while fixing it.
- The hot-path ratchet constant (`HOT_PATH_BUDGET_KB`) lives in S1's file
  — if S3 lands outside the 36865-37888 B band, that's a deviation to the
  IC, not a reach into S1's territory.
- The new field-scoped check can go red on a FUTURE incident by design
  once the 2026-08-02 effective date passes — expected behavior, not a
  defect.
- New shipped payload path (`dcs/tools/preservation_map.py`) will show as
  repo-only (exit 1) in `payload_check.py` until the post-close install —
  correct, not drift.
- Version sync (`dcs/VERSION` + `package.json`) is forbidden to all
  specialists and is the IC's job in the integration commit.
- Fixtures ship via `package.json`'s `files` whitelist — must be neutral
  fiction, no `schemas.md #N` citations inside them.

## Verification plan

1. The mechanism runs and discriminates correctly on all three frozen
   fixtures — re-run independently rather than trusting specialist paste.
2. The `dropped-criterion` fixture's dual reading (`prefix_coverage()`
   returns `[]` vs `verify()` names criterion 5) IS criterion 4's
   evidence — confirm both are separately named test cases, not one
   aggregate assertion, and the fixture is frozen (no git ref anywhere).
3. Nothing else moved: `grep` confirms both `# --- 20.` headings and the
   mislabeled `# --- 21.` are untouched, single trailing append hunk,
   `dcs_gate.py` appears in no diff, no `agents/**` file changed.
4. Whole suite green together (`npm test` + `tests/test_dcs_cli.py` as an
   extra) with each suite's own printed count read directly, plus manual
   review of both trim ledgers against their diffs to confirm no rule's
   content was actually lost in compression — this incident exists
   because a narrow revision dropped content nobody re-read, so a Safety
   Officer who accepts "compressed in place" as a claim rather than
   re-reading the before/after reproduces the defect inside its own fix.
   There is no 201 repro path to re-run (structural gap, not a runtime
   bug); the `dropped-criterion` fixture is its stand-in.

## Deviation history (this period)

none
