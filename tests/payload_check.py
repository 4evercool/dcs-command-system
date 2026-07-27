"""Payload witness: compares the DCS payload in this repo against an
installed copy, file by file, by sha256.

Why this exists (incident deploy-marker-blind, 201): the deployed-version
marker for this repo is ~/.claude/dcs/VERSION, a copy of dcs/VERSION the
installers carry inside the payload, so it only moves on a version-string
change. DCS permits shipping without a bump while a version is unpublished,
so a correct ship can leave the marker unchanged -- this has happened three
consecutive times, each requiring an Owner to rebuild a byte-for-byte sha256
comparison by hand. This script is that comparison, made permanent and
runnable.

Not part of the automated test suite (no `test_` prefix -- see the name):
it compares against a machine-local installed tree (~/.claude by default),
which is not present, or not current, in CI or on another machine, so a
glob-based test runner picking it up would fail spuriously there.

Usage:
    python tests/payload_check.py [--repo PATH] [--installed PATH]

--repo defaults to this file's repo root (two levels up from this file).
--installed defaults to ~/.claude. Both overrides are load-bearing, not a
convenience: without --installed, proving the witness goes red requires
either installing for real or mutating ~/.claude in place, and both are
forbidden for this incident (and installing is forbidden generally while
any DCS incident is active -- CLAUDE.md's hard rule).

Payload set: DERIVED by walking the same three roots the installers walk,
never a hardcoded list -- a literal list would go silently green on a
payload file added after this script was written. The three roots, and the
installer lines that define them:

    dcs/                recursively  -> ~/.claude/dcs/
        install.ps1:7          install.sh:10-11
    agents/dcs-*.md                  -> ~/.claude/agents/
        install.ps1:10         install.sh:13
    skills/dcs-*/       recursively  -> ~/.claude/skills/<name>/
        install.ps1:12-15      install.sh:15-19

If those line numbers stop matching the installers, the two derivations
(this script's, and the installers') have drifted apart and this comment
needs re-checking against install.ps1 / install.sh.

Scoping: ~/.claude/agents/ and ~/.claude/skills/ are SHARED directories,
not DCS-owned -- measured 2026-07-27, 6 dcs-* agents sit among 33 foreign
gsd-* files (39 total in ~/.claude/agents/), and 10 dcs-* skills sit among
find-skills, humanizer, reconciliation (13 total in ~/.claude/skills/).
Re-measure with:

    ls ~/.claude/agents | wc -l ; ls -d ~/.claude/skills/*/ | wc -l

(39, then 13, as of the date above -- a count is a derived fact with a
lifetime, doctrine principle 15; re-run rather than trust this comment.)
Only the agents/skills matching the dcs-* globs are ever walked on the
installed side (see collect_agents / collect_skills below), so a foreign
file under either shared directory is never a candidate for the
installed-only class -- not filtered out after the fact, simply never
looked at. ~/.claude/dcs/ is the one root treated as wholly DCS-owned, and
is walked in full on both sides.

Exit codes:
    0   payload sets are identical
    1   something differs or exists only in the repo (a real mismatch)
    2   environment error -- e.g. the repo root does not exist or has no
        dcs/ subdirectory (not a DCS repo), or the installed root does
        not exist or has no dcs/ subdirectory (not a DCS install) -- so
        this could not be checked at all. One rule, applied to both
        sides: an existing-but-empty directory is exactly as
        uncheckable as a missing one. Deliberately distinct from 1:
        "cannot check" and "differs" must never be conflated, or a
        caller (deploy.md's marker-unreadable branch) cannot tell them
        apart.
    3   nothing differs and nothing is repo-only, but the installed side
        has extra files the repo does not (installed-only only). Neither
        installer purges: robocopy /E has no /PURGE, rsync -a has no
        --delete, and install.sh's cp -R fallback deletes nothing either.
        That is a stale-extras condition, not a content mismatch.
"""
import argparse
import hashlib
import sys
from pathlib import Path

# Reused verbatim from tests/test_doctrine_integrity.py's EXCLUDED_DIRS /
# BYTECODE_SUFFIXES (matching, not importing: that module runs its own
# checks and calls sys.exit() as a side effect of being imported, which
# would hijack this script's exit code). The two installers disagree on
# whether __pycache__ is excluded -- install.ps1 passes /XD __pycache__ for
# dcs/ but not for the per-skill robocopy; install.sh excludes it via
# rsync for dcs/ only, and its cp -R fallback excludes nothing -- so there
# is no single "the way the installer does it" to defer to. This script
# excludes __pycache__ and compiled bytecode unconditionally on both sides
# instead, which is also why it is needed at all: merely importing
# dcs_gate.py (as test_doctrine_integrity.py's own check 12 does) creates
# dcs/hooks/__pycache__ in the repo tree.
EXCLUDED_DIRS = {".git", "node_modules", "__pycache__"}
BYTECODE_SUFFIXES = (".pyc", ".pyo")


