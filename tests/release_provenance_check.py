"""Release provenance gate: refuses to let `npm publish` ship a version
whose commit does not already carry a matching git tag and a truthful
CHANGELOG.md entry.

Why this exists (incident release-provenance-guard): docs/publishing.md's
"Version-sync rule (HARD)" and its tag/CHANGELOG provenance rules are only
enforced by merge-time checks and operator discipline. This incident
exists precisely because a publish can happen from a flow that never runs
the merge-time suite, so the rule was mechanized here -- at the one point
a publish cannot bypass if wired into `prepublishOnly`: the moment before
`npm publish` contacts the registry.

Not part of the automated test suite (no `test_` prefix -- see the name --
and not listed in package.json's scripts.test): this check is EXPECTED to
fail on almost every ordinary commit, because most commits are not tagged
release commits. A glob-based test runner (or `npm test` itself) picking
this script up would turn every normal commit red. It is invoked exactly
once, from scripts.prepublishOnly, at the one moment the check is
meaningful.

Usage:
    python tests/release_provenance_check.py [--repo PATH]

--repo defaults to this file's repo root (two levels up from this file),
matching tests/payload_check.py's --repo convention. Stdlib-only, no
network access -- the git commands it shells out to are local queries
(rev-parse) against the repo already on disk.

Let V = package.json's version (what npm actually ships, and the only
version that matters here -- not dcs/VERSION, except as the precondition
below).

Checks, in order:

1. Precondition: dcs/VERSION must equal V. This mechanizes
   docs/publishing.md's existing Version-sync rule (HARD) at publish
   time -- merge-time checks (tests/test_doctrine_integrity.py) already
   enforce it at merge, but this incident exists because publish flows
   bypass them. If the two files disagree, or either is missing or
   unreadable, this is a precondition failure, not a provenance failure:
   exit 2. Deliberately distinct from exit 1 below -- "cannot check" and
   "provenance incomplete" must never be conflated, or a caller (a CI
   step, or an operator reading the exit code) cannot tell them apart.
2. Past that precondition: a git tag vV must exist, and that tag's commit
   (`git rev-parse vV^{commit}`) must equal HEAD's commit (`git rev-parse
   HEAD`). The ^{commit} peel is load-bearing: it dereferences both
   annotated tag objects and lightweight tags down to the commit each
   points at, so both tag kinds are compared the same way.
3. CHANGELOG.md must have an entry for V, using this repo's real heading
   convention: "## <version> <EM DASH> <date>", where <EM DASH> is the
   literal Unicode character U+2014 -- never the two-hyphen ASCII
   sequence. Re-verify the current top heading at any time with
   `grep -n "^## " CHANGELOG.md | head -1` rather than trust a fixed line
   number, which the next release's prepended entry would move past.
   CHANGELOG.md is read with encoding="utf-8" explicitly: the platform
   default codec can mis-decode the em dash's bytes (E2 80 94 in UTF-8),
   which would make this check never match the real file. The version
   match is bounded so that "0.7.1" can never match a heading written for
   "0.7.10" (or for any version 0.7.1 is merely a prefix of).

Any failure in checks 2 or 3 is a real provenance failure, not a
precondition problem: exit 1, naming every failing check (there can be
more than one). Exit 0 only when the precondition and both checks 2 and 3
hold.

Exit codes:
    0   provenance holds: dcs/VERSION == V, tag vV exists and points at
        HEAD, and CHANGELOG.md documents V.
    1   provenance incomplete -- a real failure: no tag vV, OR the tag
        exists but its commit is not HEAD, OR CHANGELOG.md has no entry
        for V. (The precondition already holds when this code is used --
        see exit 2.)
    2   cannot check -- the precondition failed: dcs/VERSION and
        package.json disagree on the version, or either file is missing
        or unreadable. Mirrors tests/payload_check.py's exit-2 "cannot
        check" class: an environment/precondition problem, never
        conflated with a real provenance failure (exit 1).
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# The real CHANGELOG.md heading convention uses the Unicode EM DASH
# (U+2014, UTF-8 bytes E2 80 94), never the two-hyphen ASCII sequence --
# re-verify the current top heading with `grep -n "^## " CHANGELOG.md |
# head -1` rather than trust a fixed line number, which rots the moment
# the next release prepends an entry. Built via chr() rather than typed
# literally or via a \u escape, so this source file stays pure ASCII
# bytes on disk while still producing the correct runtime character.
EM_DASH = chr(0x2014)


def default_repo():
    return Path(__file__).resolve().parent.parent


def read_package_version(repo_root):
    """Returns package.json's "version" string, or None if the file is
    missing, unreadable, not valid JSON, or has no non-empty string
    "version" field."""
    path = repo_root / "package.json"
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return None
    version = data.get("version") if isinstance(data, dict) else None
    if not isinstance(version, str) or not version:
        return None
    return version


def read_dcs_version(repo_root):
    """Returns dcs/VERSION's contents stripped, or None if the file is
    missing, unreadable, undecodable, or empty after stripping. Matches
    read_package_version's (OSError, ValueError) net -- a file saved in a
    non-UTF-8 encoding raises UnicodeDecodeError (a ValueError subclass),
    not OSError."""
    path = repo_root / "dcs" / "VERSION"
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
    except (OSError, ValueError):
        return None
    return content or None


def _git_rev_parse(repo_root, *args):
    """Runs `git rev-parse <args...>` in repo_root; returns the resolved,
    stripped commit hash, or None if the rev does not resolve or git
    itself could not be run (missing executable, repo_root not a git
    repository, etc.)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse"] + list(args),
            cwd=str(repo_root),
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    resolved = result.stdout.strip()
    return resolved or None


