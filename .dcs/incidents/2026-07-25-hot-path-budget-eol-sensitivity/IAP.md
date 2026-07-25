# IAP — Incident Action Plan

**Incident:** hot-path-budget-eol-sensitivity
**Type:** 1
**Operational period:** 1
**Links:** `202-OBJECTIVES.md` · `203-ORG.md` · `204-TASKING/{S1,S2,S3,S4}.md` · logistics plan below

## Objectives (summary of 202)

**Goal.** The repo has **one line-ending policy**, and no byte-exact mechanism can
give a different answer in a different checkout of the same commit. Two things
must stop being true: that `git ls-files --eol` reports a mixture, and that the
gate's approval hash depends on which tree materialised the file. The second is
the one that matters — it is the enforcement mechanism, it is already broken for
the incident that closed today, and unlike the size check it **ships**.

**Owner-decided policy:** `* text=auto eol=lf` — LF in every checkout on every
OS. The native-EOL alternative was declined: it would leave the gate hash
diverging *across* platforms (and `dcs_gate.py` ships to any OS) and would not
heal the archived stamp.

**Acceptance criteria** (full text in `202-OBJECTIVES.md`; ownership tags shown):

| # | Criterion | Owner |
|---|---|---|
| 1 | `.gitattributes` present, `text: auto` / `eol: lf`, none `unspecified` | S1 |
| 2 | `git ls-files --eol` shows **no `w/crlf` row** in this worktree (target `84 i/lf w/lf`) | **[IC]** |
| 3a | The hot-path check is **tree-independent** — normalised byte count, target `21966 15613 37579` | S3 |
| 3b | Raw `getsize` agrees between this worktree and `C:\DCS` | **[IC]**, at close |
| 4 | The gate's verdict does not depend on line endings — **asserted as an invariant, never a pinned hash** | S2 |
| 5 | A regression test that **fails against the current implementation**, demonstrated | S2 |
| 6 | The archived stamp verifies again (`a5eec3b4` = on-disk = blob) | **[IC]** |
| 7 | A fresh clone is clean too | **[IC]** |
| 8 | All three suites green | S2, S3, S4 |
| 9 | `HOT_PATH_BUDGET_KB`'s **value** unchanged at 38 | S3 |
| 10 | Owner confirms LF-in-working-tree on Windows is acceptable | **[Owner]** |
| 11 | Version decided **at merge**, not claimed here | **[IC]** |
| 12 | `~/.claude/dcs/VERSION` matches after deploy | **[deploy period]** |

*Criteria 2, 3b, 6 and 7 were tagged `[IC]` and criterion 3 was split during
lint — untagged, all four would have surfaced as a false Safety halt at the end
of the period.*

## Tactics (from the Planning Chief)

**T1 — Policy.** A single unqualified line, `* text=auto eol=lf`, with **no
`.dcs/` exception.** Verified in a throwaway clone: `git check-attr` then returns
`text: auto` / `eol: lf` for `doctrine.md`, `dcs_gate.py` **and**
`.dcs/incidents/…/IAP.md`, and `text=auto` content detection correctly leaves the
two binary files as `i/none w/none` — no binary override rules needed.

**T2 — The gate's contract, stated precisely because the specialist implements
exactly this.** Replace `sha256_of` with `approval_digests(path)` returning the
deduped sha256 of `raw`, `lf = raw.replace(b'\r\n', b'\n')`, and
`crlf = lf.replace(b'\n', b'\r\n')` — **crlf derived from lf, never raw**, or
existing CRLF doubles into `\r\r\n`. `marker_valid` becomes
`stored_hash in approval_digests(iap)`. **Only `\r\n` is folded; a lone `\r` is
left untouched in all three forms**, so two files differing by a real CR still
hash apart — the equivalence class widens by exactly the git text-conversion the
policy declares and not one byte more.

