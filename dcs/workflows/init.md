<purpose>
Onboard a project into DCS: create its `.dcs/` state directory, copy the
gate hook into its `.claude/hooks/`, and — only on explicit Owner consent —
wire the PreToolUse hook into its `.claude/settings.json`. Settings edits
are a configuration change (see the "Explicit permission required" category
in the operating rules), so this workflow never edits `settings.json`
without asking first, in chat, and waiting for a clear yes.
</purpose>

<required_reading>
@$HOME/.claude/dcs/references/doctrine.md
</required_reading>

<process>

## 1. Determine the project root

Use `$ARGUMENTS` if a path was given; otherwise use the current working
directory. Confirm it looks like a real project root (has a `.git/` or is
otherwise clearly a project, not e.g. the user's home directory) — if
ambiguous, ask.

## 2. Check for an existing `.dcs/`

```bash
ls -la "<project>/.dcs" 2>/dev/null
```

If it already exists: report what's there (config.json, ACTIVE if
present, incident count under `.dcs/incidents/`). Ask whether to
re-initialize (this workflow never silently overwrites an existing
`config.json` — if the Owner wants a fresh config, confirm that
explicitly).

## 3. Create the project-side directory structure

```
<project>/.dcs/
<project>/.dcs/incidents/
```

Copy `$HOME/.claude/dcs/templates/config.json` to
`<project>/.dcs/config.json` (only if it doesn't already exist, or the
Owner just confirmed an overwrite in step 2).

Do **not** create `.dcs/ACTIVE` — its absence is the gate's "open" state,
and an onboarded-but-idle project should have no active incident.

## 3a. Gitignore the per-worktree/main-only state (v0.3)

Ensure `<project>/.gitignore` contains `.dcs/ACTIVE`, `.dcs/CLOSED`, and
`.dcs/esg/` — append them (creating `.gitignore` if it doesn't exist yet)
if missing, never removing or reordering anything already there. These
three are deliberately per-worktree or main-checkout-only state (doctrine
"Parallel operation" / `docs/spec-v0.3-parallel.md`'s state-split table):
a tracked `ACTIVE` would ride an incident's merge into main and wedge the
gate for every future incident; a tracked `esg/` would diverge across
every branch instead of staying the single portfolio source of truth.
`.dcs/config.json` and `.dcs/incidents/` stay tracked as before —
unaffected by this step.

## 4. Copy the gate hook

Copy `$HOME/.claude/dcs/hooks/dcs_gate.py` to
`<project>/.claude/hooks/dcs_gate.py`, creating `<project>/.claude/hooks/`
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

**b. File has a `hooks.PreToolUse` array already** (e.g. a project that
already ships its own Bash guards). The new matcher is **appended** as an
additional entry in that array — existing entries are never replaced,
reordered, or removed. This is exactly the kind of drift the project's own
guard hooks exist to prevent; DCS's hook must not create the same kind of
invisible surprise it's trying to prevent for source edits.

**Upgrading a project onboarded before v0.5.8:** an existing entry whose
matcher is the old `Edit|Write|NotebookEdit` still gates edits correctly
but will NOT catch agent resumes. Point it out and offer the one-word
fix — append `|SendMessage` to that matcher — using the same explicit
consent flow as any other settings change.

**c. File has a `PreToolUse` entry with the exact same matcher
(`Edit|Write|NotebookEdit|SendMessage`) already pointing at
`dcs_gate.py`.** Already
wired — nothing to do, report this.

The exact block to add (matcher and command are fixed; adjust only if the
project's hooks array needs a different JSON nesting to append into):

```json
{
  "matcher": "Edit|Write|NotebookEdit|SendMessage",
  "hooks": [
    {
      "type": "command",
      "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/dcs_gate.py\"",
      "timeout": 15,
      "statusMessage": "DCS gate: IAP approval check"
    }
  ]
}
```

**Print this exact block to the Owner** before touching the file, along
with which of the three cases applies and exactly where it would be
inserted (new file vs. appended to an existing array, and if appended,
what it's alongside).

## 6. Ask for explicit permission

Use `AskUserQuestion`: "Wire the DCS gate hook into
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
project, not just DCS's.

## 8. On no: leave `settings.json` untouched

Report that the hook file is copied but inert — no PreToolUse wiring means
no gate enforcement yet. Repeat the exact block from step 5 so the Owner
(or a future session) can wire it manually later. `/dcs-new` and
`/dcs-plan` still work without the hook wired, but the "no edits before
approval" guarantee becomes advisory only, not mechanical, until it's
wired — say this plainly.

## 8a. Audit agent tool grants against the project's protocols (v0.5.6)

Read the project's `CLAUDE.md` for pre-flight protocols that **name a
tool** — an MCP server, a query interface, a required script (e.g. "query
the call graph before any cross-file edit", "query the action log before
debugging"). For each, check `~/.claude/agents/dcs-*.md`'s `tools:` line
and report any role expected to honor that protocol but not granted the
tool.

The role that most often fails this is `dcs-ops-specialist`: it is the
only DCS role that edits code, so it inherits every pre-edit protocol the
project defines, while charters tend to grant analysis tools to analysis
roles (doctrine: "Relationship to project-specific protocols" — a
protocol an agent cannot execute is a charter defect).

Report the gap and the exact one-line fix (add the tool glob to that
charter's `tools:`); do **not** edit files under `~/.claude/agents/`
yourself — those are the installed copy of the DCS package, and editing
them in place is the drift the package's own source-of-truth rule
forbids. The fix belongs in the DCS repo, then a re-install.

## 9. Report completion

Summarize: `.dcs/` created (config.json path), `.gitignore` entries added
(step 3a), `dcs_gate.py` copied to (path), gate wiring status (armed /
copied-but-not-wired / already wired), and the one-incident-per-worktree
constraint (only one `.dcs/ACTIVE` per tree — `/dcs-new` will refuse to
open a second incident in the same tree while one is active; Type 3/1
incidents each get their own worktree via `git worktree add`, so multiple
can run in parallel across different worktrees — see doctrine's
"Parallel operation" section).

</process>
