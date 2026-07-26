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

print(f"\n{checks - len(failures)}/{checks} passed")
sys.exit(1 if failures else 0)
