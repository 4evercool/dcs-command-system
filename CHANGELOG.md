# Changelog

Notable changes per release, newest first.

**Read the [Upgrading](README.md#upgrading) section before applying any of
these.** Updating the package refreshes `~/.claude/` only. Two things it
never touches, in any release:

- `<project>/.claude/hooks/*.py` — the copies that actually enforce
  anything. They arrive only via `/dcs-init`.
- `<project>/.dcs/config.json` — `/dcs-init` writes the template only when
  the file is absent, so **a new config key never reaches an existing
  project on its own**. Releases that add one say so under **Config** and
  give the exact line to paste.

Entries below are written from the repository's own artifacts — merge
commits, incident AARs, and each suite's own `N/M passed` output — not
from recollection. 0.6.0–0.6.4 predate the incident-AAR trail —
self-hosting starts at 0.6.3, and the first release shipped by a
self-hosted incident is 0.6.7 — so those five are sourced from the
release commit's own message instead:
`git log --format='%B' v0.5.12..v0.6.4 -- dcs/VERSION`.

---

## 0.6.14 — 2026-07-29

### Added

- **Agent return contracts are now machine-readable on both sides, and a
  new guard checks them against each other.** `dcs/references/schemas.md`
  gained a uniform declaration shape for every contract section: a
  `Returned by` (or, where a section's prose names more than one agent, an
  explicit `Contract producer:`) sentence naming exactly one producing
  agent, plus a one-field-per-row table — closing three prior gaps in one
  pass: §3 (Logistics Chief) had no field table at all, §6 (Commander
  decisions) packed multiple field names into slash-joined cells with no
  binding to a command point, and §2's `Returned by` line named two agents
  with no way to tell which one owns its field list. Every
  `agents/dcs-*.md` charter now carries a matching `<output_contract>`
  block in the same shape — `agents/dcs-commander.md` gets one for the
  first time, and `agents/dcs-safety-officer.md`'s regains `advisories`,
  missing from its contract prose since v0.6.5 (`6a57b97`) even though the
  schema and the charter's own process had both used the field since.
- **`tests/test_doctrine_integrity.py` gained two new checks (18, 19).**
  Check 18 compares every schema section's declared fields against its
  resolved charter's own table, in one direction only (a field the schema
  declares must appear in the charter — the reverse is not checked, by
  measured design: on the prior incident's population, that direction
  gave zero false positives against one real finding, the reverse gave
  four false names and one empty result). Both populations are discovered
  by walking `schemas.md` and `agents/dcs-*.md` at run time, never listed
  as literals; degeneracy is guarded on three axes (empty section
  population, empty charter population, a section whose own declaration
  fails to parse), plus a row-parity case and a population-completeness
  case added after the Safety Officer's own review surfaced two ways a
  malformed or dropped declaration could pass silently. A permanent
  negative-proof case forges one field out of a real charter's table in
  memory (no file touched) and confirms the same comparator catches it.
  Check 19 parses every fenced JSON example in `schemas.md` with
  `json.loads`, with its own empty-population guard.

### Fixed

- `agents/dcs-safety-officer.md`'s `<output_contract>` block now lists
  `advisories`, matching `schemas.md #5, Safety-officer verdict` and the
  charter's own step 6 — the drift dated to v0.6.5 and had gone unnoticed
  until this release's own new guard made it checkable.

### Config

No new keys.

### Verified at release

`test_doctrine_integrity.py` **114/114 passed**, `test_dcs_gate.py`
**100/100 passed**, `test_dcs_intake.py` **10/10 passed** (each re-run at
this bump). `dcs/hooks/dcs_gate.py` is untouched since `v0.6.13` — `git
diff --stat v0.6.13..HEAD -- dcs/hooks/dcs_gate.py` prints nothing. Hot-path
budget check: `doctrine.md` + `schemas.md` = 37,882 of 37,888 normalized
bytes (a 6-byte corridor for the next release touching either file —
tracked in this repository's own maintainer vault, not shipped). Shipped
in one operational period, zero deviations, zero Safety halts; the Safety
Officer's six advisories (two of them new checks' own degeneracy gaps) were
folded into the merged commit before close, not deferred.

---

## 0.6.13 — 2026-07-29

### Added

