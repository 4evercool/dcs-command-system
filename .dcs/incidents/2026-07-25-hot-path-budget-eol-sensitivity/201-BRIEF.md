<!--
201-BRIEF.md — written by the IC from dcs-situation-analyst findings, once,
at the stem (/dcs-new). Never edited after typing is confirmed except to
append a note if a later period's assessment reveals the original blast
radius was wrong (append, don't rewrite — 214-LOG.md is the append-only
one, but this file's Symptom/Evidence should stay a true record of what was
known at intake).
-->

# 201 — Incident Brief

**Incident:** hot-path-budget-eol-sensitivity
**Opened:** 2026-07-25
**Type:** 1

## Symptom

This repo has **no line-ending policy** — `core.autocrlf=true`, no
`.gitattributes` anywhere in history — while two of its mechanisms read **raw
on-disk bytes**. The result is that the same commit measures and hashes
differently depending on which files a given checkout happened to rewrite.

Two manifestations, one root cause:

1. **The hot-path budget check** (`tests/test_doctrine_integrity.py`) sums
   `os.path.getsize()` of `doctrine.md` + `schemas.md`. Those two files are
   *right now* in different states in the main checkout — `doctrine.md` 100 %
   CRLF, `schemas.md` 100 % LF. Latent: currently 37,734 B against a 38,912 B
   budget, and every possible state passes today.
2. **The gate's approval marker** (`dcs/hooks/dcs_gate.py`) sha256s `IAP.md` as
   raw bytes to decide whether source edits are permitted. **This is already
   broken for the one incident that has closed** — the stamp verifies against
   the git blob and fails against the on-disk file.

Manifestation 2 is the serious one: it is the enforcement mechanism, not a
metric. It is inert only because no incident was active when it was found.

## Evidence

- **Live repro in this incident's own worktree.** Creating
  `C:\DCS-wt\hot-path-budget-eol-sensitivity` at commit `12b212f` checked out
  **83 of 83** tracked text files as CRLF, and the hot path measures **37,906 B
  here against 37,734 B in the main checkout — the same commit, 172 B apart.**
  Regenerate: `git ls-files --eol | awk '{print $1,$2}' | sort | uniq -c`, and
  the size command below, in each tree. *(Dispatcher, at worktree creation)*
- **Live mixed state in main, same commit.** `doctrine.md` 22,121 B / 155 CRLF /
  0 bare LF; `schemas.md` 15,613 B / 0 CRLF / 172 bare LF. Regenerate:
  `python -c "b=open('dcs/references/doctrine.md','rb').read(); print(len(b), b.count(b'\r\n'), b.count(b'\n'))"`
  *(both analysts, independently)*
- **The check reads raw size, no normalisation** —
  `tests/test_doctrine_integrity.py:162-166`,
  `hot = os.path.getsize(...doctrine.md) + os.path.getsize(...schemas.md)`.
- **The gate hash is already wrong on disk.** For the closed incident
  `2026-07-25-doctrine-hot-path-trim`: `IAP-APPROVED` line 1 is `a5eec3b4…`;
  `sha256` of the on-disk `IAP.md` is `375c4859…`; `sha256` of
  `git show HEAD:<path>` is `a5eec3b4…`. **The stamp matches the blob and not
  the file.** `git ls-files --eol` reports that path `i/lf w/crlf`.
  *(analyst A; independently re-verified by the Dispatcher before this brief)*
- **The gate reads bytes deliberately.** `dcs/hooks/dcs_gate.py:131-135`
  (`open(path,"rb")`, sha256) and `:166-179` (`marker_valid`). Its own comment
  at `:172-174` already records a *different* byte-representation defect — a
  PowerShell BOM silently failing this same comparison, field lesson
  2026-07-22, worked around with `utf-8-sig`. *(analyst B)*
- **Repo-wide, the index is clean and the working tree is not.** In main:
  `git ls-files --eol` → **68** `i/lf w/lf`, **15** `i/lf w/crlf`, 2 binary.
  Every tracked text file is LF *in git*; 15 have drifted on disk, including
  `doctrine.md`, `doctrine-appendix.md`, `package.json`,
  `tests/test_doctrine_integrity.py`, and **all 8 artifacts of the closed
  incident**.