*Backward compatibility, case by case:* (i) stamped LF / disk LF — allowed
before and after; (ii) **stamped LF / disk CRLF — the already-broken archived
case** — denied before, allowed after (measured on the real artifact: the LF
digest **is** `a5eec3b4`, the archived stamp); (iii) stamped CRLF / disk LF —
denied before, allowed after; (iv) stamped CRLF / disk CRLF — allowed before and
after; (v) genuinely edited content — **denied before and after**, verified both
directions; (vi) mixed-EOL stamp — exact-byte match only, unchanged.

**The key safety property:** the new `marker_valid` returns `True` wherever the
old one did (`raw` is always a member), so **no valid approval anywhere can be
broken** — it can only ever allow more.

**T3 — Measurement.** Replace the two `os.path.getsize` calls with a normalised
byte count. Deliberately **no git dependency**: `tests/` ships in `package.json`'s
`files` whitelist and must run where there is no repo.

**T4 — Enforcement that actually ships.** `.gitattributes` is **not** in the
`files` whitelist and npm performs no checkout, so it protects a clone of this
repo and nothing downstream. `tests/test_doctrine_integrity.py` **does** ship. So
add **one new check** — no file in the shipped set contains `b'\r\n'` — scoped
exactly like check 9. Follows `0428ac4`'s precedent: a new check, never a widened
old one. Do **not** assert `.gitattributes`'s presence inside it; that would go
red in an npm-installed tree.

**T5 — The re-materialisation is IC work, not a tasking.** Three independent
reasons, all measured: (a) `.gitattributes` + `git add --renormalize .` is a
**complete no-op** here — the index is already all-LF; what actually clears
`w/crlf` re-materialises 83 files across every directory **including `.dcs/`**,
barred to specialists, and the only honest glob is `**/*`, which is the absence
of a territory; (b) it is neither an Edit nor a Write, so `dcs_gate.py` never
adjudicates it and "declared territory" buys nothing even nominally; (c) it
**destroys uncommitted tracked changes**, so it may only run when someone knows
the whole tree's state — the IC, never a specialist holding one glob.

**T6 — Ordering.** Wave 1: S1 alone → **IC re-materialisation** → Wave 2: S2 ‖
S3 ‖ S4. See "IC rulings" for why this beats the Logistics ordering.

## File-territory partition

| Specialist | Territory | Forbidden |
|---|---|---|
| S1 | `.gitattributes` | everything else |
| S2 | `dcs/hooks/dcs_gate.py`, `.claude/hooks/dcs_gate.py`, `tests/test_dcs_gate.py` | S1/S3/S4's territories; `dcs/hooks/dcs_intake.py`, `dcs/templates/**`, `agents/**`, `skills/**`, `bin/**`, `install.*`, `package.json`, `.dcs/**`, `vault/**`, `docs/**` |
| S3 | `tests/test_doctrine_integrity.py` | S1/S2/S4's; `dcs/VERSION`, and the rest as above |
| S4 | `dcs/workflows/execute.md`, `dcs/workflows/status.md`, `dcs/references/forms.md` | **`dcs/workflows/plan.md` explicitly**; all other `dcs/workflows/*.md` and `dcs/references/*.md`; S1/S2/S3's; and the rest as above |

**Partition status:** **disjoint by file**, not merely by glob — no file appears
in two territories and no glob of one tasking can match a file of another.
IC-verified including the S4 extension. `partition_ok: true`.

**Execution mode: two waves with an IC step between**, not plain parallel — which
is why `203-ORG.md` is written rather than skipped.

## Deploy / environment plan (Type 1, from the Logistics Chief)

**Deploy path — unchanged, and verified rather than assumed.**
`powershell -ExecutionPolicy Bypass -File C:\DCS\install.ps1`, marker
`~/.claude/dcs/VERSION`, after `/dcs-close` and never while an incident is
active. **LF impact: none.** `install.ps1` is *already* LF-only today
(0 CRLF / 20 LF / 1176 B) and produced the currently-installed 0.6.7. A BOM-less
LF-only `.ps1` exercising `if` blocks, a `ForEach-Object` pipeline, `$()`
subexpressions and `Get-Content` ran clean under PowerShell **5.1.26100.8894**,
exit 0. `install.sh`, `bin/dcs.js` and `dcs/hooks/*.py` are already LF. robocopy
and `fs.cpSync` are byte copies, EOL-agnostic. **Nothing reads `~/.claude/dcs/`
byte-exactly** — grep for `expanduser` / `USERPROFILE` / `homedir` across
`tests/` and `dcs/hooks/`: zero hits. Rehearsed via
`DCS_PKG_ROOT=<LF clone> DCS_CLAUDE_DIR=<scratch> node bin/dcs.js install` →
byte-identical payload, green `doctor`. `install.ps1` itself deliberately **not**
run (incident active).

