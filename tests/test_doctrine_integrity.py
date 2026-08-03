"""Structural integrity checks for the DCS package itself.

Doctrine is prose, so it has no unit tests -- which is why several real
defects shipped unverified: a stale principle count in a heading, a
principle that duplicated an existing one, a "field lesson" describing an
event that had not happened, and a doctrine split that could have broken
cross-references silently.

Not everything about prose is checkable. These things are, and each one
below corresponds to a defect that actually occurred or was one edit
away:

  1. version sync (dcs/VERSION vs package.json)
  2. principle numbering: unique, contiguous, and matching any count
     stated in the heading
  3. every @-include resolves to a real file
  4. every agent named in a workflow exists in agents/
  5. every template named in a workflow exists in dcs/templates/
  6. every doctrine section referenced by name exists as a heading
  7. hot-path size budget (doctrine + schemas, read on every invocation),
     measured as a normalised (CRLF -> LF) byte count so the check is
     tree-independent
  8. no BOM and no U+FFFD anywhere in the package
  9. no Cyrillic anywhere in the shipped package (double-encoding damage)
  10. no CRLF line endings anywhere in the shipped package (the half of
      the .gitattributes policy that reaches a user)
  11. package.json stays small (double-encoding damage grows it silently)
  12. log grammar: the population of prose files that mention SAFETY-HALT:
      / SAFETY-PASS: / IAP-APPROVED: is DISCOVERED by walking dcs/**/*.md
      (never a named list), each one quotes the halt-ceiling hook's own
      published grammar (GRAMMAR_LINE) verbatim, and every fenced-code
      sentinel-shaped line in it is accepted at the hook's own entry
      boundary (sentinel_of() / STAMP_ENTRY_RE / SPECIMENS, imported from
      dcs_gate.py itself rather than re-derived here) -- so a wording pass
      can't rename a token, or a new prose surface drift from the parser,
      without this check failing at merge time first
  13. schema citation anchors: a `schemas.md #N` citation names a SECTION,
      not just a number -- the number-to-title mapping is parsed from
      dcs/references/schemas.md itself at run time (no section number or
      title appears as a literal in the check), the population of citing
      files is DISCOVERED by walking the tree (never a named list), one
      named case exists per population file, a degeneracy guard fires if
      the population, the parse, or a required citing surface collapses,
      and a named case reruns the same comparator on a forged (shifted)
      mapping to prove it actually reads titles rather than accepting
      anything -- so a section deleted and the numbering below it shifted,
      or a title silently rewritten under a stale number, fails here
      instead of resolving as "the number exists"
  14. advisory/refutation bar carrier: the same discipline as check 13,
      applied to principle 15's advisory/refutation split, whose one
      declaring step lives in agents/dcs-safety-officer.md and is parsed
      by content, never a hardcoded step number
  15. deploy-evidence contract carrier: dcs/workflows/deploy.md step 7 is
      the ONE place that states which deploy-evidence shape resolves to
      `DEPLOYED` and which resolves to a stop (incident deploy-marker-
      blind, 201: two prose surfaces disagreed about this in one form,
      because nothing held either to the other). The step is found by
      content, parsed for its live step number and class->disposition
      map, and every OTHER declaring paragraph in the package (found by
      ROLE -- `DEPLOYED` co-occurring with proof language AND bound in one
      of three rule shapes -- not by MARKER vocabulary, which is what
      missed halt 2's own line; a rule shape is still required, so a
      rewording outside those three does dodge it) must carry a citation
      to it by step number, and must not duplicate it within any file.
      The two rules have DIFFERENT scopes and the gloss must not merge
      them: the citation rule binds every declaring paragraph including
      deploy.md's own outside step 7; only the duplication rule exempts
      the source file, and it exempts it whole rather than merely its
      step-7 section. It does NOT
      check that a declaring paragraph's stated disposition agrees with
      step 7's -- that comparator (once here, named Rule B) was removed at
      halt 3 for over-claiming a coverage it could not deliver; see the
      removal note beside check 15's rule-A loop in the check body
  16. shared exclusion constants: tests/payload_check.py's EXCLUDED_DIRS
      and BYTECODE_SUFFIXES, read as source text on both sides (never
      imported -- importing this module runs its own checks), must stay
      textually identical to this module's own, so the two never quietly
      diverge on what "the package" means
  17. workflow line-count budget: every dcs/workflows/*.md file (from
      workflows(), never a second enumerator) stays within its effective
      ceiling -- WORKFLOW_BUDGET_LINES (250) for a compliant file, or its
      WORKFLOW_GRANDFATHERED_LINES entry for one of the files already over
      budget when this check was introduced, each value pinned to a
      comment recording it as documented, temporary debt rather than a
      silent permanent exception. The same check also catches the
      grandfather table itself going stale: an entry naming a file that no
      longer exists, or an entry whose file has since shrunk back to (or
      under) the 250-line policy ceiling -- debt nobody discharged by
      deleting the entry -- and it does not pass vacuously if
      dcs/workflows/ is ever empty
  18. schema field contract carrier: a schemas.md contract section (one
      discovered per "Returned by `agent`" sentence, its Contract producer
      resolved from the same sentence when it names more than one agent --
      same "parse the source of truth at run time" discipline as checks
      13/14/15) is paired with its resolved agent's agents/dcs-*.md
      <output_contract> table, both parsed fresh on every run -- no field
      name, agent slug, section number or population count appears as a
      literal below. Checked in ONE direction only: every field the schema
      section declares must appear in the resolved agent's own contract
      table; the reverse (a field the charter names that the schema
      section omits) is deliberately NOT checked, and both this check's
      names and this docstring entry say so rather than implying a
      two-way reconciliation. One named case per (section, agent) pair, so
      a new agent's contract drifting from its schema section fails by
      name, never folded into a count; an empty schema-section population,
      an empty agents/dcs-*.md population, and a section whose own
      "Returned by"/"Contract producer" declaration fails to resolve a
      producer or yields no fields are each their own named red case
      instead of silently emptying the pair loop. A permanent negative-
      proof case (idiom of check 13(f)'s forged mapping) reruns the SAME
      comparator against one real agent's <output_contract> table held in
      memory with one of its own declared fields' row removed (the field
      name comes from the parse, never typed here) -- proving the
      comparator actually reads the table rather than passing vacuously --
      and touches no file on disk; agents/** stays untouched.
  19. schemas.md JSON example carrier: every fenced code block in
      dcs/references/schemas.md parses with json.loads. The block
      population is discovered at run time by walking the file's own
      fences (reusing check 12's _fenced_blocks(), never a hardcoded list
      or count), one named case per block, and zero blocks discovered is
      its own red case rather than a vacuous pass.

Run standalone, or as the merge-time guard named in CLAUDE.md (doctrine:
close.md step 1a) so it runs before every incident merge.
"""
import io
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
# doctrine.md + schemas.md are read on EVERY workflow invocation and every
# command-point spawn, so their size is a latency tax paid continuously.
# The v0.5.0 "doctrine diet" cut the pair to 31.0 kB (31,723 B); versions
# since carried it back over 41 kB. Incident doctrine-hot-path-trim
# (2026-07-25) relocated the provenance and field lessons accumulated since
# the diet into doctrine-appendix.md (never @-included), taking doctrine.md
# from 27,167 to 22,121 B.
#
# BASIS: the figures 27,167 / 22,121 above and 36,717 below are RAW-CRLF --
# the basis in use before hot-path-budget-eol-sensitivity normalised the
# measure. Everything from "1,179" onward is normalised (CRLF -> LF). The
# two bases sit ~1 byte per line apart and must never be added across: in
# the raw basis the sentence below is 36,717 + 1,189 = 37,906, which is
# where that pair figure comes from. Normalised, the same three read
# 27,010 / 21,966 / 36,400 -- deliberately NOT substituted here, because
# that incident genuinely measured raw, and restating its numbers would
# credit it with measurements it never took.
#
# The budget is set on the MERGE RESULT, not on either branch: that incident
# measured 36,717 B and derived 37, but schemas.md grew 1,179 B on main
# (6a57b97, normalised CRLF -> LF; the raw-CRLF figure this line used to
# carry was 1,189 B) while the incident was open, so the merged pair came
# out larger and a 37 kB budget would have landed red. That is the whole
# reason it was re-derived rather than carried across -- a size is a
# derived fact with a lifetime (doctrine principle 15), and that one
# expired between being measured and being merged.
#
# Incident hot-path-budget-eol-sensitivity (2026-07-25) then made the
# measure itself tree-independent -- a *normalised* byte count (CRLF
# collapsed to LF before counting), not raw on-disk size, because on-disk
# bytes make the same commit measure differently in a CRLF checkout than
# an LF one (one extra byte per line), so a byte-exact budget must not
# depend on which checkout ran it -- and re-based the budget onto that
# measure: math.ceil(37579/1024) + 1 = 38. Both the arithmetic and the
# basis were corrected as Safety advisories on that incident's pass; the
# line used to read "math.ceil(37906/1024) + 1 = 38", which was wrong
# twice -- that expression evaluates to 39, and 37,906 was the raw-CRLF
# basis this incident replaced.
#
# Incident schemas-md-trim (2026-07-26) executed a measured cut registry
# against schemas.md (relocating #8's body to templates/209-SITREP.md,
# trimming the #7 deploy Notes cell and the #5 advisories paragraph to
# their live first sources, and landing two preamble paragraphs'
# provenance in doctrine-appendix.md), then re-derived the ratchet from
# the resulting, final, normalised size:
#
#   budget = math.ceil(36547/1024) + 1 = 37
#
# Still a ratchet: it bites 1 kB sooner than the 38 kB it replaces.
# This paragraph's figure was overwritten in place twice, by 2e15682 and
# again by e3d4bcc, and reconstructed at incident
# trim-content-loss-restoration; regenerate the original with
# `git show 2e15682^:tests/test_doctrine_integrity.py`.
#
# Incident worktree-removal-self-conflict (2026-07-29) then grew
# doctrine.md by 479 B (audit step 5's three-tier removal behaviour) and
# re-derived the ratchet from the resulting, final, normalised size
# (regenerate with `git show 2e15682 -- tests/test_doctrine_integrity.py`):
#
#   budget = math.ceil(38361/1024) = 38
#
# Incident hot-path-budget-emergency-trim (2026-07-30) executed a cut
# registry against doctrine.md (7 positions, compressed-in-place or moved
# to doctrine-appendix.md) and schemas.md (2 positions, notes tightened),
# then re-derived the ratchet from the resulting, final, normalised size:
#
#   budget = math.ceil(36539/1024) = 36
#
# Incident provisioning-script-upstreaming (2026-07-30) added a
# project-supplied provision hook convention to doctrine.md (one
# subsection, ~900 B) and provenance to doctrine-appendix.md (never
# @-included, so hot-path contribution is the doctrine.md portion only),
# then re-derived the ratchet from the resulting, final, normalised size:
#
#   budget = math.ceil(37455/1024) = 37
#
# Regenerate with:
#   python -c "d=open('dcs/references/doctrine.md','rb').read().replace(b'\r\n', b'\n'); s=open('dcs/references/schemas.md','rb').read().replace(b'\r\n', b'\n'); print(len(d), len(s), len(d)+len(s))"
HOT_PATH_BUDGET_KB = 37

# Directories holding generated/binary artefacts that are never source and
# never shipped: .git internals, npm's node_modules, and Python's
# __pycache__. __pycache__ is the load-bearing one here -- it is created by
# merely IMPORTING a module (check 12 below imports dcs_gate.py; anything
# that imports this test module, e.g. a test runner, does the same to it),
# so its presence is a side effect of how the suite happened to be invoked,
# not of the package's content. A file-content check whose result depends on
# that is nondeterministic, and compiled bytecode is arbitrary enough binary
# data that it occasionally contains a byte sequence a text check flags
# (observed: tests/__pycache__/test_doctrine_integrity.*.pyc tripped the BOM
# / U+FFFD check by chance). Exclude the directory outright rather than
# special-casing the byte pattern.
EXCLUDED_DIRS = {".git", "node_modules", "__pycache__"}
BYTECODE_SUFFIXES = (".pyc", ".pyo")

failures = []
checks = 0


def check(name, ok, detail=""):
    global checks
    checks += 1
    if not ok:
        failures.append((name, detail))
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"\n        {detail}" if not ok and detail else ""))


def read(rel):
    return io.open(REPO / rel, encoding="utf-8").read()


def workflows():
    return sorted((REPO / "dcs" / "workflows").glob("*.md"))


def skills():
    return sorted((REPO / "skills").glob("*/SKILL.md"))


# --- 1. version sync -------------------------------------------------------
ver_file = read("dcs/VERSION").strip()
ver_pkg = json.loads(read("package.json"))["version"]
check("version sync: dcs/VERSION == package.json",
      ver_file == ver_pkg, f"VERSION={ver_file!r} package.json={ver_pkg!r}")

# --- 2. principle numbering ------------------------------------------------
doctrine = read("dcs/references/doctrine.md")
# Scope to the principles section only: doctrine holds several other
# numbered-and-bolded lists (the four command points, the worktree audit,
# the unattended hard rules) that are not principles.
_sec = re.search(r"^##\s+The\s+(?:\d+\s+)?working principles\s*$(.*?)(?=^##\s)",
                 doctrine, re.M | re.S)
principles_text = _sec.group(1) if _sec else ""
check("principles section is findable", bool(_sec),
      "no '## The working principles' heading followed by another '## '")
nums, subs = [], []
for m in re.finditer(r"^(\d+)([a-z]?)\.\s+\*\*", principles_text, re.M):
    (subs if m.group(2) else nums).append(int(m.group(1)))
check("principles: no duplicate numbers", len(nums) == len(set(nums)),
      f"duplicates: {sorted(n for n in set(nums) if nums.count(n) > 1)}")
expected = list(range(1, len(nums) + 1))
check("principles: contiguous from 1", sorted(nums) == expected,
      f"got {sorted(nums)}, expected {expected}")
check("principles: sub-numbered ones attach to a real principle",
      all(s in nums for s in subs), f"orphan sub-principles: {sorted(set(subs) - set(nums))}")
hdr = re.search(r"^##\s+The\s+(\d+)?\s*working principles", doctrine, re.M)
stated = int(hdr.group(1)) if (hdr and hdr.group(1)) else None
check("principles: heading count matches the list (or states none)",
      stated is None or stated == len(nums),
      f"heading says {stated}, list has {len(nums)}")

# --- 3. @-includes resolve -------------------------------------------------
missing_inc = []
for f in workflows() + skills() + sorted((REPO / "agents").glob("dcs-*.md")):
    for m in re.finditer(r"@\$HOME/\.claude/(dcs/[^\s`)]+)", read(f.relative_to(REPO))):
        if not (REPO / m.group(1)).exists():
            missing_inc.append(f"{f.name} -> {m.group(1)}")
check("every @-include resolves to a real file", not missing_inc, "; ".join(missing_inc))

# --- 4. agents named in workflows exist ------------------------------------
known_agents = {p.stem for p in (REPO / "agents").glob("dcs-*.md")}
missing_agents = set()
for f in workflows():
    for m in re.finditer(r"`(dcs-[a-z-]+)`", read(f.relative_to(REPO))):
        name = m.group(1)
        if name.startswith("dcs-") and not name.startswith(("dcs-run", "dcs-new", "dcs-plan",
                                                            "dcs-execute", "dcs-close", "dcs-status",
                                                            "dcs-esg", "dcs-loop", "dcs-deploy",
                                                            "dcs-init", "dcs-sdk", "dcs-command")):
            if name not in known_agents:
                missing_agents.add(f"{f.name} -> {name}")
check("every agent named in a workflow exists", not missing_agents, "; ".join(sorted(missing_agents)))

# --- 5. templates named in workflows exist ---------------------------------
missing_tpl = set()
for f in workflows():
    for m in re.finditer(r"templates/([A-Za-z0-9\-]+\.(?:md|json))", read(f.relative_to(REPO))):
        if not (REPO / "dcs" / "templates" / m.group(1)).exists():
            missing_tpl.add(f"{f.name} -> {m.group(1)}")
check("every template named in a workflow exists", not missing_tpl, "; ".join(sorted(missing_tpl)))

# --- 6. doctrine sections referenced by name exist -------------------------
def norm(s):
    """Markdown hard-wraps prose, so a section reference routinely spans a
    newline. Compare on collapsed whitespace or every wrapped ref is a
    false positive."""
    return re.sub(r"\s+", " ", s).strip().lower()


headings = [norm(h) for h in re.findall(r"^#{2,3}\s+(.+)$", doctrine, re.M)]
bad_refs = set()
for f in workflows() + sorted((REPO / "agents").glob("dcs-*.md")):
    text = read(f.relative_to(REPO))
    for m in re.finditer(r'doctrine(?:\'s)?[,:]?\s+"([^"]{4,80})"', text, re.S):
        ref = norm(m.group(1))
        if not any(ref in h or h in ref for h in headings):
            bad_refs.add(f"{f.name} -> \"{norm(m.group(1))}\"")
check("doctrine sections referenced by name exist", not bad_refs, "; ".join(sorted(bad_refs)))

# --- 7. hot-path size budget ----------------------------------------------
# Normalised (CRLF -> LF) byte count, not os.path.getsize: raw on-disk size
# makes the same commit measure differently in a CRLF checkout than an LF
# one, so a byte-exact budget must be tree-independent. See the budget
# comment block just above the checks.
_doctrine_bytes = (REPO / "dcs" / "references" / "doctrine.md").read_bytes().replace(b"\r\n", b"\n")
_schemas_bytes = (REPO / "dcs" / "references" / "schemas.md").read_bytes().replace(b"\r\n", b"\n")
hot = len(_doctrine_bytes) + len(_schemas_bytes)
check(f"hot-path budget: doctrine+schemas <= {HOT_PATH_BUDGET_KB} kB",
      hot <= HOT_PATH_BUDGET_KB * 1024, f"currently {hot/1024:.1f} kB")

# --- 8. encoding -----------------------------------------------------------
bad_enc = []
for p in REPO.rglob("*"):
    if (p.is_file() and not EXCLUDED_DIRS & set(p.parts)
            and p.suffix.lower() not in BYTECODE_SUFFIXES):
        raw = p.read_bytes()
        if raw[:3] == b"\xef\xbb\xbf" or b"\xef\xbf\xbd" in raw:
            bad_enc.append(str(p.relative_to(REPO)))
check("no BOM, no U+FFFD anywhere", not bad_enc, "; ".join(bad_enc))

# --- 9. mojibake ------------------------------------------------------------
# The FFFD check above cannot see double-encoding damage: reading UTF-8 as a
# legacy codepage and writing it back produces *valid* UTF-8 Cyrillic, which
# then re-corrupts and grows on every round trip. package.json's description
# reached 6.3 MB this way, one version bump at a time, before npm refused the
# publish. The package is English-only (CLAUDE.md), so Cyrillic anywhere in it
# is by definition damage rather than content.
# Scope: everything package.json's `files` whitelist ships, so the check
# covers exactly what a user receives. The pattern uses \u escapes so this
# file stays pure ASCII and cannot match itself.
SHIPPED_DIRS = ["dcs", "agents", "skills", "bin", "docs", "tests"]
SHIPPED_FILES = ["install.ps1", "install.sh", "README.md", "package.json"]
CYRILLIC = re.compile("[" + chr(0x0400) + "-" + chr(0x052F) + "]")  # ASCII source
TEXT_SUFFIXES = (".md", ".py", ".json", ".js", ".sh", ".ps1", "")

candidates = []
for sub in SHIPPED_DIRS:
    base = REPO / sub
    if base.is_dir():
        candidates += [p for p in base.rglob("*") if p.is_file()]
candidates += [REPO / f for f in SHIPPED_FILES if (REPO / f).is_file()]

# (close-integrity-guard-bundle, incident) The English mandate (CLAUDE.md)
# binds this repo's OWN incident artifacts too, not only the shipped payload
# above -- but a repo-wide historical sweep would go permanently red against
# real data (34 incident directories total; Cyrillic measured in 81 artifact
# files across ~15 of them, the still-queued russian-artifacts-translation),
# so the incident-artifact half is date-pinned and built as a SECOND,
# SEPARATE list rather than folded into `candidates` -- check 10 (CRLF)
# below iterates `candidates` alone, unmodified, and must stay that way:
# adding incident directories to `candidates` would silently widen CRLF
# enforcement over this repo's ~292 incident markdown files, a scope change
# nobody authorized.
#
# _NE_EFFECTIVE_DATE is deliberately the SAME value as
# dcs/tools/record_integrity.py's own SAFETY_FENCE_EFFECTIVE_DATE as of this
# incident, but a SEPARATE constant for a separate reason: that one ships
# and binds every downstream project's SAFETY.md fence check universally;
# this one is repo-only and pins THIS project's own English mandate going
# forward. The two are deliberately not coupled by an equality assertion --
# they may legitimately diverge in the future.
# CORRECTED (close-integrity-guard-bundle, period 1 attempt 2, criterion
# 6(C)): this constant previously read "2026-08-03", an off-by-one-day
# bug -- the pin must be LITERALLY "2026-08-02", the same value
# dcs/tools/record_integrity.py's own SAFETY_FENCE_EFFECTIVE_DATE was
# independently corrected to (a separate constant, not asserted equal,
# per that module's own comment). _ne_dir_in_scope's own comparison just
# below (`m.group(1) > pin`) was ALREADY strict-greater-than before this
# fix and is UNCHANGED by it -- only the pinned VALUE was wrong, never
# the comparison's sense. Measured no-op: no `.dcs/incidents/` directory
# on disk is dated after 2026-08-02 (the newest two are dated exactly ON
# it), so this correction changes zero real in-scope/excluded directories
# -- see the printed "non-English mandate" line below, identical before
# and after this fix (0 in scope, 34 excluded, both times).
_NE_EFFECTIVE_DATE = "2026-08-02"  # close-integrity-guard-bundle, period 1

_NE_DIRNAME_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-.+$")