- **A defect a stem decomposes, or new intake an ESG sweep finds, that
  falls below a concrete priority bar now routes to a project-documented
  lightweight surface instead of automatically becoming a first-class
  `REGISTER.md` row.** `new.md` step 4a's decomposition check now
  assigns each split-out defect a proposed Priority (`H`/`M`/`L`,
  matching `REGISTER.md`'s own vocabulary); a defect at `L` routes to
  the project's own `CLAUDE.md`-documented backlog-style surface when
  one is documented, and registers exactly as before when none is. The
  same disposition mirrors into `esg.md` step 2's cluster (b) (new
  intake found during a sweep), offered as an `AskUserQuestion` option
  alongside queueing. `doctrine.md` principle 4 states the bar as a
  standing rule in place (no new principle; numbering/count unchanged),
  and restores a pre-existing missing word ("defects") in the same
  amended sentence. The package itself never names a specific project's
  surface — this project's own `vault/Backlog.md` is one instance, not
  a shipped default.

### Config

No new keys.

### Verified at release

`test_doctrine_integrity.py` **86/86 passed**, `test_dcs_gate.py`
**100/100 passed**, `test_dcs_intake.py` **10/10 passed** (each re-run at
this bump: `python tests/test_doctrine_integrity.py`, `python
tests/test_dcs_gate.py`, `python tests/test_dcs_intake.py`).
`dcs/hooks/dcs_gate.py` is untouched since `v0.6.12` — `git diff --stat
v0.6.12..HEAD -- dcs/hooks/dcs_gate.py` prints nothing. This release
touches no test file — its own artifact-hygiene surface is
`dcs/references/doctrine.md`, `dcs/workflows/new.md`, and
`dcs/workflows/esg.md`, all named above under "Added".

---

## 0.6.12 — 2026-07-28

### Added

- **A `dcs/workflows/*.md` file exceeding its allowed line-count
  ceiling is now caught mechanically at merge time, every time.** A new
  check in `tests/test_doctrine_integrity.py` enumerates every workflow
  file and compares its line count against a per-file ceiling: the
  existing ~250-line policy ceiling for the six files already inside
  it, and a deliberate, documented, finite grandfather ceiling — set at
  each file's own current size — for the four files already over
  budget (`plan.md`, `execute.md`, `deploy.md`, `close.md`). The
  grandfather ceiling exists so those four neither pass silently
  forever nor immediately redden the merge-time guard; trimming their
  content back toward the 250-line policy is deferred to a future
  incident.
- **`CLAUDE.md`'s "File size" rule is corrected to name the mechanism
  explicitly**, instead of reading as advisory prose.

### Config

No new keys.

### Verified at release

`test_doctrine_integrity.py` **86/86 passed**, `test_dcs_gate.py`
**100/100 passed**, `test_dcs_intake.py` **10/10 passed** (each re-run at
this bump: `python tests/test_doctrine_integrity.py`, `python
tests/test_dcs_gate.py`, `python tests/test_dcs_intake.py`).
`dcs/hooks/dcs_gate.py` is untouched since `v0.6.11` — `git diff --stat
v0.6.11..HEAD -- dcs/hooks/dcs_gate.py` prints nothing. This release's
own file, `tests/test_doctrine_integrity.py`, is the one named above —
not restated here, see "Added".

---

## 0.6.11 — 2026-07-28

### Added

- **`RESOLVED` gained a qualifier, `RESOLVED (field repair)`, for an
  Owner-authorized fix applied entirely outside DCS's lifecycle.** It
  qualifies the existing `RESOLVED` state rather than adding a new one —
  the same qualifier shape as `MERGED (deploy pending)` in 0.6.10.
  `dcs/templates/REGISTER.md` declares the convention (which cells stay
  at the row template's em-dash, the three-part Outcome minimum, and its
  sole writer). `dcs/workflows/esg.md` gives it a live writer: agenda
  item (g) surfaces Owner-reported field repairs each sweep, and step 4
  originates the post-hoc row, verifying the commit reference (`git show
  <sha> --stat`) first since its facts are reported rather than
  observed. `python tests/test_doctrine_integrity.py`: **82/82 passed**
  as of this item's own close — see "Verified at release" below for this
  bump's own count.
- **A criterion asserting state outside the working tree now has to carry
  its own proof, front to back.** `dcs/templates/202-OBJECTIVES.md`'s
  acceptance-criteria comment gains a MEASURED CLAIM paragraph, the same
  genre as the OWNERSHIP TAG paragraph beside it: a criterion about a
  registry version, whether something is published, an installed or
  deployed copy, another repository, a remote ref or a live service must
  write the command that establishes it and phrase itself as that
  command's result, never as a bare claim. `agents/dcs-planning-chief.md`
  step 2 has the Planning Chief classify this at plan time, before any
  lint runs: an outside-the-tree claim with no such command goes into
  `objectives_feedback` as unmeasured. `dcs/workflows/plan.md` lint 4a
  gains check 3b, mirroring check 3a: it runs the criterion's own
  command and records the output, the second line of defence behind the
  Chief's read. Field lesson 2026-07-26: a criterion waived a version
  bump on "0.6.9 is unpublished"; 0.6.9 had been published 75 minutes
  earlier, and the version shipped twice with different contents.
  `python tests/test_doctrine_integrity.py`: **82/82 passed** as of this
  item's own close — see "Verified at release" below for this bump's own
  count.
