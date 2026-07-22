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
dcs doctor         # version check + python-on-PATH check for the gate hook
dcs uninstall      # remove from ~/.claude (project-side files untouched)
```

Then, per project, inside a Claude Code session: `/dcs-init`.

## Version-sync rule (HARD)

`package.json → version` MUST equal `dcs/VERSION` at publish time. The
CLI prints `dcs/VERSION` as the authoritative version; `doctor` compares
installed vs package. A release bump touches BOTH files in one commit.

## Release steps (Owner runs these; the assistant prepares but never publishes)

1. Ensure the repo is at the release state: tests green
   (`python tests/test_dcs_gate.py`), `git status` clean.
2. Bump `dcs/VERSION` and `package.json` version together; commit
   (`chore(release): vX.Y.Z`).
3. Dry-run the tarball and READ the file list — nothing unexpected, no
   junk, `files:` whitelist doing its job:
   ```bash
   npm pack --dry-run
   ```
4. First time only: `npm login` (enable 2FA on the account). Optional but
   recommended: verify the name is still free right before first publish:
   `npm view dcs-command-system` should error with 404.
5. Publish (unscoped packages are public by default):
   ```bash
   npm publish
   ```
6. Verify: `npx dcs-command-system@latest version` from a directory
   outside the repo, then `dcs doctor`.
7. Tag: `git tag vX.Y.Z && git push --tags`.

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