- **The candidate fix is a no-op in git terms.** In a disposable
  `git clone --no-local`, adding `.gitattributes` with `* text=auto eol=lf` and
  running `git add --renormalize .` produced **zero** diff to any tracked file's
  recorded content — the index is already all-LF. Only future checkouts change.
  *(analyst A, disposable-clone experiment)*
- **But `.gitattributes` does not ship.** `package.json`'s `files` whitelist
  includes `dcs/` and `tests/` and not `.gitattributes` — and an npm install
  performs no git checkout at all. So a `.gitattributes`-only fix protects a
  clone of this repo and **nothing downstream**, while `dcs_gate.py` *does*
  ship. Regenerate:
  `python -c "import json;print(json.load(open('package.json'))['files'])"`.
  *(analyst B — this is the constraint the IC typed against)*
- **Prior art: the third member of a known defect family.** (i) commit
  `d604b4f` stripped BOMs from 5 files after PowerShell `Set-Content` broke
  `dcs_gate.py`'s shebang parse; (ii) the same BOM class broke the IAP hash
  comparison (2026-07-22, the reason for `utf-8-sig`); (iii) commit `0428ac4`
  (v0.6.6) repaired 2.9 M characters of PowerShell double-encoding that the
  existing BOM/U+FFFD guard could not see, and added two *new* invariant checks
  rather than widening the old one. `CLAUDE.md`'s "never PowerShell
  `Set-Content`/`Out-File`" rule exists for this family. *(analyst B)*
- **No `.gitattributes` precedent.** `git log --all -i --grep=gitattributes`
  returns nothing; `vault/Backlog.md:138-140` lists both candidate remedies as
  open and undecided. This incident makes that decision. *(analyst B)*
- **Nothing red today.** In both trees: `test_doctrine_integrity.py` 14/14,
  `test_dcs_gate.py` 25/25, `test_dcs_intake.py` 10/10.
- **No test covers this class.** `tests/test_dcs_gate.py:71-75` builds its
  `IAP.md` fixture with `write_text` and hashes it with `read_bytes` in the same
  process — self-consistent by construction, so it cannot catch a cross-checkout
  mismatch. A grep for `CRLF|newline|autocrlf` across `tests/` returns nothing.
  *(analyst B)*

**Analyst correction, recorded so it is not transcribed onward:** both analysts
reported `HEAD` as `51dd073`. It was `12b212f` at intake
(`git log --oneline -1`). Their file-level measurements were re-verified against
the real HEAD and hold.

## Reproduction path

Deterministic, two ways.

**The measurement instability** — run in main and in this worktree, compare:

```
python -c "import os; d=os.path.getsize('dcs/references/doctrine.md'); s=os.path.getsize('dcs/references/schemas.md'); print(d, s, d+s)"
```

At commit `12b212f`: main → `22121 15613 37734`; this worktree →
`22121 15785 37906`.

**The gate-hash break**, which is the one that matters:

```
D=.dcs/incidents/2026-07-25-doctrine-hot-path-trim
head -1 $D/IAP-APPROVED
python -c "import hashlib;print(hashlib.sha256(open('$D/IAP.md','rb').read()).hexdigest())"
git show HEAD:$D/IAP.md | python -c "import hashlib,sys;print(hashlib.sha256(sys.stdin.buffer.read()).hexdigest())"
```

Line 1 and line 3 agree; line 2 differs. **The stamp verifies against git and
not against the file it names.**

## Blast radius (best guess at intake)

Territory as typed by the IC at command point 1 — **all five items**:

1. `.gitattributes` — **new file**, the line-ending policy itself
2. `tests/test_doctrine_integrity.py` — normalise the hot-path measurement
3. `dcs/hooks/dcs_gate.py` — hash normalised bytes rather than trusting the tree
4. `tests/test_dcs_gate.py` — a cross-EOL fixture proving it
5. a `git add --renormalize` pass over the working tree