def iter_files(root):
    """All files under root, recursively, minus EXCLUDED_DIRS and
    BYTECODE_SUFFIXES. Empty if root does not exist."""
    if not root.is_dir():
        return []
    return [
        p for p in root.rglob("*")
        if p.is_file()
        and not EXCLUDED_DIRS & set(p.parts)
        and p.suffix.lower() not in BYTECODE_SUFFIXES
    ]


def collect_dcs(root):
    """dcs/ walked recursively. install.ps1:7, install.sh:10-11."""
    base = root / "dcs"
    return {f"dcs/{p.relative_to(base).as_posix()}": p for p in iter_files(base)}


def collect_agents(root):
    """agents/dcs-*.md only -- never the whole (shared) agents/ directory.
    install.ps1:10, install.sh:13."""
    base = root / "agents"
    if not base.is_dir():
        return {}
    return {
        f"agents/{p.name}": p
        for p in sorted(base.glob("dcs-*.md"))
        if p.is_file()
    }


def collect_skills(root):
    """Each skills/dcs-*/ directory walked recursively -- never the whole
    (shared) skills/ directory. install.ps1:12-15, install.sh:15-19."""
    base = root / "skills"
    payload = {}
    if not base.is_dir():
        return payload
    for skill_dir in sorted(base.glob("dcs-*")):
        if not skill_dir.is_dir():
            continue
        for p in iter_files(skill_dir):
            rel = p.relative_to(skill_dir).as_posix()
            payload[f"skills/{skill_dir.name}/{rel}"] = p
    return payload


def collect_payload(root):
    """The full derived payload set rooted at `root`: canonical relative
    path (POSIX-style, stable across repo and installed roots) -> Path.
    Never a hardcoded list -- every entry comes from walking the three
    roots above."""
    payload = {}
    payload.update(collect_dcs(root))
    payload.update(collect_agents(root))
    payload.update(collect_skills(root))
    return payload


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def compare(repo_root, installed_root):
    """Returns (identical, differing, repo_only, installed_only), each a
    sorted list of canonical relative paths."""
    repo_payload = collect_payload(repo_root)
    installed_payload = collect_payload(installed_root)

    identical, differing, repo_only, installed_only = [], [], [], []
    for key in sorted(set(repo_payload) | set(installed_payload)):
        in_repo = key in repo_payload
        in_installed = key in installed_payload
        if in_repo and in_installed:
            if sha256_of(repo_payload[key]) == sha256_of(installed_payload[key]):
                identical.append(key)
            else:
                differing.append(key)
        elif in_repo:
            repo_only.append(key)
        else:
            installed_only.append(key)
    return identical, differing, repo_only, installed_only


def default_repo():
    return Path(__file__).resolve().parent.parent


def default_installed():
    return Path.home() / ".claude"


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Compare this repo's DCS payload against an installed "
                     "copy, file by file, by sha256.")
    parser.add_argument("--repo", default=None,
                         help="repo root to read the payload from "
                              "(default: this script's own repo root)")
    parser.add_argument("--installed", default=None,
                         help="installed root to compare against "
                              "(default: ~/.claude)")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo).resolve() if args.repo else default_repo()
    installed_root = Path(args.installed).resolve() if args.installed else default_installed()

    if not repo_root.is_dir():
        print(f"ERROR: cannot check -- repo root does not exist: {repo_root}")
        return 2
    if not (repo_root / "dcs").is_dir():
        print(f"ERROR: cannot check -- repo root has no dcs/ subdirectory, "
              f"not a DCS repo: {repo_root}")
        return 2
    if not installed_root.is_dir():
        print(f"ERROR: cannot check -- installed root does not exist: "
              f"{installed_root}")
        return 2
    if not (installed_root / "dcs").is_dir():
        print(f"ERROR: cannot check -- installed root has no dcs/ "
              f"subdirectory, not a DCS install: {installed_root}")
        return 2

    identical, differing, repo_only, installed_only = compare(repo_root, installed_root)

    print(f"repo:      {repo_root}")
    print(f"installed: {installed_root}")
    print()
    print(f"identical:      {len(identical)}")
    print(f"differing:      {len(differing)}")
    for k in differing:
        print(f"  {k}")
    print(f"repo-only:      {len(repo_only)}")
    for k in repo_only:
        print(f"  {k}")
    print(f"installed-only: {len(installed_only)}")
    for k in installed_only:
        print(f"  {k}")
    print()
    print(f"{len(identical)} identical, {len(differing)} differing, "
          f"{len(repo_only)} repo-only, {len(installed_only)} installed-only")

    if differing or repo_only:
        return 1
    if installed_only:
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
