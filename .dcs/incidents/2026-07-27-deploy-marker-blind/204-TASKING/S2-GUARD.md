# 204 — Tasking S2-GUARD (revision 2)

**Incident:** deploy-marker-blind · **Period:** 1 · **Revision:** 2
**Specialist:** dcs-ops-specialist (S2-GUARD) — fresh spawn
**Runs AFTER S1-CONTRACT returns.** Its finished prose is your population.

## Task — criteria 11 and 12

Add two checks to `tests/test_doctrine_integrity.py`, in the idiom of
checks 13 and 14. **Read both in full before writing a line**, including
their comment blocks, which state why each design choice exists.

### Check 15 — deploy-evidence contract carrier (criterion 11)

**(a) Source of truth, parsed at run time.** Find `deploy.md`'s
post-deploy verification section **by content**, never by a hardcoded
number — iterate the `## (\d+)\.` sections and select by a predicate over
the body. **Assert the predicate matches exactly one section**: zero or two
is red, not a silent first-match. From that one section derive (i) its live
step number and (ii) the class→disposition map — each named branch/class
and whether the section resolves it to `DEPLOYED` or to a stop. Both parsed
from the section's own text. Red if fewer than two distinct classes parse,
or the comparator has nothing to compare.

**(b) Population, derived by walking.** Scan `*.md` under `dcs/`,
`agents/`, `skills/`, plus root `CLAUDE.md` and `README.md`, excluding
`.git` / `node_modules` / `__pycache__` / `.dcs` / `vault`. Scope
**structurally**, never by a file list. **Write the reason for the scope in
the comment:** `CHANGELOG.md` and `docs/` are **dated records** of what the
contract was at a past release — holding them to live text would rewrite
history — so they stay inside criterion 5's human walk instead.

**(c) Declaring predicate — BY ROLE, NOT VOCABULARY.** This is the whole
point of the revision. A declaring paragraph contains the token `DEPLOYED`
co-occurring with proof language (verified / read / confirmed / proof /
ancestor / witness / evidence). **No marker vocabulary in the predicate:**
the halting line *"DEPLOYED only after the project's deployed marker was
read"* is caught by role and was missed by vocabulary. Paragraph =
blank-line delimited, the same unit check 14 uses.

**(d) Three rules, one named check per population file** so a NEW site
fails by name (idiom of 12(c) / 13(d) / 14(d)):

- **Rule A** — a declaring paragraph outside the source section MUST carry
  a `` `dcs/workflows/deploy.md` step N `` citation with N equal to the
  live parsed number. **A MISSING citation is RED.** Check 14 goes green
  when a declaring site drops its citation entirely — registered as
  `check-14-hardening`, rank 3. **Do not inherit that gap.**
- **Rule B** — any disposition a citing paragraph states for a parsed class
  must equal the source section's own disposition for that class.
- **Rule C** — **at most ONE declaring paragraph per file outside the
  source file.** This is criterion 10 mechanised, and it is what catches
  halt 2 phrasing-independently. **Tree-wide** over the whole population,
  not narrowed to one file — check 14's bare-census rule stops at one file,
  the second registered gap.

**(e) Structural degeneracy guard**, so an emptied population is red and
never vacuously green: population non-empty; the source file itself is a
member; the population spans at least two of the scanned surfaces, stated
as **surface prefixes** and never as a file list; and the computed
population **plus** the parsed class→disposition map are **PRINTED** in the
check details so a collapse is visible in the output.

**(f) Literals — IC DIRECTIVE (i), narrow reading, binding.** The only file
literals permitted in check 15's body are:

- `dcs/workflows/deploy.md`, the source of truth's own path; and
- **exactly one** named anti-erasure floor: `dcs/templates/REGISTER.md`
  (the halt-2 site) asserted as *"the population must include this"*.

  > The IC ruled the narrow reading because
  > `tests/test_doctrine_integrity.py:549-555` — **shipped precedent,
  > check 13** — does exactly this: a structural non-emptiness assertion
  > plus a named floor (`agents/dcs-commander.md`) so the one hard-won
  > population member cannot silently drop out. **The pin is a floor on a
  > walked population, not a population source.** The hazard the no-literal
  > rule guards against is a *fitted list*, which a floor assertion is not.

No step number, no class name, no disposition token, and no other file path
appears as a literal — all parsed.

### Check 16 — shared exclusion constants (criterion 12)

Assert `tests/payload_check.py`'s `EXCLUDED_DIRS` and `BYTECODE_SUFFIXES`
are textually identical to this suite's own. Read **both as source text** —
`payload_check.py` via its path, this module via
`Path(__file__).read_text()` — and compare the extracted assignment text.
**NEVER import either module:** importing `test_doctrine_integrity.py` runs
its checks and calls `sys.exit()` at module scope, and importing
`payload_check.py` under a runner is its own hazard. A missing file or a
non-matching extraction is **RED, never skipped**.