def check_tag_at_head(repo_root, tag):
    """Returns None if `tag` exists and its commit is HEAD, else a
    failure-message string naming which of the two conditions broke.
    The tag lookup is qualified to refs/tags/ and passed --verify so
    that ONLY an actual tag can satisfy it -- git rev-parse's default
    disambiguation order also tries refs/heads/ and refs/remotes/, so an
    unqualified "tag + '^{commit}'" lookup is satisfied by a same-named
    branch or remote ref even when zero tags exist."""
    tag_commit = _git_rev_parse(
        repo_root, "--verify", "refs/tags/" + tag + "^{commit}")
    if tag_commit is None:
        return "no git tag %s exists" % tag
    head_commit = _git_rev_parse(repo_root, "--verify", "HEAD")
    if head_commit is None:
        return "HEAD commit could not be resolved (not a git repository?)"
    if tag_commit != head_commit:
        return "tag %s points at %s, which is not HEAD (%s)" % (
            tag, tag_commit, head_commit)
    return None


def changelog_has_entry(repo_root, version):
    """True if CHANGELOG.md has a heading for exactly `version`, using
    the real convention "## <version> <EM DASH> <date>" (U+2014, never
    ASCII "--"). The negative lookahead after the escaped version blocks
    a further digit or dot, so "0.7.1" can never match a heading written
    for "0.7.10" (or "0.7.1.5", etc.) -- only an exact version token
    followed by whitespace then the em dash counts as a match. The two
    [ \t]+ runs immediately around EM_DASH (rather than \s+) keep the
    version, the dash, and the date pinned to one physical line: \s+ also
    matches "\n", so a dateless "## <version>" heading followed, anywhere
    later in the file across only blank lines, by an unrelated
    em-dash-leading line would otherwise glue into a false match. Reads
    the file with encoding="utf-8" explicitly, since the platform default
    codec can mis-decode the em dash's bytes (E2 80 94) and would then
    never match the real file; ValueError is caught alongside OSError
    because an undecodable file raises UnicodeDecodeError (a ValueError
    subclass), not OSError."""
    path = repo_root / "CHANGELOG.md"
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except (OSError, ValueError):
        return False
    pattern = re.compile(
        r"^##\s+" + re.escape(version) + r"(?![\d.])[ \t]+" + EM_DASH + r"[ \t]+\S.*$",
        re.MULTILINE,
    )
    return pattern.search(content) is not None


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Release provenance gate: checks that package.json's "
                     "version is synced with dcs/VERSION, is tagged vV at "
                     "HEAD, and has a CHANGELOG.md entry -- before a "
                     "publish reaches the registry.")
    parser.add_argument("--repo", default=None,
                         help="repo root to check (default: this "
                              "script's own repo root)")
    args = parser.parse_args(argv)

    repo_root = Path(args.repo).resolve() if args.repo else default_repo()

    package_version = read_package_version(repo_root)
    if package_version is None:
        print("ERROR: cannot check -- package.json is missing, unreadable, "
              "or has no version field: %s" % (repo_root / "package.json"))
        return 2

    dcs_version = read_dcs_version(repo_root)
    if dcs_version is None:
        print("ERROR: cannot check -- dcs/VERSION is missing or unreadable: "
              "%s" % (repo_root / "dcs" / "VERSION"))
        return 2

    if dcs_version != package_version:
        print("ERROR: cannot check -- dcs/VERSION (%r) does not match "
              "package.json's version (%r)" % (dcs_version, package_version))
        return 2

    version = package_version
    tag = "v" + version

    failures = []

    tag_failure = check_tag_at_head(repo_root, tag)
    if tag_failure:
        failures.append(tag_failure)

    if not changelog_has_entry(repo_root, version):
        failures.append("CHANGELOG.md has no entry for %s" % version)

    if failures:
        print("PROVENANCE INCOMPLETE for version %s:" % version)
        for f in failures:
            print("  - %s" % f)
        return 1

    print("PROVENANCE OK: %s is HEAD, dcs/VERSION and package.json agree, "
          "CHANGELOG.md documents %s" % (tag, version))
    return 0


if __name__ == "__main__":
    sys.exit(main())