**Environment / dependencies.** No new dependency, no new env var, no npm
package, hooks stay stdlib-only. **Do not touch `core.autocrlf`** — it stays
`true` and is correctly overridden by the attribute (proven: a fresh clone with
autocrlf still set came out `84 i/lf w/lf`). Verified on git 2.53.0.windows.3;
`eol` has existed since git 1.7.2, but an older git could not be tested here —
**git ≥ 2.10 is stated as a requirement, not a verified floor.** No binary-safety
rules needed. `.gitattributes` is **not** to be added to `package.json`'s `files`
whitelist (out of scope; T4's shipped check is the deliberate substitute).

**Migration ordering (binding, as amended by the IC).**

1. **S1** — create `.gitattributes`. Gate risk: zero; changes nothing on disk.
2. **IC re-materialisation** of this worktree. Precondition:
   `git status --porcelain --untracked-files=no` **must be empty.**
   **Path-scoped form is mandatory:**

   ```
   git ls-files --eol | grep 'w/crlf' | sed 's/^[^\t]*\t//' > <scratch>/stale.txt
   while IFS= read -r f; do rm -f "$f"; git checkout -- "$f"; done < <scratch>/stale.txt
   ```

   Expect `84 i/lf w/lf` + `2 i/none w/none`. Then re-verify criterion 6's three
   digests and **this incident's own `IAP.md` against `IAP-APPROVED`** before
   spawning Wave 2. The stale list is written to the session scratchpad, **not**
   the repo.
3. **S2 ‖ S3 ‖ S4.**
4. Close: commit artifacts → merge-time guard → `git merge --no-ff` into `C:\DCS`.
5. **Stage 8 — post-merge re-materialisation of `C:\DCS`. Binding.**

**Struck by IC directive:** the Logistics Chief's Stage 4 (a separate renormalise
commit — measured no-op) and Stage 6 (mid-incident live-hook swap in `C:\DCS` —
the merge propagates it instead).

**Rollback plan.** **Additive — no down-migration should be written**, and that
is a conclusion, not an empty field. The renormalise commit changes **zero blob
contents** (`git diff --cached --numstat` yields only `1 0 .gitattributes`); the
index was already all-LF, so there is no data transformation to reverse.
Rollback is **not symmetric, and the asymmetry runs the safe way**: the tracked
side reverts cleanly, while the working-tree side stays LF with a *clean*
`git status`, because LF is what the index always held. The pre-state was an
accidental *mixture* — there is nothing anyone wants restored, and no command
short of re-corrupting the tree would restore it. **The archived stamp stays
healed even if `.gitattributes` is removed** — a one-way change in the desired
direction.

- Undo the merge: `git -C C:\DCS revert -m 1 <merge-sha>`
- Undo the deploy: restore `dcs/VERSION` **and** `package.json` in one commit,
  re-run `install.ps1`, verify the marker reads the prior version
- Rollback reference: branch `dcs/hot-path-budget-eol-sensitivity`, kept until
  `/dcs-deploy` confirms the merge shipped
- **Do not attempt to restore CRLF.**

## IC rulings — binding on execution (command point 2)

