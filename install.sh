#!/usr/bin/env bash
# DCS install (POSIX): copy the ICC package from this repo (canonical) into ~/.claude.
# Idempotent; overwrites installed files with repo versions. Run after every committed change.
set -euo pipefail
repo="$(cd "$(dirname "$0")" && pwd)"
claude="${HOME}/.claude"

mkdir -p "$claude/icc" "$claude/agents" "$claude/skills"

rsync -a --exclude '__pycache__' "$repo/icc/" "$claude/icc/" 2>/dev/null \
  || cp -R "$repo/icc/." "$claude/icc/"

cp "$repo"/agents/icc-*.md "$claude/agents/"

for d in "$repo"/skills/icc-*/; do
  name="$(basename "$d")"
  mkdir -p "$claude/skills/$name"
  cp -R "$d." "$claude/skills/$name/"
done

version="$(tr -d '[:space:]' < "$repo/icc/VERSION")"
echo "ICC $version installed to $claude"
echo "NOTE: projects hold their own copy of icc_gate.py in <project>/.claude/hooks/ -- re-run /icc-init (or copy icc/hooks/icc_gate.py manually) in each onboarded project after a hook change."
