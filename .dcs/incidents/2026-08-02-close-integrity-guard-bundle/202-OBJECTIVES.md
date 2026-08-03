<!--
202-OBJECTIVES.md -- written by the IC together with the Owner, at the
start of EACH operational period (/dcs-plan). Re-drafted (new file content,
same filename) each time the incident re-enters the P-loop for another
period -- the prior period's 202 is preserved in 214-LOG.md's phase-
transition history and, once complete, in AAR.md's summary, not in this
file itself.
-->

# 202 — Objectives (Operational Period 1)

**Incident:** close-integrity-guard-bundle
**Period:** 1

**Revision note (attempt 2 of period 1):** the period-1 IAP was approved,
executed (S1-S4 all `status: "done"`), and the Safety Officer halted on
two refutations — a tautological term-census check, and a permanent,
unremediable false-positive this incident's OWN `214-LOG.md` now
contains (line 30, discovered by running the shipped tool against this
incident's own directory per criterion 14). `dcs-commander` ruled
**replan**, not fix-taskings, because the correct fix revises
Owner-facing 202 content (criterion 1(b)'s suppression mechanism and
criterion 14's own procedure), not implementation detail. Full ruling:
`214-LOG.md`'s `command: verdict_disposition replan` entry. What changed
in this revision: criterion 1(b) (a real, grammar-recognized correction
mechanism, replacing a substring-mention suppression that was broken at
both ends), criterion 3 and 6's date-pin constants (an off-by-one-day bug
fixed by stating the exact required value and comparison, not just prose
that admitted two readings), criterion 6's term census (excludes its own
defining file from the population it checks, adds `CLAUDE.md` as a real
citing site), criterion 13 (a new fixture class proving the corrected
suppression actually works both ways), and criterion 14 (the self-
application procedure now has a real remedy step instead of discovering
an unfixable block). S3's and S4's prior work (doctrine/forms.md,
close.md wiring/version) is **unaffected by any of these fixes** and
stands as already done — see `## Chief feedback` for the re-spawned
Planning Chief's confirmation of that scoping.

## Goal

