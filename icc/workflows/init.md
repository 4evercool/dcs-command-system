<purpose>
Onboard a project into ICC: create its `.icc/` state directory, copy the
gate hook into its `.claude/hooks/`, and — only on explicit Owner consent —
wire the PreToolUse hook into its `.claude/settings.json`. Settings edits
are a configuration change (see the "Explicit permission required" category
in the operating rules), so this workflow never edits `settings.json`
without asking first, in chat, and waiting for a clear yes.
</purpose>

<required_reading>
@$HOME/.claude/icc/references/doctrine.md
</required_reading>

<process>

## 1. Determine the project root

Use `$ARGUMENTS` if a path was given; otherwise use the current working
directory. Confirm it looks like a real project root (has a `.git/` or is
otherwise clearly a project, not e.g. the user's home directory) — if
ambiguous, ask.

## 2. Check for an existing `.icc/`

```bash
ls -la "<project>/.icc" 2>/dev/null
```

If it already exists: report what's there (config.json, ACTIVE if
present, incident count under `.icc/incidents/`). Ask whether to
re-initialize (this workflow never silently overwrites an existing
`config.json` — if the Owner wants a fresh config, confirm that
explicitly).

## 3. Create the project-side directory structure

```
<project>/.icc/
<project>/.icc/incidents/
```

Copy `$HOME/.claude/icc/templates/config.json` to
`<project>/.icc/config.json` (only if it doesn't already exist, or the
Owner just confirmed an overwrite in step 2).

Do **not** create `.icc/ACTIVE` — its absence is the gate's "open" state,
and an onboarded-but-idle project should have no active incident.

## 4. Copy the gate hook

Copy `$HOME/.claude/icc/hooks/icc_gate.py` to
`<project>/.claude/hooks/icc_gate.py`, creating `<project>/.claude/hooks/`
if it doesn't exist. This is a new file under the project's own
`.claude/`, not a shared reference — the hook must be self-contained
(stdlib only) since it will run from the project's own hook invocation, not
from `~/.claude/`.

## 5. Inspect the project's existing `.claude/settings.json`

```bash
cat "<project>/.claude/settings.json" 2>/dev/null
```

Three cases:

**a. File doesn't exist, or has no `hooks.PreToolUse` array.** The block to
add is a whole new `hooks.PreToolUse` array (or a new array if `hooks`
exists but has no `PreToolUse` key).

**b. File has a `hooks.PreToolUse` array already** (e.g. a project like
bread_bot with its own Bash guards). The new matcher is **appended** as an
additional entry in that array — existing entries are never replaced,
reordered, or removed. This is exactly the kind of drift the project's own
guard hooks exist to prevent; ICC's hook must not create the same kind of
invisible surprise it's trying to prevent for source edits.

**c. File has a `PreToolUse` entry with the exact same matcher
(`Edit|Write|NotebookEdit`) already pointing at `icc_gate.py`.** Already
wired — nothing to do, report this.

The exact block to add (matcher and command are fixed; adjust only if the
project's hooks array needs a different JSON nesting to append into):

```json
{
  "matcher": "Edit|Write|NotebookEdit",
  "hooks": [
    {
      "type": "command",
      "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/icc_gate.py\"",
      "timeout": 15,
      "statusMessage": "ICC gate: IAP approval check"
    }
  ]
}
```

**Print this exact block to the Owner** before touching the file, along
with which of the three cases applies and exactly where it would be
inserted (new file vs. appended to an existing array, and if appended,
what it's alongside).

## 6. Ask for explicit permission

Use `AskUserQuestion`: "Wire the ICC gate hook into
`<project>/.claude/settings.json` now? [yes / no, just copy the hook file /
show me the exact diff first]". Do not proceed to edit `settings.json`
without an explicit yes — this matches the general rule that changing
account/config settings requires asking first, every time, regardless of
how mechanical the edit looks.

## 7. On yes: perform the edit

Use the `Edit` tool (never a raw stream redirect) to append the matcher
block into the existing `PreToolUse` array, or create the `hooks` /
`PreToolUse` structure if absent. After editing, re-read the file and
confirm it's still valid JSON (`python -c "import json; json.load(open(r'<path>'))"`
or equivalent) — a broken `settings.json` disables every hook in the
project, not just ICC's.

## 8. On no: leave `settings.json` untouched

Report that the hook file is copied but inert — no PreToolUse wiring means
no gate enforcement yet. Repeat the exact block from step 5 so the Owner
(or a future session) can wire it manually later. `/icc-new` and
`/icc-plan` still work without the hook wired, but the "no edits before
approval" guarantee becomes advisory only, not mechanical, until it's
wired — say this plainly.

## 9. Report completion

Summarize: `.icc/` created (config.json path), `icc_gate.py` copied to
(path), gate wiring status (armed / copied-but-not-wired / already wired),
and the v0.1 one-incident-at-a-time constraint (only one `.icc/ACTIVE` at a
time — `/icc-new` will refuse to open a second incident while one is
active).

</process>
