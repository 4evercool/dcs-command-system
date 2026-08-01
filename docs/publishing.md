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
tarball-install-tested (2026-07-22): existing target → the whole payload
lands; missing target → nothing created, npm install still succeeds;
opt-out → untouched. (The payload is not a fixed size — count it at any
time with `python tests/payload_check.py --repo . --installed ~/.claude`,
which is the same comparison `dcs doctor` runs.)

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

## Publish-from-the-pushed-tip rule (HARD)

`npm publish` packs **the working tree on disk**, not a tag and not
`origin/main`. Whatever is checked out when you run it is what ships. So
the tree you publish from must be the same commit you pushed — and that
commit must already contain the release's own paperwork (`CHANGELOG.md`
entry included). Verify it, never assume it:

```bash
git status --porcelain            # must be empty
git fetch origin
git rev-parse HEAD origin/main    # must print the same sha twice
```

If a tag for this version already exists, it must point at that same
commit — `git rev-parse vX.Y.Z^{commit}` — or you are about to ship
something the tag does not describe.

Both 0.7.x failures were this one rule, unwritten:

- **0.7.1** went to npm with no tag, no GitHub release and no changelog
  entry at all. Nothing checked, so nothing complained; the gap was found
  a day later by diffing the published tarball against candidate trees.
- **0.7.2** was published from a tree one commit behind `main`, so the
  shipped `CHANGELOG.md` still claimed a defect was unfixed that the very
  same release had fixed. The payload was correct; the paperwork beside it
  was not.

npm forbids republishing a version, so neither was repairable afterwards —
which is why this is a pre-publish gate and not a review note.

## Release steps (Owner runs these; the assistant prepares but never publishes)

Repeat this whole sequence for every update, not just the first one.

1. Land the change on `main` — **including this release's `CHANGELOG.md`
   entry**, which is part of the release, not follow-up work. Commit,
   `git push`, tests green (`npm test`), `git status` clean.
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
   `package.json`'s `files:` ends with a `"!**/__pycache__"` negation —
   keep it. Without it npm ships compiled `.pyc` bytecode (0.7.1 went out
   with three, one of them 50 kB), because a directory listed in `files:`
   is included wholesale and `.gitignore` does not hold it back.
4. Confirm you're logged in (`npm whoami`; re-run `npm login` if it
   errors) and that this version isn't already on the registry:
   `npm view dcs-command-system versions` shouldn't list `X.Y.Z` yet.
5. **The tip gate — run this immediately before publishing, from the repo
   root, and read the output.** It is the whole
   publish-from-the-pushed-tip rule in three commands:
   ```bash
   git status --porcelain
   git fetch origin
   git rev-parse HEAD origin/main
   ```
   Nothing from the first, two identical shas from the third. Anything
   else means the tree about to be packed is not the tree you pushed —
   stop and reconcile. Do not `git checkout` a tag to publish "the tagged
   version": that is precisely how 0.7.2 shipped a stale `CHANGELOG.md`.
6. Publish (unscoped packages are public by default):
   ```bash
   npm publish
   ```
7. **Content witness — prove what actually shipped**, rather than
   trusting the version string. From a scratch directory outside the
   repo, fetch the published tarball back and compare it file by file
   against the commit you published from:
   ```bash
   npm pack dcs-command-system@X.Y.Z
   tar xzf dcs-command-system-X.Y.Z.tgz && cd package
   find . -type f ! -name package.json | sed 's|^\./||' | sort |
     while read -r f; do
       [ "$(git -C /path/to/repo show "HEAD:$f" | sha256sum)" = "$(sha256sum < "$f")" ] ||
         echo "DIFFERS: $f"
     done
   ```
   Silence is the pass. (`package.json` is excluded because npm
   normalizes it during packing, so it never matches byte-for-byte.)
   Record the result — "N identical, 0 differing" — the same way a
   `/dcs-deploy` witness is recorded; a bare version label is never
   sufficient evidence that a ship happened. Also confirm the end-user
   path works, from outside the repo:
   ```bash
   npx dcs-command-system@latest version
   ```
8. Tag and push it — two separate commands, `&&` is bash syntax and
   breaks in Windows PowerShell 5.1:
   ```bash
   git tag vX.Y.Z
   git push --tags
   ```
   If the tag already exists (someone tagged ahead of the publish),
   do not create it — verify it instead:
   `git rev-parse vX.Y.Z^{commit}` must equal the commit you published
   from. If it does not, the tag describes a different tree than npm has,
   and that mismatch is the thing to fix before cutting a release off it.
9. Cut a GitHub Release off the tag, so the update is visible to
   watchers instead of sitting as a bare tag. Keep the notes and the
   `CHANGELOG.md` entry saying the same thing:
   ```bash
   gh release create vX.Y.Z --title vX.Y.Z --notes-file notes.md
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