def _ne_dir_in_scope(dirname, pin=_NE_EFFECTIVE_DATE):
    """True iff an incident directory's own leading YYYY-MM-DD is strictly
    after `pin`. A name with no parseable date is out of scope (never
    guessed at) -- the unparseable-date disposition mirrors
    _PM_EFFECTIVE_DATE's precedent in check 22; the comparison sense does
    NOT -- this is deliberately exclusive (`>`) where check 22's is
    inclusive (`>=`), so do not 'align' them (Safety Officer advisory,
    attempt 2: attempt 1's off-by-one pin bug came from exactly that kind
    of well-intentioned alignment)."""
    m = _NE_DIRNAME_RE.match(dirname)
    return bool(m) and m.group(1) > pin


def _ne_dirname_from_path(path_str):
    """The `<date>-<slug>` incident-directory path component of a path
    string (POSIX or Windows separators), or None if the path names no
    directory directly under `.dcs/incidents/`."""
    parts = Path(path_str.replace("\\", "/")).parts
    for i, part in enumerate(parts):
        if part == "incidents" and i + 1 < len(parts) and _NE_DIRNAME_RE.match(parts[i + 1]):
            return parts[i + 1]
    return None


def _ne_finding(path_str, text, pin=_NE_EFFECTIVE_DATE):
    """The single predicate for the incident-artifact half: is (path,
    text) a non-English finding? True iff `path_str` sits inside a
    post-pin incident directory (_ne_dir_in_scope) AND `text` contains
    Cyrillic. Used both to scan real incident-artifact candidates below
    and, standalone, for the in-memory non-vacuity proof that follows
    check 9's own verdict (never a fixture planted under
    .dcs/incidents/, per this incident's own tasking constraint)."""
    dirname = _ne_dirname_from_path(path_str)
    if dirname is None or not _ne_dir_in_scope(dirname, pin):
        return False
    return bool(CYRILLIC.search(text))


_ne_incidents_root = REPO / ".dcs" / "incidents"
_ne_all_dirs = (
    sorted((d for d in _ne_incidents_root.iterdir() if d.is_dir()), key=lambda d: d.name)
    if _ne_incidents_root.is_dir() else []
)
_ne_in_scope_dirs = [d for d in _ne_all_dirs if _ne_dir_in_scope(d.name)]
_ne_out_of_scope_dirs = [d for d in _ne_all_dirs if not _ne_dir_in_scope(d.name)]

incident_candidates = []
for _ne_d in _ne_in_scope_dirs:
    incident_candidates += [p for p in _ne_d.rglob("*") if p.is_file()]

print(
    f"\nnon-English mandate (check 9 widened scope): effective date "
    f"{_NE_EFFECTIVE_DATE}; {len(_ne_in_scope_dirs)} incident director"
    f"{'y' if len(_ne_in_scope_dirs) == 1 else 'ies'} in scope, "
    f"{len(_ne_out_of_scope_dirs)} excluded as on-or-before the pin "
    "(never silently skipped)"
)

mojibake = []
for p in candidates:
    if EXCLUDED_DIRS & set(p.parts):
        continue
    if p.suffix.lower() not in TEXT_SUFFIXES:
        continue
    try:
        text = p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    if CYRILLIC.search(text):
        mojibake.append(str(p.relative_to(REPO)))
# Second, separate scan (this incident): the same content rule, applied to
# the incident-artifact candidate list built above -- two loops feeding one
# shared `mojibake` list and one shared verdict below, so check 9 stays ONE
# named case while check 10 (unmodified, next) keeps reading `candidates`
# alone.
for p in incident_candidates:
    if EXCLUDED_DIRS & set(p.parts):
        continue
    if p.suffix.lower() not in TEXT_SUFFIXES:
        continue
    try:
        text = p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        continue
    rel = str(p.relative_to(REPO)).replace("\\", "/")
    if _ne_finding(rel, text):
        mojibake.append(rel)
check("no Cyrillic anywhere in the shipped package or in this repo's own "
      "post-pin incident artifacts (widened scope, close-integrity-guard-"
      "bundle)",
      not mojibake, "; ".join(sorted(set(mojibake))))

# Non-vacuity proof (in memory, no fixture planted under .dcs/incidents/,
# per this incident's own tasking constraint): the SAME predicate
# (_ne_finding) the real scan above uses, called directly with synthetic
# inputs. A post-pin path + Cyrillic text must flag; the SAME Cyrillic text
# under a pre-pin path must not -- proving the date predicate inside
# _ne_finding is load-bearing, not decorative window dressing.
_ne_cyrillic_sample = chr(0x0442) + chr(0x0435) + chr(0x0441) + chr(0x0442)  # Cyrillic "test", built via chr() (CYRILLIC's own idiom above) so this file stays pure ASCII
_ne_post_pin_path = ".dcs/incidents/2026-08-10-sample-incident/201-BRIEF.md"
_ne_pre_pin_path = ".dcs/incidents/2026-07-01-sample-incident/201-BRIEF.md"
check("check 9 non-vacuity: a post-pin path + Cyrillic text is flagged by "
      "_ne_finding (the same predicate the real scan above uses)",
      _ne_finding(_ne_post_pin_path, _ne_cyrillic_sample) is True,
      f"_ne_finding({_ne_post_pin_path!r}, <Cyrillic sample>) = "
      f"{_ne_finding(_ne_post_pin_path, _ne_cyrillic_sample)!r}")
check("check 9 non-vacuity: the SAME Cyrillic text under a pre-pin path is "
      "excluded by _ne_finding's date predicate, not by content",
      _ne_finding(_ne_pre_pin_path, _ne_cyrillic_sample) is False,
      f"_ne_finding({_ne_pre_pin_path!r}, <Cyrillic sample>) = "
      f"{_ne_finding(_ne_pre_pin_path, _ne_cyrillic_sample)!r}")

# =============================================================================
# LOAD-BEARING-TERM CENSUS (criterion 6, other half) -- own banner, distinct
# from section 23's below, so a reviewer skimming the diff can tell "check
# 9's widened scope" (immediately above) apart from this at a glance
# (command-point-2 cosmetic note). A curated list of terms that are
# genuinely operative in the shipped package's current content (the same
# `candidates` population check 9 already built, spanning
# dcs/agents/skills/bin/docs/tests) -- if any of them silently vanished,
# something real would break: a config key the gate reads, a sentinel the
# halt-ceiling counter parses, a schema field the IC's own plan-lint
# rejects on. Each entry is a (term, why-it-breaks) pair -- the reason is
# mandatory, so a red case names the CONSEQUENCE, not just the missing
# string.
# =============================================================================
_TERM_CENSUS = [
    ("guarded_paths", "dcs_gate.py's load_config() reads this exact "
     "config.json key; a rename here silently stops a project's own "
     "guarded-path override from ever being read"),
    ("unguarded_paths", "load_config()'s counterpart key; a rename "
     "silently stops a project's own unguarded_paths override from ever "
     "being read, gating paths it was supposed to exempt"),
    ("IAP-APPROVED:", "one of the three sentinels dcs_gate.py's "
     "halt-ceiling counter (sentinel_of()/STAMP_RE) parses out of "
     "214-LOG.md; losing this string from prose orphans its own citation "
     "of the grammar it depends on"),
    ("SAFETY-HALT:", "the halt sentinel dcs_gate.py's halt_cycles() "
     "counts -- same consequence as IAP-APPROVED: above"),
    ("SAFETY-PASS:", "the reset sentinel dcs_gate.py's halt_cycles() "
     "anchors on -- same consequence"),
    ("esg_activation", "escalation trigger (e)'s own field name (doctrine "
     "principle 14); losing it from prose orphans the field from its "
     "documented rationale"),
    ("partition_ok", "the chief-plan schema field the IC's plan-lint "
     "rejects a taskings[] return on when false/absent; losing it from "
     "prose leaves that rejection undocumented"),
    ("WORKFLOW_BUDGET_LINES", "the merge-time guard's own workflow "
     "line-count budget constant (this file); CLAUDE.md's coding-rules "
     "section cites it by this exact name"),
    # (close-integrity-guard-bundle, period 1 attempt 2, criterion 6(B))
    # REPLACES a former "HOT_PATH_BUDGET_KB" entry, removed rather than
    # kept: measured (candidates population minus this file, plus
    # CLAUDE.md -- the exact corrected population below) that
    # HOT_PATH_BUDGET_KB has ZERO occurrences outside the file that
    # defines it, even after adding CLAUDE.md, so it could never survive
    # the corrected, non-tautological census -- and its own stated reason
    # ("CLAUDE.md cites it by this exact name") was independently false:
    # CLAUDE.md's coding-rules section names WORKFLOW_BUDGET_LINES and
    # WORKFLOW_GRANDFATHERED_LINES, never HOT_PATH_BUDGET_KB. ONE
    # regenerating command for both facts:
    #   python -c "from pathlib import Path; import re; r=Path('CLAUDE.md').read_text(encoding='utf-8'); print('HOT_PATH_BUDGET_KB' in r, 'WORKFLOW_GRANDFATHERED_LINES' in r)"
    # -> False True (re-run from the repo root to reproduce).
    ("WORKFLOW_GRANDFATHERED_LINES", "the merge-time guard's own "
     "grandfather-exemption table for workflow files already over the "
     "line-count budget when this check was introduced (this file); "
     "CLAUDE.md's coding-rules section cites it by this exact name "
     "(twice), describing it as recorded, temporary debt"),
]

check("load-bearing-term census: term list is non-empty (degeneracy guard "
      "-- without it every case below passes vacuously)",
      bool(_TERM_CENSUS), "population is empty")

# (close-integrity-guard-bundle, period 1 attempt 2, criterion 6(A) --
# refutation 1) This file (`tests/test_doctrine_integrity.py`) is itself
# one of `candidates` (SHIPPED_DIRS contains "tests"), and every term in
# _TERM_CENSUS above is, by construction, a literal string inside this
# same file (the census entry that names it). Scanning this file as part
# of the SATISFYING population therefore made `_term_missing` provably
# always [] -- every term trivially "found itself". The fix is
# PATH-IDENTITY exclusion: resolve this file's own path once, resolve
# each candidate, and skip the one whose resolved path matches -- never
# name-matching (`p.name == "test_doctrine_integrity.py"` would silently
# stop excluding anything the day this file is renamed) and never list
# surgery on `candidates` itself (candidates stays exactly what check 10,
# next, iterates unmodified -- see that check's own comment on why it
# must not widen).
_census_self_path = Path(__file__).resolve()

_term_census_texts = []
for p in candidates:
    if p.resolve() == _census_self_path:
        continue
    if EXCLUDED_DIRS & set(p.parts):
        continue
    if p.suffix.lower() not in TEXT_SUFFIXES:
        continue
    try:
        _term_census_texts.append(p.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, OSError):
        continue

# The project's root CLAUDE.md is the real citing site for
# WORKFLOW_BUDGET_LINES and WORKFLOW_GRANDFATHERED_LINES's coding-rule
# mentions (measured above: both are otherwise zero-occurrence outside
# this census file) -- added to the CENSUS POPULATION ONLY. It is
# deliberately NOT added to `candidates` itself: `candidates` is also
# what check 10 (CRLF, next) iterates unmodified, and the comment above
# `candidates`'s own definition already warns that widening it would
# silently widen CRLF enforcement over files nobody authorized for that
# check -- CLAUDE.md is deliberately unguarded by the merge-time gate
# (CLAUDE.md's own "Self-hosting notes" section), and folding it into
# `candidates` would contradict that for a check that has nothing to do
# with the term census.
_claude_md_path = REPO / "CLAUDE.md"
if _claude_md_path.is_file():
    try:
        _term_census_texts.append(_claude_md_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, OSError):
        pass


def _term_found(term, texts):
    """The one predicate both the real census check and its non-vacuity
    proof below call -- a term counts as found iff it is a substring of
    at least one text in `texts`. Factored out so the non-vacuity case
    exercises the EXACT SAME logic the real check uses, rather than a
    parallel re-implementation that could itself drift and pass
    vacuously."""
    return any(term in t for t in texts)


_term_missing = [
    f"{term!r} -- {why}"
    for term, why in _TERM_CENSUS
    if not _term_found(term, _term_census_texts)
]
check("load-bearing-term census: every curated term appears at least once "
      "in the shipped package's current content, OTHER than the file "
      "that defines the census itself (path-identity exclusion, "
      "criterion 6(A))",
      not _term_missing, "; ".join(_term_missing))

# Non-vacuity proof (criterion 6(B)): a synthetic term deliberately built
# so it cannot exist anywhere in the scanned population (a random suffix,
# never typed anywhere else in this repository) must be reported as
# NOT found by the exact same predicate (_term_found) the real check
# above uses. This is distinct from -- and stronger than -- the
# empty-census degeneracy guard just above: that guard only proves
# _TERM_CENSUS itself is non-empty, never that a present-but-vanished
# term would actually be caught. If _term_found degenerated to "always
# True" (e.g. the self-exclusion above silently stopped excluding this
# file, restoring the tautology), this case would go red.
_term_census_synthetic_absent = "DCS_CENSUS_PROBE_KNOWN_ABSENT_7f3c1a9d"
check("load-bearing-term census non-vacuity: a synthetic term known to "
      "exist nowhere in the scanned population is reported as NOT found "
      "by the same predicate the real check uses",
      not _term_found(_term_census_synthetic_absent, _term_census_texts),
      f"_term_found({_term_census_synthetic_absent!r}, <corrected "
      f"population, {len(_term_census_texts)} texts>) = "
      f"{_term_found(_term_census_synthetic_absent, _term_census_texts)!r}")

# --- 10. no CRLF in the shipped package -------------------------------------
# The line-ending policy itself lives in .gitattributes (text eol=lf), but
# .gitattributes is absent from package.json's `files` whitelist and `npm
# install` performs no git checkout -- so it protects a clone of this repo
# and nothing downstream. This check is the half of the policy that actually
# reaches a user: it scans the same shipped set as check 9 above (same
# SHIPPED_DIRS / SHIPPED_FILES / TEXT_SUFFIXES), so vault/ and .dcs/, which
# never ship, stay out of its reach.
crlf_files = []
for p in candidates:
    if EXCLUDED_DIRS & set(p.parts):
        continue
    if p.suffix.lower() not in TEXT_SUFFIXES:
        continue
    try:
        raw = p.read_bytes()
    except OSError:
        continue
    if b"\r\n" in raw:
        crlf_files.append(str(p.relative_to(REPO)))
check("no CRLF line endings anywhere in the shipped package", not crlf_files,
      "; ".join(sorted(crlf_files)))

# --- 11. package.json stays small ------------------------------------------
pkg_bytes = os.path.getsize(REPO / "package.json")
check("package.json under 8 kB", pkg_bytes < 8 * 1024,
      f"currently {pkg_bytes:,} bytes — check for a field growing on each edit")

# --- 12. log grammar --------------------------------------------------------
# The halt-ceiling mechanism (dcs_gate.py, doctrine principle 13) parses
# SAFETY-HALT: / SAFETY-PASS: / IAP-APPROVED: sentinels out of 214-LOG.md
# using its OWN compiled patterns and its OWN published grammar
# (GRAMMAR_LINE, ENTRY_PREFIX, SPECIMENS, sentinel_of(), STAMP_ENTRY_RE).
# Import the hook module itself (stdlib only; main() sits behind
# `if __name__ == "__main__"`, so importing it has no side effects) and hold
# every prose surface to THAT grammar, rather than re-deriving it here -- a
# duplicate would let this check and the hook drift apart exactly like the
# bare-substring grammar it replaces once did.
#
# The population is DISCOVERED, not named (halt-loop-unbounded, period 1
# revision 3): every dcs/**/*.md file mentioning any of the three sentinel
# tokens is in scope, so a new prose surface that starts quoting the log
# format is caught here the moment it exists, instead of waiting for a
# Safety Officer to spot it by eye -- a seventh such file existed in the
# field and was found exactly that way before this revision.
import importlib.util

_gate_spec = importlib.util.spec_from_file_location(
    "dcs_gate", REPO / "dcs" / "hooks" / "dcs_gate.py")
_gate = importlib.util.module_from_spec(_gate_spec)
_gate_spec.loader.exec_module(_gate)

_SENTINEL_TOKENS = ("SAFETY-HALT:", "SAFETY-PASS:", "IAP-APPROVED:")


def _ws_norm(s):
    """Collapse any run of whitespace to one space -- markdown hard-wraps
    prose, so GRAMMAR_LINE quoted verbatim still spans a line break on
    disk, and comparing raw strings would false-fail on the wrap alone."""
    return re.sub(r"\s+", " ", s).strip()


def _fenced_blocks(text):
    """Every fenced (```/```) code block's lines, as a list of line lists.
    The boundary claim in check (d) below only applies to a line meant to
    BE a 214-LOG.md entry -- an inline mention of a token in running prose
    (e.g. an inline `` `SAFETY-HALT:` `` reference) is not a log line and
    is out of scope for that check."""
    blocks = []
    in_block = False
    cur = []
    for line in text.splitlines():
        if line.strip().startswith("```"):
            if in_block:
                blocks.append(cur)
                cur = []
            in_block = not in_block
        elif in_block:
            cur.append(line)
    return blocks


# (a) population: discovered by walking dcs/**/*.md, never a named list.
_population = sorted(
    (p for p in (REPO / "dcs").rglob("*.md")
     if any(tok in p.read_text(encoding="utf-8") for tok in _SENTINEL_TOKENS)),
    key=lambda p: p.as_posix(),
)
_population_rel = [str(p.relative_to(REPO)).replace("\\", "/") for p in _population]

# (b) non-degenerate: population is non-empty and includes doctrine.md --
# a check whose own input set silently shrank to zero would pass vacuously.
check("log grammar: population is non-empty and includes doctrine.md",
      bool(_population) and any(p.name == "doctrine.md" and p.parent.name == "references"
                                 for p in _population),
      f"population: {_population_rel}")

# (c) GRAMMAR_LINE quoted verbatim (whitespace-normalised) in every file of
# the population -- one named case per file, so a missing quote in a NEW
# population member fails by name instead of folding into one aggregate.
for _p in _population:
    _rel = str(_p.relative_to(REPO)).replace("\\", "/")
    _text = _p.read_text(encoding="utf-8")
    check(f"log grammar: {_rel} quotes GRAMMAR_LINE verbatim",
          _ws_norm(_gate.GRAMMAR_LINE) in _ws_norm(_text))

# (d) every fenced-code-block line containing a sentinel token, in every
# population file, is accepted at the entry boundary: either sentinel_of()
# itself classifies it (halt/pass/stamp), or -- the ONLY placeholder
# concession, and only for the stamp token, because only there is the
# argument's format part of the sentinel -- it carries IAP-APPROVED: and
# matches the published positional form STAMP_ENTRY_RE. SAFETY-HALT: and
# SAFETY-PASS: get no such concession: their placeholder forms must pass
# sentinel_of() as-is.
_all_fenced_lines = []
for _p in _population:
    _rel = str(_p.relative_to(REPO)).replace("\\", "/")
    _text = _p.read_text(encoding="utf-8")
    _bad = []
    for _block in _fenced_blocks(_text):
        for _line in _block:
            if not any(tok in _line for tok in _SENTINEL_TOKENS):
                continue
            _all_fenced_lines.append(_line)
            _ok = _gate.sentinel_of(_line) is not None
            if not _ok and "IAP-APPROVED:" in _line:
                _ok = bool(_gate.STAMP_ENTRY_RE.match(_line))
            if not _ok:
                _bad.append(_line)
    check(f"log grammar: {_rel} -- every fenced sentinel-shaped line is boundary-valid",
          not _bad, "; ".join(_bad))

# (e) SPECIMENS: the module's own published examples, one named case each
# -- the prose sentinel of a boundary defect is exactly these pairs, never
# a private re-derivation of the boundary rule.
for _line, _expected in _gate.SPECIMENS:
    check(f"log grammar: SPECIMENS -- sentinel_of({_line!r}) == {_expected!r}",
          _gate.sentinel_of(_line) == _expected)

# (f) doctrine.md still names all three tokens (unchanged from revision 2).
check("doctrine.md names all three sentinels (IAP-APPROVED:, SAFETY-HALT:, SAFETY-PASS:)",
      all(tok in doctrine for tok in _SENTINEL_TOKENS))

# (g) lint defect 3: no population file quotes the rollback act's own body
# verbatim -- ROLLBACK_BODY dictated word for word would let a second
# author walk a fabricated pass sentinel back in through the one door this
# pivot exists to nail shut. Measured to hold today; this fixes it.
_rollback_quotes = [
    str(_p.relative_to(REPO)).replace("\\", "/")
    for _p in _population
    if _gate.ROLLBACK_BODY in _p.read_text(encoding="utf-8")
]
check("log grammar: no population file quotes the rollback body verbatim",
      not _rollback_quotes, "; ".join(_rollback_quotes))

# (h) lint defect 1: the identifier Channel A's `grep -c` preflight
# (execute.md step 9) searches for in the project's installed hook copy
# must actually be defined in dcs_gate.py -- otherwise a rename here makes
# that preflight print "advisory" against a hook that is, in fact, still
# enforcing.
execute_text = read("dcs/workflows/execute.md")
_channel_a = re.search(r"grep -c (\w+)", execute_text)
check("log grammar: Channel A's grep -c identifier is defined in dcs_gate.py",
      bool(_channel_a) and hasattr(_gate, _channel_a.group(1)),
      f"identifier: {_channel_a.group(1) if _channel_a else None!r}")

# (i) the IAP-APPROVED: witness: the population must contain at least one
# line sentinel_of() classifies 'stamp' -- an unfilled template line with
# a placeholder hex is correct at the boundary (STAMP_ENTRY_RE) but is not
# this witness, because sentinel_of() itself returns None for it (STAMP_RE
# never matches a non-hex argument). Softening check (d) for the stamp
# token must not be allowed to quietly erase this requirement too.
check("log grammar: population contains a real IAP-APPROVED: witness (sentinel_of == 'stamp')",
      any(_gate.sentinel_of(_l) == 'stamp' for _l in _all_fenced_lines))