## Hard constraints

- **All proofs run in SCRATCH COPIES** under the session scratch
  directory. Copy the worktree (excluding `.git`, `.dcs`, `node_modules`,
  `__pycache__`) or `git archive` as appropriate. **Never perturb-and-revert
  a file in the worktree**, and never edit a file outside your territory
  even temporarily — so no forged text can survive your return.
- **Extracting an archive INSIDE either checkout would poison the suite.**
  Check 8 walks `REPO.rglob('*')` filtered only by
  `{.git, node_modules, __pycache__}`, so any extracted tree under the
  worktree or under `C:\DCS` is walked as repo content. Extract **only**
  into the scratch directory.
- **Encoding:** checks 9 and 10 scope to `SHIPPED_DIRS`, which **includes
  `tests/`** — your new code must be English-only and LF-only, no BOM.
  `.gitattributes` protects the git object, not the working-tree bytes the
  check reads.
- **`tests/payload_check.py` is forbidden.** It is Safety-proven and its
  constants are byte-identical to the suite's today. Criterion 12 asks for a
  check that they **stay** so, not for an edit. If you find them already
  drifted, that is a **finding for the IC**, not a repair.

## File territory (may edit ONLY this)

`tests/test_doctrine_integrity.py`

## Forbidden zones

`tests/payload_check.py` · `tests/test_dcs_gate.py` ·
`tests/test_dcs_intake.py` · `dcs/**` · `agents/**` · `skills/**` ·
`docs/**` · `CLAUDE.md` · `CHANGELOG.md` · `install.ps1` · `install.sh` ·
`package.json` · `dcs/VERSION` · `bin/**` · `.dcs/**`

**If check 15 goes red against S1's finished prose, that is the mechanism
working, not a plan failure** — it is the first time anything has been able
to detect this class. **Do NOT edit prose to make your guard green.** Raise
a deviation naming the file, the paragraph and which of rules A/B/C failed,
and let the IC route it. A silent cross-territory prose edit is worse than
the defect.

## Evidence required in the return

1. `python tests/test_doctrine_integrity.py` — green, with its final
   `N/M passed` line **and exit code** (73/73 before your change), plus
   every check 15 and 16 PASS line quoted **including the printed
   population list and the parsed class→disposition map**.
2. **P1 — disposition flip.** In a scratch copy, flip ONE exit-class
   disposition in ONE citing site; run the suite there; paste the FAIL line
   — it must **name the file and the mismatch**, not just a count. State
   the exact edit made.
3. **P2 — halt-2 reintroduction.** In a scratch copy, re-add the halt-2
   sentence — *"DEPLOYED only after the project's deployed marker was read
   and the merge commit confirmed an ancestor of it"* — as a **second**
   declaring paragraph in `dcs/templates/REGISTER.md`; show the suite goes
   red naming that file **under rule C**. This forgery must go red **on its
   structure alone, before any wording is read.**
4. **P3 — the old tree stays green. IC DIRECTIVE, binding.**
   `git archive ba6019e` — **the literal sha, NEVER `HEAD`**: HEAD
   currently equals `ba6019e` and silently stops being the pre-incident
   tree at the first commit. Extract into a **second scratch directory
   outside both checkouts**, apply the same forgery as P1 to the
   corresponding site, run **that tree's own** suite, paste its
   `N/M passed` line showing green. State how the forgery maps on — the old
   sites carry no citations and no shape branches, so it is a **semantic**
   mapping, not a byte-identical patch.

   > **P3 is valid ONLY if your check PRINTS its derived population size
   > and parsed token set on the `ba6019e` tree and BOTH ARE NON-EMPTY.**
   > Green without the printed counts is not evidence — the old step 7
   > enumerates no exit classes, so an empty population would pass by
   > finding nothing. This is the top risk on the whole tasking.
5. **P4 — degeneracy.** In a scratch copy, **delete** a declaring paragraph
   from a citing site entirely (the erase-instead-of-repair evasion) and
   show the result is red, not vacuously green. Separately show what the
   check reports if the population collapses to nothing.
6. **P5 — criterion 12.** In a scratch copy, change one element of
   `EXCLUDED_DIRS` in `tests/payload_check.py`; show check 16 goes red
   naming the drift. Paste `grep -n '^import\|^from' tests/payload_check.py`
   and the corresponding lines of check 16, proving neither module imports
   the other.
7. **Criterion 11's literal rule.** Paste check 15's full body and confirm
   by inspection that the only file literals are `dcs/workflows/deploy.md`
   and the one authorised anti-erasure floor, and that no step number,
   class name or disposition token is hardcoded.
8. All three suites, each from its **own** `N/M passed` line and exit code.
9. `git status --short` proving no scratch artefact and no forged text
   landed in the worktree.

## On discovering the plan doesn't fit reality

STOP. Return `status: "deviation"` per `schemas.md` #4.
