# 201 — Incident Brief

**Incident:** deploy-marker-blind
**Opened:** 2026-07-27 (+1100)
**Type:** 1

## Symptom

`/dcs-deploy`'s two verification steps both read the project's
"deployed-version marker", and for this repo that marker is
`~/.claude/dcs/VERSION` — a copy of `dcs/VERSION` that `install.ps1` /
`install.sh` carry along inside the payload they copy. It therefore moves
only when the *version string* changes, never when the *content* does. DCS
deliberately permits shipping without a version bump while the target
version is unpublished, so a real, correct, fully-verified ship can leave
the marker reading exactly what it read before. That has now happened
**three consecutive times** (`schemas-md-trim` 0.6.9→0.6.9,
`schema-citation-guard` 0.6.10→0.6.10, `safety-halt-functional-scope`
0.6.10→0.6.10), and each one required an explicit Owner authorisation to
substitute a different check. Both failure directions are live and neither
is loud: **step 7** (`deploy.md:172-183`) stops and refuses to mark a row
`DEPLOYED` when the marker "didn't advance" — which is the *correct-ship*
case here, so the stop condition fires on success and trains whoever hits
it to override a safeguard; **step 4** (`deploy.md:86-105`) reconciles
`MERGED` rows against the marker to avoid re-shipping out-of-band work,
and a marker that cannot distinguish shipped from unshipped can silently
record unshipped work as live. Compounding it, step 4's reconciliation
command presumes the marker is a **git sha**
(`git merge-base --is-ancestor <merge commit> <deployed marker sha>`), so
against a version string it does not degrade — it errors, and has never
once been runnable in this repo. The witness that has actually done the
job all three times — a byte-for-byte sha256 comparison of every payload
file against the repo — exists nowhere in the tree and was rebuilt from a
one-liner each time.

## Evidence

- `deploy.md:86-93` (step 4) specifies the reconciliation as
  `git merge-base --is-ancestor <row merge commit> <deployed marker sha>`
  — the marker is named as a sha explicitly. Source: analyst A, quoting
  the file.
- `deploy.md:101-103` gives step 4 exactly one escape hatch — *"Marker
  unreadable (no SSH, no documented marker): skip the reconciliation"*.
  The case that actually occurs here (marker readable, but a version
  string rather than a commit-ish) is unaddressed and falls through to the
  literal invocation. Source: analyst A, quoting the file.
- `deploy.md:172-183` (step 7): *"Check the project's own deployed-version
  marker … before and after … and confirm it actually advanced … If it
  didn't advance … **stop** … do not mark anything `DEPLOYED`"*. Source:
  analyst A, quoting the file.
- Reproduced live, read-only: `git merge-base --is-ancestor aab9f06 0.6.10`
  → `fatal: Not a valid object name 0.6.10`, exit 128. Step 4's command has
  never been runnable in this repo. Source: analyst A and analyst B
  independently (analyst B ran it against `HEAD`, same result).
- Current state, measured 2026-07-27: `C:\DCS\dcs\VERSION` = `0.6.10` and
  `~/.claude/dcs/VERSION` = `0.6.10`, while a full sha256 walk of all 47
  payload files (`dcs/**` 31, `agents/dcs-*.md` 6, `skills/dcs-*/` 10)
  reports **0 differing, 0 repo-only, 0 installed-only**. The installed
  copy is byte-identical to `HEAD` (`ba6019e`) — a real ship the marker
  witnessed in neither direction. Regenerate by diffing `C:\DCS\dcs`
  against `~/.claude/dcs` (and the two glob sets above); the counts move
  with the tree.
- `install.ps1:7,10,12-15` robocopies `dcs/`, `agents\dcs-*.md` and each
  `skills\dcs-*` directory; `install.ps1:17-18` reads `dcs\VERSION` only to
  **print** it. The installer writes **no manifest, no hash file, no file
  list** — the only artifact left for a later comparison is the copied
  `VERSION` file itself. `install.sh:10-11,21-23` has the identical shape.
  Source: analyst A.
- The payload set is not declared anywhere as a static list; it is a
  glob/directory walk performed at install time. Source: analyst A.
- `CLAUDE.md:30` is the normative definition of the flawed contract:
  *"Deployed-version marker | `~/.claude/dcs/VERSION` — must equal
  `dcs/VERSION` after deploy"*. Any fix that changes what the marker **is**
  has to change this table too. Source: analyst B.