# --- 13. schema citation anchors --------------------------------------------
# A "schemas.md #N" citation is a pointer to a numbered SECTION; what it
# actually promises the reader is the section's identity (its title), not
# merely that N resolves to *some* heading. "number exists" catches zero of
# fourteen silent title/number drifts (schema-citation-guard, 201 finding
# A) -- a section deleted and the numbering below it shifted, or a title
# rewritten while a stale number stayed put, both leave every citing "#N"
# resolving to a heading, just the wrong one.
#
# The source of truth is dcs/references/schemas.md ITSELF, parsed at run
# time -- there is no executor for a schema citation the way dcs_gate.py is
# the executor check 12 imports its grammar from, so that "import the rule
# from the mechanism" move does not apply here. No section number and no
# section title appears as a literal anywhere below (criterion 2 of the
# schema-citation-guard incident's 202); parsing schemas.md at run time is
# what keeps this check itself from becoming the kind of stale duplicate it
# exists to catch.
schemas_md = read("dcs/references/schemas.md")
_CITE_TITLE_CUT = re.compile(r"\s*[(" + chr(0x2014) + "]")  # em-dash via \u escape, ASCII source
SCHEMA_KEY = {
    int(_n): _CITE_TITLE_CUT.split(_t.strip())[0].strip().lower()
    for _n, _t in re.findall(r"^##\s+(\d+)\.\s+(.+)$", schemas_md, re.M)
}

_CITE_RE = re.compile(r"schemas\.md`?\s*#\s*(\d+)")
_CITE_WINDOW = 80


def _schema_citation_matches(norm_text, key):
    """Every 'schemas.md #N' citation in norm_text -- already whitespace-
    collapsed AND lower-cased, because this reuses norm() (defined above,
    check 6) rather than adding a third copy of the wrap normaliser next to
    norm() and _ws_norm(): a hand-rolled third copy of one normalisation
    rule, with no arbiter between the three, is the literal root cause this
    incident opened over. Returns one (n, ok) pair per citation found: ok
    is True iff key[n]'s title text appears within _CITE_WINDOW characters
    after the digit -- same window size, same case-folding (via norm()),
    same title truncation as the enumerator command 202's acceptance
    criterion 1 runs verbatim."""
    out = []
    for _m in _CITE_RE.finditer(norm_text):
        _n = int(_m.group(1))
        _title = key.get(_n)
        _ok = bool(_title) and _title in norm_text[_m.end():_m.end() + _CITE_WINDOW]
        out.append((_n, _ok))
    return out


# (e) degeneracy guard, part 1: schemas.md must actually have yielded a
# parsed heading, or the comparator below would find no title to check
# against and every downstream case would pass vacuously.
check("schema citation: schemas.md yields at least one parsed section heading",
      bool(SCHEMA_KEY), f"parsed: {SCHEMA_KEY}")

# (b) population: discovered by walking the tree, never a named list --
# same exclusion set as 202's enumerator command (.git, node_modules,
# __pycache__, .dcs, vault; .dcs/incidents is a frozen archive and vault/
# never ships, per 202's stated rationale for both).
_CITE_EXCLUDED = {".git", "node_modules", "__pycache__", ".dcs", "vault"}
_cite_all_md = sorted(
    p for p in REPO.rglob("*.md")
    if not (_CITE_EXCLUDED & set(p.relative_to(REPO).parts))
)

_cite_population = []
_cite_bad = {}
for _p in _cite_all_md:
    _rel = str(_p.relative_to(REPO)).replace("\\", "/")
    _norm_text = norm(_p.read_text(encoding="utf-8"))
    _matches = _schema_citation_matches(_norm_text, SCHEMA_KEY)
    if not _matches:
        continue
    _cite_population.append(_rel)
    _bad = [_n for _n, _ok in _matches if not _ok]
    if _bad:
        _cite_bad[_rel] = _bad

# (e) degeneracy guard, part 2: red if the population itself collapsed, if
# the one file known to need line-wrap normalisation to even enter the
# population dropped out, or if a whole citing surface disappeared --
# without these, "delete the citation instead of fixing the anchor" makes
# the offending file (and its named case) vanish from the population
# together, and the check would go green by erasure rather than by repair.
check("schema citation: population is non-empty",
      bool(_cite_population), f"population: {_cite_population}")

check("schema citation: population includes agents/dcs-commander.md "
      "(visible only after line-wrap normalisation)",
      "agents/dcs-commander.md" in _cite_population,
      f"population: {_cite_population}")

_CITE_SURFACES = {
    "agents/": lambda r: r.startswith("agents/"),
    "dcs/workflows/": lambda r: r.startswith("dcs/workflows/"),
    "dcs/templates/": lambda r: r.startswith("dcs/templates/"),
    "dcs/references/doctrine.md": lambda r: r == "dcs/references/doctrine.md",
}
_cite_missing_surfaces = [
    _label for _label, _pred in _CITE_SURFACES.items()
    if not any(_pred(_r) for _r in _cite_population)
]
check("schema citation: all four citing surfaces represented "
      "(agents/, dcs/workflows/, dcs/templates/, dcs/references/doctrine.md)",
      not _cite_missing_surfaces, f"missing: {_cite_missing_surfaces}")

# (d) one named case per population file, as in check 12(c) -- a missing or
# mismatched anchor in a NEW file fails by name, not folded into one
# aggregate count.
for _rel in _cite_population:
    _bad = _cite_bad.get(_rel, [])
    check(f"schema citation: {_rel} -- every schemas.md #N carries N's real title",
          not _bad, f"unanchored/mismatched: {['#' + str(_n) for _n in _bad]}")

# (f) negative proof (202 acceptance criterion 3): rerun the SAME
# comparator against a forged mapping derived from SCHEMA_KEY by shifting
# every number onto its neighbour's title (never typed as a literal, per
# criterion 2) -- a comparator that still reports every citation as "ok"
# against the wrong title would be accepting anything, not reading titles.
if SCHEMA_KEY:
    _cite_nums = sorted(SCHEMA_KEY)
    _cite_shifted_key = {
        _n: SCHEMA_KEY[_cite_nums[(_i + 1) % len(_cite_nums)]]
        for _i, _n in enumerate(_cite_nums)
    }
    _forged_mismatch_at = None
    for _p in _cite_all_md:
        _norm_text = norm(_p.read_text(encoding="utf-8"))
        _matches = _schema_citation_matches(_norm_text, _cite_shifted_key)
        if any(not _ok for _n, _ok in _matches):
            _forged_mismatch_at = (str(_p.relative_to(REPO)).replace("\\", "/"), _matches)
            break
    check("schema citation: comparator flags a forged (shifted-numbering) mapping",
          _forged_mismatch_at is not None,
          f"no mismatch found against the shifted mapping {_cite_shifted_key}")
else:
    check("schema citation: comparator flags a forged (shifted-numbering) mapping",
          False, "no SCHEMA_KEY parsed -- cannot build a forged mapping to test against")

# --- 14. advisory/refutation bar carrier ------------------------------------
# Doctrine principle 15's advisory/refutation split names its bars in
# exactly ONE place -- a numbered step inside agents/dcs-safety-officer.md,
# discovered here by content, never by a hardcoded number. Every other prose
# surface that discusses the split cites that step rather than restating
# the bars. Until this check, that citation contract was prose: nothing
# caught a renumbered step, a bar count quoted stale beside a citation, or
# the whole declaring population shrinking to nothing if a rewrite deleted
# the split instead of reconciling every citation to it.
#
# The charter IS the source of truth and is parsed at run time -- no other
# file's name, and no line number, appears as a literal below (criterion 2
# of this incident's 202); parsing the charter here is what keeps this
# check from becoming the kind of stale duplicate it exists to catch, the
# same discipline check 13's schema-citation anchors use, because this rule
# likewise has no executing module the way check 12's grammar does.
safety_officer_md = read("agents/dcs-safety-officer.md")

_BAR_ADVISORY_RE = re.compile(r"advisor(?:y|ies)", re.I)
_BAR_HALT_OR_REFUTATION_RE = re.compile(r"refutation|\bhalts?\b", re.I)
_BAR_CITE_RE = re.compile(r"agents/dcs-safety-officer\.md`?\s+step\s+(\d+)", re.I)
_BAR_NUM_WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                  "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
_BAR_COUNT_RE = re.compile(
    r"\b(\d+|" + "|".join(_BAR_NUM_WORDS) + r")\s+(?:named\s+)?bars?\b", re.I)
_BAR_DEFAULT_TOKEN_RE = re.compile(
    r"`(pass|halt)`[^.\n]{0,40}\bnormal\b|\bstill return[^`\n]{0,10}`(pass|halt)`",
    re.I)


def _bar_num(word):
    return int(word) if word.isdigit() else _BAR_NUM_WORDS[word.lower()]


def _bar_paragraphs(text):
    """Blank-line-delimited paragraphs -- the same unit criterion 3's
    mechanical half below uses, and the binding definition of 'same
    paragraph' the Owner confirmed at this incident's IAP approval."""
    return re.split(r"\n\s*\n", text)


# (a) source of truth: parse the charter's own <process> steps to find the
# one whose body introduces the advisory/refutation split -- by content
# ("ADVISORIES, not refutations"), never by a hardcoded step number -- its
# live step number, how many bars its bullet list names, and the default
# verdict token its own sentence states in code markup. Never a copy of
# that prose here.
_bar_proc_m = re.search(r"<process>(.*?)</process>", safety_officer_md, re.S)
_bar_proc_text = _bar_proc_m.group(1) if _bar_proc_m else ""
_bar_step_starts = list(re.finditer(r"^(\d+)\.\s+\*\*", _bar_proc_text, re.M))
_bar_step_num = None
_bar_step_body = ""
for _bar_i, _bar_sm in enumerate(_bar_step_starts):
    _bar_end = (_bar_step_starts[_bar_i + 1].start()
                if _bar_i + 1 < len(_bar_step_starts) else len(_bar_proc_text))
    _bar_body = _bar_proc_text[_bar_sm.start():_bar_end]
    if re.search(r"advisories,\s*not\s*refutations", _bar_body, re.I):
        _bar_step_num = int(_bar_sm.group(1))
        _bar_step_body = _bar_body
        break

check("bar carrier: charter names a <process> step introducing the "
      "advisory/refutation split",
      _bar_step_num is not None,
      "no numbered <process> step contains 'ADVISORIES, not refutations'")

_bar_charter_count = len(re.findall(r"^\s*-\s+\*\*", _bar_step_body, re.M))
check("bar carrier: charter's own step lists at least one bar",
      _bar_charter_count > 0, f"step {_bar_step_num}: 0 bullet bars found")

_bar_default_m = re.search(r"return\s*`(\w+)`", _ws_norm(_bar_step_body))
_bar_charter_token = _bar_default_m.group(1) if _bar_default_m else None
check("bar carrier: charter's own step states a default verdict token in "
      "code markup",
      bool(_bar_charter_token),
      f"step {_bar_step_num}: no 'return `token`' sentence found")

# (b) candidate population: same filter as the incident's own reproducing
# command -- *.md under the three scanned surfaces, matching
# advisor(y|ies)|refutation case-insensitively -- discovered by walking the
# tree, never a named list.
_bar_pop_re = re.compile(r"advisor(?:y|ies)|refutation", re.I)
_bar_scan_dirs = [REPO / "dcs" / "references", REPO / "dcs" / "workflows", REPO / "agents"]
_bar_candidates = sorted(
    {p for _bar_d in _bar_scan_dirs if _bar_d.is_dir() for p in _bar_d.rglob("*.md")
     if _bar_pop_re.search(p.read_text(encoding="utf-8"))},
    key=lambda p: p.as_posix(),
)
_bar_line_count = sum(
    1 for _bar_p in _bar_candidates
    for _bar_l in _bar_p.read_text(encoding="utf-8").splitlines()
    if _bar_pop_re.search(_bar_l)
)
check(f"bar carrier: candidate population has {_bar_line_count} matching "
      f"lines across {len(_bar_candidates)} files (compare: grep -rniE "
      "\"advisor(y|ies)|refutation\" dcs/references/ dcs/workflows/ agents/ "
      "--include=*.md | wc -l)",
      _bar_line_count > 0 and len(_bar_candidates) > 0)

# A "declaring site" is a candidate file with at least one paragraph where
# an advisory token AND a refutation/halt-verdict token co-occur -- the
# token-co-occurrence predicate that qualifies a file for the citation
# checks below, distinct from a "citation" or "reference" (explicit
# `agents/dcs-safety-officer.md step N` backtick citation). The co-
# occurrence is necessary but not sufficient for check 14(d) -- a
# declaring site must also carry a citation to the charter step.
# Measured at period start: four candidate files each carry only one of
# the two token classes, so a correct co-occurrence predicate captures
# none of them -- never special-cased by name here; the exclusion falls
# out of the predicate itself.
_bar_declaring = []
_bar_declaring_paras = {}
for _bar_p in _bar_candidates:
    _bar_text = _bar_p.read_text(encoding="utf-8")
    _bar_paras = [
        _bar_para for _bar_para in _bar_paragraphs(_bar_text)
        if _BAR_ADVISORY_RE.search(_bar_para) and _BAR_HALT_OR_REFUTATION_RE.search(_bar_para)
    ]
    if _bar_paras:
        _bar_declaring.append(_bar_p)
        _bar_declaring_paras[_bar_p] = _bar_paras

_bar_declaring_rel = [str(p.relative_to(REPO)).replace("\\", "/") for p in _bar_declaring]

# (c) degeneracy guard: non-empty, includes the charter itself, spans at
# least two of the three scanned surfaces -- stated structurally, never as
# a file list, so a rewrite that deletes the prose instead of reconciling
# it (population collapses to nothing) fails here instead of "passing" by
# vacuous truth.
check("bar carrier: declaring-site set is non-empty and includes the "
      "charter itself",
      bool(_bar_declaring) and any(r == "agents/dcs-safety-officer.md" for r in _bar_declaring_rel),
      f"declaring sites: {_bar_declaring_rel}")

_BAR_SURFACES = {
    "agents/": lambda r: r.startswith("agents/"),
    "dcs/references/": lambda r: r.startswith("dcs/references/"),
    "dcs/workflows/": lambda r: r.startswith("dcs/workflows/"),
}
_bar_surfaces_hit = [_bar_label for _bar_label, _bar_pred in _BAR_SURFACES.items()
                     if any(_bar_pred(r) for r in _bar_declaring_rel)]
check("bar carrier: declaring sites span at least two of the three "
      "scanned surfaces",
      len(_bar_surfaces_hit) >= 2, f"surfaces hit: {_bar_surfaces_hit}")


def _bar_paragraph_problems(paragraph, expected_step, expected_bar_count, expected_token,
                           check_zero_cite=False):
    """Every problem invariants 1/2/3 find in one qualifying paragraph,
    against the SUPPLIED expected values -- never a private
    re-derivation -- so the same function serves both the real comparator
    below and the forged-parse negative proof that follows it.

    When check_zero_cite is True, also flag a declaring site
    (advisory+refutation token co-occurrence) with zero citations to the
    charter step -- a silent-pass failure mode that the negative-proof test
    below exists to catch. Defaults to False so the per-file comparator
    preserves existing behaviour until source files are updated."""
    _problems = []
    _norm_para = _ws_norm(paragraph)
    _cites = list(_BAR_CITE_RE.finditer(_norm_para))
    if _cites:
        for _cm in _cites:
            _n = int(_cm.group(1))
            if _n != expected_step:
                _problems.append(f"cites step {_n}, charter's live step is {expected_step}")
            _window = _norm_para[max(0, _cm.start() - 150):_cm.end() + 150]
            _bar_m = _BAR_COUNT_RE.search(_window)
            if _bar_m:
                _named = _bar_num(_bar_m.group(1))
                if _named != expected_bar_count:
                    _problems.append(
                        f"names {_named} bars beside the step citation, "
                        f"charter's step {expected_step} lists {expected_bar_count}")
    elif check_zero_cite:
        # A declaring site (advisory+refutation token co-occurrence, the
        # predicate that placed this paragraph in _bar_declaring_paras) with
        # zero citations to the charter step -- silently passes the per-file
        # comparator below without this negative-proof guard.
        _problems.append(
            f"declaring site (advisory+refutation token co-occurrence) "
            f"carries no citation to agents/dcs-safety-officer.md step {expected_step}")
    for _tm in _BAR_DEFAULT_TOKEN_RE.finditer(_norm_para):
        _tok = _tm.group(1) or _tm.group(2)
        if _tok != expected_token:
            _problems.append(
                f"states default verdict token `{_tok}`, charter states `{expected_token}`")
    return _problems


# (d) one named case per declaring site (idiom of checks 12(c)/13(d)): a
# missing or mismatched citation in a NEW declaring site fails by name,
# not folded into one aggregate.
for _bar_p in _bar_declaring:
    _bar_rel = str(_bar_p.relative_to(REPO)).replace("\\", "/")
    _bar_problems = []
    for _bar_para in _bar_declaring_paras[_bar_p]:
        _bar_problems += _bar_paragraph_problems(
            _bar_para, _bar_step_num, _bar_charter_count, _bar_charter_token, check_zero_cite=True)
    check(f"bar carrier: {_bar_rel} -- every safety-officer.md step "
          f"citation matches the charter (step {_bar_step_num}, "
          f"{_bar_charter_count} bars, default `{_bar_charter_token}`)",
          not _bar_problems, "; ".join(_bar_problems))

# (e) negative proof (sample of checks 12(e)/13(f)): the SAME comparator,
# rerun against a forged parse of the charter -- the live step shifted onto
# its neighbour, and separately one bar dropped -- must find a mismatch
# somewhere in the same declaring population. A comparator that stays
# quiet against both forgeries reads nothing.
_bar_forged_step_problems = []
for _bar_p in _bar_declaring:
    for _bar_para in _bar_declaring_paras[_bar_p]:
        _bar_forged_step_problems += _bar_paragraph_problems(
            _bar_para, _bar_step_num + 1, _bar_charter_count, _bar_charter_token)
check("bar carrier: comparator flags a forged (shifted) step number",
      bool(_bar_forged_step_problems),
      f"no mismatch found citing step {_bar_step_num + 1} instead of {_bar_step_num}")

_bar_forged_count_problems = []
for _bar_p in _bar_declaring:
    for _bar_para in _bar_declaring_paras[_bar_p]:
        _bar_forged_count_problems += _bar_paragraph_problems(
            _bar_para, _bar_step_num, max(0, _bar_charter_count - 1), _bar_charter_token)
check("bar carrier: comparator flags a forged (one bar dropped) bar count",
      bool(_bar_forged_count_problems),
      f"no mismatch found expecting {max(0, _bar_charter_count - 1)} bars "
      f"instead of {_bar_charter_count}")

# (e)(iii) negative proof: a declaring site (advisory+refutation token
# co-occurrence) with zero citations to agents/dcs-safety-officer.md must
# produce a non-empty problem list -- a comparator that stays quiet against
# a paragraph carrying both tokens but no step citation silently passes the
# per-file comparator below on a site that never cited the charter.
_bar_forged_zero_cite_para = (
    "This advisory paragraph discusses a refutation. "
    "No citation to any charter step appears here."
)
_bar_forged_zero_cite_problems = _bar_paragraph_problems(
    _bar_forged_zero_cite_para, _bar_step_num, _bar_charter_count, _bar_charter_token,
    check_zero_cite=True)
check("bar carrier: comparator flags a declaring site with zero citations",
      bool(_bar_forged_zero_cite_problems),
      f"no problem reported for a paragraph with advisory+refutation "
      f"tokens but zero citations")

# --- criterion 3 (mechanical half): a bare 'N of M' census in the charter,
# with no regenerating command in the same paragraph, is red. "Same
# paragraph" (blank-line delimited) was confirmed by the Owner at this
# incident's IAP approval as the binding definition. Narrow to the charter
# file on purpose -- a tree-wide version would false-positive on ordinary
# prose that has nothing to do with this rule.
_BARE_CENSUS_RE = re.compile(r"\b\d+\s+of\s+\d+\b")
_REGEN_CMD_RE = re.compile(
    r"```|`[^`\n]*\b(?:grep|python|git|wc|find|awk|sed|jq)\b[^`\n]*`", re.I)
_bar_census_bad = []
for _bar_para in _bar_paragraphs(safety_officer_md):
    for _bar_cm in _BARE_CENSUS_RE.finditer(_bar_para):
        if not _REGEN_CMD_RE.search(_bar_para):
            _bar_census_bad.append(_bar_cm.group(0))
check("bar carrier (criterion 3): the charter has no bare 'N of M' census "
      "without a regenerating command in the same paragraph",
      not _bar_census_bad, "; ".join(_bar_census_bad))

# (criterion 3, appendix): same rule applied to doctrine-appendix.md, but
# only to bare-census matches inside double-quoted spans -- a quoted census
# is a direct assertion of a specific number, more binding than a running-
# text mention. The appendix carries field-lesson narratives that recount
# past figures in running prose (e.g. "0 cases across 5 files"); those are
# not inside quotation marks and are out of scope here.
_appendix_md = read("dcs/references/doctrine-appendix.md")
_appendix_census_bad = []
for _appendix_para in _bar_paragraphs(_appendix_md):
    _quoted_census = []
    for _appendix_cm in _BARE_CENSUS_RE.finditer(_appendix_para):
        _match_pos = _appendix_cm.start()
        _before = _appendix_para[:_match_pos]
        if _before.count('"') % 2 == 1:  # inside double quotes
            _quoted_census.append(_appendix_cm.group(0))
    if _quoted_census and not _REGEN_CMD_RE.search(_appendix_para):
        _appendix_census_bad.extend(_quoted_census)
check("bar carrier (criterion 3): doctrine-appendix.md has no bare 'N of M' "
      "census inside quotation marks without a regenerating command in "
      "the same paragraph",
      not _appendix_census_bad, "; ".join(_appendix_census_bad))

