#!/usr/bin/env bash
# DCS install (POSIX): copy the DCS package from this repo (canonical) into ~/.claude.
# Idempotent; overwrites installed files with repo versions. Run after every committed change.
set -euo pipefail
repo="$(cd "$(dirname "$0")" && pwd)"
claude="${HOME}/.claude"

mkdir -p "$claude/dcs" "$claude/agents" "$claude/skills"

rsync -a --exclude '__pycache__' "$repo/dcs/" "$claude/dcs/" 2>/dev/null \
  || cp -R "$repo/dcs/." "$claude/dcs/"

cp "$repo"/agents/dcs-*.md "$claude/agents/"

for d in "$repo"/skills/dcs-*/; do
  name="$(basename "$d")"
  mkdir -p "$claude/skills/$name"
  cp -R "$d." "$claude/skills/$name/"
done

version="$(tr -d '[:space:]' < "$repo/dcs/VERSION")"
echo "DCS $version installed to $claude"
echo "NOTE: projects hold their own copy of dcs_gate.py in <project>/.claude/hooks/ -- re-run /dcs-init (or copy dcs/hooks/dcs_gate.py manually) in each onboarded project after a hook change."