- **A bounded amendment path, `plan.md`'s new `## 6c`, for a change that
  stays inside a set of boundary conditions instead of costing a full
  steps-1-9 re-plan.** Reachable only from three already-logged
  command-point entries, each cited by its own timestamp rather than
  re-litigated: `execute.md` step 6's `command: deviation ->
  amend_tasking` / `-> replan` / `-> escalate_owner` (command point 3),
  step 9's `command: verdict -> fix_taskings` (command point 4) when the
  fix also changes `IAP.md`'s own content, and step 9's
  advisories-on-a-pass paragraph when an advisory's own fix touches
  `IAP.md` — a case that paragraph previously left with no route once
  "fix it now" would leave the approval marker stale. The boundary
  conditions decide reachability, never the disposition label by itself
  — see `plan.md` `## 6c` for their current text rather than a paraphrase
  here, which would be a second copy of a fast-moving contract (this
  incident's own period revised the boundary conditions four times
  before they held under adversarial verification). Inside it, `## 6c`
  still terminates at the unmodified steps 7-8 (step 7 gains a bounded
  exception naming the already-logged decision as the pre-stamp
  checklist's `command: iap_review`, in place of a fresh one), so the
  sha256 recompute, the `IAP-APPROVED` rewrite and the sentinel append
  are identical regardless of path — `marker_valid()`
  (`dcs_gate.py:515-528`) stays satisfied and trigger (c)'s attempt
  tally stays accurate by construction.

### Changed

- **Doctrine principles 8 and 15 each gained a dated `(v0.6.11)`
  clause.** Principle 8 (deviation doctrine) now points to `plan.md`'s
  bounded amendment path as the proportionate route inside its stated
  limits, full path outside them. Principle 15 (no derived facts in
  durable artifacts) extends "write the derivation, not the result" to
  the handoff between seats: a fact a prior seat already established
  moves into a later artifact by file reference or regenerating command,
  never by a later seat retyping it from memory.
- **Two `execute.md` command-point spawn prompts now cite sources
  instead of retyping them.** Step 6 (command point 3, deviation
  arbitration) passes the commander any fact an earlier seat already
  established by its source — file path and line range, or the command
  that regenerates it — instead of a summary from memory. Step 9
  (command point 4, verdict handling) sources its ESG-state line
  directly from the register row instead of paraphrasing it.

### Config

No new keys.

### Verified at release

`test_doctrine_integrity.py` **83/83 passed**, `test_dcs_gate.py`
**100/100 passed**, `test_dcs_intake.py` **10/10 passed** (each re-run at
this bump: `python tests/test_doctrine_integrity.py`, `python
tests/test_dcs_gate.py`, `python tests/test_dcs_intake.py`).
`dcs/hooks/dcs_gate.py` and `tests/` are untouched this release —
`git diff --stat -- dcs/hooks/dcs_gate.py tests/` prints nothing.

---

## 0.6.10 — 2026-07-26

Hot-path trim, and a correction: **0.6.9 shipped twice with different
contents.** If you installed 0.6.9, take 0.6.10 — see below.

### Added

- **Register gained a seventh state, `RESOLVED`, for work that never
  opens a worktree.** `dcs/templates/REGISTER.md` now defines it as
  terminal for an incident whose work completed inline — `Worktree` and
  `Branch` stay at the row template's em-dash, `Closed` and `Outcome` are
  filled at the same time as the state. The Type 5 express lane
  (`dcs/workflows/new.md` step 7a) writes it, update-only, when the
  register already tracks the incident — a typo fix with no row underneath
  it still gets no register ceremony. `dcs/references/forms.md`'s register
  description and `dcs/workflows/close.md`'s pre-v0.3 fallback (formerly
  `ACTIVE` → `CLOSED`, a state `CLOSED` never actually was) both now name
  it instead. `python tests/test_doctrine_integrity.py`: **82/82 passed**,
  unchanged — the one live declaring paragraph is still
  `dcs/templates/REGISTER.md`'s state-description block (the FACTS-ONLY note
  carries the token and a proof word but no rule shape, so it does not
  declare). Regenerate:
  `python tests/test_doctrine_integrity.py | grep 'declaring population'`.