- Three field instances, each with the Owner authorising a substituted
  check: `REGISTER.md` row `schemas-md-trim` (31 files, 0.6.9 before and
  after), row `schema-citation-guard` (47 files, 0.6.10 before and after;
  9 genuinely differed beforehand — and this is the one instance where the
  substitution was **declared in the IAP in advance** rather than
  improvised at deploy time), row `safety-halt-functional-scope` (4 of 47
  differed before, 47/47 identical after; 0.6.10 before and after,
  *"the third consecutive ship it could not see"*). Source: analyst B,
  quoting the register's Outcome cells.
- The substituted witness has no in-repo home. `Glob **/payload_check*`
  under `C:\DCS` returns nothing, and a filesystem-wide `find -iname
  payload_check.py` finds nothing — the register's own regenerate
  instruction is `python <scratch>/payload_check.py C:/DCS`, a scratch
  path. It has been rebuilt by hand three times. Source: analyst B.
- Contrast case proving the mechanism is sound when a bump *does* happen:
  `REGISTER.md` row `halt-loop-unbounded` — *"marker `~/.claude/dcs/VERSION`
  advanced 0.6.8 → 0.6.9, verified after the run and not on the exit
  code"*. The defect is specific to the unbumped case, not to step 7
  generally. Source: analyst A.
- `git log` shows no version bump between `4b5e7b0` (`chore(release):
  0.6.10`) and `HEAD` `ba6019e`; both `e24f120` and `aab9f06` merged under
  the same 0.6.10. Source: analyst A.
- Second consumer with the same blind spot, **outside this incident's
  scope** (see Decomposition): `bin/dcs.js:121-146`'s `doctor()` reads the
  same installed marker and does a plain string-equality comparison.
  Source: analyst B.
- No automated test exercises `deploy.md`, `install.ps1`, `install.sh` or
  `doctor()`; none of the three suites (`test_dcs_gate.py`,
  `test_dcs_intake.py`, `test_doctrine_integrity.py`) touch them.
  `test_doctrine_integrity.py`'s only VERSION-related check is version
  sync (`dcs/VERSION` == `package.json`), at lines 152-157. Source:
  analyst B, full-file grep.
- Constraints the fix must respect, all quoted rather than assumed:
  `CLAUDE.md:146-148` types installer changes as **Type 1**; the live
  Delegation v3 lists `install.ps1` / `install.sh` in `forbidden_globs` at
  **both** the top level and inside the `deploy` object; `CLAUDE.md:124-125`
  requires `dcs/VERSION` and `package.json` to move in the same commit;
  `package.json:12-23`'s `files` whitelist would need a new entry if a
  witness script joins the shipped payload; `deploy.md` is **215 lines /
  11,456 B**, inside the ~250-line workflow budget, so there is headroom
  in that file. Source: analyst B.
- No other `QUEUED` register row claims `dcs/workflows/deploy.md`,
  `install.ps1`, `install.sh` or `CLAUDE.md` — full table scan of every
  queued row. `version-bump-command` (rank 9) claims `bin/dcs.js`, which is
  a soft collision only if this incident reaches into `bin/**`. Source:
  analyst B.

## Reproduction path

This is a mechanism defect in a workflow, not a code path, and it has been
reproduced three times by actually running the deploy train. Two parts of
it reproduce on demand, read-only, without shipping anything:

1. **Step 4's ancestry check is unrunnable.**
   `git merge-base --is-ancestor aab9f06 0.6.10` →
   `fatal: Not a valid object name 0.6.10` (exit 128). No deploy needed.
2. **The marker is currently blind, right now.** `cat dcs/VERSION` and
   `cat ~/.claude/dcs/VERSION` both read `0.6.10`, while a sha256 walk of
   the payload files shows 0 differences — i.e. the last ship happened
   and the marker records nothing either way.
3. **Full reproduction (mutating — not performed at the stem):** make any
   payload-only change without bumping `dcs/VERSION`, run `install.ps1`,
   and read the marker before and after. It is unchanged while the payload
   genuinely differs; `deploy.md` step 7's stop condition then fires on a
   correct ship.

## Blast radius (best guess at intake)

- `dcs/workflows/deploy.md` — steps 4 and 7, the two load-bearing marker
  reads.
- `install.ps1`, `install.sh` — if the fix makes the installer emit a
  content witness (backlog candidate fix 1).
