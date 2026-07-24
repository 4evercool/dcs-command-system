"""Comparative metrics across DCS incidents in one or more project trees.

Maintainer tool, repo-local (never shipped -- see package.json `files`).
Exists so [[Metrics/incident-metrics]] carries its derivation rather than
a frozen table: doctrine principle 15, applied to the vault itself.

Usage:
    python vault/_scripts/incident_metrics.py <project-root> [<more roots>...]

A "root" is any tree holding .dcs/incidents/ -- a main checkout or a
worktree. Later roots win for the same incident slug when their log is
longer (a worktree mid-incident holds more than the merged copy).
"""
import io
import os
import re
import sys
import glob


def collect(roots):
    found = {}
    for root in roots:
        base = os.path.join(root, ".dcs", "incidents")
        if not os.path.isdir(base):
            continue
        for slug in os.listdir(base):
            p = os.path.join(base, slug)
            log = os.path.join(p, "214-LOG.md")
            if not os.path.exists(log):
                continue
            if slug not in found or os.path.getsize(log) > os.path.getsize(
                    os.path.join(found[slug], "214-LOG.md")):
                found[slug] = p
    return found


def read(p):
    try:
        return io.open(p, encoding="utf-8").read()
    except OSError:
        return ""


def row(slug, p):
    log = read(os.path.join(p, "214-LOG.md"))
    entries = [l for l in log.splitlines() if re.match(r"^\[\d{4}-", l)]
    stamps = [re.match(r"\[([\d\-T:+]+)", l).group(1) for l in entries
              if re.match(r"\[([\d\-T:+]+)", l)]
    brief = os.path.join(p, "201-BRIEF.md")
    return dict(
        slug=slug,
        brief_kb=round(os.path.getsize(brief) / 1024) if os.path.exists(brief) else 0,
        log_kb=round(len(log.encode("utf-8")) / 1024),
        entries=len(entries),
        halts=len(re.findall(r"SAFETY: halt", log)),
        passes=len(re.findall(r"SAFETY: pass", log)),
        rejects=len(re.findall(r"iap_review REJECT", log)),
        escalations=len(re.findall(r"ESCALATION: trigger", log)),
        taskings=len(glob.glob(os.path.join(p, "204-TASKING", "*.md"))),
        first=stamps[0][:16] if stamps else "?",
        last=stamps[-1][:16] if stamps else "?",
    )


def main(roots):
    rows = [row(s, p) for s, p in sorted(collect(roots).items())]
    if not rows:
        print("no incidents found under:", ", ".join(roots))
        return 1
    hdr = (f"{'incident':46}{'201kB':>6}{'logkB':>6}{'ent':>5}{'halt':>5}"
           f"{'pass':>5}{'rej':>4}{'esc':>4}{'tsk':>4}")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['slug'][:46]:46}{r['brief_kb']:>6}{r['log_kb']:>6}{r['entries']:>5}"
              f"{r['halts']:>5}{r['passes']:>5}{r['rejects']:>4}"
              f"{r['escalations']:>4}{r['taskings']:>4}")
    print()
    for r in rows:
        print(f"{r['slug'][:46]:46} {r['first']} -> {r['last']}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
