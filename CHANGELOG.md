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
from recollection. Releases before 0.6.5 are recorded only in
`git log --format='%h %ad %s' --date=short -- dcs/VERSION`.

---

## 0.6.10 — 2026-07-26

Hot-path trim, and a correction: **0.6.9 shipped twice with different
contents.** If you installed 0.6.9, take 0.6.10 — see below.

### Added

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