- **`test_doctrine_integrity.py` check 14, "bar carrier."** The
  advisory/refutation split (which artifact-hygiene finding is an
  `advisories[]` entry rather than a `halt`) had existed since v0.6.5 only
  as prose inside one agent's charter; it now has a check that parses the
  charter at run time and holds every other prose surface citing it to
  the charter's own live step number, bar count and default verdict
  token, plus a separate, charter-scoped check that **fails** a bare
  `N of M` census whose paragraph carries no command to regenerate it.
  Both derive their population by walking the tree, never from a
  hand-kept file list. `python tests/test_doctrine_integrity.py`:
  **73/73 passed**, up from **59/59** on the tree this incident forked
  from — extract that tree somewhere outside your working copy and run
  its own suite:

  ```bash
  git archive 6ef9c47 | tar -x -C /tmp/dcs-6ef9c47
  ```

  Candidate population for the split: **43** matching lines across **9**
  files, each number by its own command —

  ```bash
  grep -rniE "advisor(y|ies)|refutation" dcs/references/ dcs/workflows/ agents/ --include=*.md | wc -l
  grep -rliE "advisor(y|ies)|refutation" dcs/references/ dcs/workflows/ agents/ --include=*.md | wc -l
  ```

  `test_dcs_gate.py` and `test_dcs_intake.py` are untouched by this
  change: 100/100 (`python tests/test_dcs_gate.py`) and 10/10 (`python
  tests/test_dcs_intake.py`).
- **`tests/payload_check.py`, an in-repo witness for "did the deploy
  actually land."** Invoked `python tests/payload_check.py [--repo PATH]
  [--installed PATH]` (defaults: repo root, `~/.claude`), it walks the
  same three roots both installers walk (`dcs/`, `agents/dcs-*.md`,
  `skills/dcs-*/`) and reports the installed payload against the repo
  file-by-file into four classes — identical, differing, repo-only,
  installed-only — exiting `0` all identical, `1` differing or
  repo-only, `3` installed-only only, `2` on an environment error.
  Installed-only-only debris (files an installer copied and never
  purges — neither `robocopy /E` nor `rsync -a` deletes on its own)
  resolves `DEPLOYED` with a mandatory flag naming the stale files,
  never a stop.

### Changed

- **`schemas.md` trimmed 15,613 → 13,296 B, and the hot-path ratchet
  re-seated 38 → 37 kB.** The pair (`doctrine.md` + `schemas.md`, read on
  every invocation and every command-point spawn) is now 36,561 B with
  1,327 B of headroom, against 34 B before. Slack was restored *and* the
  ceiling lowered in one act, because unclaimed slack under an unchanged
  ceiling grows straight back.
- The bytes came from provenance, worked examples and duplication — **never
  from contract**. A line-by-line slice of "section number + Field + Type"
  is byte-identical across the edit for sections 1–7. Section 8's body moved
  to the 209-sitrep template that already carried its fields plus a trigger
  enum, `Decided at` and `Notes`; the section **keeps its number**, reserved
  with a pointer, because `schemas.md #N` citations scattered across the
  package depend on positional numbering, and `tests/test_doctrine_integrity.py`
  check 13 (schema citation anchors) now verifies each citation in the
  shipped package against the section title it actually names. The walk
  covers `*.md` and excludes `.dcs/` and `vault/`, neither of which ships.
- **`/dcs-deploy` stops trusting `~/.claude/dcs/VERSION` alone as proof
  of a ship.** The marker is a version label the installer copies from
  `dcs/VERSION`; DCS permits shipping without a bump while a release is
  unpublished, so a correct ship can leave it unchanged — it did, three
  times in a row (`schemas-md-trim` 0.6.9→0.6.9, `schema-citation-guard`
  0.6.10→0.6.10, `safety-halt-functional-scope` 0.6.10→0.6.10), each
  requiring an Owner-authorised hand-built sha256 comparison in its
  place. Step 4 now branches on the marker's own shape: commit-ish keeps
  the ancestry check unchanged; a content witness resolves rows green
  against the integration tip and treats red as every row unshipped;
  anything readable but neither shape is treated as unshipped and
  flagged. **`dcs/workflows/deploy.md` step 7 is now the single source
  of every disposition this workflow reaches** (`DEPLOYED` / stop /
  stays `MERGED (deploy pending)`) — shape-aware the same way step 4 is,
  not witness-only: a commit-ish marker gets an ancestry check against
  every row about to ship; a content witness runs once **before** step
  6, to capture the deployed side's starting state (a red before-run is
  expected input to the ship, never a stop — it's the reason the deploy
  is happening), and again **after**, read into its four classes. The
  after run's "the checkout equals what was merged" argument holds only
  because step 3 already confirmed the payload paths clean and step 7
  pins the sha that checkout equals — a deploy that writes into its own
  payload paths between step 3 and the after run breaks that
  equivalence, so step 7 says to re-confirm step 3's cleanliness first.
  A shape that's readable but neither a commit-ish marker nor a content
  witness no longer stops outright — an earlier draft of this entry said
  it did, which was wrong: it gets step 6's harness-refusal shape
  instead, staying `MERGED (deploy pending)` with a named remedy
  (document a witness in the project's `CLAUDE.md`, then re-run
  `/dcs-deploy`), never an override and never a substituted check. Only
  an unreadable marker or a witness environment error stops. Every other
  prose surface now cites step 7 by number rather than restating its
  dispositions — rebuilt from `git diff --stat` at end state, that
  surface list is `CLAUDE.md`'s Deploy table, `dcs/templates/REGISTER.md`'s
  `DEPLOYED` definition, `dcs/workflows/close.md`'s AAR facts-only and
  deploy-status paragraphs, and `skills/dcs-deploy/SKILL.md`'s
  frontmatter description and `<objective>` — `close.md` is the surface
  an earlier draft of this entry omitted.
