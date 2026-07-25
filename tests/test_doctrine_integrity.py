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
  7. hot-path size budget (doctrine + schemas, read on every invocation)
  8. no BOM and no U+FFFD anywhere in the package

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
# The budget is set on the MERGE RESULT, not on either branch: that incident
# measured 36,717 B and derived 37, but schemas.md grew 1,189 B on main
# (6a57b97) while the incident was open, so the merged pair is 37,906 B and
# a 37 kB budget would have landed red. That is the whole reason this is
# re-derived here rather than carried across -- a size is a derived fact
# with a lifetime (doctrine principle 15), and this one expired between
# being measured and being merged.
#
#   budget = math.ceil(37906/1024) + 1 = 38
#
# Still a ratchet: it bites ~1.2 kB sooner than the 42 kB it replaces.
# Sizes are on-disk bytes, so a CRLF checkout measures one byte per line
# more than an LF one -- see vault/Backlog.md item 8. Regenerate with:
#   python -c "import os; d=os.path.getsize('dcs/references/doctrine.md'); s=os.path.getsize('dcs/references/schemas.md'); print(d, s, d+s)"
HOT_PATH_BUDGET_KB = 38

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
hot = os.path.getsize(REPO / "dcs" / "references" / "doctrine.md") + \
      os.path.getsize(REPO / "dcs" / "references" / "schemas.md")
check(f"hot-path budget: doctrine+schemas <= {HOT_PATH_BUDGET_KB} kB",
      hot <= HOT_PATH_BUDGET_KB * 1024, f"currently {hot/1024:.1f} kB")

# --- 8. encoding -----------------------------------------------------------
bad_enc = []
for p in REPO.rglob("*"):
    if p.is_file() and ".git" not in p.parts and "node_modules" not in p.parts:
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
    if ".git" in p.parts or "node_modules" in p.parts:
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

# --- 10. package.json stays small ------------------------------------------
pkg_bytes = os.path.getsize(REPO / "package.json")
check("package.json under 8 kB", pkg_bytes < 8 * 1024,
      f"currently {pkg_bytes:,} bytes — check for a field growing on each edit")

print(f"\n{checks - len(failures)}/{checks} passed")
sys.exit(1 if failures else 0)
