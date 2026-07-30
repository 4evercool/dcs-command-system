# Publishing DCS to npm (runbook)

Package name: **`dcs-command-system`** (verified free on the registry
2026-07-22; bare `dcs` is squatted by a dead 2018 Angular package).
Distribution model: npm is the delivery vehicle for the same flat install
`install.ps1`/`install.sh` perform — the CLI (`bin/dcs.js`, Node stdlib
only) copies `dcs/`, `agents/dcs-*.md`, `skills/dcs-*` into `~/.claude`.
**Guarded postinstall:** `npm i -g dcs-command-system` auto-installs into
`~/.claude` via a postinstall hook — but only when safe: it skips in CI
(`CI` env), skips politely when `~/.claude` doesn't exist (machine has no
Claude Code — prints the manual command instead), honors
`DCS_SKIP_POSTINSTALL=1` as opt-out, and NEVER fails the surrounding npm
install (all errors degrade to a warning + manual instruction). Note npm
≥7 hides lifecycle-script output by default, so the auto-install is
silent unless `--foreground-scripts` is passed — the behavior still
happens; `dcs doctor` confirms it. All three branches are
tarball-install-tested (2026-07-22): existing target → 28 payload files
land; missing target → nothing created, npm install still succeeds;
opt-out → untouched.

## End-user experience (what the README should show)

```bash
npx dcs-command-system install    # one-shot, no global install
```

or

```bash
npm i -g dcs-command-system
dcs install        # copy package -> ~/.claude
dcs doctor         # content-aware payload comparison (sha256 of every file, via tests/payload_check.py) + python-on-PATH check
dcs uninstall      # remove from ~/.claude (project-side files untouched)
```

Then, per project, inside a Claude Code session: `/dcs-init`.

## Version-sync rule (HARD)

`package.json → version` MUST equal `dcs/VERSION` at publish time. The
CLI prints `dcs/VERSION` as the authoritative version; `doctor` performs
a content-aware comparison — sha256 of every payload file, via
`tests/payload_check.py` — instead of a simple version-string check.
A release bump touches both files in one commit (use `dcs bump <version>`
— see step 2 below).

## Release steps (Owner runs these; the assistant prepares but never publishes)

Repeat this whole sequence for every update, not just the first one.

1. Land the change on `main`: commit, `git push`, tests green
   (`python tests/test_dcs_gate.py`), `git status` clean.
2. Run `dcs bump <version>` (e.g. `dcs bump 0.6.0`). This atomically
   updates both `dcs/VERSION` and `package.json` → `version` to the same
   value. Commit the result (`chore(release): vX.Y.Z`) and push:
   - patch `0.4.x` — fixes, docs, internal cleanup
   - minor `0.x.0` — new capability, backward-compatible
   - major `x.0.0` — breaking change to hook behavior, schemas, or CLI
     flags that existing installs rely on
3. Dry-run the tarball and READ the file list — nothing unexpected, no
   junk, new files actually covered by the `files:` whitelist:
   ```bash
   npm pack --dry-run
   ```
4. Confirm you're logged in (`npm whoami`; re-run `npm login` if it
   errors) and that this version isn't already on the registry:
   `npm view dcs-command-system versions` shouldn't list `X.Y.Z` yet.
5. Publish (unscoped packages are public by default):
   ```bash
   npm publish
   ```
6. Verify end-to-end, from a directory outside the repo:
   ```bash
   npx dcs-command-system@latest version
   ```
   should print the new version; `dcs doctor` too if installed globally.
7. Tag and push it — two separate commands, `&&` is bash syntax and
   breaks in Windows PowerShell 5.1:
   ```bash
   git tag vX.Y.Z
   git push --tags
   ```
8. Cut a GitHub Release off the tag, so the update is visible to
   watchers instead of sitting as a bare tag:
   ```bash
   gh release create vX.Y.Z --title vX.Y.Z --notes "..."
   ```

Existing installs don't get any of this automatically — see "Upgrade
flow for users" below for what they still have to run.

## Upgrade flow for users

```bash
npm i -g dcs-command-system@latest   # or npx dcs-command-system@latest install
dcs install
```

Then in each onboarded project: re-run `/dcs-init` (or copy
`dcs/hooks/dcs_gate.py` manually) — projects hold their own gate-hook
copy, and `settings.json` wiring survives upgrades untouched.

## Notes / future

- A native Claude Code *plugin* format (plugin.json, marketplace) is a
  separate distribution channel; DCS mirrors GSD's flat-install model,
  which works everywhere today. Revisit if/when a public marketplace
  matters.
- `repository`/`homepage`/`bugs` fields in package.json point at the
  GitHub remote (github.com/4evercool/dcs-command-system), added once
  the repo gained one (2026-07-23).