# --- 15. deploy-evidence contract carrier -----------------------------------
# Incident deploy-marker-blind, 201: two prose surfaces stated the DEPLOYED
# condition in one form, disagreeing with each other and with
# dcs/workflows/deploy.md step 7's real (shape-dependent) logic -- and one
# of the two disagreeing statements used no vocabulary an earlier,
# word-list-based guard would have recognised ("DEPLOYED only after the
# project's deployed marker was read and the merge commit confirmed an
# ancestor of it"). Step 7 IS the source of truth and is parsed at run
# time, same discipline as check 13's schemas.md parse and check 14's
# dcs-safety-officer.md parse -- no step number, class name or disposition
# token appears as a literal below (criterion 11's own no-literal rule).
deploy_md_text = read("dcs/workflows/deploy.md")
_DEP_SOURCE_REL = "dcs/workflows/deploy.md"

# (a) source of truth: the ONE `## N.` process step whose own text states
# it is the single source of every disposition -- found by content, never
# a hardcoded number (idiom of check 14(a)'s search for "ADVISORIES, not
# refutations" inside dcs-safety-officer.md's <process>). Exactly one match
# is required; zero or two is red, not a silent first-match.
_dep_step_starts = list(re.finditer(r"^##\s+(\d+)\.\s", deploy_md_text, re.M))
_dep_source_hits = []
for _dep_i, _dep_sm in enumerate(_dep_step_starts):
    _dep_end = (_dep_step_starts[_dep_i + 1].start()
                if _dep_i + 1 < len(_dep_step_starts) else len(deploy_md_text))
    _dep_body = deploy_md_text[_dep_sm.start():_dep_end]
    if re.search(r"single source of (?:every|any) disposition", _dep_body, re.I):
        _dep_source_hits.append((int(_dep_sm.group(1)), _dep_sm.start(), _dep_end, _dep_body))

check(f"deploy-evidence: exactly one deploy.md section is the disposition "
      f"source of truth (found {len(_dep_source_hits)})",
      len(_dep_source_hits) == 1,
      f"matching step numbers: {[n for n, *_ in _dep_source_hits]}")

if len(_dep_source_hits) == 1:
    _dep_step_num, _dep_source_start, _dep_source_end, _dep_source_body = _dep_source_hits[0]
else:
    _dep_step_num, _dep_source_start, _dep_source_end, _dep_source_body = None, -1, -1, ""

# class->disposition map: every bold bullet `- **Name**` at any indentation
# inside the source section is a candidate named branch/class. Each one is
# resolved from ITS OWN body (up to the next bullet at the same or a
# shallower indent, so a parent's nested children never leak into a
# sibling's body) by searching for an arrow-qualified `` `DEPLOYED` ``
# token or a bold **stop** token -- arrow-qualified so an unrelated,
# possibly negated mention elsewhere in the same bullet (e.g. "never mark
# anything `DEPLOYED`") is not mistaken for a resolution. A bullet whose
# body carries BOTH, or NEITHER, is a branching or non-resolving bullet
# (e.g. the "Content witness" parent, which is itself shape-dependent) and
# is excluded from the map rather than guessed at.
_dep_bullet_re = re.compile(r"^( *)-\s+\*\*([^*]+?)\*\*", re.M)
_dep_bullets = list(_dep_bullet_re.finditer(_dep_source_body))


def _dep_bullet_body(idx):
    _indent = len(_dep_bullets[idx].group(1))
    _start = _dep_bullets[idx].end()
    _end = len(_dep_source_body)
    for _j in range(idx + 1, len(_dep_bullets)):
        if len(_dep_bullets[_j].group(1)) <= _indent:
            _end = _dep_bullets[_j].start()
            break
    return _dep_source_body[_start:_end]


_DEP_ARROW = chr(0x2192)  # ASCII source -- U+2192 RIGHTWARDS ARROW
# Backtick optional (halt 3 fix, same discipline as _DEP_RULE_SHAPE_RE
# above): deploy.md's own bullets happen to backtick every arrow
# resolution today, but the parser reading the source of truth should not
# itself depend on markup any more than the population predicate does.
_DEP_ARROW_DEPLOYED_RE = re.compile(re.escape(_DEP_ARROW) + r"\s*`?DEPLOYED`?")
_DEP_BOLD_STOP_RE = re.compile(r"\*\*stop\*\*", re.I)

_dep_class_map = {}
for _dep_idx, _dep_m in enumerate(_dep_bullets):
    _dep_name = _ws_norm(_dep_m.group(2))
    _dep_body = _dep_bullet_body(_dep_idx)
    _dep_has_deployed = bool(_DEP_ARROW_DEPLOYED_RE.search(_dep_body))
    _dep_has_stop = bool(_DEP_BOLD_STOP_RE.search(_dep_body))
    if _dep_has_deployed and not _dep_has_stop:
        _dep_class_map[_dep_name] = "DEPLOYED"
    elif _dep_has_stop and not _dep_has_deployed:
        _dep_class_map[_dep_name] = "stop"

check(f"deploy-evidence: class->disposition map has {len(_dep_class_map)} "
      f"resolved classes (need >= 2; parsed as a degeneracy tripwire only "
      f"-- no rule compares a declaring paragraph against it since Rule B's "
      f"removal): {_dep_class_map}",
      len(_dep_class_map) >= 2)

# (b) population: *.md under dcs/, agents/, skills/, plus root CLAUDE.md and
# README.md -- scoped structurally (three directory walks + two named
# files), never by a hand-kept file list. CHANGELOG.md and docs/ are
# deliberately OUT of scope: both are dated records of what the contract
# was at a past release (CHANGELOG.md narrates each past release; a spec
# doc like docs/spec-v0.3-parallel.md documents the design as of when it
# was written) -- holding a dated record to LIVE text would rewrite
# history, so both stay inside criterion 5's human walk instead, never
# this run-time one.
#
# REASONED EXCEPTION (halt 3, IC directive (i)'s literal rule -- two file
# literals permitted, deploy.md the source and REGISTER.md the anti-erasure
# floor): CLAUDE.md and README.md are two MORE literals here, by name
# rather than by walk. A non-recursive `REPO.glob("*.md")` at the repo root
# was considered instead and rejected: it would also sweep in CHANGELOG.md,
# which the paragraph above holds deliberately OUT of scope as a dated
# record, so a walk would need its own CHANGELOG.md exclusion bolted on
# right next to it -- two named files is the narrower, more honest choice
# than a walk carrying a silent carve-out. Both are root-level prose DCS
# does not ship as payload (README.md documents the package; CLAUDE.md is
# this project's own protocol file, unguarded per this repo's CLAUDE.md
# itself) and neither is reachable by the three directory walks below, so
# naming them is the only way either enters this population at all.
_dep_scan_roots = [REPO / "dcs", REPO / "agents", REPO / "skills"]
_dep_scan_files = [REPO / "CLAUDE.md", REPO / "README.md"]
_dep_population = sorted(
    {p for _dep_r in _dep_scan_roots if _dep_r.is_dir() for p in _dep_r.rglob("*.md")
     if not (_CITE_EXCLUDED & set(p.relative_to(REPO).parts))}
    | {p for p in _dep_scan_files if p.is_file()},
    key=lambda p: p.as_posix(),
)
_dep_population_rel = [str(p.relative_to(REPO)).replace("\\", "/") for p in _dep_population]
_DEP_SURFACES = {"dcs/": lambda r: r.startswith("dcs/"),
                  "agents/": lambda r: r.startswith("agents/"),
                  "skills/": lambda r: r.startswith("skills/")}
_dep_pop_surfaces_hit = sorted(s for s, pred in _DEP_SURFACES.items()
                                if any(pred(r) for r in _dep_population_rel))

check(f"deploy-evidence: population spans walked surfaces "
      f"{_dep_pop_surfaces_hit} plus the named root files, "
      f"{len(_dep_population_rel)} total, and includes the source file",
      bool(_dep_population_rel) and _DEP_SOURCE_REL in _dep_population_rel
      and len(_dep_pop_surfaces_hit) >= 2
      # The named root files must actually BE there. Without this the line
      # printed "plus the named root files" while both were deleted and the
      # suite stayed green -- a claim outliving the thing it claims, which
      # is this check's own subject matter (Safety advisory, verdict 5).
      and all(p.is_file() for p in _dep_scan_files))

# (c) declaring predicate -- BY ROLE, NOT VOCABULARY: a paragraph (blank-
# line delimited, the same unit check 14 uses) is declaring iff it (i)
# names the literal `DEPLOYED` token, (ii) co-occurs with proof language
# (verified/read/confirmed/proof/ancestor/witness/evidence -- no marker
# vocabulary, so the halting line "DEPLOYED only after the project's
# deployed marker was read..." is caught by role), AND (iii) binds
# `DEPLOYED` in a RULE shape -- a definitional dash/colon ("DEPLOYED --"),
# an "only after/once/when/if" conditional immediately on `DEPLOYED`, or an
# arrow resolution ("-> `DEPLOYED`") -- rather than merely narrating a
# workflow ACTION ("marks rows DEPLOYED", "move it to `DEPLOYED`"). (iii)
# is a deliberate narrowing of (i)+(ii) alone: co-occurrence without it
# flags skills/dcs-deploy/SKILL.md's frontmatter description and its
# <objective> (both narrate the same action, "verifies... then marks rows
# DEPLOYED" / "verify... move shipped rows to `DEPLOYED`", never asserting
# an independent condition) and dcs/templates/REGISTER.md's FACTS-ONLY
# paragraph (which explicitly defers -- "DEPLOYED only per the
# deploy-evidence disposition defined above -- a row never restates that
# condition" -- and is not itself a competing rule) as second declaring
# paragraphs in their files, which is exactly the shape of a false
# positive, not the shape of the defect this check exists to catch. The
# halting line itself ("DEPLOYED only after X and Y") remains caught: it
# is a rule ("only after"), not an action.
#
# Halt 3 (Officer 3) fix: the dash/colon alternative below used to require
# a BARE "DEPLOYED --"/"DEPLOYED:" -- a backticked "`DEPLOYED` --" (the
# other two alternatives already tolerate an optional backtick either
# side) silently failed to enter the population through this alternative.
# Markup must never gate whether a rule statement is found; `?` around the
# backtick makes all three alternatives symmetric on that point.
_DEP_TOKEN_RE = re.compile(r"\bDEPLOYED\b")
_DEP_PROOF_RE = re.compile(
    r"\b(verif(?:y|ies|ied)|read|confirm(?:s|ed)?|proof|ancestors?|"
    r"witness(?:es)?|evidence)\b", re.I)
_DEP_RULE_SHAPE_RE = re.compile(
    r"DEPLOYED`?\s*(?:--|:)"
    r"|DEPLOYED`?\s+only\s+(?:after|once|when|if)\b"
    r"|" + re.escape(_DEP_ARROW) + r"\s*`?DEPLOYED`?")


def _dep_is_declaring(paragraph):
    return bool(_DEP_TOKEN_RE.search(paragraph)
                and _DEP_PROOF_RE.search(paragraph)
                and _DEP_RULE_SHAPE_RE.search(paragraph))


def _dep_paragraph_spans(text):
    """Blank-line-delimited paragraph (start, end) offsets in `text` -- the
    same split _bar_paragraphs uses, but keeping spans lets the source
    file's OWN section be excluded by position rather than by (fragile)
    substring identity."""
    _seps = [(m.start(), m.end()) for m in re.finditer(r"\n\s*\n", text)]
    _spans, _prev = [], 0
    for _s, _e in _seps:
        if _s > _prev:
            _spans.append((_prev, _s))
        _prev = _e
    if _prev < len(text):
        _spans.append((_prev, len(text)))
    return _spans


_dep_declaring = {}
for _dep_p in _dep_population:
    _dep_text = _dep_p.read_text(encoding="utf-8")
    _dep_rel = str(_dep_p.relative_to(REPO)).replace("\\", "/")
    if _dep_rel == _DEP_SOURCE_REL and _dep_step_num is not None:
        # The source SECTION's own paragraphs don't cite themselves -- but
        # any OTHER section of this same file (e.g. step 8) is NOT exempt:
        # the rule is "outside the source section", not "outside the
        # source file".
        _dep_paras = [
            _dep_text[_s:_e] for _s, _e in _dep_paragraph_spans(_dep_text)
            if not (_s >= _dep_source_start and _e <= _dep_source_end)
            and _dep_is_declaring(_dep_text[_s:_e])
        ]
    else:
        _dep_paras = [p for p in _bar_paragraphs(_dep_text) if _dep_is_declaring(p)]
    if _dep_paras:
        _dep_declaring[_dep_rel] = _dep_paras

_dep_declaring_surfaces_hit = sorted(
    s for s, pred in _DEP_SURFACES.items() if any(pred(r) for r in _dep_declaring))

check(f"deploy-evidence: declaring population is non-empty, spans "
      f"{_dep_declaring_surfaces_hit}, and has "
      f"{sum(len(v) for v in _dep_declaring.values())} paragraphs across "
      f"{len(_dep_declaring)} files: {sorted(_dep_declaring)}",
      bool(_dep_declaring))

# (f) anti-erasure floor (IC directive (i), narrow reading -- precedent:
# check 13's own `agents/dcs-commander.md` pin, cited by symbol because a
# line range is a derived fact about one tree and the first version of this
# comment carried one that was already wrong in the tree it was written in,
# in a file that grew 384 lines this period): the ONE authorised file
# literal beyond the source
# itself. A structural non-emptiness assertion plus this named floor keeps
# the halt-2 site from silently dropping out of the declaring population --
# NOT a population source (the population above is entirely walked).
check("deploy-evidence: declaring population includes "
      "dcs/templates/REGISTER.md (the halt-2 anti-erasure floor)",
      "dcs/templates/REGISTER.md" in _dep_declaring,
      f"declaring population: {sorted(_dep_declaring)}")

# (d) Rule A (citation), one named check per population file (idiom of
# check 14(d)'s combined per-file comparator) so a NEW site fails by name.
#
# Rule B (disposition equality -- "and states no disposition contradicting
# it") is REMOVED as of halt 3 (Officer 3), not merely re-tuned. It was a
# per-class substring-and-window comparator: find a step-7 class name
# (e.g. "Differing or repo-only") inside the paragraph, then look within a
# fixed +-100/150 character window for a disposition token. Officer 3
# forged four contradictions that stayed green under it, and each is a
# different way the comparator's premise fails, not one bug with one fix:
#   - the one live declaring paragraph (dcs/templates/REGISTER.md) never
#     mentions ANY of step 7's four resolved class names at all -- it uses
#     different words ("green", "stale-extras-only") -- so on the unforged
#     tree the comparator matches zero times and contributes NO binding;
#   - when a class name IS injected (F1), REGISTER.md's own paragraph
#     structure (six state descriptions concatenated with no blank lines,
#     so they are ONE paragraph to this check's blank-line-delimited unit)
#     places the class name 180+ characters from the paragraph's own
#     `DEPLOYED` label -- wider than the fixed window regardless of the
#     backtick fix directly above, so widening the window to fit this one
#     file's shape is fitting the check to a single population member,
#     exactly the kind of narrow-surface assumption this halt is about;
#   - a paragraph can restate step 7's OLD, superseded rule (F2: "the
#     project's deployed version string advanced") while citing step 7's
#     live number correctly and mentioning NONE of its four class names --
#     a comparator keyed on recognising class-name vocabulary cannot see
#     this by construction, no matter how the window is tuned, because
#     there is nothing class-shaped in the text to anchor on. This is the
#     same root failure this check exists to guard against (a prose
#     restatement using vocabulary a recogniser does not expect), now
#     inside the recogniser itself.
# A version of the comparator DOES work -- REGR_flip below (a class name
# placed directly beside a backticked `DEPLOYED` via an arrow) reproduces
# Rule B's original green-to-red behaviour under the unfixed code, proving
# it was never inert by construction. But "works when the contradiction
# happens to sit inside a fixed character window and happens to name a
# recognised class" is exactly the shape of guard this incident opened
# over, and F2 shows even a maximally generous window cannot close the
# gap. Per the Owner's ruling on this halt (a guard that under-claims
# truthfully beats one that over-claims greenly): removed, and the PASS
# line below claims only what Rule A does -- the citation, not the
# content. Disposition-content agreement between a declaring paragraph and
# step 7 is NOT CHECKED MECHANICALLY ANYWHERE -- it relies on review. Said
# that way deliberately: an earlier draft said "a human read at merge/close
# time", which names a control that does not exist, since close.md step 1a
# runs this suite and stops. Honest about the delta is not the same as
# honest about the state (Safety advisory, verdict 5).
_DEP_CITE_RE = re.compile(r"`dcs/workflows/deploy\.md`\s+step\s+(\d+)")


def _dep_paragraph_problems(paragraph, step_num):
    _problems = []
    _norm_p = _ws_norm(paragraph)
    _cites = list(_DEP_CITE_RE.finditer(_norm_p))
    if not _cites:
        _problems.append("missing a `dcs/workflows/deploy.md` step N citation")
    else:
        for _cm in _cites:
            _n = int(_cm.group(1))
            if _n != step_num:
                _problems.append(f"cites step {_n}, live step is {step_num}")
    return _problems


for _dep_rel in sorted(_dep_declaring):
    _dep_problems = []
    for _dep_para in _dep_declaring[_dep_rel]:
        _dep_problems += _dep_paragraph_problems(_dep_para, _dep_step_num)
    check(f"deploy-evidence rule A: {_dep_rel} -- every declaring paragraph "
          f"cites `dcs/workflows/deploy.md` step {_dep_step_num} by number "
          f"(disposition-content agreement beyond the citation is a human "
          f"read, not checked here -- see the Rule B removal note above)",
          not _dep_problems, "; ".join(_dep_problems))

# (d) Rule C: at most one declaring paragraph per file OUTSIDE THE SOURCE
# FILE -- tree-wide over the whole population, never narrowed to one file
# (check 14's bare-census rule stops at one file; this does not repeat
# that gap). This is criterion 10 mechanised, and it is what would catch a
# reintroduced halt-2 phrasing-independently even if its wording dodged
# Rule A entirely (Rule B, which this comment used to also name, was
# removed at halt 3 -- see the note above the rule-A loop).
_dep_rule_c_bad = {r: len(ps) for r, ps in _dep_declaring.items()
                    if r != _DEP_SOURCE_REL and len(ps) > 1}
check(f"deploy-evidence rule C: at most one declaring paragraph per file "
      f"outside the source file, tree-wide ({len(_dep_declaring)} declaring "
      f"files total)",
      not _dep_rule_c_bad, f"files with >1 declaring paragraph: {_dep_rule_c_bad}")

# --- 16. shared exclusion constants (criterion 12) ---------------------------
# tests/payload_check.py's EXCLUDED_DIRS / BYTECODE_SUFFIXES are reused
# verbatim from this module's own (its own header comment says so) --
# assert they STAY textually identical, never re-derive or re-import them:
# importing test_doctrine_integrity.py runs its own checks and calls
# sys.exit() at module scope (see this module's own header), which would
# hijack whatever imported it, and importing payload_check.py under a test
# runner is its own hazard (argv parsing, __main__ side effects). Both
# sides are read as source TEXT instead -- payload_check.py via its path,
# this module via Path(__file__).read_text(). A missing file or a
# non-matching extraction is RED, never skipped.
_PAYLOAD_CHECK_PATH = REPO / "tests" / "payload_check.py"
_THIS_MODULE_SOURCE = Path(__file__).read_text(encoding="utf-8")
_EXCLUDED_DIRS_ASSIGN_RE = re.compile(r"^EXCLUDED_DIRS\s*=\s*(\{[^\n]*\})", re.M)
_BYTECODE_SUFFIXES_ASSIGN_RE = re.compile(r"^BYTECODE_SUFFIXES\s*=\s*(\([^\n]*\))", re.M)

_self_excl_m = _EXCLUDED_DIRS_ASSIGN_RE.search(_THIS_MODULE_SOURCE)
_self_byte_m = _BYTECODE_SUFFIXES_ASSIGN_RE.search(_THIS_MODULE_SOURCE)

if _PAYLOAD_CHECK_PATH.is_file():
    _payload_check_source = _PAYLOAD_CHECK_PATH.read_text(encoding="utf-8")
    _pc_excl_m = _EXCLUDED_DIRS_ASSIGN_RE.search(_payload_check_source)
    _pc_byte_m = _BYTECODE_SUFFIXES_ASSIGN_RE.search(_payload_check_source)
    check("shared constants: tests/payload_check.py EXCLUDED_DIRS is "
          "textually identical to this suite's own",
          bool(_pc_excl_m) and bool(_self_excl_m)
          and _pc_excl_m.group(1) == _self_excl_m.group(1),
          f"payload_check.py: {_pc_excl_m.group(1) if _pc_excl_m else 'NOT FOUND'}; "
          f"this suite: {_self_excl_m.group(1) if _self_excl_m else 'NOT FOUND'}")
    check("shared constants: tests/payload_check.py BYTECODE_SUFFIXES is "
          "textually identical to this suite's own",
          bool(_pc_byte_m) and bool(_self_byte_m)
          and _pc_byte_m.group(1) == _self_byte_m.group(1),
          f"payload_check.py: {_pc_byte_m.group(1) if _pc_byte_m else 'NOT FOUND'}; "
          f"this suite: {_self_byte_m.group(1) if _self_byte_m else 'NOT FOUND'}")
else:
    check("shared constants: tests/payload_check.py exists", False,
          f"not found at {_PAYLOAD_CHECK_PATH}")

# --- 17. workflow line-count budget -----------------------------------------
# A dcs/workflows/*.md file exceeding its allowed line count is now caught
# mechanically at merge time, every time. Six of the ten files hold the
# plain policy ceiling; the four already over budget when this check was
# introduced get a named, dated, finite exemption instead of silently
# blocking every merge -- each one below is documented, temporary debt,
# not a bespoke permanent ceiling for that file. This check also fails the
# moment an exemption goes stale: its file no longer exists, or its file
# has shrunk back into policy and nobody deleted the entry.
WORKFLOW_BUDGET_LINES = 250