- **`test_doctrine_integrity.py` checks 15 and 16.** Check 15 walks
  `dcs/`, `agents/`, `skills/`, `CLAUDE.md` and `README.md` (never
  `CHANGELOG.md` or `docs/` — both are dated records, and holding a
  dated record to live text would rewrite history) for every paragraph
  that binds `DEPLOYED` in a rule shape — a definitional dash, an `only
  after/once/when/if` conditional, or an arrow resolution — rather than
  merely narrating an action ("marks rows `DEPLOYED`" doesn't count,
  so `SKILL.md`'s and `REGISTER.md`'s facts-only deferrals don't
  false-positive). Every paragraph the walk finds must cite
  `dcs/workflows/deploy.md` step 7 by its live number; and, in every file
  but `deploy.md` itself, must be the only such paragraph. The citation
  rule binds `deploy.md`'s own paragraphs outside step 7 too — only the
  duplication rule exempts the source file whole. A
  per-class disposition comparator (rule B) was built and withdrawn at
  halt 3, not merely re-tuned: on the live tree it matched zero times —
  `dcs/templates/REGISTER.md`'s own declaring paragraph names none of
  step 7's class tokens — so it bound nothing there, and two forged
  contradictions (a class name placed outside any fixed comparison
  window, and a paragraph restating step 7's superseded rule while
  citing its live number and naming no class) survived it regardless of
  how the window was tuned. It was removed rather than repaired,
  because a contradiction can cite step 7 correctly while naming none
  of its classes, which a vocabulary-anchored comparator can never see
  by construction. What check 15 enforces now is narrower: the citation
  to the live step number, at most one declaring paragraph per file
  outside `deploy.md`, and a named anti-erasure floor
  (`dcs/templates/REGISTER.md`) so the halt-2 site cannot silently drop
  out of the declaring population — erasing it does not buy green.
  Disposition-content agreement between a declaring paragraph and step 7
  is **not checked mechanically anywhere** — it relies on review. Worth
  saying that way rather than "a human read at merge/close time", which
  would name a control that does not exist: `close.md` step 1a runs this
  suite and stops. Check 16 holds `tests/payload_check.py`'s
  `EXCLUDED_DIRS` and `BYTECODE_SUFFIXES` textually identical to
  `test_doctrine_integrity.py`'s own (read as source text on both sides,
  never imported), so the two never quietly diverge on what "the
  package" means. `python tests/test_doctrine_integrity.py`:
  **82/82 passed**, up from 73/73 before this incident.
- **`docs/spec-v0.3-parallel.md`'s deploy-train walkthrough now carries a
  supersession annotation** on its old "verify the project's
  deployed-version marker actually advanced" line, pointing at
  `dcs/workflows/deploy.md` step 7 for the shape-dependent evidence that
  line no longer states on its own. The doc itself stays as written — a
  dated design record, outside step 7's citation requirement by the same
  reasoning as this file — only the pointer is new.
- **Rejected alternative: an installer-written hash marker
  (`~/.claude/dcs/.deployed`).** Considered and dropped — an aggregate
  hash cannot produce the per-file report the witness needs (so it
  would be additive to a real witness, not a replacement for one), a
  marker the installer writes attests to what it believes it copied
  rather than to what is actually on disk, and a witness living outside
  the payload has zero bootstrap and leaves no rollback residue. Both
  installers are deliberately untouched by this change.

### Fixed