**(1) Ordering — Planning Chief's, not Logistics'.** Decided on measured fact:
**83 files in this worktree are `w/crlf`, 54 of them in shipped scope**, so S3's
new check is red until the tree is re-materialised and a specialist could not
deliver green evidence for its own tasking. The Logistics counter-reason ("the
gate invariant must exist before the census changes under it") is **void by its
own measurements** — the re-materialisation is not an Edit or Write so the old
gate never adjudicates it, and this incident's `IAP.md`/`IAP-APPROVED` are
untracked and pure LF, so no census change can move the stamp. Logistics' Stage 4
is a measured no-op and its Stage 6 is a mid-incident enforcement swap; both
struck.

**(2) `.claude/hooks/dcs_gate.py` stays in S2's territory.** The worktree copy
gates only worktree-rooted specialist sessions; the change is a proven superset
so it can only allow more; and excluding it would merge a repo that **ships a
fixed gate beside a stale enforcing copy with nothing to detect the divergence.**
The live `C:\DCS` hook updates via the merge at close — no mid-incident swap.
**The detection hole is closed now, not registered:** S2 adds a test asserting
the two tracked copies are byte-identical.

**(3) Scope gap (E) — extend by one tasking (S4), not a follow-up.**
`execute.md:35` and `status.md:75` both compute a raw sha256 and instruct a hard
**stop** on mismatch; after S2 they would halt `/dcs-execute` on exactly the
drift the gate now tolerates. **Shipping a contract with unmigrated readers is
the canonical non-shippable half-migration.** `plan.md` is **forbidden** — its
raw digest is a member of the accepted set by construction; its `:347-349`
wording imprecision goes to the register.

**(4) Stage 8 is binding, and the path-scoped form is mandatory.** Measured: the
merge leaves `C:\DCS` at 15 stale `w/crlf`, criteria 2/3b/6 unverifiable, and
`test_doctrine_integrity.py` **blind to it** — both 37,734 and 37,579 pass the
budget. That is the failure mode `close.md` step 1a warns about, recurring one
incident later. The git-FAQ form (`git rm --cached -r` + `reset --hard`, or
`git checkout -- .`) **measurably destroys uncommitted work and is forbidden.**

**Registered at close, not fixed here:** (a) `.gitattributes` matches neither
`guarded_paths` nor `unguarded_paths` in `.dcs/config.json`; (b) `CLAUDE.md` doc
drift — "12 checks" vs 14 actual, plus the gate case count once S2 lands;
(c) `plan.md:347-349` wording.

## Risks

1. **The live gate is edited mid-period (S2).** Bounded by superset semantics
   (cannot deny what was allowed), mirror-last discipline, and `py_compile` on
   both copies. Residual: a syntax error there makes the hook exit non-zero with
   a traceback rather than denying — noisy and briefly under-enforcing, not
   session-bricking.
2. **The re-materialisation destroys uncommitted work** if the wrong form is
   used. Both git-FAQ forms wiped a planted edit in the lab. Mitigated by the
   mandatory path-scoped form plus an empty-`porcelain` precondition on **both**
   step 2 and Stage 8.
3. **Stage 8 skipped → `C:\DCS` keeps 15 stale files**, criteria 2/3b/6 fail in
   main while passing in the worktree, and the merge-time guard cannot see it.
   Mitigated by making Stage 8 a binding IC step verified by an explicit census,
   not by the suite.
4. **S2 and S4 must agree on the digest rule.** If they diverge, the gate is
   authoritative and the divergence is a deviation. S4's tasking says so.
5. **Heredoc trap:** authoring `b'\r\n'` literals through a bash heredoc silently
   produces real control characters and a `SyntaxError` — and the gate **fails
   open** on error, so the resulting "allow" looks like a passing test. Both S2's
   and S4's taskings mandate Write/Edit for those literals.
6. **Mixed-EOL stamps are deliberately not healed** — exact-byte match only.
   Accepted residual: they cannot arise from a checkout under the new policy, and
   widening further would be guesswork.
7. **Shape (B) — the IC hand-writing `IAP-APPROVED` — remains an unplanned
   emergency lever, never a routine step.** The gate short-circuits `.dcs/` at
   `:299-300`, so it is always available; that is precisely why it must not be
   planned.
8. **`C:\bread_bot`'s `.claude/hooks/dcs_gate.py` goes stale after deploy**
   (15,806 B, sha `95b30ed6`). Outside this repo; `install.ps1` prints the NOTE
   but `/dcs-deploy` verifies only the VERSION marker. Owner follow-up.
9. **git version:** `* text=auto eol=lf` verified only on 2.53.0.windows.3.
   git ≥ 2.10 stated as a requirement, not a verified floor. No CI exists to break.
10. **Disk space.** This plan was written across an ENOSPC halt (`C:` hit 0 bytes
    free mid-IAP; the Owner cleared 7.5 GB). Two `git clone --no-local` operations
    remain (criterion 7, and the Safety Officer's verification) — hardlink clones,
    so cheap, but not free. Check free space before each rather than discovering
    it as a failed write.

## Verification plan

Run **after all four taskings return and the work is committed** on
`dcs/hot-path-budget-eol-sensitivity`.

1. **The original 201 repro path, both manifestations.** (a) The three digests
   for `.dcs/incidents/2026-07-25-doctrine-hot-path-trim/` must now **all print
   the same value** (baseline `a5eec3b4` / `375c4859` / `a5eec3b4`). (b) Raw
   `getsize` must print `21966 15613 37579` in this worktree, **and** the check
   inside `test_doctrine_integrity.py` must reach the same figure by
   normalisation, independent of what the checkout did.
2. **Tree state:** `git ls-files --eol | awk '{print $1,$2}' | sort | uniq -c` →
   `84 i/lf w/lf` + `2 i/none w/none`, **no `w/crlf` row**; `git status
   --porcelain` clean apart from the untracked incident directory.
3. **Fresh checkout, where the defect actually lives (criterion 7):**
   `git clone --no-local -q <worktree> <scratch>/eolcheck` — verified to carry the
   branch — then run criterion 2's census, the criterion 3 size command (expect
   the **identical** `21966 15613 37579`), the criterion 6 three-way comparison,
   and all three suites. Delete the clone; it is not a deliverable.
4. **All three suites from the worktree root**, not just each specialist's own:
   `test_doctrine_integrity.py` (expect 15/15), `test_dcs_gate.py` (the
   pre-existing 25 plus the new cross-EOL cases **and** the copy-divergence
   case), `test_dcs_intake.py` (10/10).
5. **The invariant, not an instance (criterion 4).** Read `tests/test_dcs_gate.py`
   and confirm the fixture asserts all four stamp×disk combinations **and at
   least two negative controls** where content genuinely changed, and that every
   `IAP.md` in it is built with `write_bytes`. **A test that pins today's digest,
   or omits the negatives, does not prove criterion 4 and should be sent back.**
6. **Red-before is evidence, not narrative (criterion 5).** S2's return must
   contain a **verbatim failing run** taken against the unmodified
   `dcs/hooks/dcs_gate.py`. If it is described rather than pasted, the criterion
   is unmet.
7. **No scope drift.** `git diff --stat` must list exactly `.gitattributes`,
   `dcs/hooks/dcs_gate.py`, `.claude/hooks/dcs_gate.py`, `tests/test_dcs_gate.py`,
   `tests/test_doctrine_integrity.py`, `dcs/workflows/execute.md`,
   `dcs/workflows/status.md`, `dcs/references/forms.md` — **plus** the whole-tree
   representation change from the re-materialisation, which changes no recorded
   content. `HOT_PATH_BUDGET_KB` unchanged at 38. `install.ps1`, `install.sh`,
   `doctrine.md`, `schemas.md`, `package.json` and **`plan.md`** must appear in
   no content diff.
8. **Manual check no test covers:** confirm `dcs/hooks/dcs_gate.py` and
   `.claude/hooks/dcs_gate.py` are byte-identical (`diff`, no output) — and note
   that the gate which actually runs in a *downstream* project is that project's
   own copy, which `install.ps1` does not refresh and says so.
9. **Not verifiable this period:** criterion 3b (needs the merge and Stage 8),
   criterion 10 (Owner's), 11 (settled at merge), 12 (deploy period).

## Deviation history (this period)

none
