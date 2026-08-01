<purpose>
Onboard a project into DCS: create its `.dcs/` state directory, copy the
register view generator and all three hooks into their project-side
locations, and — only on explicit Owner consent — wire the hooks into its
`.claude/settings.json`. Settings edits are a configuration change (see
the "Explicit permission required" category in the operating rules), so
this workflow never edits `settings.json` without asking first, in chat,
and waiting for a clear yes.
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
`.dcs/esg/` — append if missing (creating `.gitignore` if absent), never
removing or reordering what is already there. These three are
per-worktree or main-checkout-only state (doctrine "Parallel operation" /
`docs/spec-v0.3-parallel.md`'s state-split table): a tracked `ACTIVE`
would ride an incident's merge into main and wedge the gate for every
future incident; a tracked `esg/` would diverge across every branch
instead of staying one portfolio source of truth. `.dcs/config.json` and
`.dcs/incidents/` stay tracked, unaffected by this step.

## 3b. Copy the register view generator

Copy `$HOME/.claude/dcs/esg/register_view.py` to
`<project>/.dcs/register_view.py` — NOT `.dcs/esg/`, which step 3a just
gitignored. Unlike `REGISTER.md` this is a static tool, not per-worktree
data, so it must survive a plain `git clone`: tracked like step 4's
hooks, freshly overwritten on re-init. Reads `.dcs/esg/REGISTER.md`,
writes the sibling `register-view.html` (creating `.dcs/esg/` if needed),
never touches `REGISTER-LOCK`. Inert until run by hand or the hook below
is wired.

## 4. Copy the hooks

Copy all **three** hooks to `<project>/.claude/hooks/`, creating the
directory if needed — `$HOME/.claude/dcs/hooks/dcs_gate.py`,
`dcs_intake.py`, and `register_view_regen.py`. These are project-owned
copies, not shared references: each is self-contained (stdlib only)
because it runs from the project's own hook invocation.

- **`dcs_gate.py`** (PreToolUse) — the approval gate. Blocking.
- **`dcs_intake.py`** (UserPromptSubmit, v0.6.0) — one short note on the
  first prompt of each session: offer `/dcs-run` for a bug/feature ask,
  or report an active incident's slug/type/phase. **Advisory, never
  blocking**, once per session — the gate is silent when no incident is
  active, so nothing else would mention that one was an option. Tell the
  Owner this part: since v0.7.2 it also appends one JSON line per session
  to `.dcs/esg/intake-telemetry.log` — timestamp, hashed session id, which
  note fired, the project's absolute path. Local and gitignored, nothing
  leaves the machine, but **no opt-out short of declining the hook**.
- **`register_view_regen.py`** (PostToolUse) — regenerates
  `register-view.html` whenever the project's own `REGISTER.md` is
  edited, so the view can't go stale between manual runs. **Can never
  deny or block** (PostToolUse fires after the edit already happened),
  but does run `register_view.py` as a subprocess and write a file as a
  side effect. Silent no-op if step 3b was skipped or the edit target
  isn't that `REGISTER.md`.

## 5. Inspect the project's existing `.claude/settings.json`

```bash
cat "<project>/.claude/settings.json" 2>/dev/null
```

Three cases:

**a. File doesn't exist, or has no `hooks.PreToolUse` array.** The block to
add is a whole new `hooks.PreToolUse` array (or a new array if `hooks`
exists but has no `PreToolUse` key).

**b. File has a `hooks.PreToolUse` array already** (e.g. a project that
already ships its own Bash guards). The new matcher is **appended** —
existing entries are never replaced, reordered, or removed. DCS's own hook
must not create the drift that a project's guard hooks exist to prevent.

**Upgrading a project onboarded before v0.5.8:** an existing entry whose
matcher is the old `Edit|Write|NotebookEdit` still gates edits correctly
but will NOT catch agent resumes. Point it out and offer the one-word
fix — append `|SendMessage` to that matcher — using the same explicit
consent flow as any other settings change.

**c. File has a `PreToolUse` entry with the exact same matcher
(`Edit|Write|NotebookEdit|SendMessage`) already pointing at `dcs_gate.py`.**
Already wired — nothing to do, report this.

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

**And the intake nudge (v0.6.0)** — a sibling of `hooks.PreToolUse`, not
an entry inside it. `UserPromptSubmit` takes no `matcher`, so the block is:

```json
"UserPromptSubmit": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/dcs_intake.py\"",
        "timeout": 10
      }
    ]
  }
]
```

**And the register-view regen hook** — a third sibling array,
`hooks.PostToolUse`, checked by the same three cases (a/b/c)
independently. Only worth presenting if step 3b actually ran:

```json
"PostToolUse": [
  {
    "matcher": "Edit|Write",
    "hooks": [
      {
        "type": "command",
        "command": "python \"$CLAUDE_PROJECT_DIR/.claude/hooks/register_view_regen.py\"",
        "timeout": 20,
        "statusMessage": "Regenerating register view"
      }
    ]
  }
]
```

Present all three blocks together in step 6, stating plainly what each
does: the gate can **deny** a tool call; the intake nudge only adds
context and can never block; the regen hook can't block either but does
write a file as a side effect. An Owner may want any subset — take that
as given rather than arguing for the full set.

**Print the exact blocks to the Owner** first, with which case applies to
each array and exactly where each would be inserted.

## 6. Ask for explicit permission

Use `AskUserQuestion`: "Wire the DCS hooks into
`<project>/.claude/settings.json` now — gate, intake nudge, and
register-view regen? [yes, wire all three / no, just copy the hook files
/ show me the exact diff first]". Do not edit `settings.json` without an
explicit yes — settings changes always require asking first, however
mechanical the edit looks. An Owner may want only a subset (e.g. the gate
but not the regen hook) — take a partial answer as given.

## 7. On yes: perform the edit

Use the `Edit` tool (never a raw stream redirect) to append each block
into its respective array (`PreToolUse`, `UserPromptSubmit`,
`PostToolUse`), creating whichever `hooks.*` structures are absent — skip
any array the Owner didn't consent to. After editing, re-read the file
and confirm it's still valid JSON (`python -c "import json;
json.load(open(r'<path>'))"`) — a broken `settings.json` disables every
hook in the project, not just DCS's.

## 8. On no: leave `settings.json` untouched

Report the hook files are copied but inert — no gate enforcement, no
intake nudge, no register-view auto-regen. Repeat the exact blocks from
step 5 for later manual wiring. `/dcs-new` and `/dcs-plan` still work
without the gate wired, but "no edits before approval" becomes advisory,
not mechanical — say so plainly. Unwired, the regen hook just means
running `python .dcs/register_view.py` by hand.

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
(step 3a), `register_view.py` and all three hooks copied (paths), each
hook's wiring status individually — gate, intake, and regen may each land
differently if the Owner consented to a subset — and the
one-incident-per-worktree constraint (only one `.dcs/ACTIVE` per tree;
Type 3/1 incidents each get their own worktree via `git worktree add`, so
multiple run in parallel across worktrees — see doctrine's "Parallel
operation" section).

</process>