- **The published 0.6.9 was not the 0.6.9 in the repository.** 0.6.9 was
  published from a tree whose `schemas.md` was 15,613 B and whose ratchet
  was 38; the trim landed two hours later under the same version number.
  Two shipped trees, one published version — which is exactly what "version
  sync is atomic" exists to prevent. 0.6.10 is that correction, and the
  version number is the only way to make it visible.
- **Doctrine principle 15 stopped contradicting the Safety Officer's
  charter.** It closed with "Enforced by the Safety Officer's checklist
  (principle 7), not by discipline," which named no default; it now names
  the actual one (an artifact-hygiene finding is an advisory unless it
  clears a bar in `agents/dcs-safety-officer.md` step 6) and points at
  that step, so both documents give the same answer
  (`git diff 6ef9c47 -- dcs/references/doctrine.md`).
- **An un-regenerable count left the charter.** Step 6 justified the
  advisory/refutation default with a census of Safety halts to date that
  carried no command to reproduce it and cannot be reconstructed from the
  artifacts that remain. The sentence's argument didn't depend on the
  count, so the count was deleted rather than replaced
  (`git diff 6ef9c47 -- agents/dcs-safety-officer.md`).

### Config

No new keys. **0.6.9's `esg.max_halts_per_attempt` still has to be added by
hand** if you have not already — see [Upgrading](README.md#upgrading).

### Verified at release

`test_doctrine_integrity.py` 73/73, `test_dcs_gate.py` 100/100,
`test_dcs_intake.py` 10/10 (each re-run at close: `python
tests/test_doctrine_integrity.py`, `python tests/test_dcs_gate.py`,
`python tests/test_dcs_intake.py`). Hot path (`doctrine.md` + `schemas.md`,
CRLF normalised to LF) **36,683 B**, headroom **1,205 B** against the
37 kB ceiling — up from 36,582 B / 1,306 B on the tree this incident
forked from. Both figures come out of one command, run in each tree:

```bash
python -c "import pathlib; d=pathlib.Path('dcs/references/doctrine.md').read_bytes().replace(b'\r\n',b'\n'); s=pathlib.Path('dcs/references/schemas.md').read_bytes().replace(b'\r\n',b'\n'); print(len(d)+len(s), 37*1024-len(d)-len(s))"
```

Behavioural proof that check 14 is load-bearing: forging `schemas.md`
§5's "three bars" to "two bars" and re-running
`test_doctrine_integrity.py` takes the suite to **72/73**, naming the
file and the mismatch; the identical forgery applied to an extraction of
`6ef9c47` (`git archive 6ef9c47 | tar -x -C /tmp/dcs-6ef9c47`) leaves
that tree's own suite green at **59/59**, because check 14 does not
exist there.

Shipped by incident `safety-halt-functional-scope`.

---

## 0.6.9 — 2026-07-26

The halt → fix-tasking → re-verify loop is bounded by a mechanism instead
of by the Owner's patience.

### Added

- **Halt ceiling in `dcs_gate.py`.** The hook counts `SAFETY-HALT:`
  entries in an incident's `214-LOG.md` since the last reset anchor and
  denies every guarded edit once the count reaches the ceiling. The count
  is derived entirely from incident artifacts, so it survives a session
  boundary and a context reset. Answering "continue" on an escalation is a
  decision, not a reset — the wall lifts only on a freshly stamped,
  Owner-approved IAP or a logged Safety Officer pass verdict.
- **A single published sentinel grammar.** `ENTRY_PREFIX` is the one
  definition of where a `214-LOG.md` entry begins; the halt, pass and
  stamp patterns are built from it by concatenation. `GRAMMAR_LINE`
  publishes the rule in one line of prose, quoted verbatim by every
  document that describes it. The emergency rollback act is rendered by
  the same module that parses it, so printing a line the parser would
  reject is not possible by construction.
- **A ceiling-breach deny message that names its own escape.** It carries
  the exact bytes of the rollback act between two markers, so the act can
  be extracted mechanically rather than transcribed by eye — including a
  leading newline, which makes the append correct against a log that does
  not end in one.
- **Integrity check 12 derives its own population.** It walks
  `dcs/**/*.md` for sentinel tokens instead of reading a hand-maintained
  list of files, and validates each hit against the hook module's own
  specimens. A seventh prose site cannot appear unnoticed.

### Config

**One new key. It will not reach an existing project by itself** — add it
to `<project>/.dcs/config.json` by hand:

```json
"esg": { "max_halts_per_attempt": 3 }
```

Absent, malformed, `0`, `-1`, `3.0`, `true` or `"three"` all fall back to
the built-in default of **3**. There is deliberately no value that means
"no ceiling": disabling it requires writing a large integer, which is an
explicit, typed, diff-visible act.

### Fixed

- Integrity checks 8, 9 and 10 walked the repository without an extension
  filter and read `.pyc` bytecode as text. Check 8 could therefore report a
  U+FFFD failure whenever a stale `__pycache__` happened to sit next to the
  tests — a false positive in a guard that blocks merges. Bytecode and
  `.git`, `node_modules`, `__pycache__` are now excluded consistently
  across all three; no check was removed or weakened.

### Verified at release

`test_dcs_gate.py` 100/100 · `test_doctrine_integrity.py` 40/40 ·
`test_dcs_intake.py` 10/10. Hot path 38 878 of 38 912 B with the ratchet
held at 38 kB. Both copies of the hook byte-identical.

Shipped by incident `halt-loop-unbounded`: one operational period, four
stamped attempts, two Safety halts, one deviation, two Owner escalations.
Full account in `.dcs/incidents/2026-07-25-halt-loop-unbounded/AAR.md`.

---

## 0.6.8 — 2026-07-25

A line-ending policy, and an approval marker that was already broken.

### Fixed

- **The approval gate hashed the wrong bytes.** With `core.autocrlf=true`
  and no `.gitattributes`, `IAP.md` could sit on disk with different line
  endings than when it was approved, so a valid stamp could stop verifying
  — this had already happened to an incident that closed hours earlier.
  The gate now compares against a set of digests covering the raw,
  LF-normalised and CRLF-normalised forms.
- **The hot-path measurement had no stable definition** for the same
  reason: the number depended on which files git had last rewritten.
  `.gitattributes` pins the policy and the measurement normalises before
  counting.

Shipped by incident `hot-path-budget-eol-sensitivity` — four specialists,
no deviations and no Safety halts.

---

## 0.6.7 — 2026-07-25

### Changed

- **Doctrine hot path trimmed 42 623 → 37 734 B**, ratchet 42 → 38 kB. The
  provenance behind each rule moved to `doctrine-appendix.md`, which is
  shipped but never `@`-included, so it costs nothing per invocation. No
  rule was lost in the move.

---

## 0.6.6 — 2026-07-25

### Fixed

- Repaired double-encoding damage in `package.json`'s description, which
  had grown large enough to fail `npm publish` with E415, and added two
  guards that can see the class the BOM/U+FFFD check cannot: no Cyrillic
  anywhere in the shipped package, and `package.json` under 8 kB.

---

## 0.6.5 — 2026-07-25

### Changed

- **Artifact hygiene advises; only the acceptance criteria halt.** The
  Safety Officer's `halt` stops a merge, so its value comes from being
  reserved. Stale counts, rough wording and missing cross-references are
  now `advisories[]` on a passing verdict, fixed by the IC and folded into
  the integration commit rather than costing an execute-and-verify cycle.

---

## 0.6.4 — 2026-07-25

### Added

- **A maintainer-only Obsidian vault (`vault/`), never shipped.** DCS
  already had a memory system — doctrine for rules, the appendix for
  their provenance — so the risk in adding a vault was a second store
  that competes with it and rots. The split: package docs ship to
  *users* of DCS; the vault holds what only a *maintainer* of DCS needs,
  and is absent from `package.json`'s `files` whitelist, so `npm pack`
  excludes it. `CLAUDE.md` now routes a lesson three ways: does it
  change how DCS *behaves* (doctrine), explain *why* a rule exists
  (appendix), or would it only ever be read while improving DCS itself
  (vault)?
- **Seeded with real content rather than scaffolding**: `Post-mortems/`
  (the 31-hour `energy-cost-model-rework` incident, its three causes,
  and what today's rules would have changed), `Metrics/` (comparative
  numbers across all eight incidents to date, plus
  `vault/_scripts/incident_metrics.py` to regenerate them — principle 15
  applied to the vault itself — including the hot-path size history:
  42.2 kB → 31.7 kB after the v0.5.0 diet → 40.5 kB as of 0.6.3),
  `Meta/building-dcs-lessons.md` (recurring patterns in building DCS),
  `Decisions/distribution-and-scheduling.md` (npm over a plugin, guarded
  postinstall, scheduler-agnostic by design, and what self-hosting does
  *not* buy), and a five-item `Backlog.md`, headed by the hot-path trim.
- `vault/**` is unguarded like `docs/`, so a close can write lessons
  without holding territory; `.obsidian/` per-user UI state is
  gitignored, the notes themselves are tracked.

---

## 0.6.3 — 2026-07-25

DCS begins governing changes to itself. Three pieces, all pre-incident
setup — the bootstrap cannot itself be an incident.

### Added

- **`CLAUDE.md`**, the protocols DCS discovers at runtime for this
  repo: deploy command and marker, the merge-time guard, the
  verification suite, where lessons route, and the self-hosting rules —
  chief among them, never run `install.ps1` while an incident is
  active, since a session reads its workflows from the *installed*
  copy while an incident edits the *repo*, and that gap is what makes
  self-hosting safe.
- **An explicitly guarded `.dcs/config.json`**, in place of the default
  template. The template's `unguarded_paths` included `*.md`, and the
  gate matches with `fnmatch`, where `*` also matches `/` — so every
  markdown file at any depth was exempt: 48 of ~57 tracked files,
  including all doctrine, every workflow, every agent charter. The
  guarded set is now explicit (`dcs/**`, `agents/**`, `skills/**`,
  `tests/**`, `bin/**`, `install.*`, `package.json`); `docs/`, `README`,
  `CLAUDE.md` and `.dcs/` stay deliberately unguarded. Verified
  empirically: a `doctrine.md` edit is denied during an active incident,
  a `docs/` edit is allowed, and the gate stays silent with none open.
- **`tests/test_doctrine_integrity.py`, 12 checks**, making prose
  mechanically verifiable: version sync, principle numbering (unique,
  contiguous, matching any stated count), `@`-include resolution,
  agent/template references, doctrine sections referenced by name, the
  hot-path size budget, and encoding. Its first run found a real
  defect: three files cited a doctrine *section*, "A command point is
  never a silent wait," that existed only as a bolded paragraph
  (introduced in v0.5.10 and never resolvable) — promoted to a heading.
  It also measured hot-path regrowth: doctrine + schemas back to
  **40.5 kB** from the **31.7 kB** the v0.5.0 diet achieved. Budget set
  at **42 kB** as a ratchet rather than a ceiling — the trim it invites
  is 0.6.7, named in this same commit as "the natural first
  self-hosted incident."

---

## 0.6.2 — 2026-07-25

### Added

- **`plan.md` lint check 8: an incident's territory can never leave its
  own project.** Raised while planning DCS self-hosting: every artifact
  already resolves relative to the project root holding `.dcs/`
  (config, `ACTIVE`, incidents, register, delegation, worktrees), so two
  onboarded repos never share state on their own. The gap was a session
  rooted in the *wrong* repo — the approval gate deliberately allows
  targets outside its own project, since it cannot judge a tree it has
  no `.dcs/` for, which left cross-project territory silently ungated.
  The check resolves every territory and forbidden glob against the
  incident's own project root; an absolute path into another repo, or a
  `../` climb, is now a lint defect. Doctrine principle 6 states the
  rule.

---

## 0.6.1 — 2026-07-25

### Fixed

- **Model availability is per-spawn, not session-scoped.** Field
  observation: a session hit the Fable quota at command points 1 and 2
  of an operational period, then kept taking the opus seat at every
  later command point on the grounds that the Fable quota was
  exhausted — hours after it had restored. Doctrine said which fallback
  to use but never said when to re-test, so the reasonable reading
  cached the fallback for the rest of the incident. Rule now: try the
  preferred tier first at *every* command point, never cache the
  fallback, log a failure as scoped to that attempt rather than as a
  blanket claim. An instance of principle 15 — a derived fact ("Fable is
  exhausted") has a lifetime, and an append-only log makes it easy to
  misread as a standing condition.

---

## 0.6.0 — 2026-07-25

### Added

- **`dcs/hooks/dcs_intake.py`, a `UserPromptSubmit` hook that offers DCS
  instead of waiting to be remembered.** Until now DCS engaged only when
  someone typed a `/dcs-*` command; the approval gate stays deliberately
  silent with no incident active, which keeps non-incident work free of
  overhead but also meant nothing ever surfaced that an incident was an
  option. The hook injects one short note on the first prompt of a
  session in an onboarded project: with no active incident, it tells the
  session to *ask*, in one line, whether to open a bug or feature as an
  incident, and to just proceed for questions, exploration, trivial or
  single-file changes, docs and tooling; with an active incident, it
  reports the slug, type and phase. Classification is left to the model
  rather than keyword matching — phrasing and language vary too much for
  a keyword rule, which would either nag constantly or stay silent when
  it mattered.
- Advisory by design: cannot deny a tool call, fires once per session
  (marker keyed by session + project, in the system temp dir, never
  inside the project), fails open.
- `dcs/workflows/init.md` now copies both hooks and presents both
  settings blocks together, stating plainly that one can deny a tool
  call and the other can only add context.
- **`tests/test_dcs_intake.py`: 10 cases** (silent outside DCS projects,
  nudge content, once-per-session dedupe, per-project independence,
  active-incident reporting, malformed input). `npm test` now runs both
  suites.