WORKFLOW_GRANDFATHERED_LINES = {
    # 263 lines measured at incident provisioning-script-upstreaming
    # (2026-07-30), 13 over the 250-line policy ceiling. Documented,
    # temporary debt pending a follow-up trim.
    'new.md': 270,
}


def _workflow_line_count(path):
    """Line count, not newline count: read_bytes(), collapse CRLF -> LF,
    then collapse any surviving lone CR -> LF (old Mac-style, or a stray
    mid-file CR), count LF occurrences, and add 1 if the result is
    non-empty and does not end in LF. This deliberately diverges from
    `wc -l`, which counts NEWLINES, not lines -- a file with content after
    its last LF (no trailing newline) has one more line than it has
    newlines, and `wc -l` under-counts it by exactly one there."""
    _raw = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    _n = _raw.count(b"\n")
    if _raw and not _raw.endswith(b"\n"):
        _n += 1
    return _n


_wb_files = workflows()
_wb_counts = {_p.name: _workflow_line_count(_p) for _p in _wb_files}
_wb_offenders = []

# (i) every file within its effective ceiling: the grandfather value if it
# has one, else the plain policy constant.
for _wb_name, _wb_count in _wb_counts.items():
    _wb_ceiling = WORKFLOW_GRANDFATHERED_LINES.get(_wb_name, WORKFLOW_BUDGET_LINES)
    if _wb_count > _wb_ceiling:
        _wb_offenders.append(f"{_wb_name}: {_wb_count} lines > ceiling {_wb_ceiling}")

# (ii) no grandfather entry names a file that no longer exists.
for _wb_name in WORKFLOW_GRANDFATHERED_LINES:
    if _wb_name not in _wb_counts:
        _wb_offenders.append(f"{_wb_name}: grandfathered but no longer exists in dcs/workflows/")

# (iii) no grandfather entry has gone slack -- its file back at or under
# the plain policy ceiling means the debt is discharged, and the entry
# left in place would just silently accumulate as dead exemption.
for _wb_name, _wb_ceiling in WORKFLOW_GRANDFATHERED_LINES.items():
    _wb_count = _wb_counts.get(_wb_name)
    if _wb_count is not None and _wb_count <= WORKFLOW_BUDGET_LINES:
        _wb_offenders.append(
            f"{_wb_name}: grandfathered at {_wb_ceiling} lines but now "
            f"{_wb_count}, at or under the {WORKFLOW_BUDGET_LINES}-line "
            "ceiling -- debt discharged, delete the entry")

# (iv) the population itself must be non-empty, or (i)-(iii) pass vacuously.
if not _wb_files:
    _wb_offenders.append("dcs/workflows/*.md population is empty")

check("workflow budget: every workflow is within its effective ceiling, "
      "every grandfather entry names a file that still exists, no "
      "grandfather entry has gone slack (fallen to or under "
      f"{WORKFLOW_BUDGET_LINES} lines), and the workflow population is "
      "non-empty",
      not _wb_offenders, "; ".join(_wb_offenders))

# --- 18. schema field contract carrier ---------------------------------------
# A schemas.md contract section is the pairing "## N. Title" + a "Returned
# by `agent`" sentence + the section's OWN field table (one field per row,
# first cell a backtick name, no `/`-joined cells -- S1's stated shape).
# Where the sentence names more than one agent (schemas.md #2 names both
# dcs-planning-chief and, parenthetically, dcs-logistics-chief) a separate
# "Contract producer: `agent-slug`" sentence pins the ONE agent whose own
# charter carries this section's field table -- both sentences are parsed
# fresh from schemas.md itself, at run time, same "read the source of
# truth, don't re-derive it" discipline as checks 13/14/15. No field name,
# agent slug, section number, or population count is a literal below.
#
# Direction: ONLY "a field the schema section declares is present in the
# resolved agent's own <output_contract> table" is checked. The reverse --
# a field the charter's table names that the schema section's table omits
# -- is NOT checked. Every case name and this comment say so; a "pairs
# reconciled" or "contracts synced" name would overclaim a direction this
# check does not verify.
_SFC_RETURNED_BY_RE = re.compile(r"Returned by(.*?)\.", re.S)
_SFC_AGENT_TOKEN_RE = re.compile(r"`(dcs-[\w-]+)`")
_SFC_PRODUCER_RE = re.compile(r"Contract producer:\s*`([\w-]+)`")
_SFC_TABLE_HEADER_RE = re.compile(r"^\|\s*Field\s*\|.*\|\s*$", re.M)
_SFC_ROW_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|")
_SFC_SEP_RE = re.compile(r"^\|[\s:\-|]+$")


def _sfc_field_table(body):
    """The FIRST '| Field | ... |'-headed table in `body`, as an ordered
    list of first-cell backtick names -- reading only up to the first line
    that no longer opens with '|' stops before any LATER, nested table
    (e.g. schemas.md #2's own "Tasking object" sub-table, which reuses the
    identical header shape one section further down) ever enters the
    result."""
    _hdr_m = _SFC_TABLE_HEADER_RE.search(body)
    if not _hdr_m:
        return []
    _fields = []
    # `$` in MULTILINE mode matches just before the header line's own
    # trailing "\n" without consuming it, so the text right after
    # _hdr_m.end() always starts with that "\n" -- split("\n")[1:] steps
    # past it instead of splitlines() reading it back as a spurious
    # leading blank "line" that would break the loop on iteration zero.
    for _line in body[_hdr_m.end():].split("\n")[1:]:
        if not _line.strip().startswith("|"):
            break
        _row_m = _SFC_ROW_RE.match(_line)
        if _row_m:
            _fields.append(_row_m.group(1))
    return _fields


def _sfc_table_data_rows(body):
    """The count of '|'-opening DATA lines in the same first table
    _sfc_field_table reads (separator lines excluded). A row _SFC_ROW_RE
    fails to parse -- e.g. a slash-joined cell -- is the difference
    between this count and len(_sfc_field_table(body)): it must fail
    loudly in a named case below, never vanish from the comparison
    (Safety advisory 1, period 1)."""
    _hdr_m = _SFC_TABLE_HEADER_RE.search(body)
    if not _hdr_m:
        return 0
    _rows = 0
    for _line in body[_hdr_m.end():].split("\n")[1:]:
        if not _line.strip().startswith("|"):
            break
        if _SFC_SEP_RE.match(_line.strip()):
            continue
        _rows += 1
    return _rows


def _sfc_producer(body):
    """The resolved contract-producing agent slug for one schemas.md
    section body, or None if the declaration itself does not resolve."""
    _rb_m = _SFC_RETURNED_BY_RE.search(body)
    if not _rb_m:
        return None
    _agents = _SFC_AGENT_TOKEN_RE.findall(_rb_m.group(1))
    if len(_agents) == 1:
        return _agents[0]
    _prod_m = _SFC_PRODUCER_RE.search(body)
    return _prod_m.group(1) if _prod_m else None


_SFC_OUTPUT_CONTRACT_RE = re.compile(r"<output_contract>(.*?)</output_contract>", re.S)


def _sfc_charter_fields(agent_text):
    """The resolved agent's OWN declared field names, read from its
    <output_contract> block's field table -- None if the block itself is
    missing (a structurally different failure than "block present, table
    empty"), so callers can tell the two apart."""
    _oc_m = _SFC_OUTPUT_CONTRACT_RE.search(agent_text)
    if not _oc_m:
        return None
    return _sfc_field_table(_oc_m.group(1))


# (a) section population: discovered by walking schemas.md's own "## N."
# headings and keeping only the ones with a "Returned by" sentence --
# schemas.md #7 (Delegation bounds) and #8 (209 sitrep, relocated) name no
# agent and are correctly excluded this way, never by a hardcoded number.
_sfc_section_starts = list(re.finditer(r"^##\s+(\d+)\.\s+(.+)$", schemas_md, re.M))
_sfc_sections = []
for _sfc_i, _sfc_m in enumerate(_sfc_section_starts):
    _sfc_end = (_sfc_section_starts[_sfc_i + 1].start()
                if _sfc_i + 1 < len(_sfc_section_starts) else len(schemas_md))
    _sfc_body = schemas_md[_sfc_m.start():_sfc_end]
    if not _SFC_RETURNED_BY_RE.search(_sfc_body):
        continue
    _sfc_sections.append({
        "num": int(_sfc_m.group(1)),
        "title": _sfc_m.group(2).strip(),
        "producer": _sfc_producer(_sfc_body),
        "fields": _sfc_field_table(_sfc_body),
        "rows": _sfc_table_data_rows(_sfc_body),
    })

# (b) degeneracy guard, part 1: the section population itself must be
# non-empty, or every case below passes by vacuous truth.
check("field guard: schemas.md yields at least one \"Returned by <agent>\" "
      "contract section",
      bool(_sfc_sections),
      "no '## N. Title' section with a 'Returned by' sentence was found")

# (c) charter population: discovered by walking agents/dcs-*.md, never a
# named list -- same glob idiom as known_agents (check 4) and workflows().
_sfc_agent_files = sorted((REPO / "agents").glob("dcs-*.md"))
check("field guard: agents/dcs-*.md yields at least one charter",
      bool(_sfc_agent_files),
      "agents/dcs-*.md glob returned nothing")

_sfc_agent_fields = {
    _p.stem: _sfc_charter_fields(_p.read_text(encoding="utf-8"))
    for _p in _sfc_agent_files
}

# (d) degeneracy guard, part 2: every discovered section's OWN declaration
# (its "Returned by"/"Contract producer" sentence resolving to exactly one
# agent slug, AND its field table yielding at least one field) must itself
# parse -- a section whose declaration silently failed would otherwise
# just vanish from every downstream comparison instead of failing loudly.
_sfc_bad_declarations = [
    f"schemas.md #{_s['num']} ({_s['title']})"
    for _s in _sfc_sections
    if _s["producer"] is None or not _s["fields"]
]
check("field guard: every contract section's own declaration (a resolved "
      "producer and at least one declared field) parses",
      not _sfc_bad_declarations, "; ".join(_sfc_bad_declarations))

# (d2) population completeness (Safety advisory 2, period 1): a section
# that loses its "Returned by" sentence silently leaves the population in
# (a) -- but its producer then stops being matched by ANY section, so
# pinning "every charter is some section's resolved producer" makes the
# drop loud. Both populations are discovered at run time above, never
# listed here.
_sfc_producers = {_s["producer"] for _s in _sfc_sections if _s["producer"]}
_sfc_unmatched = sorted(_p.stem for _p in _sfc_agent_files
                        if _p.stem not in _sfc_producers)
check("field guard: every charter agents/dcs-*.md is the resolved "
      "producer of at least one schemas.md contract section (a section "
      "dropping its 'Returned by' line fails here instead of vanishing)",
      not _sfc_unmatched,
      f"charters no contract section resolves to: {_sfc_unmatched}")

# (e) one named case per (section, agent) pair (idiom of checks 12(c) /
# 13(d) / 14(d)) -- a mismatch in a NEW pair fails by name, not folded
# into an aggregate count.
for _sfc_s in _sfc_sections:
    _sfc_label = f"field guard: schemas.md #{_sfc_s['num']} ({_sfc_s['title']})"
    check(f"{_sfc_label} -- every `|` data row in its field table parses "
          "as one declared field (an unparsed row fails, never vanishes)",
          _sfc_s["rows"] == len(_sfc_s["fields"]),
          f"{_sfc_s['rows']} data rows vs {len(_sfc_s['fields'])} parsed "
          "fields -- a row the field regex cannot read (e.g. a "
          "slash-joined cell) is invisible to the comparison")
    if _sfc_s["producer"] is None:
        check(f"{_sfc_label} -- contract producer resolves", False,
              "the 'Returned by'/'Contract producer' sentence did not "
              "resolve to exactly one agent slug")
        continue
    _sfc_charter_path = REPO / "agents" / f"{_sfc_s['producer']}.md"
    _sfc_label = f"{_sfc_label} -> agents/{_sfc_s['producer']}.md"
    if not _sfc_charter_path.is_file():
        check(_sfc_label, False,
              f"agents/{_sfc_s['producer']}.md does not exist")
        continue
    _sfc_target_fields = _sfc_agent_fields.get(_sfc_s["producer"])
    if _sfc_target_fields is None:
        check(_sfc_label, False,
              f"agents/{_sfc_s['producer']}.md has no <output_contract> block")
        continue
    _sfc_missing = [_f for _f in _sfc_s["fields"] if _f not in _sfc_target_fields]
    check(f"{_sfc_label} -- every field this section declares is present "
          "in the charter's own contract table (this direction only, "
          "never the reverse)",
          not _sfc_missing,
          f"declared in schemas.md but missing from the charter: {_sfc_missing}")

# (f) negative proof (idiom of check 13(f)'s forged mapping): rerun the
# SAME comparator (_sfc_charter_fields) against one real agent's
# <output_contract> table held IN MEMORY with one of its own declared
# fields' table row removed -- the field name taken from the parse above,
# never typed here -- proving the comparator actually reads the table
# rather than passing whatever it is handed. No file on disk is touched;
# agents/** stays untouched.
_sfc_forge_target = None
for _sfc_s in _sfc_sections:
    if not _sfc_s["producer"] or not _sfc_s["fields"]:
        continue
    _sfc_p = REPO / "agents" / f"{_sfc_s['producer']}.md"
    if _sfc_p.is_file():
        _sfc_forge_target = (_sfc_s, _sfc_p)
        break

if _sfc_forge_target:
    _sfc_fs, _sfc_fp = _sfc_forge_target
    _sfc_real_text = _sfc_fp.read_text(encoding="utf-8")
    _sfc_victim = _sfc_fs["fields"][0]
    _sfc_row_re = re.compile(r"^\|\s*`" + re.escape(_sfc_victim) + r"`.*$\n?", re.M)
    _sfc_forged_text, _sfc_n_removed = _sfc_row_re.subn("", _sfc_real_text)
    _sfc_forged_fields = _sfc_charter_fields(_sfc_forged_text) or []
    _sfc_forged_missing = [_f for _f in _sfc_fs["fields"] if _f not in _sfc_forged_fields]
    check(f"field guard negative proof: removing `{_sfc_victim}` in memory "
          f"from agents/{_sfc_fs['producer']}.md's own contract table is "
          "caught by the same comparator (no file touched)",
          _sfc_n_removed == 1 and bool(_sfc_forged_missing),
          f"rows removed: {_sfc_n_removed}, fields still reported missing "
          f"after the forgery: {_sfc_forged_missing}")
else:
    check("field guard negative proof: a representative (section, agent) "
          "pair exists to forge against",
          False, "no section with a resolved producer, at least one "
          "declared field, and an existing charter file was found")

# --- 19. schemas.md JSON example carrier -------------------------------------
# Every fenced code block in dcs/references/schemas.md must parse as JSON
# -- an example that stopped being valid JSON stops being a worked example.
# The block population is discovered at run time by walking schemas.md's
# own ``` fences (_fenced_blocks(), already defined above for check 12 --
# reused rather than re-derived, same discipline as check 16's reuse of
# EXCLUDED_DIRS), never a hardcoded list or count.
_sjb_blocks = _fenced_blocks(schemas_md)

check("json block guard: dcs/references/schemas.md has at least one "
      "fenced code block",
      bool(_sjb_blocks),
      "no ``` fenced block found in dcs/references/schemas.md")

for _sjb_i, _sjb_lines in enumerate(_sjb_blocks, start=1):
    _sjb_text = "\n".join(_sjb_lines)
    try:
        json.loads(_sjb_text)
        _sjb_err = None
    except json.JSONDecodeError as _sjb_e:
        _sjb_err = str(_sjb_e)
    check(f"json block guard: schemas.md fenced block #{_sjb_i} parses "
          "with json.loads",
          _sjb_err is None, _sjb_err or "")

# --- 20. inbound field-presence guard -----------------------------------------
# For each workflow that spawns an agent, verify that ALL required fields
# from the relevant schema contract section(s) appear in backtick context in
# the workflow text. A field declared in a schema section that is NOT found in
# backtick-context in the workflow means the workflow no longer names a field
# the schema requires -- real inbound drift: a spawned agent reading the
# workflow would be unaware of a required return field.
#
# Workflow-to-section mapping is the one declared place; the field set for
# each section comes from the _sfc_sections parse above (check 18) -- same
# "parse the source of truth at run time" discipline as checks 13/14/15/18.
# No field name, section number or workflow name appears as a literal in any
# comparator below.

_INBOUND_WF_SECTIONS = {
    'new.md':    [1],      # schema #1 -> dcs-situation-analyst
    'plan.md':   [2, 3],   # schema #2 -> dcs-planning-chief, #3 -> dcs-logistics-chief
    'execute.md': [4, 5],  # schema #4 -> dcs-ops-specialist, #5 -> dcs-safety-officer
}

for _iwf_name, _iwf_sections in _INBOUND_WF_SECTIONS.items():
    _iwf_path = REPO / "dcs" / "workflows" / _iwf_name
    if not _iwf_path.is_file():
        check(f"inbound field guard: {_iwf_name} exists", False,
              f"dcs/workflows/{_iwf_name} not found")
        continue
    _iwf_text = _iwf_path.read_text(encoding="utf-8")
    # Every backtick-wrapped token in the workflow -- restrict to single-line
    # matches: [^`\n] won't cross newlines, which is correct for Markdown
    # inline code (fenced blocks use ```, never a single backtick span).
    _iwf_backticks = set(re.findall(r'`([^`\n]+)`', _iwf_text))

    for _iwf_sec in _iwf_sections:
        _iwf_section = next((_s for _s in _sfc_sections if _s["num"] == _iwf_sec), None)
        if _iwf_section is None:
            check(f"inbound field guard: {_iwf_name} -> schemas.md #{_iwf_sec} -- "
                  "section found in schemas.md parse",
                  False,
                  f"schemas.md section #{_iwf_sec} not found in _sfc_sections "
                  "(no 'Returned by' sentence, or section does not exist)")
            continue
        _iwf_fields = _iwf_section.get("fields", [])
        if not _iwf_fields:
            check(f"inbound field guard: {_iwf_name} -> schemas.md #{_iwf_sec} -- "
                  "section has declared fields",
                  False,
                  f"section #{_iwf_sec} ({_iwf_section.get('title', '?')}) "
                  "has no parsed field table")
            continue

        _iwf_missing = [_f for _f in _iwf_fields if _f not in _iwf_backticks]
        check(f"inbound field guard: {_iwf_name} -> schemas.md #{_iwf_sec} "
              f"({_iwf_section['title']}) -- all {len(_iwf_fields)} required "
              "fields present in backtick context",
              not _iwf_missing,
              f"declared in schema but missing from backtick context: {_iwf_missing}")

# --- 20. field-lesson citation guard -----------------------------------------
# Every "field lesson" mention in the shipped package must carry an
# incident identifier: an incident slug, a version number, or an explicit
# "(predates self-hosting)" note. A false field lesson shipped once
# (v0.5.10); this guard makes a recurrence mechanically detectable.
_FL_FILES = [
    "dcs/references/doctrine-appendix.md",
    "dcs/workflows/deploy.md",
    "dcs/workflows/new.md",
    "dcs/workflows/close.md",
    "dcs/templates/202-OBJECTIVES.md",
    "dcs/templates/REGISTER.md",
]
# Match "field lesson" only when near a date pattern (YYYY-MM-DD) —
# filters out title lines, convention prose, cross-references, and
# compound adjectives ("field-lesson narratives") that are not claims.
_FL_LINE_RE = re.compile(r"[Ff]ield lesson.*\d{4}-\d{2}-\d{2}", re.I)
_FL_ID_RE = re.compile(
    r"incident `[a-z0-9-]+`|v\d+\.\d+\.\d+|predates self-hosting", re.I)
_fl_bad = []
for _fl_fname in _FL_FILES:
    _fl_path = REPO / _fl_fname
    if not _fl_path.exists():
        _fl_bad.append(f"{_fl_fname}: file not found")
        continue
    _fl_text = _fl_path.read_text(encoding="utf-8")
    for _fl_li, _fl_line in enumerate(_fl_text.splitlines(), start=1):
        if _FL_LINE_RE.search(_fl_line) and not _FL_ID_RE.search(_fl_line):
            # Check if the next line carries the identifier (multi-line
            # citations like "field lesson,\n2026-07-22, predates...")
            _fl_lines = _fl_text.splitlines()
            _fl_next = (
                _fl_lines[_fl_li]
                if _fl_li < len(_fl_lines)
                else ""
            )
            if not _FL_ID_RE.search(_fl_next):
                _fl_bad.append(f"{_fl_fname}:{_fl_li}: {_fl_line.strip()[:80]}")
check("field-lesson citations: every field lesson mention in shipped "
      "package carries an incident identifier (slug, version, or "
      "'predates self-hosting')",
      not _fl_bad, "; ".join(_fl_bad))

# --- 21. outbound missing-required-fields guard --------------------------------
# Walk .dcs/incidents/*/ looking for SAFETY.md, AAR.md, 214-LOG.md -- files
# that contain JSON blocks resembling agent returns. For each JSON block found,
# compare its fields against the relevant schema section's required fields.
# Findings are INFORMATIONAL only (never fail the test): historical artifacts
# contain documented pre-existing drift that must not block the suite.
#
# SAFETY.md maps to schemas.md #5 (safety-officer). AAR.md and 214-LOG.md are
# matched by field presence -- the schema section whose required fields overlap
# most with the block's keys is treated as the relevant one.

_INCIDENTS_DIR = REPO / ".dcs" / "incidents"
_OUTBOUND_FNAMES = ["SAFETY.md", "AAR.md", "214-LOG.md"]

# File-name to primary schema section guess
_OUTBOUND_FILE_SCHEMA = {
    "SAFETY.md": 5,   # safety-officer verdict
}

# Known schema required-field sets (from the _sfc_sections parse above)
_OUTBOUND_SCHEMA_FIELDS = {
    _s["num"]: _s["fields"]
    for _s in _sfc_sections
    if _s.get("fields")
}

_ob_findings = []

