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
commit must already contain the release's own paperwork: a `CHANGELOG.md`
entry that is not merely present but **true of what actually merged**.
Verify it, never assume it:

```bash
git status --porcelain            # must be empty
git fetch origin
git rev-parse HEAD origin/main    # must print the same sha twice
```

If a tag for this version already exists, it must point at that same
commit — `git rev-parse vX.Y.Z^{commit}` — or you are about to ship
something the tag does not describe.

Three releases have failed here, in three different ways — and only the
first is this rule. Do not collapse them; they need different checks:

- **v0.4.2** shipped from a tree that predated the README's audit-trail
  section. This is the rule above, exactly: a stale working tree got
  packed. The tip gate in step 5 catches it.
- **0.7.1** went to npm with no tag, no GitHub release and no changelog
  entry at all — all three were created retroactively a day later. The
  tip gate would **not** have caught this: the tree was fine. What was
  missing was provenance. `package.json`'s `scripts.prepublishOnly` now
  runs `python tests/release_provenance_check.py` and fails `npm publish`
  — including `npm publish --dry-run` — before any registry contact
  when the tag or the `CHANGELOG.md` entry is missing. `npm pack` and
  `npm pack --dry-run` are unaffected — they never run `prepublishOnly`
  (measured, npm 11.8.0).
  Tracked as incident `release-provenance-guard`.
- **0.7.2** was published faithfully from the true tip of `main`, and its
  tarball is byte-identical to its tag — 75 of 75 files. `3d559ce` was
  committed 00:42:24Z and published 00:45:48Z; the corrective commit did
  not exist until 00:51:51Z, six minutes later. **Neither the tip gate nor
  any tag-versus-tarball comparison would have caught it**, because
  nothing disagreed. What shipped wrong was the *content* of the tip's own
  `CHANGELOG.md`: an incident had merged without updating its entry, so
  the entry still called a defect unfixed that the same release had just
  fixed. The only thing that catches this is reading the entry against
  what actually merged — hence "true of what actually merged" above, not
  merely "present".

npm forbids republishing a version, so none of the three was repairable
afterwards — which is why these are pre-publish gates and not review notes.

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
   stop and reconcile. Do not `git checkout` a tag or an older commit to
   publish "the tagged version": a stale checkout is how v0.4.2 shipped a
   tree predating its own README section.
6. Tag and push it — two separate commands, `&&` is bash syntax and
   breaks in Windows PowerShell 5.1:
   ```bash
   git tag vX.Y.Z
   git push --tags
   ```
   If the tag already exists — the normal case when this sequence is
   being retried after an earlier interruption — do not create it again:
   verify it instead. `git rev-parse vX.Y.Z^{commit}` must equal `HEAD`,
   the commit about to be published in the next step. If it does not,
   the tag describes a different tree than the one about to ship, and
   that mismatch is the thing to fix before publishing.
7. Publish (unscoped packages are public by default). The provenance
   gate above now runs automatically as part of this step:
   ```bash
   npm publish
   ```
8. **Content witness — prove what actually shipped**, rather than
   trusting the version string. From a scratch directory outside the
   repo, fetch the published tarball back and compare it file by file
   against the commit you published from:
   ```bash
   npm pack dcs-command-system@X.Y.Z
   tar xzf dcs-command-system-X.Y.Z.tgz && cd package
   find . -type f | sed 's|^\./||' | sort |
     while read -r f; do
       [ "$(git -C /path/to/repo show "HEAD:$f" | sha256sum)" = "$(sha256sum < "$f")" ] ||
         echo "DIFFERS: $f"
     done
   ```
   Silence is the pass. `package.json` is compared like every other file:
   npm packs it verbatim, measured — the published 0.7.2 copy and
   `git show 3d559ce:package.json` have identical sha256 under npm 11.8.0.
   If some future npm does rewrite it on pack, it will show up here as a
   single expected difference; confirm that is what happened before calling
   it a defect, and do not silently drop the file from the comparison.
   Record the result — "N identical, 0 differing" — the same way a
   `/dcs-deploy` witness is recorded; a bare version label is never
   sufficient evidence that a ship happened. Also confirm the end-user
   path works, from outside the repo:
   ```bash
   npx dcs-command-system@latest version
   ```
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