**Item 5 has repo-wide reach by construction** — a renormalise touches every
tracked text file. Nothing else may be `ACTIVE` while it runs, and the register's
territory column records that honestly rather than pretending the territory is
five paths.

Explicitly **out of scope** (separate root cause, already registered as part of
rank 2 `schemas-md-trim`): the **kB-granularity band** — `HOT_PATH_BUDGET_KB` is
an integer kB, so an acceptance bar finer than 1,024 B cannot be enforced. That
is ratchet *resolution*, not *which bytes get measured*. **This incident must not
change `HOT_PATH_BUDGET_KB`'s value.**

Read-only but constraining: `install.ps1` / `install.sh` (byte-for-byte copies —
they propagate whatever is on disk), `package.json`'s `files` whitelist,
`dcs/references/doctrine.md`, `dcs/references/schemas.md`.

## The hazard that shapes the plan

**This incident's own fix can invalidate this incident's own approval marker.**
Adding `.gitattributes` and renormalising rewrites working-tree files. If that
runs inside a worktree holding a live `IAP.md`, its bytes change, its sha256
changes, and `IAP-APPROVED` stops matching — the gate slams shut mid-execution on
a plan that was validly approved.

Every prior artifact is already in this state. The incident must be planned so it
does not add itself to the list. The IC named this a sequencing problem for the
Logistics Chief, not a scope problem — see "Type + rationale".

## Prior art

`vault/Backlog.md` item 8 (register rank 1) states the defect and names both
candidate remedies without choosing. `vault/Meta/building-dcs-lessons.md` §8
carries it as a field lesson; `vault/Metrics/incident-metrics.md` carries it as a
standing caveat on every historical size figure ("this metric currently has no
stable definition"). It was discovered at plan time inside
`doctrine-hot-path-trim` and deliberately registered rather than absorbed
(principle 4) — that incident then paid for it anyway, at escalation trigger (a),
when its ratchet landed 18 B red on the merge result
(`.dcs/esg/SITREPS/doctrine-hot-path-trim-p1-merge.md`).

## Type + rationale

**Proposed type:** 1

**Rationale (IC — `dcs-commander`, Fable seat, command point 1):** Territory is
all five items because the analysts proved **`.gitattributes` does not ship while
the already-broken gate hash does** — verified: the closed incident's marker
matches the git blob `a5eec3b4`, not the on-disk file `375c4859` — so the
root-cause fix must live in the gate itself, which puts `dcs_gate.py` and its
guarding tests in scope, triggering `CLAUDE.md`'s Type 1 clause. Independently,
changing the bytes the gate hashes **migrates the approval-marker contract**, and
the self-invalidation hazard demands exactly the deploy-ordering and rollback
discipline `typing.md` reserves for Type 1.

The IC's three grounds, verbatim in substance: (1) `CLAUDE.md`'s explicit clause —
`dcs_gate.py` and `test_dcs_gate.py` are "the enforcement mechanism itself";
(2) `typing.md`'s own Type 1 examples name the gate hook as shared cross-cutting
infrastructure, and changing what bytes it hashes changes the validity contract
of every existing `IAP-APPROVED` marker; (3) the migration hazard is "anything
requiring a deploy-ordering decision… or a rollback plan" verbatim. It added that
a tree-only fix "repairs the symptom where we happen to live and ships the defect
everywhere else."

**Open question carried forward from the IC (sequencing, not typing):** the
renormalise pass must be ordered so it cannot rewrite this incident's own live
`IAP.md` after approval — either land gate normalisation first, run the
renormalise as the final tasking with a marker re-stamp, or exclude `.dcs/` from
renormalisation.

**Owner confirmation:** confirmed as proposed (Type 1), 2026-07-25. The Owner was
shown the register's original Type 3 assumption and the two narrower alternatives
(Type 3 narrow scope; Type 3 now with the gate fix split into its own Type 1) and
chose the IC's proposal.

## Intake source (for /dcs-close to route back to)

`/dcs-run` from the Owner ("fix the line-ending sensitivity in the hot-path
budget check") — register rank 1 `hot-path-budget-eol-sensitivity`, itself from
`vault/Backlog.md` item 8.