if _INCIDENTS_DIR.is_dir():
    for _ob_incident_dir in sorted(_INCIDENTS_DIR.iterdir()):
        if not _ob_incident_dir.is_dir():
            continue
        for _ob_fname in _OUTBOUND_FNAMES:
            _ob_fpath = _ob_incident_dir / _ob_fname
            if not _ob_fpath.is_file():
                continue
            _ob_text = _ob_fpath.read_text(encoding="utf-8")
            _ob_rel = str(_ob_fpath.relative_to(REPO)).replace("\\", "/")

            for _ob_block_i, _ob_lines in enumerate(_fenced_blocks(_ob_text), start=1):
                _ob_json_text = "\n".join(_ob_lines)
                try:
                    _ob_parsed = json.loads(_ob_json_text)
                except json.JSONDecodeError:
                    continue
                if not isinstance(_ob_parsed, dict):
                    continue

                _ob_keys = set(_ob_parsed.keys())

                # Determine which schema section(s) to check against
                _ob_primary = _OUTBOUND_FILE_SCHEMA.get(_ob_fname)
                if _ob_primary is not None:
                    _ob_secs = [_ob_primary]
                else:
                    # Best match by field overlap
                    if _OUTBOUND_SCHEMA_FIELDS:
                        _ob_secs = sorted(
                            _OUTBOUND_SCHEMA_FIELDS,
                            key=lambda _sn: len(_ob_keys & set(_OUTBOUND_SCHEMA_FIELDS.get(_sn, []))),
                            reverse=True,
                        )[:1]
                    else:
                        _ob_secs = []

                for _ob_sec in _ob_secs:
                    _ob_required = _OUTBOUND_SCHEMA_FIELDS.get(_ob_sec, [])
                    if not _ob_required:
                        continue
                    _ob_missing = sorted(_f for _f in _ob_required if _f not in _ob_keys)
                    if _ob_missing:
                        _ob_findings.append(
                            f"  {_ob_rel} block #{_ob_block_i} vs schemas.md "
                            f"#{_ob_sec}: missing required fields: {_ob_missing}"
                        )

if _ob_findings:
    print(f"\nINFO: outbound field guard -- {len(_ob_findings)} finding(s) "
          "(informational only, not test failures):")
    for _ob_f in _ob_findings:
        print(_ob_f)
else:
    print("\nINFO: outbound field guard -- no missing-required-field "
          "discrepancies found in .dcs/incidents/*/ artifacts")

# --- 22. preservation-map mechanism (revision-preservation-map) -------------
# `dcs/workflows/plan.md`'s `## 6c.` bounded-amendment path can re-stamp the
# approval marker after touching only a narrow slice of the IAP -- and
# `register-field-repair-path` (2026-07-27) showed that path silently
# dropping a different, already-satisfied 202 criterion's section while
# doing so, with nothing mechanical catching it. `dcs/tools/preservation_map.py`
# is the mechanism: a `## 6c.` amendment must carry a preservation map (a
# fenced JSON block in 214-LOG.md) naming, for every criterion the
# amendment itself does not touch, the screened artifact and anchor text
# that proves it still holds -- re-derived from the artifact's current
# bytes every time, never trusted from the map's own self-report (the
# AAR.md:82-89 false-fidelity defect). Imported via the same
# `importlib.util.spec_from_file_location` idiom check 12 uses for
# dcs_gate.py, never re-implemented here.
_pm_spec = importlib.util.spec_from_file_location(
    "preservation_map", REPO / "dcs" / "tools" / "preservation_map.py")
pm = importlib.util.module_from_spec(_pm_spec)
_pm_spec.loader.exec_module(pm)

_PM_FIXTURES_ROOT = REPO / "tests" / "fixtures" / "preservation-map"
_PM_SCENARIOS = ("clean", "dropped-criterion", "no-map")

# (i) degeneracy guard: without a non-empty, three-scenario fixture
# population, every case below would pass vacuously.
_pm_scenario_dirs = (
    {p.name for p in _PM_FIXTURES_ROOT.iterdir() if p.is_dir()}
    if _PM_FIXTURES_ROOT.is_dir() else set()
)
check("preservation map: fixture population is non-empty and covers all "
      "three scenarios (degeneracy guard -- without it every case below "
      "passes vacuously)",
      _PM_FIXTURES_ROOT.is_dir() and set(_PM_SCENARIOS) <= _pm_scenario_dirs,
      f"found scenario dirs under {_PM_FIXTURES_ROOT}: {sorted(_pm_scenario_dirs)}")

# (ii) clean/ -- an amendment naming criterion 6 whose map re-proves
# criteria 1-5 against this fixture's own IAP.md bytes. Admissible.
_pm_clean_dir = _PM_FIXTURES_ROOT / "clean"
_pm_clean_findings = pm.verify(_pm_clean_dir)
check("preservation map: clean/ is accepted -- verify() returns []",
      not _pm_clean_findings, "; ".join(_pm_clean_findings))

# (iii) no-map/ -- a `## 6c.` re-stamp entry with no preservation-map block
# at all. Rejected.
_pm_nomap_dir = _PM_FIXTURES_ROOT / "no-map"
_pm_nomap_findings = pm.verify(_pm_nomap_dir)
check("preservation map: no-map/ is rejected -- verify() returns a finding",
      bool(_pm_nomap_findings), "verify() returned [] -- expected a finding")

# (iv) THE REGRESSION PAIR on dropped-criterion/ (register-field-repair-path's
# defect shape): verify() must name criterion 5 by number, AND the PRE-FIX
# comparator (prefix_coverage(), which only checks "maps to a tasking id")
# must return [] on the SAME fixture -- proving its blindness is real, not
# asserted. One case each, so the contrast fails by name.
_pm_dropped_dir = _PM_FIXTURES_ROOT / "dropped-criterion"
_pm_dropped_findings = pm.verify(_pm_dropped_dir)
check("preservation map: dropped-criterion/ -- verify() names criterion 5",
      any(re.search(r"\bcriterion 5\b", f) for f in _pm_dropped_findings),
      f"findings: {_pm_dropped_findings}")
_pm_dropped_prefix = pm.prefix_coverage(_pm_dropped_dir)
check("preservation map: dropped-criterion/ -- prefix_coverage() (the "
      "pre-fix comparator) returns [] on the same fixture (every criterion "
      "still maps to a tasking id; this is its documented blind spot)",
      _pm_dropped_prefix == [], f"prefix_coverage(): {_pm_dropped_prefix}")

# (v) in-memory forgery proof (idiom of the schema field contract carrier's
# own in-memory forgery cases -- cited by name, not section number, since
# this file's section numbers are due to shift when field-lesson-guard-vacuity
# fixes the duplicate-20 defect): take clean/'s IAP.md text and its map's
# first preserved entry, delete that entry's anchor's OWN LINE in memory,
# and rerun the SAME comparator (preserved_findings) against the forged
# text -- proving it reads content rather than passing whatever it is
# handed. No file on disk is modified.
_pm_clean_log_text = (_pm_clean_dir / "214-LOG.md").read_text(encoding="utf-8")
_pm_clean_iap_text = (_pm_clean_dir / "IAP.md").read_text(encoding="utf-8")
_pm_clean_block = pm.find_map(_pm_clean_log_text) or {}
_pm_clean_entries = (_pm_clean_block.get(pm.MAP_KEY) or {}).get("preserved") or []
_pm_victim = _pm_clean_entries[0] if _pm_clean_entries else None
if _pm_victim:
    _pm_victim_anchor = _pm_victim.get("anchor", "")
    _pm_forged_text = "\n".join(
        ln for ln in _pm_clean_iap_text.splitlines() if _pm_victim_anchor not in ln
    )
    _pm_forged_findings = pm.preserved_findings(_pm_victim, _pm_forged_text, "IAP.md")
    check("preservation map negative proof: deleting clean/'s first preserved "
          "entry's anchor line in memory is caught by the SAME comparator "
          "(preserved_findings) -- no file on disk touched",
          bool(_pm_forged_findings), f"findings after forging: {_pm_forged_findings}")
else:
    check("preservation map negative proof: clean/'s map has a preserved "
          "entry to forge against",
          False, "no preserved entries found in clean/'s preservation map")

# (v-b) the false-fidelity forgery proof (AAR.md:82-89's exact defect
# shape): take clean/'s first preserved entry AS-IS (anchor still present,
# artifact untouched) but mutate ONLY its self-reported `output` field to a
# plausible-looking lie, and confirm preserved_findings() -- the same
# comparator, not a second implementation -- still catches the disagreement
# even though the anchor itself is fine. This is the branch (v)'s
# anchor-deletion proof does not exercise: a map can lie about `output`
# while the anchor is genuinely present, and that lie must be caught too.
if _pm_victim:
    _pm_lying_entry = dict(_pm_victim)
    _pm_lying_entry["output"] = "this line was never in the artifact"
    _pm_lying_findings = pm.preserved_findings(
        _pm_lying_entry, _pm_clean_iap_text, "IAP.md")
    check("preservation map false-fidelity proof: a preserved entry whose "
          "anchor is genuinely present but whose self-reported output is "
          "a lie is still caught by preserved_findings() -- output is "
          "never trusted as the proof",
          bool(_pm_lying_findings), f"findings: {_pm_lying_findings}")

# (vi) the carrier case: INVOCATION, read from the imported module (never
# typed as a literal here), must appear in dcs/workflows/plan.md compared
# on whitespace-collapsed text (markdown hard-wraps) -- reusing _ws_norm(),
# never a third normaliser. S2 writes this literal into plan.md; if this
# case is red because S2 has not landed it yet, that is reported as red by
# name, not described as "expected to pass later".
_pm_plan_text = read("dcs/workflows/plan.md")
check("preservation map carrier: INVOCATION (from the imported module) "
      "appears in dcs/workflows/plan.md, whitespace-collapsed",
      _ws_norm(pm.INVOCATION) in _ws_norm(_pm_plan_text),
      f"INVOCATION: {pm.INVOCATION!r}")

# (vii) the field half: every REAL .dcs/incidents/*/214-LOG.md `## 6c.`
# re-stamp entry -- recognised via the imported dcs_gate.py grammar
# (sentinel_of() == 'stamp'), never a re-derived regex, plus the literal
# "re-stamp" plan.md step 8 uses for this disposition's own log line --
# whose timestamp is on or after the pinned effective date below must pass
# verify() clean. Entries before the pin are OUT OF SCOPE, not silently
# skipped: the count in scope is printed even at zero, since this
# mechanism cannot retroactively bind a log entry written before it
# existed.
#
# Effective date: 2026-08-02, the day after revision-preservation-map (this
# incident) opened (2026-08-01) -- pinned so a zero-in-scope result today
# is the expected, visible state, not a silent gap.
_PM_EFFECTIVE_DATE = "2026-08-02"  # revision-preservation-map, period 1

_pm_entry_ts_re = re.compile(r"^\[([^\]]*)\]\s+")
_pm_incidents_root = REPO / ".dcs" / "incidents"
_pm_in_scope = []
if _pm_incidents_root.is_dir():
    for _pm_inc_dir in sorted(_pm_incidents_root.iterdir()):
        if not _pm_inc_dir.is_dir():
            continue
        _pm_log_path = _pm_inc_dir / "214-LOG.md"
        if not _pm_log_path.is_file():
            continue
        for _pm_line in _pm_log_path.read_text(encoding="utf-8").splitlines():
            if _gate.sentinel_of(_pm_line) == "stamp" and "re-stamp" in _pm_line.lower():
                _pm_m = _pm_entry_ts_re.match(_pm_line)
                if _pm_m and _pm_m.group(1) >= _PM_EFFECTIVE_DATE:
                    _pm_in_scope.append((_pm_inc_dir, _pm_m.group(1)))

print(
    f"\npreservation map field guard: {len(_pm_in_scope)} `## 6c.` re-stamp "
    f"entr{'y' if len(_pm_in_scope) == 1 else 'ies'} in scope "
    f"(effective date {_PM_EFFECTIVE_DATE}; entries before it are out of "
    "scope, not silently skipped)"
)

for _pm_inc_dir, _pm_ts in _pm_in_scope:
    _pm_rel = _pm_inc_dir.relative_to(REPO).as_posix()
    try:
        _pm_field_findings = pm.verify(_pm_inc_dir)
    except OSError as _pm_exc:
        check(f"preservation map field guard: {_pm_rel}'s 6c re-stamp at "
              f"{_pm_ts} -- verify() returns []",
              False, f"verify() raised: {_pm_exc}")
        continue
    check(f"preservation map field guard: {_pm_rel}'s 6c re-stamp at "
          f"{_pm_ts} -- verify() returns []",
          not _pm_field_findings, "; ".join(_pm_field_findings))

# --- 23. record-integrity mechanism (close-integrity-guard-bundle) ---------
# `dcs/tools/record_integrity.py` (S1's territory this incident) is the
# shipped, project-agnostic close-time record-integrity check: citation-
# position sha existence, 9-artifact-set completeness, SAFETY.md real-fence
# schema conformance, a clean tree, non-degenerate commit messages -- all
# running unconditionally at close, never opt-in (doctrine principle 16).
# Imported via the SAME `importlib.util.spec_from_file_location` idiom
# check 22 uses for preservation_map.py, never re-implemented here (T1).
#
# Unlike check 22's pm import, this one is GUARDED: this incident runs four
# specialists in parallel and S1's module is a read dependency this file
# does not control the landing order of -- a bare, unguarded import
# (section 22's own style) would raise on a missing file and abort this
# whole script before its final "N/M passed" line ever printed. Every case
# below that depends on the import degrades to a named red finding instead
# of a crash when `ri` is None or lacks an expected attribute, per this
# incident's own tasking: "your suite is legitimately red until S1/S3/S4
# land ... report red-by-name" -- the convention section 22 case (vi)
# already states for its own plan.md carrier.
import subprocess

_ri_path = REPO / "dcs" / "tools" / "record_integrity.py"
_ri_import_error = None
try:
    _ri_spec = importlib.util.spec_from_file_location("record_integrity", _ri_path)
    ri = importlib.util.module_from_spec(_ri_spec)
    _ri_spec.loader.exec_module(ri)
except Exception as _ri_exc:  # noqa: broad on purpose -- see comment above
    ri = None
    _ri_import_error = _ri_exc

_RI_FIXTURES_ROOT = REPO / "tests" / "fixtures" / "record-integrity"
_RI_SCENARIOS = (
    "fabricated-sha", "suppressed-stamp", "suppressed-correction",
    "missing-artifact", "type1-no-skip", "prose-fence", "boundary-pin",
)

# (i) degeneracy guard: without a non-empty fixture population covering
# every named scenario, every case below would pass vacuously.
_ri_scenario_dirs = (
    {p.name for p in _RI_FIXTURES_ROOT.iterdir() if p.is_dir()}
    if _RI_FIXTURES_ROOT.is_dir() else set()
)
check("record integrity: fixture population is non-empty and covers all "
      "named scenarios (degeneracy guard -- without it every case below "
      "passes vacuously)",
      _RI_FIXTURES_ROOT.is_dir() and set(_RI_SCENARIOS) <= _ri_scenario_dirs,
      f"found scenario dirs under {_RI_FIXTURES_ROOT}: {sorted(_ri_scenario_dirs)}")


def _ri_run(incident_dir):
    """Invoke record_integrity.py as a subprocess against `incident_dir`
    -- mirrors S1's OWN evidence-gathering shape (a CLI run against a
    real directory) for criteria 1/2/3, which S1's tasking does not
    expose as guessable-at pure functions the way criteria 4/5 are.
    Returns (returncode, combined stdout+stderr). subprocess.run does
    NOT raise merely because the target script does not exist yet --
    Python's own launcher reports that on stderr with a non-zero exit --
    so this helper needs no import-style try/except."""
    proc = subprocess.run(
        [sys.executable, str(_ri_path), str(incident_dir)],
        cwd=REPO, capture_output=True, text=True,
        encoding="utf-8", errors="replace")
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


# (ii) fabricated-sha/ -- one fabricated token in citation position.
_ri_rc, _ri_out = _ri_run(_RI_FIXTURES_ROOT / "fabricated-sha")
check("record integrity: fabricated-sha/ -- a fabricated citation-"
      "position token is a named, non-empty finding",
      _ri_rc != 0 and "deadbeef0" in _ri_out,
      f"exit={_ri_rc}; output: {_ri_out!r}")

# (iii) suppressed-stamp/ -- suppression (a), genuinely reached: the token
# must not be reported as a finding, and a suppression line naming it
# must be emitted. Every line mentioning the token must ALSO mention
# "suppress" (case-insensitive) -- i.e. no OTHER, non-suppression line
# calls it out, which is what "not reported as a finding" means here
# without hardcoding S1's exact finding-line wording.
_ri_rc, _ri_out = _ri_run(_RI_FIXTURES_ROOT / "suppressed-stamp")
_ri_token = "35fce4016641deadbeef"
_ri_token_lines = [ln for ln in _ri_out.splitlines() if _ri_token in ln]
check("record integrity: suppressed-stamp/ -- the stamp entry's own "
      "digest, re-cited with a commit keyword in the same entry, is "
      "suppressed (not a finding) and a suppression line names it",
      bool(_ri_token_lines) and all("suppress" in ln.lower() for ln in _ri_token_lines),
      f"exit={_ri_rc}; lines mentioning {_ri_token!r}: {_ri_token_lines}; "
      f"full output: {_ri_out!r}")

# (iv) suppressed-correction/ -- suppression (b), S1's corrected, two-pass,
# file-scoped mechanism (close-integrity-guard-bundle, period 1 attempt 2's
# fix to the Safety Officer's refutation 2): a genuine, entry-INITIAL
# RECORD-CORRECTION: entry (dcs_gate.py's own entry grammar -- never a
# body-anywhere substring match) suppresses every occurrence, anywhere in
# the same 214-LOG.md, of the token it names; a mere MID-LINE prose
# mention of the literal "RECORD-CORRECTION:" string suppresses nothing
# (required behavior (i)). Proven as a genuine PAIR (criterion 13's own
# required shape) rather than the prior fixture's single self-correcting
# entry, which tested nothing about clearing an EARLIER, separate
# occurrence and only passed under the discarded substring rule:
# uncorrected/214-LOG.md carries the unresolvable citation plus the
# mid-line mention and NO correction entry; corrected/214-LOG.md is
# uncorrected/214-LOG.md byte-for-byte plus ONE appended, correctly-formed
# RECORD-CORRECTION: entry naming that exact token (verified below by
# reading both files directly, not merely asserted). Assertions are
# CRITERION-1-SCOPED, never whole-tool exit code: every fixture under
# tests/fixtures/ is untracked, so criteria 2/4 fire regardless of
# criterion 1's own correctness -- the whole-tool exit-0 claim stays on
# the REAL clean incident (record-integrity-corrections, below), never on
# a fixture.
_ri_corr_token = "cafef00d1"
_ri_corr_uncorrected_dir = _RI_FIXTURES_ROOT / "suppressed-correction" / "uncorrected"
_ri_corr_corrected_dir = _RI_FIXTURES_ROOT / "suppressed-correction" / "corrected"

_ri_rc, _ri_out = _ri_run(_ri_corr_uncorrected_dir)
_ri_corr_uncorrected_findings = [
    ln for ln in _ri_out.splitlines()
    if ln.startswith("criterion 1: FINDING") and f"'{_ri_corr_token}'" in ln
]
_ri_corr_uncorrected_suppressed = [
    ln for ln in _ri_out.splitlines()
    if ln.startswith("criterion 1: SUPPRESSED") and f"'{_ri_corr_token}'" in ln
]
check("record integrity: suppressed-correction/uncorrected/ -- the "
      "earlier, unresolvable citation is a criterion 1 FINDING naming "
      "the token, and the different entry's mid-line RECORD-CORRECTION: "
      "mention (not entry-initial) suppresses nothing (zero SUPPRESSED "
      "lines)",
      bool(_ri_corr_uncorrected_findings) and not _ri_corr_uncorrected_suppressed,
      f"exit={_ri_rc}; criterion 1 FINDING lines naming {_ri_corr_token!r}: "
      f"{_ri_corr_uncorrected_findings}; SUPPRESSED lines: "
      f"{_ri_corr_uncorrected_suppressed}; full output: {_ri_out!r}")

_ri_rc, _ri_out = _ri_run(_ri_corr_corrected_dir)
_ri_corr_corrected_findings = [
    ln for ln in _ri_out.splitlines()
    if ln.startswith("criterion 1: FINDING") and f"'{_ri_corr_token}'" in ln
]
_ri_corr_corrected_suppressed = [
    ln for ln in _ri_out.splitlines()
    if ln.startswith("criterion 1: SUPPRESSED") and f"'{_ri_corr_token}'" in ln
]
check("record integrity: suppressed-correction/corrected/ -- byte-"
      "identical to uncorrected/214-LOG.md plus one appended, genuine "
      "entry-initial RECORD-CORRECTION: entry naming the token clears "
      "EVERY earlier occurrence (zero criterion 1 FINDING lines) and "
      "prints a SUPPRESSED line naming it",
      not _ri_corr_corrected_findings and bool(_ri_corr_corrected_suppressed),
      f"exit={_ri_rc}; FINDING lines: {_ri_corr_corrected_findings}; "
      f"SUPPRESSED lines: {_ri_corr_corrected_suppressed}; full output: "
      f"{_ri_out!r}")

_ri_corr_uncorrected_log = (_ri_corr_uncorrected_dir / "214-LOG.md").read_text(encoding="utf-8")
_ri_corr_corrected_log = (_ri_corr_corrected_dir / "214-LOG.md").read_text(encoding="utf-8")
_ri_corr_appended = _ri_corr_corrected_log[len(_ri_corr_uncorrected_log):]
check("record integrity: suppressed-correction/ pair -- corrected/"
      "214-LOG.md is uncorrected/214-LOG.md byte-for-byte plus exactly "
      "one appended line (never a rewrite of any existing line), and "
      "that appended line is itself a genuine, entry-initial "
      "RECORD-CORRECTION: entry naming the token",
      _ri_corr_corrected_log.startswith(_ri_corr_uncorrected_log)
      and _ri_corr_appended.count("\n") <= 1
      and re.match(r"^\[[^\]]*\]\s+RECORD-CORRECTION:", _ri_corr_appended) is not None
      and _ri_corr_token in _ri_corr_appended,
      f"uncorrected length {len(_ri_corr_uncorrected_log)}; corrected "
      f"length {len(_ri_corr_corrected_log)}; corrected startswith "
      f"uncorrected: {_ri_corr_corrected_log.startswith(_ri_corr_uncorrected_log)}; "
      f"appended text: {_ri_corr_appended!r}")