DCS's close-time process (`/dcs-close`) mechanically enforces, for every
project shipping DCS (not only this repo), the **universal** record-integrity
properties of an incident's own artifacts — commit-SHA existence,
artifact-set completeness, `SAFETY.md` schema conformance, a clean tree
after the archive commit, and non-degenerate commit messages — running
**unconditionally**, not gated behind a project's own opt-in `CLAUDE.md`
declaration, **with a real, append-only-compatible remedy for a legitimate
record a specialist or IC needs to write about the mechanism itself**
(the exact gap that produced this period's halt). Separately, DCS's own
package content (this repo's shipped payload and this repo's own incident
artifacts) stays English-only and retains its load-bearing operative
terms, enforced the way this repo already enforces its other
package-integrity properties — a policy of *this project*, per
`CLAUDE.md`'s "Ship no project facts" rule, never forced onto a downstream
project's own artifacts. Either way, a close can no longer silently lose
or misstate its own records regardless of operator discipline.

## Acceptance criteria (the Definition of Done)

1. A new stdlib-only, project-agnostic tool under `dcs/tools/`, invoked as
   `python "$HOME/.claude/dcs/tools/<name>.py" <incident_dir>`
   (single-incident-directory argument, `preservation_map.py`'s exact
   interface convention — exit 0 clean / 1 findings / 2 environment
   error), flags a commit sha cited **in citation position** (immediately
   preceded by a commit keyword — `commit`, `merge`, `integration
   commit`, `sha` — on the same line) anywhere in **that one incident's
   own** `214-LOG.md`/`AAR.md` that `git cat-file -t` cannot resolve.
   **Keep `sha` in the keyword list** — re-ratified on corpus evidence
   gathered during the replan: 5 of 8 historical `sha`-keyword tokens are
   genuine commit citations across 4 incidents (regenerate:
   `dcs/tools/record_integrity.py`'s own docstring carries the command
   that reproduces this and every other corpus figure beside it —
   Safety Officer advisory, attempt 2); dropping the keyword would
   under-detect real fabrications, not just avoid false positives.

   Two suppressions, each of which must print what it suppressed and why:

   (a) a sha256 digest carried by an `IAP-APPROVED:` sentinel entry
   (recognized via `dcs_gate.py`'s own published grammar, imported, never
   re-derived) — it is a hash, not a commit, and citing it is not a claim
   `git cat-file` can ever resolve.

   (b) **[REVISED — this is what the halt was about]** a token named by a
   genuine `RECORD-CORRECTION:` **entry** — recognized the same way any
   other log entry is recognized (`dcs_gate.py`'s entry grammar: a
   column-zero bracketed timestamp starts an entry; the sentinel token
   immediately follows it), **never** a mid-line, anywhere-in-the-body
   substring match on the literal text `RECORD-CORRECTION:`. The prior
   design was broken at both ends and both must be fixed together: **(i)**
   a mere prose *mention* of the string (e.g. a log entry that quotes the
   sentinel name while explaining a design decision, as this incident's
   own command-point-2 entry does) must **not** suppress anything — only a
   real, correctly-formed `RECORD-CORRECTION:` entry counts; **(ii)** such
   an entry must **name the specific token(s) it corrects**, and the tool
   must then suppress **every occurrence of that named token anywhere
   earlier in the log**, not merely the correction entry's own restatement
   of it — a corrected original line must actually clear, or the remedy is
   decorative. This is the incident's own append-only-compatible answer to
   "a citation was flagged but the citing text is legitimate" — the
   operator does not edit history, they append a correction that names
   what it corrects, loudly and reviewably, and the tool honors it.
   **Explicitly out of scope by design:** distinguishing a *true* correction
   from a *false* one (someone "correcting" a genuine fabrication to hide
   it) — the remedy's honesty rests on the correction being a permanent,
   visible, append-only record anyone can audit, the same trust model the
   `RECORD-CORRECTION:` convention already carries from
   `record-integrity-corrections`.

   Verified against a fixture incident with one fabricated token in
   citation position and no correction (must exit 1), the same fixture
   with a genuine `RECORD-CORRECTION:` entry naming that exact token
   (must exit 0, suppression printed), and a real, clean incident (must
   exit 0) — see criterion 14 for why `record-integrity-corrections` is
   the load-bearing verification case here, not an arbitrary clean
   fixture.

2. The same tool, scoped to that one `<incident_dir>`, confirms the
   canonical artifact set (criterion 9's corrected count) is present AND
   `git ls-files`-tracked, correctly resolving a `203-ORG.md` skip as
   compliant **only** when the incident's own `201-BRIEF.md` types it
   Type 3 AND its `214-LOG.md` carries the doctrine-required skip note
   (`"203 skipped (default Type 3 activation ...)"`) — Type 1 requires
   `203-ORG.md` unconditionally, no skip. Verified against
   `record-integrity-corrections`
   (`.dcs/incidents/2026-08-02-record-integrity-corrections/`, Type 3,
   compliant skip present — must exit 0, reporting 8 present-and-tracked
   plus one compliant skip, never "9/9 tracked" as a witness claim the
   tree does not support) and a fixture missing one required file with no
   compliant-skip justification (must exit 1).
3. The same tool parses `SAFETY.md` for a genuine JSON verdict fence using
   real fence parsing, never a substring match — it must NOT be fooled by
   `record-integrity-corrections/SAFETY.md:33`'s inline prose mention of a
   fence. **[REVISED]** Once a genuine fence is found, validate its fields
   against schema #5 **only when the fence is verdict-shaped (carries a
   `verdict` key)**; a non-verdict JSON fence (e.g. a specialist return or
   a different schema quoted for reference inside `SAFETY.md`'s prose) is
   at most a printed note, **never** a fail-closed "unrecognized key"
   finding — a `SAFETY.md` may legitimately quote other JSON for context.
   **[REVISED — exact value, not just prose, to close the off-by-one bug
   this period's halt surfaced]** Date-scoped via a constant **literally
   equal to `"2026-08-02"`**, compared with a **strict greater-than** (a
   directory dated after the pin is in scope; the pin date itself is not)
   — this is what "strictly after 2026-08-02" means and is the only
   reading that satisfies it; a pin of `"2026-08-03"` combined with
   "on-or-before is out of scope" is a *different*, off-by-one rule and
   must not be used. Verified: `record-integrity-corrections` (dated
   2026-08-02, on the pin) must NOT be flagged; a fixture dated
   2026-08-03 (exactly one day after the pin — the boundary the previous
   attempt never tested) with a genuine post-pin prose-only `SAFETY.md`
   must be flagged.
4. The same tool confirms `git status --short` is empty under the
   incident's own directory, plus every path supplied via repeatable
   `--also-clean <path>` arguments — **never a hardcoded project path**
   (the original "and `vault/`" wording named this repo's own memory
   system directly inside shipped, project-agnostic code, violating
   `CLAUDE.md`'s "ship no project facts" rule; `close.md` passes whatever
   memory-routing destinations its own step 4 actually wrote, which is
   already project-specific prose, not tool code). Verified against a
   fixture with a deliberately-left untracked file (must exit 1) and a
   real clean close (must exit 0).
5. The same tool (or a documented sibling check) scans commit messages for
   degenerate bodies (a bare `@`-only line, the exact shape 22 of 70
   reviewed commits carried). Commit scope is explicit and printed, never
   assumed: default to commits touching the incident directory, override
   with `--commit-range <range>`; `close.md` passes the real merge range
   it already computes at step 5a.2, since the default under-covers —
   measured: `git log -- .dcs/incidents/2026-08-02-record-integrity-corrections/`
   returns only that incident's 2 archive commits, missing its
   integration commit `7fcab05`. Verified against a fixture reproducing
   the known defect shape and a clean commit.
6. **DCS's own package-content policies — English-only content and
   load-bearing-term retention — live in `tests/test_doctrine_integrity.py`
   (this repo's existing, DCS-repo-only merge-time guard), not in the
   shipped `dcs/tools/` mechanism, and continue to ride the existing
   opt-in step 5a.1a rather than the new unconditional step.** Two
   reasons, both load-bearing: (a) a non-English-content rule is *this
   project's own* mandate ("the repo is publicly cloned... read by an
   English-speaking audience"), not a property DCS itself requires of
   every downstream project's own artifacts — forcing it into the
   unconditional, universally-shipped mechanism would violate `CLAUDE.md`
   coding rule "ship no project facts" the same way criterion 4's
   original `vault/` hardcoding did; (b) a Cyrillic/non-whitelisted-script
   sweep over the shipped payload **already exists** (check 9) —
   generalize it in place to a full non-English sweep (covering BOTH the
   shipped `dcs/` payload's current content AND the artifacts of the
   incident currently closing, dated strictly after the same
   `"2026-08-02"` pin criterion 3 uses — same value, separate constant,
   never all of history per criterion 7) rather than shipping a second,
   drifting implementation.

   **The load-bearing-term census [REVISED — this is what refutation 1
   was about]:** a curated list of operative terms (e.g. `guarded_paths`,
   `escalate_owner`, the three sentinel tokens, `WORKFLOW_BUDGET_LINES`,
   `HOT_PATH_BUDGET_KB`) — each entry documenting which mechanism breaks
   if it disappears — is satisfied only by an occurrence in a file **OTHER
   THAN** the file that defines the census itself; a term whose only
   occurrence in the scanned population is its own list entry is a
   **finding**, not a pass. The scanned population for this check
   specifically includes the project's root `CLAUDE.md` (the real citing
   site for `WORKFLOW_BUDGET_LINES` and `HOT_PATH_BUDGET_KB`'s coding-rule
   mentions, previously unscanned by check 9's payload-only population).
   Verified with a genuine non-vacuity proof: a synthetic term known to
   exist nowhere in the scanned population must be reported as a finding
   — not merely an empty-census guard, which does not test whether a
   *present-but-unfindable* term is caught.
7. **Scope boundary (load-bearing).** Every blocking check — criteria 1–5
   in the shipped tool, and criterion 6's checks in
   `test_doctrine_integrity.py` — scopes to the incident currently
   closing (plus, for criterion 6's payload half, the payload's current
   state) only — **never** a blocking sweep across all of
   `.dcs/incidents/**` history. Today's history already contains ~7 known
   non-English incidents (owned by the separate, still-`QUEUED`
   `russian-artifacts-translation`) and 3 known artifact-sparse incidents;
   a blocking check scoped to all of history would red-flag, or
   permanently block, every future close until those separate incidents
   land. A repo-wide historical sweep may exist as a separate, explicitly
   non-blocking, informational mode of either mechanism — mirroring
   `test_doctrine_integrity.py` check 21's existing convention — but must
   never gate a close.
8. `dcs/workflows/close.md` invokes criteria 1–5's tool **unconditionally**
   — not gated behind a project's own `CLAUDE.md`-declared opt-in — in a
   new step (positioned after 5a.1, commit in worktree, and before 5a.2,
   merge). The existing step 5a.1a hook is left **completely untouched**:
   it stays the opt-in slot for project-specific merge-result guards, and
   per criterion 6 it remains how THIS repo's own `test_doctrine_integrity.py`
   (English-content + term census included) keeps running. A red result
   from the new unconditional step is fail-closed: blocks the merge, is
   escalation trigger (a), and is never silently resolved (same
   justification as the `.dcs/CLOSED` zombie rule) — **and now has a real
   remedy path via criterion 1(b)'s corrected suppression, rather than a
   dead end.**
9. Criterion 2's check and `dcs/references/forms.md` both state the
   canonical artifact set as **9** files (`201-BRIEF.md`,
   `202-OBJECTIVES.md`, `203-ORG.md` [conditional — Type 3 default
   activation may doctrine-compliantly skip it, Type 1 never does],
   `204-TASKING/` counted as one directory-entry, `IAP.md`,
   `IAP-APPROVED`, `214-LOG.md`, `SAFETY.md`, `AAR.md`) — never "seven,"
   which traced to one incident's count of artifacts found **missing**,
   not the set's size. **Already done (S3, prior attempt) — unaffected by
   this revision.**
10. `dcs/references/doctrine.md` states the new close-time fail-closed
    rule — a new principle, or an explicit extension of principle 11.
    **Already done (S3, prior attempt: new principle 16, funded by
    relocating one paragraph to `doctrine-appendix.md`, 17 bytes of
    hot-path headroom remaining) — unaffected by this revision.**
11. `dcs/workflows/close.md` stays within `WORKFLOW_BUDGET_LINES` (250, no
    grandfather exemption) after the new step is added. **Already done
    (S4, prior attempt: 248/250 lines) — unaffected by this revision,
    provided criterion 1(b)'s redesign doesn't require new close.md
    prose; if it does, that trim's budget is this attempt's problem, not
    a re-opening of S4's already-verified work.**
12. `dcs/VERSION` and `package.json` bump atomically (0.8.0, IC-ratified
    at command point 2). `CHANGELOG.md` gains a correctly-em-dashed entry.
    **Already done (S4, prior attempt) — unaffected by this revision.**
13. All three test suites (`test_dcs_gate.py`, `test_dcs_intake.py`,
    `test_doctrine_integrity.py`) pass, including fixture-backed tests for
    criteria 1–6 (immutable fixtures, never a moving ref — doctrine
    principle 15). **[REVISED — new required fixture class, the direct
    proof the halt demands]:** a fixture pair proving criterion 1(b)'s
    corrected suppression actually works both ways — (a) an unresolvable
    citation with **no** correction entry exits 1; (b) the same citation
    **with** a genuine, correctly-formed `RECORD-CORRECTION:` entry naming
    that exact token exits 0, with the suppression printed. Both cases are
    new; the prior `suppressed-correction/` fixture (a mid-line mention,
    not a real entry) must be corrected or replaced, not left as the
    passing case for a mechanism criterion 1(b) no longer implements that
    way.
14. **Self-application ([IC]). [REVISED — the halt's second refutation is
    exactly this criterion discovering an unfixable state under the old
    design; it now has a real remedy step.]** A running session reads the
    installed `~/.claude/dcs/` copy, never the repo being edited — this
    incident's own close executes under the OLD `close.md`, without the
    new step. Before this incident closes, the IC:
    1. Appends a genuine `RECORD-CORRECTION:` entry to this incident's own
       `214-LOG.md`, naming the token `3df43fc8` at line 30 and stating
       plainly it is a file-content digest, not a commit — a true
       statement, already established at command point 2 and re-verified
       at command point 4.
    2. Runs the corrected tool by hand against this incident's own
       directory with the real commit range and memory-routing
       destinations.
    3. Confirms a genuine exit 0 (not merely "no *new* findings") and
       records the real output in `214-LOG.md`.
    **An incident never closes over a recorded exit 1 from its own gate**
    — if step 3 does not produce exit 0, that is itself grounds to stop
    and re-examine the mechanism, not to close anyway.
15. [IC] The register's territory cell for this incident is refined to the
    union of the actual `204-TASKING/*.md` territories at `/dcs-plan` step
    5a, and the row is updated at close per `REGISTER.md`'s own
    conventions. **Already done (prior attempt) — unaffected.**

## Out of scope this period

- Measure 1's log-append helper and "facts-by-command in AARs" — the
  packaging (`non-anthropic-hardening.md`, "Packaging" section) explicitly
  excludes both from this bundle; the helper is the separate queued
  incident `log-append-helper`.
- Measures 4+5 (independence-loss-is-a-halt, the Delegation model floor) —
  the separate queued incident `independence-fail-closed-and-model-floor`.
- Historical remediation: actually fixing the ~7 already-known
  non-English incidents (`russian-artifacts-translation`, separate
  `QUEUED` row) or restoring the 3 already-known artifact-sparse
  incidents beyond what `record-integrity-corrections` already corrected.
  This incident builds the guard going forward only (criterion 7's scope
  boundary is exactly this line).
- A blocking, repo-wide historical sweep across all of
  `.dcs/incidents/**` — explicitly excluded from the blocking gate by
  criterion 7; an informational-only full-sweep mode is optional, not
  required by any criterion above.
- Promoting `RECORD-CORRECTION:` into a first-class `dcs_gate.py` grammar
  sentinel with its own dedicated regex constant, beyond reusing the
  gate's existing entry-boundary grammar to recognize where an entry
  starts — would widen this Type 1 further; criterion 1(b)'s revision
  reuses what `dcs_gate.py` already publishes, it does not add to it.
- Distinguishing a true correction from a bad-faith false one — criterion
  1(b)'s own "explicitly out of scope by design" clause; the record being
  loud, permanent, and append-only is the control, not code-level intent
  detection.
- `field-lesson-guard-vacuity`'s duplicate-`# --- 20.` numbering fix in
  `tests/test_doctrine_integrity.py` — separate queued incident. This
  incident's own new checks/tests must not disturb that numbering.
- `semantic-content-loss-guard`'s broader semantic-loss-across-any-trim
  guard — separate queued incident.
- `close-md-lock-diagnostic-inert`'s Windows lock-holder diagnostic fix —
  separate queued incident, even though it also touches `close.md`;
  sequencing (do not run concurrently) applies, not folding the fix in.
- `shipped-set-defined-three-times` — checked, not applicable.
- Any sequencing decision among this incident and the other `QUEUED` rows
  sharing territory — deferred to the next `/dcs-esg`.

## Chief feedback

**Period 1, attempt 1** (both chiefs' original findings, criteria
1/2/4/6/12/13's original resolutions): unchanged from the prior revision
— see `214-LOG.md`'s entries for the full record; not restated here to
keep this section focused on what attempt 2 changed.

**Period 1, attempt 2 — Safety Officer halt + `dcs-commander` replan
ruling** (full verbatim ruling: `214-LOG.md`'s `command: verdict_disposition
replan` entry): two refutations, both now resolved above. Refutation 1
(term census tautology — `tests/test_doctrine_integrity.py` scanning
itself, every term trivially "finding itself") is fixed by criterion 6's
revision (exclude the defining file, add `CLAUDE.md`, require a real
non-vacuity proof). Refutation 2 (this incident's own `214-LOG.md`
permanently and unremediably flagged by its own command-point-2 entry
quoting the `sha`-keyword false-positive example) is fixed by criterion
1(b)'s complete redesign (a real `RECORD-CORRECTION:` entry, recognized
by grammar and naming its target, clears the target — not a substring
mention) plus criterion 14's corrected procedure. Three advisories folded
in: the date-pin off-by-one (criteria 3 and 6 now state the exact
constant value and comparison, not just prose that admitted two
readings), the fence-trap "pair" framing overstatement (an AAR-writing
note, not a code change), and SAFETY.md fence-field over-validation
(criterion 3's "verdict-shaped fences only" clause). The commander's own
corpus measurement — 5 of 8 historical `sha`-keyword citations are real —
is why criterion 1 keeps the keyword rather than dropping it, reversing
what the IC's own command-point-2 ruling might otherwise have drifted
toward on a second look.
