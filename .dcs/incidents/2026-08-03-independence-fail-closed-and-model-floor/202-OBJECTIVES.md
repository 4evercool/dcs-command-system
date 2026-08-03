# 202 — Objectives (Operational Period 1)

**Incident:** independence-fail-closed-and-model-floor
**Period:** 1

## Goal

DCS's close-time and Delegation-approval machinery stop treating every
operating model and every Safety-Officer-spawn outcome identically. An
unattended close is refused whenever this period's Safety verdict either
lacks proof of independent-agent origin or contains `checked` commands
that do not reproduce — refusal means PARK or an Owner `AskUserQuestion`
gate, never a silent close. Separately, `.dcs/esg/DELEGATION.md` gains an
approved-model list, and unattended/auto-approval bounds
(`auto_approve_type3`, `deploy.auto`, `deploy.auto_after_close`) apply
only when the session's operating model is on that list — every other
model gets full v0.1 every-gate-is-an-Owner-gate behavior at every site
that currently reads those bounds.

## Acceptance criteria (the Definition of Done)

1. **[CORRECTED at /dcs-plan lint 3a, second pass — the original
   `Verified:` clause below was vacuous: `grep -c "step 8\|Safety
   Officer" dcs/workflows/execute.md` returns 10 matches on today's
   UNCHANGED tree, so it would pass identically before and after the
   work and witnesses nothing. Independently re-confirmed by the IC.]**
   `dcs/workflows/execute.md` step 8 (Safety Officer spawn) gains an
   explicit spawn-liveness fallback, written into step 8's own body —
   either doctrine's existing "empty/errored return is a FAILED spawn,
   re-spawn on the next tier, log both attempts" rule (`doctrine.md:33-36`,
   citable by section name, not to be edited here) extended in spirit to
   the Safety Officer spawn, or an equivalent dedicated rule — such that a
   spawn that never returns a decision is never silently treated as
   "Safety verification happened." **Verified (discriminating,
   before/after):** `sed -n '/^## 8\./,/^## 9\./p' dcs/workflows/execute.md`
   shows the fallback inside step 8's own body, plus a before/after count
   on whichever token is actually written (measured pre-change baseline,
   all zero: `grep -c "FAILED spawn"` = 0, `grep -c "never returns"` = 0,
   `grep -c "re-spawn on the next tier"` = 0, in `dcs/workflows/execute.md`).
2. When independent Safety Officer spawn cannot be established after
   criterion 1's retry protocol is exhausted, `dcs/workflows/close.md`
   refuses to complete an unattended close this period: it either PARKs
   the incident (register row state `PARKED`, reason naming the spawn
   failure) or routes to the Owner via `AskUserQuestion` before the merge
   step — never proceeding as if verification happened. Verified: `grep
   -n "unattended" dcs/workflows/close.md` returns at least one match
   tying the word to this new gate (the word occurs zero times today, per
   201-BRIEF.md's evidence).
3. `dcs/references/schemas.md` #5 (Safety-officer verdict)'s `checked`
   field definition states explicitly that each entry must be a
   **regenerable** command — one whose output a later reader can re-run
   and compare, not a description or a one-off manual observation.
   Verified: `grep -n "regenerable" dcs/references/schemas.md` matches
   inside the #5 section (zero matches anywhere in the shipped payload
   today).
4. `dcs/workflows/close.md` re-runs at least one `checked[]` command from
   the current period's `SAFETY.md` verdict before completing the merge;
   if the re-run's output does not match the recorded output, that is
   treated as a halt through the existing halt-handling machinery
   (`SAFETY-HALT:` sentinel, IC disposition) — never a silent
   pass-through. The concrete mechanism (inline close.md step vs. a new
   `dcs/tools/` script in the `preservation_map.py`/`record_integrity.py`
   convention) is the Planning Chief's tactical call, but it must be
   fixture-verifiable per criterion 8, not merely prose describing
   intent.
