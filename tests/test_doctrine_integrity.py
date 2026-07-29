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
#   budget = math.ceil(38361/1024) = 38
#
# Regenerate with:
#   python -c "d=open('dcs/references/doctrine.md','rb').read().replace(b'\r\n', b'\n'); s=open('dcs/references/schemas.md','rb').read().replace(b'\r\n', b'\n'); print(len(d), len(s), len(d)+len(s))"
HOT_PATH_BUDGET_KB = 38

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
check("no Cyrillic anywhere in the shipped package", not mojibake,
      "; ".join(sorted(set(mojibake))))

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

# A "declaring place" is a candidate file with at least one paragraph where
# an advisory token AND a refutation/halt-verdict token co-occur -- the
# bounded window (d) requires. Measured at period start: four candidate
# files each carry only one of the two token classes, so a correct
# co-occurrence predicate captures none of them -- never special-cased by
# name here; the exclusion falls out of the predicate itself.
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
check("bar carrier: declaring-place set is non-empty and includes the "
      "charter itself",
      bool(_bar_declaring) and any(r == "agents/dcs-safety-officer.md" for r in _bar_declaring_rel),
      f"declaring places: {_bar_declaring_rel}")

_BAR_SURFACES = {
    "agents/": lambda r: r.startswith("agents/"),
    "dcs/references/": lambda r: r.startswith("dcs/references/"),
    "dcs/workflows/": lambda r: r.startswith("dcs/workflows/"),
}
_bar_surfaces_hit = [_bar_label for _bar_label, _bar_pred in _BAR_SURFACES.items()
                     if any(_bar_pred(r) for r in _bar_declaring_rel)]
check("bar carrier: declaring places span at least two of the three "
      "scanned surfaces",
      len(_bar_surfaces_hit) >= 2, f"surfaces hit: {_bar_surfaces_hit}")


def _bar_paragraph_problems(paragraph, expected_step, expected_bar_count, expected_token):
    """Every problem invariants 1/2/3 find in one qualifying paragraph,
    against the SUPPLIED expected values -- never a private
    re-derivation -- so the same function serves both the real comparator
    below and the forged-parse negative proof that follows it."""
    _problems = []
    _norm_para = _ws_norm(paragraph)
    for _cm in _BAR_CITE_RE.finditer(_norm_para):
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
    for _tm in _BAR_DEFAULT_TOKEN_RE.finditer(_norm_para):
        _tok = _tm.group(1) or _tm.group(2)
        if _tok != expected_token:
            _problems.append(
                f"states default verdict token `{_tok}`, charter states `{expected_token}`")
    return _problems


# (d) one named case per declaring place (idiom of checks 12(c)/13(d)): a
# missing or mismatched citation in a NEW declaring place fails by name,
# not folded into one aggregate.
for _bar_p in _bar_declaring:
    _bar_rel = str(_bar_p.relative_to(REPO)).replace("\\", "/")
    _bar_problems = []
    for _bar_para in _bar_declaring_paras[_bar_p]:
        _bar_problems += _bar_paragraph_problems(
            _bar_para, _bar_step_num, _bar_charter_count, _bar_charter_token)
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
    # 282 lines measured at incident worktree-removal-self-conflict
    # (2026-07-29), 32 over the 250-line policy ceiling. Documented,
    # temporary debt pending a follow-up trim -- not a bespoke permanent
    # ceiling for this file.
    'close.md': 283,
    # 282 lines measured at incident workflow-budget-enforcement
    # (2026-07-28), 32 over the 250-line policy ceiling. Documented,
    # temporary debt pending a follow-up trim.
    'deploy.md': 282,
    # 255 lines measured at incident prompt-vs-schema-drift
    # (2026-07-29), 5 over the 250-line policy ceiling. Documented,
    # temporary debt pending a follow-up trim.
    'new.md': 260,
    # 445 lines measured at incident prompt-vs-schema-drift
    # (2026-07-29), 195 over the 250-line policy ceiling. Documented,
    # temporary debt pending a follow-up trim.
    'execute.md': 450,
    # 682 lines measured at incident prompt-vs-schema-drift
    # (2026-07-29), 432 over the 250-line policy ceiling. Documented,
    # temporary debt pending a follow-up trim.
    'plan.md': 687,
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

print(f"\n{checks - len(failures)}/{checks} passed")
sys.exit(1 if failures else 0)