# (v) missing-artifact/ -- Type 3, one required artifact (AAR.md) absent,
# NO skip note -> finding. Plus type1-no-skip/ -- Type 1, 203-ORG.md
# absent, skip note PRESENT -> still a finding (the skip exemption is
# Type-3-only). Two named cases, so the Type asymmetry fails by name.
_ri_rc, _ri_out = _ri_run(_RI_FIXTURES_ROOT / "missing-artifact")
check("record integrity: missing-artifact/ -- Type 3 with one artifact "
      "(AAR.md) absent and no skip note is a finding naming AAR.md",
      _ri_rc != 0 and "AAR.md" in _ri_out,
      f"exit={_ri_rc}; output: {_ri_out!r}")

_ri_rc, _ri_out = _ri_run(_RI_FIXTURES_ROOT / "type1-no-skip")
check("record integrity: type1-no-skip/ -- Type 1 with 203-ORG.md absent "
      "is a finding even though a skip note is present (the skip "
      "exemption is Type-3-only, never Type-1)",
      _ri_rc != 0 and "203-ORG" in _ri_out,
      f"exit={_ri_rc}; output: {_ri_out!r}")

# (vi) prose-fence/ -- a post-pin incident whose SAFETY.md only mentions a
# fence in prose -> finding. Paired with the REAL record-integrity-
# corrections/SAFETY.md (line 33's naive-substring trap: "```json" inside
# prose about the ABSENCE of fences), which must NOT be flagged. That real
# incident is dated 2026-08-02 (on the pin, out of scope by date alone),
# and S1's own required evidence (204-TASKING/S1.md) states exit 0 against
# it -- a stronger, better-grounded assertion than guessing S1's exact
# "out of scope" wording.
_ri_prose_fence_dir = _RI_FIXTURES_ROOT / "prose-fence" / "2026-08-10-prose-fence"
_ri_rc, _ri_out = _ri_run(_ri_prose_fence_dir)
_ri_prose_fence_c3_findings = [
    ln for ln in _ri_out.splitlines() if ln.startswith("criterion 3: FINDING")
]
check("record integrity: prose-fence/ -- a post-pin SAFETY.md that only "
      "mentions a fence in prose (no genuine fenced block) is a criterion "
      "3 finding specifically -- filtered to the criterion-3-prefixed "
      "line, never a bare substring test, since every fixture here is "
      "untracked and criterion 2 always emits its own unrelated "
      "'SAFETY.md is present ... not tracked' finding regardless of what "
      "criterion 3 finds (Safety Officer advisory, attempt 2)",
      bool(_ri_prose_fence_c3_findings),
      f"exit={_ri_rc}; criterion 3 FINDING lines: {_ri_prose_fence_c3_findings}; "
      f"full output: {_ri_out!r}")

# (vi-b) boundary-pin/ -- criterion 3's exact boundary (close-integrity-
# guard-bundle, period 1 attempt 2, criterion 3's own revision note): a
# directory dated EXACTLY one day after the corrected
# SAFETY_FENCE_EFFECTIVE_DATE pin (2026-08-03, vs. prose-fence/'s safely
# eight-days-later 2026-08-10 above) is IN SCOPE, and its prose-only
# SAFETY.md (no genuine fence at all) is flagged -- the boundary the
# previous attempt never tested.
_ri_boundary_dir = _RI_FIXTURES_ROOT / "boundary-pin" / "2026-08-03-boundary-pin"
_ri_rc, _ri_out = _ri_run(_ri_boundary_dir)
_ri_boundary_c3_findings = [
    ln for ln in _ri_out.splitlines() if ln.startswith("criterion 3: FINDING")
]
check("record integrity: boundary-pin/ -- a directory dated exactly one "
      "day after SAFETY_FENCE_EFFECTIVE_DATE is in scope (criterion 3's "
      "own 'in scope' line) and produces a criterion-3-prefixed finding "
      "specifically, not merely criterion 2's untracked-fixture noise "
      "(Safety Officer advisory, attempt 2 -- this case is what actually "
      "discriminates the pin fix: reverting the pin to the prior "
      "off-by-one value makes this case's 'in scope' conjunct false)",
      "in scope" in _ri_out and bool(_ri_boundary_c3_findings),
      f"exit={_ri_rc}; criterion 3 FINDING lines: {_ri_boundary_c3_findings}; "
      f"full output: {_ri_out!r}")

_ri_real_dir = REPO / ".dcs" / "incidents" / "2026-08-02-record-integrity-corrections"
_ri_real_rc, _ri_real_out = _ri_run(_ri_real_dir)
check("record integrity: the REAL record-integrity-corrections/ "
      "(2026-08-02, on-the-pin) exits clean -- S1's own evidence contract "
      "for this exact fixture (204-TASKING/S1.md) requires exit 0, which "
      "in particular means its SAFETY.md line 33 naive-substring trap "
      "('```json' inside prose about the ABSENCE of fences) is not "
      "flagged as a genuine fence",
      _ri_real_rc == 0,
      f"exit={_ri_real_rc}; output: {_ri_real_out!r}")

# (vii) in-memory proofs for criteria 4 and 5 -- git stores neither an
# untracked file nor a corrupt commit message, so these are pure-function
# calls against synthetic text, never a fixture/file/git touch (T3).
if ri is None or not hasattr(ri, "clean_tree_findings"):
    _ri_reason = (f"record_integrity.py not importable yet (S1 has not "
                   f"landed): {_ri_import_error!r}") if ri is None else (
                   "module has no clean_tree_findings attribute")
    check("record integrity in-memory proof: clean_tree_findings(<non-"
          "empty porcelain>, label) is a non-empty finding list",
          False, _ri_reason)
    check("record integrity in-memory proof: clean_tree_findings('', "
          "label) is an empty finding list",
          False, _ri_reason)
else:
    _ri_dirty_porcelain = " M tests/fixtures/record-integrity/example.md\n?? tests/fixtures/record-integrity/new.md\n"
    try:
        _ri_dirty_findings = ri.clean_tree_findings(_ri_dirty_porcelain, "fixture-check")
        check("record integrity in-memory proof: clean_tree_findings(<non-"
              "empty porcelain>, label) is a non-empty finding list",
              bool(_ri_dirty_findings), f"result: {_ri_dirty_findings!r}")
    except Exception as _ri_exc:
        check("record integrity in-memory proof: clean_tree_findings(<non-"
              "empty porcelain>, label) is a non-empty finding list",
              False, f"raised {_ri_exc!r}")
    try:
        _ri_clean_findings = ri.clean_tree_findings("", "fixture-check")
        check("record integrity in-memory proof: clean_tree_findings('', "
              "label) is an empty finding list",
              not _ri_clean_findings, f"result: {_ri_clean_findings!r}")
    except Exception as _ri_exc:
        check("record integrity in-memory proof: clean_tree_findings('', "
              "label) is an empty finding list",
              False, f"raised {_ri_exc!r}")

if ri is None or not hasattr(ri, "degenerate_message_findings"):
    _ri_reason = (f"record_integrity.py not importable yet (S1 has not "
                   f"landed): {_ri_import_error!r}") if ri is None else (
                   "module has no degenerate_message_findings attribute")
    check("record integrity in-memory proof: degenerate_message_findings"
          "([<message with a bare @ line>]) is a non-empty finding list",
          False, _ri_reason)
    check("record integrity in-memory proof: degenerate_message_findings"
          "([<message without a bare @ line>]) is an empty finding list",
          False, _ri_reason)
else:
    # degenerate_message_findings() takes a list of (commit_ref,
    # message_text) PAIRS, per its own docstring -- not bare message
    # strings; commit_ref lets several checked commits stay
    # distinguishable in its own finding text.
    _ri_bad_message = "Fix the record-integrity fixture\n\n@\n"
    try:
        _ri_bad_findings = ri.degenerate_message_findings(
            [("deadbeef1", _ri_bad_message)])
        check("record integrity in-memory proof: degenerate_message_"
              "findings([(ref, <message with a bare @ line>)]) is a "
              "non-empty finding list",
              bool(_ri_bad_findings), f"result: {_ri_bad_findings!r}")
    except Exception as _ri_exc:
        check("record integrity in-memory proof: degenerate_message_"
              "findings([(ref, <message with a bare @ line>)]) is a "
              "non-empty finding list",
              False, f"raised {_ri_exc!r}")
    _ri_good_message = "Fix the record-integrity fixture\n\nDetails about the fix, no bare @ line.\n"
    try:
        _ri_good_findings = ri.degenerate_message_findings(
            [("deadbeef2", _ri_good_message)])
        check("record integrity in-memory proof: degenerate_message_"
              "findings([(ref, <message without a bare @ line>)]) is an "
              "empty finding list",
              not _ri_good_findings, f"result: {_ri_good_findings!r}")
    except Exception as _ri_exc:
        check("record integrity in-memory proof: degenerate_message_"
              "findings([(ref, <message without a bare @ line>)]) is an "
              "empty finding list",
              False, f"raised {_ri_exc!r}")

# (viii) carrier cases -- constants read from the IMPORTED module, never
# retyped as literals here (T5). If a carrier is red because S3 or S4 has
# not landed yet, it is reported RED BY NAME below, never described as
# "expected to pass later" (section 22 case (vi)'s convention).
if ri is None or not hasattr(ri, "INVOCATION"):
    _ri_reason = (f"record_integrity.py not importable yet (S1 has not "
                   f"landed): {_ri_import_error!r}") if ri is None else (
                   "module has no INVOCATION attribute")
    check("record integrity carrier: INVOCATION (from the imported "
          "module) appears in dcs/workflows/close.md, whitespace-"
          "collapsed",
          False, _ri_reason)
else:
    _close_text = read("dcs/workflows/close.md")
    check("record integrity carrier: INVOCATION (from the imported "
          "module) appears in dcs/workflows/close.md, whitespace-"
          "collapsed",
          _ws_norm(ri.INVOCATION) in _ws_norm(_close_text),
          f"INVOCATION: {ri.INVOCATION!r}")


def _ri_find_artifact_set(mod):
    """Discover S1's canonical-9-artifact-set constant by SHAPE (a
    module-level list/tuple of exactly nine strings) rather than by a
    guessed literal attribute name -- S1's tasking (204-TASKING/S1.md)
    names the constant's CONTENT (the nine filenames, in order) but not
    a Python attribute name, and this file must never retype those nine
    strings as literals (T5). Returns a list of (name, tuple(values))
    candidates; the carrier case below reports ambiguity (more than one
    match) or absence (zero matches) as its own named red case rather
    than guessing wrong and misreporting what is actually missing."""
    found = []
    for name in dir(mod):
        if name.startswith("_"):
            continue
        val = getattr(mod, name)
        if (isinstance(val, (list, tuple)) and len(val) == 9
                and all(isinstance(x, str) for x in val)):
            found.append((name, tuple(val)))
    return found


if ri is None:
    check("record integrity carrier: S1's module exports exactly one "
          "9-entry string constant (the canonical artifact set), "
          "discovered by shape rather than a guessed name",
          False, f"record_integrity.py not importable yet (S1 has not "
          f"landed): {_ri_import_error!r}")
    _ri_artifact_set = None
else:
    _ri_artifact_candidates = _ri_find_artifact_set(ri)
    check("record integrity carrier: S1's module exports exactly one "
          "9-entry string constant (the canonical artifact set), "
          "discovered by shape rather than a guessed name",
          len(_ri_artifact_candidates) == 1,
          f"candidates found by shape: {[n for n, _ in _ri_artifact_candidates]!r}")
    _ri_artifact_set = (
        _ri_artifact_candidates[0][1] if len(_ri_artifact_candidates) == 1 else None)

if _ri_artifact_set is None:
    check("record integrity carrier: every entry of S1's 9-artifact set "
          "appears in dcs/references/forms.md, and forms.md states the "
          "count as 9",
          False, "no single 9-entry artifact-set constant resolved above")
else:
    _forms_text = read("dcs/references/forms.md")
    _ri_missing_entries = [e for e in _ri_artifact_set if e not in _forms_text]
    _ri_states_nine = bool(re.search(r"\b9\s+files\b", _forms_text)) or bool(
        re.search(r"artifact set is 9\b", _forms_text, re.I))
    check("record integrity carrier: every entry of S1's 9-artifact set "
          "appears in dcs/references/forms.md, and forms.md states the "
          "count as 9",
          not _ri_missing_entries and _ri_states_nine,
          f"artifact set: {_ri_artifact_set!r}; missing from forms.md: "
          f"{_ri_missing_entries}; states count as 9: {_ri_states_nine}")

# (ix) field half (informational, criterion 7): how many of this repo's
# OWN incident directories are in scope for S1's SAFETY-fence pin
# (SAFETY_FENCE_EFFECTIVE_DATE, read from the imported module -- never
# retyped -- so this number tracks S1's actual pin even if it diverges
# from _NE_EFFECTIVE_DATE above in the future, per T4). Reuses
# _ne_all_dirs/_ne_dir_in_scope from check 9's own generalization above
# rather than re-deriving the incident-directory walk. A print, not a
# check(): informational only, never a blocking historical sweep.
if ri is not None and hasattr(ri, "SAFETY_FENCE_EFFECTIVE_DATE"):
    _ri_field_pin = ri.SAFETY_FENCE_EFFECTIVE_DATE
    _ri_field_in_scope = [
        d for d in _ne_all_dirs if _ne_dir_in_scope(d.name, pin=_ri_field_pin)
    ]
    print(
        f"\nrecord integrity field half (informational, criterion 7): "
        f"{len(_ri_field_in_scope)} of this repo's own incident "
        f"director{'y' if len(_ri_field_in_scope) == 1 else 'ies'} in "
        f"scope by S1's SAFETY_FENCE_EFFECTIVE_DATE pin ({_ri_field_pin})"
    )
else:
    print(
        "\nrecord integrity field half (informational, criterion 7): 0 "
        "-- record_integrity.py not importable yet (S1 has not landed), "
        "so SAFETY_FENCE_EFFECTIVE_DATE cannot be resolved"
    )

# --- 24. verdict-rerun mechanism (independence-fail-closed-and-model-floor,
# criteria 4/8(a)) ------------------------------------------------------
# `dcs/tools/verdict_rerun.py` (S4's own territory this incident) is the
# close-time check that selects one SAFETY.md `checked[]` entry by a
# printed stability rule and asserts CONTAINMENT (never byte equality)
# of its recorded observation in the fresh re-run output --
# `dcs/workflows/close.md` step 1c runs it unconditionally, fail-closed
# on exit 1/2, exactly like check 23's record_integrity.py and check
# 22's preservation_map.py. Imported via the SAME
# `importlib.util.spec_from_file_location` idiom those two checks use,
# never re-implemented here (T1). Guarded like check 23's import: a
# crashed import must never abort this whole script before its final
# "N/M passed" line prints.
_vr_path = REPO / "dcs" / "tools" / "verdict_rerun.py"
_vr_import_error = None
try:
    _vr_spec = importlib.util.spec_from_file_location("verdict_rerun", _vr_path)
    vr = importlib.util.module_from_spec(_vr_spec)
    _vr_spec.loader.exec_module(vr)
except Exception as _vr_exc:  # noqa: broad on purpose -- see comment above
    vr = None
    _vr_import_error = _vr_exc

check("verdict-rerun: dcs/tools/verdict_rerun.py imports cleanly",
      vr is not None, f"{_vr_import_error!r}" if _vr_import_error else "")

_VR_FIXTURES_ROOT = REPO / "tests" / "fixtures" / "verdict-rerun"
_VR_SCENARIOS = ("reproduces", "non-reproducing", "all-non-reproducible", "fence-robustness")

# (i) degeneracy guard: without a non-empty fixture population covering
# every named scenario, every case below would pass vacuously.
_vr_scenario_dirs = (
    {p.name for p in _VR_FIXTURES_ROOT.iterdir() if p.is_dir()}
    if _VR_FIXTURES_ROOT.is_dir() else set()
)
check("verdict-rerun: fixture population is non-empty and covers all "
      "named scenarios (degeneracy guard -- without it every case below "
      "passes vacuously)",
      _VR_FIXTURES_ROOT.is_dir() and set(_VR_SCENARIOS) <= _vr_scenario_dirs,
      f"found scenario dirs under {_VR_FIXTURES_ROOT}: {sorted(_vr_scenario_dirs)}")


def _vr_run(incident_dir):
    """Invoke verdict_rerun.py as a subprocess against `incident_dir` --
    the real CLI entry point, mirroring check 23's own `_ri_run` shape,
    so this exercises main()'s argument parsing and exit-code contract,
    not just the imported functions."""
    proc = subprocess.run(
        [sys.executable, str(_vr_path), str(incident_dir)],
        cwd=REPO, capture_output=True, text=True,
        encoding="utf-8", errors="replace")
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


# (ii) reproduces/ -- two entries correctly skipped (a working-tree
# git-diff, then unparseable prose), then a genuine, allowlisted entry
# re-runs and its recorded observation is contained in the fresh output
# -- exit 0.
_vr_rc, _vr_out = _vr_run(_VR_FIXTURES_ROOT / "reproduces")
check("verdict-rerun: reproduces/ -- a genuine checked[] entry re-runs "
      "and its recorded observation is contained in the fresh output "
      "-- exit 0",
      _vr_rc == 0 and "reproduces cleanly" in _vr_out,
      f"exit={_vr_rc}; output: {_vr_out!r}")

# (iii) non-reproducing/ -- a real, allowlisted, selected entry whose
# recorded observation is NOT contained in the fresh output -- exit 1,
# finding names the selected entry (checked[1]) by index and command.
_vr_rc, _vr_out = _vr_run(_VR_FIXTURES_ROOT / "non-reproducing")
_vr_nonrepro_finding = [
    ln for ln in _vr_out.splitlines()
    if ln.startswith("verdict-rerun: FINDING") and "checked[1]" in ln
]
check("verdict-rerun: non-reproducing/ -- a selected entry that re-runs "
      "but whose recorded observation is NOT contained in the fresh "
      "output is exit 1, with a finding naming checked[1] by index and "
      "command",
      _vr_rc == 1 and bool(_vr_nonrepro_finding),
      f"exit={_vr_rc}; FINDING lines naming checked[1]: "
      f"{_vr_nonrepro_finding}; full output: {_vr_out!r}")

# (iv) all-non-reproducible/ -- every entry is non-reproducible BY
# DESIGN (a working-tree diff, unparseable prose, no em dash at all) --
# design point (iii): a FINDING, never a silent exit 0.
_vr_rc, _vr_out = _vr_run(_VR_FIXTURES_ROOT / "all-non-reproducible")
check("verdict-rerun: all-non-reproducible/ -- every checked[] entry is "
      "non-reproducible by design -- a FINDING ('no stable entry "
      "found'), never a silent exit 0 (design point (iii))",
      _vr_rc == 1 and "no stable, re-runnable checked[] entry found" in _vr_out,
      f"exit={_vr_rc}; output: {_vr_out!r}")

# (v) fence-robustness/ -- an inline, single-backtick "```json" mention
# inside running prose (record_integrity.py:683-692's own documented
# counterexample) must NOT be mistaken for a fence delimiter; the one
# genuine fence elsewhere in the same file must still be found and its
# one reproducing entry selected -- exit 0.
_vr_rc, _vr_out = _vr_run(_VR_FIXTURES_ROOT / "fence-robustness")
check("verdict-rerun: fence-robustness/ -- an inline '```json' mention "
      "inside prose (never at a physical line's own start) is not "
      "mistaken for a fence delimiter; the genuine fence elsewhere in "
      "the file is found and its reproducing entry re-runs -- exit 0",
      _vr_rc == 0 and "fence-robustness probe" in _vr_out,
      f"exit={_vr_rc}; output: {_vr_out!r}")

# (vi) in-memory proofs of the pure comparator functions -- same
# rationale as check 23(vii): git/subprocess state (a working-tree
# diff, a timed-out command) is not fixture-friendly, so these exercise
# the functions directly.
if vr is None:
    check("verdict-rerun in-memory proof: split_checked_entry() on an "
          "entry with no em dash returns (None, None)",
          False, f"verdict_rerun.py not importable: {_vr_import_error!r}")
    check("verdict-rerun in-memory proof: is_working_tree_diff() "
          "distinguishes a bare `git diff` from one carrying a "
          "commit-ish argument",
          False, f"verdict_rerun.py not importable: {_vr_import_error!r}")
    check("verdict-rerun in-memory proof: looks_like_command() refuses "
          "prose and an unbalanced quote, accepts an allowlisted command",
          False, f"verdict_rerun.py not importable: {_vr_import_error!r}")
else:
    check("verdict-rerun in-memory proof: split_checked_entry() on an "
          "entry with no em dash returns (None, None)",
          vr.split_checked_entry("no dash here at all") == (None, None),
          f"result: {vr.split_checked_entry('no dash here at all')!r}")
    _vr_bare_diff = vr.is_working_tree_diff("git diff some_file.py")
    _vr_sha_diff = vr.is_working_tree_diff("git diff --stat 48ea59a")
    check("verdict-rerun in-memory proof: is_working_tree_diff() "
          "distinguishes a bare `git diff` (True -- skip) from one "
          "carrying a commit-ish argument (False -- eligible)",
          _vr_bare_diff is True and _vr_sha_diff is False,
          f"bare: {_vr_bare_diff!r}; with sha: {_vr_sha_diff!r}")
    _vr_prose_cmd = vr.looks_like_command("repro of 201 path")
    _vr_unbalanced_cmd = vr.looks_like_command('python -c "unterminated')
    _vr_real_cmd = vr.looks_like_command("git status")
    check("verdict-rerun in-memory proof: looks_like_command() refuses "
          "prose and an unbalanced quote, accepts an allowlisted command",
          _vr_prose_cmd is False and _vr_unbalanced_cmd is False and _vr_real_cmd is True,
          f"prose: {_vr_prose_cmd!r}; unbalanced: {_vr_unbalanced_cmd!r}; "
          f"real: {_vr_real_cmd!r}")