- `CLAUDE.md` — the Deploy table at line 30 defines the marker contract.
  Unguarded by the gate in this repo, but normative.
- A new in-repo witness command (location undecided at intake — a script,
  a `bin/` subcommand, or a documented one-liner), plus `package.json`'s
  `files` whitelist **if** it ships in the payload.
- **Not** in scope, split out below: `bin/dcs.js`'s `doctor()`.
- **Not implicated:** `tests/test_doctrine_integrity.py` (its only VERSION
  check is version sync), and the generic "deployed-version marker" prose
  in `close.md:75-79`, `skills/dcs-deploy/SKILL.md:15-24`,
  `run.md:135-147`, `docs/spec-v0.3-parallel.md:127` — those describe any
  project's marker, not this repo's mechanism.

This is a starting hypothesis, not a commitment; `/dcs-plan` refines it
into the actual territory partition.

## Decomposition (new.md step 4a — one incident, one defect)

**One defect is opened here:** the deploy train has no witness for a ship
that does not bump the version. Steps 4 and 7 both read the same marker
and both assume properties it does not have — that it advances on content
change, and that it is a commit-ish. Those are two symptoms of one root
(the marker's identity), they are fixed by the same act, and `deploy.md`
would be internally inconsistent if only one were fixed.

**One defect is split out and registered as `QUEUED`, not absorbed:**

- **`doctor-version-only-check`** — `bin/dcs.js:121-146`'s `doctor()`
  compares the installed `~/.claude/dcs/VERSION` to `package.json`'s
  version by string equality and reports "current" when they match, so a
  user whose install is a stale same-version payload is told everything is
  fine. Independent root (a different consumer, a user-facing health
  check rather than the deploy train's gate), it ships on its own, and its
  territory `bin/**` is both a Delegation `forbidden_glob` and a soft
  collision with the queued `version-bump-command` row. Evidence above is
  already gathered; its 201 costs a cheap stem.

## Prior art

`vault/Backlog.md` item 12 (lines 352-411), *"The deployed-version marker
is blind to a same-version ship"*, is the origin finding and the direct
intake source. It already proposes three candidate fixes in order of
invasiveness: **(1)** make the payload hash itself the marker, via a new
`~/.claude/dcs/.deployed` file the installer writes; **(2)** keep the
version marker but add the sha256 content comparison as a permanent second
gate — *"exactly what this run did by hand"*; **(3)** require a version
bump on every deploy, which the item **rejects on the merits**, since DCS
deliberately permits skipping the bump while a version is unpublished. It
also flags step 4's sha-shaped ancestry check as adjacent and undecided.

`vault/Decisions/`, `vault/Post-mortems/`, `vault/Meta/`, `vault/Metrics/`
were each grepped for `marker` / `deployed` / `VERSION` / `payload` /
`sha256`; nothing bearing on this defect. Backlog item 13 (which became
the queued `criterion-unmeasured-fact` row) surfaced the same day on the
same release and is adjacent, but has a different root.

**No prior DCS incident has attempted this fix.** It has only been worked
around, three times, by hand.

## Type + rationale

**Proposed type:** 1

**Rationale (IC at command point 1, `dcs-commander`, seat Fable):** the
analysts confirmed the blast radius forks on an undecided approach.
Backlog fix (1) must edit `install.ps1` / `install.sh`, which
`CLAUDE.md:146-148` types as Type 1 by name; typing is fixed at the stem
before planning, so a Type 3 would silently foreclose approach (1) by
ceremony selection rather than by a planning decision. Under **either**
approach the incident rewrites what this repo accepts as proof of
deployment — `CLAUDE.md:30`'s marker contract and the step that gates
`DEPLOYED` register rows — so per `typing.md`'s "type up, not down" the
doubt resolves upward. The over-typing cost if the plan lands on approach
(2) is one Logistics Chief spawn.

**Owner confirmation:** confirmed as proposed — Type 1, 2026-07-27.

**Owner decision on the IC's open question (approach):** *not* constrained
at the stem. The Planning Chief proposes; the Owner decides between
approach (1) and (2) at the mandatory Type 1 IAP approval, where the
tactics, partition and risks are visible alongside the choice.

## Intake source (for /dcs-close to route back to)

`vault/Backlog.md` item 12, queued at the 2026-07-26 `/dcs-esg` session as
register row `deploy-marker-blind` (rank 1, priority H); pulled by
`/dcs-run deploy-marker-blind`, 2026-07-27.