5. `dcs/references/doctrine.md` states the new independence/regenerability
   rule — either an explicit extension of principle 7 ("Independent
   safety authority") or a new principle — funded within the existing
   hot-path budget. **Measured now:** `python -c "d=open('dcs/references/doctrine.md','rb').read().replace(b'\r\n',b'\n'); s=open('dcs/references/schemas.md','rb').read().replace(b'\r\n',b'\n'); print(len(d)+len(s))"`
   currently returns 37834 bytes against the `HOT_PATH_BUDGET_KB = 37`
   (37888-byte) ceiling in `tests/test_doctrine_integrity.py` — 54 bytes
   of headroom. Any net addition across `doctrine.md` + `schemas.md`
   beyond that must be funded by a trim in the same tasking (pay-as-you-go,
   the v0.6.14 precedent), not discovered as a red check at merge time.
   [IC] for the measurement above; the edit + any funding trim is
   specialist work.
6. `.dcs/esg/DELEGATION.md`'s `delegation-bounds` JSON schema
   (`dcs/references/schemas.md` #7) gains an `approved_models` (or
   equivalently-named) array field; `dcs/templates/DELEGATION.md` (the
   founding template every new project receives) carries the same field
   with a documented default (empty, or a comment explaining the
   v0.1-fallback behavior when the list is empty/absent). Verified: grep
   both files for the new key.
7. **[CORRECTED at /dcs-plan lint 3a — the original list below was stale;
   regenerate with `grep -rn "auto_approve_type3\|auto_after_close\|deploy\.auto\b"
   dcs/ agents/ skills/ README.md` plus a direct read of `deploy.md` (its
   `auto: true`/`false` phrasing defeats a literal `deploy\.auto` grep),
   never hand-carry this list forward.]** Every existing read site for
   `auto_approve_type3` / `deploy.auto` / `deploy.auto_after_close` — nine
   sites across six files: `dcs/workflows/plan.md:31` (step 2,
   Delegation-aware confirm — decides whether the Owner even sees the 202
   before planning proceeds) **and** `plan.md:124-130` (step 6, IAP
   approval bound check); `run.md:70-71` (`auto_approve_type3`) **and**
   `run.md:154-158` (step 7a, `deploy.auto_after_close`); `loop.md:28-38`
   (specifically ~33/36, the every-run expectation-setting statement)
   **and** `loop.md:71` (hard rule 2's `auto_after_close` reference);
   `deploy.md:117-124` (step 5's deploy-delegation check); `status.md:106`
   (read-only report); `esg.md:33` (founding-default note) — is updated so
   that bound genuinely holds **only when** the session's current
   operating model appears in `approved_models`; a session on an unlisted
   model gets full v0.1 every-gate-is-an-Owner-gate behavior at each site,
   regardless of what the bound's other fields say. **Not dependent on
   the separate, still-unshipped `log-append-helper` incident** (rank 3)
   — the model check reads the CURRENT session's own identity the same
   way doctrine's existing "Transfer of command" mechanics already do
   when deciding whether to spawn `dcs-commander`; it does not require a
   structured 214-LOG.md record to function. **Known, deliberately
   out-of-scope gap (report to Owner at IAP presentation, candidate
   follow-up row, not silently absorbed):** `plan.md:130`'s "no
   DELEGATION.md → fallback to `config.json`" auto-approval branch has no
   model-floor check after this incident ships, since that branch by
   definition has no `DELEGATION.md` to read `approved_models` from;
   `vault/Decisions/non-anthropic-hardening.md` measure 5 names
   `.dcs/esg/DELEGATION.md` specifically, never `config.json`'s separate
   fallback mechanism. Verified: grep each of the six files for the new
   model check; `plan.md` and `run.md` and `loop.md` must each match
   twice (their two independent read sites).
8. Regression/fixture coverage proves both new mechanisms actually gate,
   not merely exist in prose: (a) a fixture proving criterion 4's re-run
   step halts on a non-reproducing `checked` entry and passes on a
   genuine one; (b) a fixture or documented dry-run trace proving
   criterion 7's model check actually withholds auto-approval for an
   unlisted-model session at no fewer than two of the read sites listed
   in criterion 7 (not just the one easiest to test).
9. `tests/test_doctrine_integrity.py`, `test_dcs_gate.py`, and
   `test_dcs_intake.py` all continue to pass; if criteria 3/6's schema
   additions warrant a corresponding structural check (e.g. extending an
   existing citation or field-presence check), that check is added now
   rather than left for a later incident to discover missing. Verified:
   `python tests/test_doctrine_integrity.py`, `python tests/test_dcs_gate.py`,
   `python tests/test_dcs_intake.py` each report `N/N passed`.
10. [Owner] `.dcs/esg/DELEGATION.md` is amended to v7 with the new
    `approved_models` list populated. `fable` belongs on it at minimum,
    since doctrine already treats Fable as the trusted command-judgment
    seat; which other models (if any) join the list is the Owner's call
    alone, confirmed via `AskUserQuestion` before v7 is written — never a
    default the IC or a specialist infers.
11. [IC] The register's territory cell for this incident is refined to
    the union of the actual `204-TASKING/*.md` territories at `/dcs-plan`
    step 5a, replacing the corrected-but-still-provisional list in
    201-BRIEF.md.

## Out of scope this period

- Measure 1's log-append helper (structured, timestamped `214-LOG.md`
  entries with operator identity) — the separate queued incident
  `log-append-helper` (register rank 3). Criterion 7 is explicitly
  designed not to depend on it landing first.
- Historical remediation: the two already-known false-"verbatim"
  attributions this period's own 201 evidence cites
  (`worktree-removal-self-conflict`, `check-14-hardening`) are the
  separate queued incident `record-verbatim-attribution-followup`. This
  incident builds the guard going forward only.
- Any change to `dcs/hooks/dcs_gate.py` itself (the PreToolUse
  source-edit gate and its halt-ceiling counter) — the new mechanisms are
  close-time and Delegation-bound-read logic, a different layer. If a
  tasking discovers this is genuinely unavoidable, that is a deviation,
  not a silent scope expansion — `dcs/hooks/**` is also a Delegation
  `forbidden_globs` entry and a `CLAUDE.md`-designated Type 1 trigger in
  its own right.
- The already-shipped `spawn-effort-control` "Capability tier"
  per-spawn-seat mechanism (`doctrine.md:31`) — distinct, not touched.
- Populating `approved_models` with any model beyond what the Owner
  explicitly names at criterion 10 — no default heuristic list, no
  IC-inferred "models that seem trustworthy."
- `russian-artifacts-translation`, `shipped-project-facts-sweep`,
  `close-md-lock-diagnostic-inert`, `field-lesson-guard-vacuity`,
  `semantic-content-loss-guard`, `shipped-set-defined-three-times` — all
  separate queued rows; `close-md-lock-diagnostic-inert` and
  `field-lesson-guard-vacuity` also touch `close.md`/`test_doctrine_integrity.py`
  and must not run concurrently with this incident (sequencing, not
  folding in).
- Any sequencing decision among this incident and the other `QUEUED` rows
  sharing territory — deferred to the next `/dcs-esg`.

## Chief feedback

Planning Chief (opus) returned 5 `objectives_feedback` items. IC resolution
of each:

1. **Criterion 7's site enumeration was stale (5 of 9 real sites named).**
   Accepted and applied — criterion 7 above is corrected in place, and the
   correction was independently re-verified by the IC (not merely
   transcribed from the chief), per lint 3a. See `214-LOG.md`'s lint
   entry for the regenerating command and full output.
2. **Criterion 4's "does not match the recorded output" is unimplementable
   as literal byte equality, and most `checked[]` entries cannot
   reproduce at close time by construction (they're pre-integration-commit
   working-tree diffs).** Accepted. The chief's fix — containment
   (recorded observation is a substring of fresh output) plus a selection
   rule that skips non-reproducible-by-design entries and treats "no
   stable entry found" as a finding, never a silent pass — is the
   intended reading of criterion 4 going forward. This is a
   clarification of intent, not a scope change: criterion 4's text is
   unchanged above, and S4's tasking carries the operative detail.
3. **Criterion 3's schema text and schemas.md's own halt-shape example
   (line 102) are coupled** — the existing example's `checked` entries
   carry no observation, making them non-conforming under criterion 3's
   new rule and giving criterion 4's tool nothing to compare against.
   Accepted. Folded into S1's tasking (fix both the field-table row and
   both example blocks).
4. **Criterion 10 cannot be witnessed from this worktree** —
   `.dcs/esg/DELEGATION.md` is git-ignored and lives only in the main
   checkout, never entering the branch or the merge. Accepted as a real
   3b measured-claim gap. Resolution: the IAP's verification plan will
   require the witness commands' OUTPUT (`grep -n "approved_models"` and
   `grep -n '"version": 7'` against `<esg_root>/.dcs/esg/DELEGATION.md`)
   to be pasted into `214-LOG.md` at the point the Owner writes v7 — not
   left as an unmeasured assertion. Criterion 11 (register territory,
   [IC]) gets the same treatment.
5. **Criterion 8(b)'s "dry-run trace" is not achievable for prose
   workflows** — there is no runtime to dry-run six markdown files
   against. Accepted. The chief's substitute — a merge-guard presence-
   and-coverage check (every bound-read site has a co-located model gate;
   a new site added later fails by name, the `test_doctrine_integrity.py`
   check-14 pattern) — is a structurally honest replacement for a
   behavioral test criterion 8(b) as literally worded could never have
   gotten from this codebase. Criterion 8(b)'s text is unchanged (it
   still reads as a floor, not a ceiling, per the chief's own framing);
   S4's tasking carries the actual mechanism.