# (vii) carrier case -- INVOCATION, read from the imported module (never
# retyped as a literal here, T5), must appear in dcs/workflows/close.md
# whitespace-collapsed -- same idiom as checks 22(vi)/23(viii).
if vr is None or not hasattr(vr, "INVOCATION"):
    check("verdict-rerun carrier: INVOCATION (from the imported module) "
          "appears in dcs/workflows/close.md, whitespace-collapsed",
          False, f"verdict_rerun.py not importable or has no INVOCATION: "
          f"{_vr_import_error!r}")
else:
    _vr_close_text = read("dcs/workflows/close.md")
    check("verdict-rerun carrier: INVOCATION (from the imported module) "
          "appears in dcs/workflows/close.md, whitespace-collapsed",
          _ws_norm(vr.INVOCATION) in _ws_norm(_vr_close_text),
          f"INVOCATION: {vr.INVOCATION!r}")


# --- 25. model-gate coverage (independence-fail-closed-and-model-floor,
# criterion 7/8(b)) ------------------------------------------------------
# Criterion 7: every existing read site for `auto_approve_type3` /
# `deploy.auto` / `deploy.auto_after_close` must be updated so the bound
# holds only when the session's current operating model appears in
# `approved_models` (the model floor). The ORIGINAL plan's coverage-check
# design (derive the site population from the three literal bound-key
# substrings alone) was REJECTED by dcs-commander at command point 2,
# first pass, precisely because it would silently miss deploy.md's own
# site, whose real phrasing (deploy.md:117-124) is "a `deploy` object
# with `auto: true`" -- containing NO literal bound-key substring at all
# (measured, confirmed by direct grep: zero class-A hits on that
# sentence). This check's population is therefore DISCOVERED from TWO
# named phrasing classes (IAP tactic T7), never from the bound-key
# substrings alone, and never hardcodes "9 sites" anywhere below (IAP
# tactic T11, doctrine principle 15) -- it asserts the INVARIANT (both
# classes non-empty, every discovered site gated), never the instance.
#
# Corpus scope (dcs-commander's second-pass review, non-blocking
# observation, directly this check's own): scoped to dcs/workflows/*.md
# specifically, via workflows() (already defined above, never a second
# enumerator) -- a broader corpus would self-announce red on
# definitional class-A matches inside schemas.md's own JSON example and
# templates/DELEGATION.md, which discuss these bound keys without
# needing a model gate of their own.

# CLASS A -- literal bound key: any of the three substrings, matched as
# a single alternation over the WHOLE file text (never per-line) so
# line-number recovery (counting "\n" before the match start) is the
# ONE shared primitive both classes use -- see _mg_sites() below. These
# three substrings can legitimately overlap in one physical span (e.g.
# "deploy.auto_after_close" contains both "deploy.auto" and
# "auto_after_close"); alternation + non-overlapping finditer already
# collapses that into ONE match, never a double-count, because the
# leftmost alternative that matches first consumes the span.
_MG_CLASS_A_KEYS = ("auto_approve_type3", "auto_after_close", "deploy.auto")
_MG_CLASS_A_RE = re.compile("|".join(re.escape(k) for k in _MG_CLASS_A_KEYS))

# CLASS B -- deploy-object phrasing: deploy.md:117-124's own wording, "a
# `deploy` object with `auto: true`" -- contains NO literal class-A
# substring (non-vacuity case (iv) below proves this against the SAME
# predicate the real walk uses). `\s+` between tokens already matches a
# markdown hard-wrap's own newline (Python's \s includes \n), so this
# needs no separate line-joining step to survive deploy.md wrapping the
# phrase across two physical lines.
_MG_CLASS_B_RE = re.compile(r"`deploy`\s+object\s+with\s+`auto:\s*true`", re.I)

# The literal model-gate token, and how far away (in LINES, in the same
# file) it may sit from a matched site and still count as "co-located".
# Chosen generously against every site's OWN measured span in this
# incident's 202-OBJECTIVES.md criterion 7 (the widest, loop.md:28-38,
# is 11 lines; plan.md's step-6 block separates its `auto_approve_type3`
# bullet from the paragraph stating the model-floor rule by 2-4 lines) --
# wide enough that a model gate written as its own adjacent bullet or
# sentence is still found, narrow enough that "co-located" remains a
# real, bounded claim rather than "anywhere in the file".
_MG_GATE_TOKEN = "approved_models"
_MG_GATE_WINDOW_LINES = 20


def _mg_sites(text, pattern):
    """(line_no, matched_text) for every regex match in `text`, with
    line_no computed by counting newlines before the match start -- the
    ONE shared primitive both phrasing classes' site discovery uses.
    Class A (three literal, single-token substrings, immune to a
    markdown hard-wrap by construction -- none contains internal
    whitespace) and class B (a multi-word phrase whose own `\\s+` joints
    already span a hard-wrapped newline) are found the identical way, by
    the SAME function, so neither gets a bespoke, separately-drifting
    matcher."""
    return [
        (text.count("\n", 0, m.start()) + 1, _ws_norm(m.group(0)))
        for m in pattern.finditer(text)
    ]


def _mg_class_a_hit(text):
    """The class-A predicate, standalone -- used both by the real walk
    (via _mg_sites) and by the non-vacuity proof below, so both call
    the SAME compiled pattern rather than a parallel re-implementation."""
    return bool(_MG_CLASS_A_RE.search(text))


def _mg_class_b_hit(text):
    """The class-B predicate, standalone -- same rationale as
    _mg_class_a_hit."""
    return bool(_MG_CLASS_B_RE.search(text))


def _mg_gate_nearby(file_lines, line_no, window=_MG_GATE_WINDOW_LINES):
    """True iff `_MG_GATE_TOKEN` occurs on some line within `window`
    lines either side of `line_no` (1-indexed) in `file_lines` -- the
    ONE co-location predicate both the real per-site cases and the
    in-memory liveness proof below call, so neither drifts from the
    other."""
    lo = max(0, line_no - 1 - window)
    hi = min(len(file_lines), line_no + window)
    return any(_MG_GATE_TOKEN in ln for ln in file_lines[lo:hi])


_mg_workflow_files = workflows()
_mg_file_lines = {}
_mg_file_text = {}
for _mg_p in _mg_workflow_files:
    _mg_rel = str(_mg_p.relative_to(REPO)).replace("\\", "/")
    _mg_text = _mg_p.read_text(encoding="utf-8")
    _mg_file_text[_mg_rel] = _mg_text
    _mg_file_lines[_mg_rel] = _mg_text.splitlines()

_mg_sites_a = []
_mg_sites_b = []
for _mg_rel, _mg_text in _mg_file_text.items():
    _mg_seen_a, _mg_seen_b = set(), set()
    for _mg_line_no, _mg_snippet in _mg_sites(_mg_text, _MG_CLASS_A_RE):
        if _mg_line_no in _mg_seen_a:
            continue
        _mg_seen_a.add(_mg_line_no)
        _mg_sites_a.append((_mg_rel, _mg_line_no, _mg_snippet))
    for _mg_line_no, _mg_snippet in _mg_sites(_mg_text, _MG_CLASS_B_RE):
        if _mg_line_no in _mg_seen_b:
            continue
        _mg_seen_b.add(_mg_line_no)
        _mg_sites_b.append((_mg_rel, _mg_line_no, _mg_snippet))
_mg_sites_a.sort()
_mg_sites_b.sort()

# (iii) PER-CLASS INVENTORY, printed at run time -- class name, matched
# count, every file:line -- so the evidence discloses WHICH phrasing
# classes actually matched, not merely that the check passed.
print(
    f"\nmodel-gate coverage (criterion 7): CLASS A (literal bound key: "
    f"{', '.join(_MG_CLASS_A_KEYS)}) -- {len(_mg_sites_a)} matched site(s):"
)
for _mg_rel, _mg_line_no, _mg_snippet in _mg_sites_a:
    print(f"  {_mg_rel}:{_mg_line_no}")
print(
    f"model-gate coverage (criterion 7): CLASS B (deploy-object "
    f"phrasing: \"a `deploy` object with `auto: true`\") -- "
    f"{len(_mg_sites_b)} matched site(s):"
)
for _mg_rel, _mg_line_no, _mg_snippet in _mg_sites_b:
    print(f"  {_mg_rel}:{_mg_line_no}")

# (i) PER CLASS, its matched-site population is non-empty, as its OWN
# named case -- an empty class is a FAILURE, never a silently skipped
# loop.
check("model-gate coverage: CLASS A (literal bound key) matched-site "
      "population is non-empty",
      bool(_mg_sites_a), f"matched sites: {_mg_sites_a!r}")
check("model-gate coverage: CLASS B (deploy-object phrasing) "
      "matched-site population is non-empty",
      bool(_mg_sites_b), f"matched sites: {_mg_sites_b!r}")

# (ii) per site, one named case each carrying file:line: a model gate
# (the literal `approved_models`) is co-located with it -- so a
# bound-read site added by a later incident fails BY NAME.
for _mg_rel, _mg_line_no, _mg_snippet in _mg_sites_a:
    _mg_gated = _mg_gate_nearby(_mg_file_lines[_mg_rel], _mg_line_no)
    check(f"model-gate coverage: {_mg_rel}:{_mg_line_no} (CLASS A: "
          f"literal bound key) has a co-located `approved_models` "
          f"model gate within {_MG_GATE_WINDOW_LINES} lines",
          _mg_gated, f"matched text: {_mg_snippet!r}")
for _mg_rel, _mg_line_no, _mg_snippet in _mg_sites_b:
    _mg_gated = _mg_gate_nearby(_mg_file_lines[_mg_rel], _mg_line_no)
    check(f"model-gate coverage: {_mg_rel}:{_mg_line_no} (CLASS B: "
          f"deploy-object phrasing) has a co-located `approved_models` "
          f"model gate within {_MG_GATE_WINDOW_LINES} lines",
          _mg_gated, f"matched text: {_mg_snippet!r}")

# (iv) NON-VACUITY proof, calling the SAME predicates the real walk uses
# (idiom of check 9's _ne_finding / the load-bearing-term census's
# _term_found) on SYNTHETIC input: deploy.md's own deploy-object
# sentence must return True under the class-B matcher AND False under
# the class-A matcher -- proving class B is load-bearing and not
# shadowed by class A.
_MG_SYNTHETIC_DEPLOY_SENTENCE = (
    "If it has a `deploy` object with `auto: true`, evaluate every row "
    "about to ship against its bounds."
)
check("model-gate coverage non-vacuity: deploy.md's own deploy-object "
      "phrasing (synthetic, mirroring deploy.md:117-124's real wording) "
      "returns True under the CLASS-B predicate (the same predicate the "
      "real walk uses)",
      _mg_class_b_hit(_MG_SYNTHETIC_DEPLOY_SENTENCE) is True,
      f"_mg_class_b_hit(...) = {_mg_class_b_hit(_MG_SYNTHETIC_DEPLOY_SENTENCE)!r}")
check("model-gate coverage non-vacuity: the SAME synthetic sentence "
      "returns False under the CLASS-A predicate -- proving class B is "
      "load-bearing, not shadowed by class A",
      _mg_class_a_hit(_MG_SYNTHETIC_DEPLOY_SENTENCE) is False,
      f"_mg_class_a_hit(...) = {_mg_class_a_hit(_MG_SYNTHETIC_DEPLOY_SENTENCE)!r}")

# PER-CLASS LIVENESS PROBE -- SUBSTITUTED, deliberately, from the
# tasking's literal "edit dcs/workflows/deploy.md on disk, `git checkout
# --` to restore" procedure. Full rationale (also in this specialist's
# final report): dcs/workflows/** is S4's hard forbidden zone with zero
# discretion, and S1/S2/S3 are concurrently editing these exact six
# files in this SAME shared worktree right now -- a `git checkout --
# <file>` revert step carries a real, concrete risk of discarding a
# sibling's uncommitted work mid-flight, a risk no "check it's clean
# first" fully closes (a sibling can write between the check and the
# revert). This in-memory proof instead exercises the IDENTICAL
# predicate (_mg_gate_nearby) the real per-site cases above call,
# against a COPY of one real site's own surrounding lines with
# `approved_models` deleted -- proving the SAME mechanism that gates the
# real walk goes red when a gate is absent, by name and by class, with
# NO disk write to dcs/workflows/** at all (same idiom as checks
# 13(f)/14(e)/15's Rule-A negative proof/18(f)/22(v)'s in-memory
# forgeries). Class B's forged target is asserted to be
# dcs/workflows/deploy.md specifically -- MANDATORY per this incident's
# own tasking.
if _mg_sites_a:
    _mg_forge_rel, _mg_forge_line, _ = _mg_sites_a[0]
    _mg_forged_lines = [
        ln.replace(_MG_GATE_TOKEN, "REDACTED") for ln in _mg_file_lines[_mg_forge_rel]
    ]
    _mg_forged_gated = _mg_gate_nearby(_mg_forged_lines, _mg_forge_line)
    check(f"model-gate coverage liveness proof (CLASS A, target "
          f"{_mg_forge_rel}:{_mg_forge_line}): deleting `approved_models` "
          "from an IN-MEMORY copy of the file (dcs/workflows/** stays "
          "untouched on disk) is caught by the SAME predicate "
          "(_mg_gate_nearby) the real per-site cases call",
          _mg_forged_gated is False, f"gated after forging: {_mg_forged_gated!r}")
else:
    check("model-gate coverage liveness proof: a CLASS A site exists to "
          "forge against",
          False, "_mg_sites_a is empty")

if _mg_sites_b:
    _mg_forge_rel_b, _mg_forge_line_b, _ = _mg_sites_b[0]
    _mg_forged_lines_b = [
        ln.replace(_MG_GATE_TOKEN, "REDACTED") for ln in _mg_file_lines[_mg_forge_rel_b]
    ]
    _mg_forged_gated_b = _mg_gate_nearby(_mg_forged_lines_b, _mg_forge_line_b)
    check(f"model-gate coverage liveness proof (CLASS B, MANDATORY "
          f"target {_mg_forge_rel_b}:{_mg_forge_line_b}): deleting "
          "`approved_models` from an IN-MEMORY copy of the file "
          "(dcs/workflows/** stays untouched on disk) is caught by the "
          "SAME predicate (_mg_gate_nearby) the real per-site cases call",
          _mg_forged_gated_b is False, f"gated after forging: {_mg_forged_gated_b!r}")
    check("model-gate coverage liveness proof: CLASS B's forged target "
          "is dcs/workflows/deploy.md (mandatory per this incident's "
          "own tasking)",
          _mg_forge_rel_b == "dcs/workflows/deploy.md",
          f"actual target: {_mg_forge_rel_b!r}")
else:
    check("model-gate coverage liveness proof: a CLASS B site exists to "
          "forge against",
          False, "_mg_sites_b is empty")


# --- 26. criterion 2 coverage (independence-fail-closed-and-model-floor,
# Planning Chief's accepted feedback item 2) -----------------------------
# 202-OBJECTIVES.md criterion 2: when independent Safety Officer spawn
# cannot be established, dcs/workflows/close.md refuses to complete an
# unattended close this period -- it either PARKs the incident (register
# row state `PARKED`) or routes to the Owner via `AskUserQuestion`,
# BEFORE the merge step. This case asserts both sanctioned dispositions
# are named, and that they sit before the merge step, so a later edit
# deleting either fails by name -- S3's territory (close.md), read here
# by content, never a hardcoded line number.
_c2cov_close_text = read("dcs/workflows/close.md")
_C2COV_MERGE_MARKER_RE = re.compile(r"Merge into the integration branch", re.I)
_C2COV_UNATTENDED_RE = re.compile(r"\bunattended\b", re.I)
_C2COV_PARKED_RE = re.compile(r"`?PARKED`?")
_C2COV_ASKUSERQUESTION_RE = re.compile(r"AskUserQuestion")

_c2cov_merge_m = _C2COV_MERGE_MARKER_RE.search(_c2cov_close_text)
check("criterion 2 coverage: close.md names its merge step (\"Merge "
      "into the integration branch\") by content, discovered at run "
      "time, never a hardcoded step number",
      bool(_c2cov_merge_m),
      "no 'Merge into the integration branch' text found in "
      "dcs/workflows/close.md")

if _c2cov_merge_m is None:
    check("criterion 2 coverage: close.md's unattended-close gate names "
          "BOTH sanctioned dispositions (a PARKED register-row state "
          "and an AskUserQuestion route) before the merge step",
          False,
          "cannot scope 'before the merge step' -- no merge marker found")
else:
    _c2cov_unattended_m = _C2COV_UNATTENDED_RE.search(
        _c2cov_close_text, 0, _c2cov_merge_m.start())
    check("criterion 2 coverage: close.md's unattended-close gate (the "
          "word 'unattended') appears before the merge step",
          bool(_c2cov_unattended_m),
          f"no 'unattended' text found in close.md before offset "
          f"{_c2cov_merge_m.start()} (the merge marker)")
    if _c2cov_unattended_m is None:
        check("criterion 2 coverage: close.md's unattended-close gate "
              "names BOTH sanctioned dispositions (a PARKED "
              "register-row state and an AskUserQuestion route) before "
              "the merge step",
              False,
              "no 'unattended' text found before the merge step -- "
              "cannot scope the region to check")
    else:
        _c2cov_region = _c2cov_close_text[
            _c2cov_unattended_m.start():_c2cov_merge_m.start()]
        _c2cov_parked_in_region = bool(_C2COV_PARKED_RE.search(_c2cov_region))
        _c2cov_ask_in_region = bool(_C2COV_ASKUSERQUESTION_RE.search(_c2cov_region))
        check("criterion 2 coverage: close.md's unattended-close gate "
              "names BOTH sanctioned dispositions -- a PARKED "
              "register-row state and an AskUserQuestion route -- "
              "between its own 'unattended' mention and the merge step, "
              "so a later edit deleting either fails by name",
              _c2cov_parked_in_region and _c2cov_ask_in_region,
              f"PARKED found in region: {_c2cov_parked_in_region}; "
              f"AskUserQuestion found in region: {_c2cov_ask_in_region}; "
              f"region: {_c2cov_region!r}")


# --- 27. criterion 3/6 schema-addition structural checks
# (independence-fail-closed-and-model-floor, criterion 9) ---------------
# 202-OBJECTIVES.md criterion 9: "if criteria 3/6's schema additions
# warrant a corresponding structural check ... that check is added now
# rather than left for a later incident to discover missing." Both
# additions are S1's territory (schemas.md, dcs/templates/DELEGATION.md);
# both are mechanised here by finding schemas.md's own section headings
# BY TITLE TEXT, reusing check 18's own `_sfc_section_starts` parse of
# schemas.md rather than re-deriving a second heading regex over the
# same source text -- same "parse the source of truth at run time"
# discipline as checks 13/14/15/18 above, since a section number is
# exactly the kind of derived fact that shifts if an earlier section is
# ever inserted or removed.
def _c9_section_body(text, section_starts, title_substring):
    """The body of the FIRST '## N. Title' section (from a pre-parsed
    `section_starts` list of re.Match objects over `text`) whose title
    contains `title_substring` (case-insensitive), up to the next
    heading -- discovered by TITLE TEXT, never a hardcoded section
    number. Returns None if no such heading exists."""
    for i, m in enumerate(section_starts):
        if title_substring.lower() in m.group(2).lower():
            end = (section_starts[i + 1].start()
                   if i + 1 < len(section_starts) else len(text))
            return text[m.start():end]
    return None


_c9_safety_section = _c9_section_body(
    schemas_md, _sfc_section_starts, "Safety-officer verdict")
check("criterion 3 structural check: schemas.md's Safety-officer "
      "verdict section is findable by title (never a hardcoded section "
      "number)",
      _c9_safety_section is not None,
      "no '## N. ...Safety-officer verdict...' heading found in "
      "schemas.md")
if _c9_safety_section is not None:
    check("criterion 3 structural check: schemas.md's Safety-officer "
          "verdict section states the `checked` field must be a "
          "'regenerable' command (criterion 3's own Verified clause, "
          "mechanised)",
          "regenerable" in _c9_safety_section.lower(),
          f"section body (first 400 chars): {_c9_safety_section[:400]!r}")

_c9_delegation_section = _c9_section_body(
    schemas_md, _sfc_section_starts, "Delegation bounds")
check("criterion 6 structural check: schemas.md's Delegation bounds "
      "section is findable by title (never a hardcoded section number)",
      _c9_delegation_section is not None,
      "no '## N. ...Delegation bounds...' heading found in schemas.md")
if _c9_delegation_section is not None:
    check("criterion 6 structural check: schemas.md's Delegation bounds "
          "section names the new `approved_models` field",
          "approved_models" in _c9_delegation_section,
          f"section body (first 400 chars): {_c9_delegation_section[:400]!r}")

_c9_delegation_tpl_path = REPO / "dcs" / "templates" / "DELEGATION.md"
if _c9_delegation_tpl_path.is_file():
    _c9_delegation_tpl_text = _c9_delegation_tpl_path.read_text(encoding="utf-8")
    check("criterion 6 structural check: dcs/templates/DELEGATION.md "
          "(the founding template) carries the new `approved_models` "
          "field",
          "approved_models" in _c9_delegation_tpl_text,
          "dcs/templates/DELEGATION.md does not contain 'approved_models'")
else:
    check("criterion 6 structural check: dcs/templates/DELEGATION.md "
          "exists",
          False, f"not found at {_c9_delegation_tpl_path}")

print(f"\n{checks - len(failures)}/{checks} passed")
sys.exit(1 if failures else 0)
