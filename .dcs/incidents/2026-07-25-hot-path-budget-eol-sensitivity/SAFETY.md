# SAFETY — Operational Period 1

**Incident:** hot-path-budget-eol-sensitivity
**Period:** 1
**Verdict:** **`pass`**, zero refutations, **seven advisories** — the first
verdict in this repo to exercise v0.6.5's advisory path.

---

## Verdict — verbatim

**`verdict: pass`** · **`refutations: []`**

### The officer's bottom line, verbatim

> All nine in-period acceptance criteria are met, and criterion 4 — the one I
> was told to attack hardest — survives an exhaustive assault: 13,120
> uniform-conversion combos with zero violations, 1.19 million text pairs with
> zero leakage, and 8/8 correct verdicts through the real hook binary. I
> reconstructed criterion 5's red-before myself rather than trusting the paste,
> and it landed exactly as claimed. No forbidden-zone violations; the 83-file
> re-materialisation lost nothing.

### checks_run — verbatim

- Read the full `git diff` for all 7 modified files plus the untracked `.gitattributes`; `od -c` confirmed it is exactly `* text=auto eol=lf\n` (19 bytes).
- **C1:** ran the 202's `git check-attr` command — all three paths return `text: auto` / `eol: lf`, none unspecified.
- **C2:** ran the census — `83 i/lf w/lf` + `2 i/none w/none`, **zero `w/crlf` rows**. (83 not 84 solely because `.gitattributes` is untracked.)
- **C3a:** normalised measurement returns exactly `21966 15613 37579`. **Proved tree-independence empirically:** same commit `12b212f`, `C:\DCS` raw is `22121 15613` vs worktree raw `21966 15613`, yet the normalised measure gives identical `21966 15613 37579` in BOTH trees.
- **C4:** exhaustive brute force — 3,280 logical contents × 4 uniform stamp/disk combos = **13,120 cases, 0 violations.** Verified the in-memory model matched the real `approval_digests` on 300 random inputs first.
- **C4 leakage:** 1,194,649 text pairs × 4 representations — **0** cases where genuinely different logical text was accepted.
- **C4 end-to-end through the real `.claude/hooks/dcs_gate.py` binary:** 8/8 correct, including LF-stamp/CRLF-disk allow, CRLF-stamp/LF-disk allow, tampered-in-both-representations deny, and lone-CR-edited deny.
- **C4 invariant-not-instance:** grepped the gate test for any 64-hex literal — none. Digests are computed at runtime from fixture bytes. Confirmed the new fixture uses `write_bytes` exclusively.
- **C5 red-before RECONSTRUCTED independently** (not trusting S2's paste): checked out HEAD's `dcs_gate.py` into a scratch tree, ran the NEW test file against it → **30/32 with exactly the two predicted failures** (stamp=LF/disk=CRLF, stamp=CRLF/disk=LF), negative controls green before the fix, proving the test discriminates.
- **C6:** ran the three-line archived-stamp comparison — all three print `a5eec3b4de96e18be…`. **Archive healed.**
- **C7:** cloned to a throwaway path twice (checked 15 GB free first). Clone of current HEAD reproduces `83 i/lf w/crlf`; clone of a commit including `.gitattributes` gives `84 i/lf w/lf` + `2 i/none w/none` with `check-attr` returning `eol: lf`, **despite system-wide `core.autocrlf=true`**. Both clones deleted.
- **C8:** re-ran all three suites — `15/15`, `32/32`, `10/10`, all exit 0.
- **C9:** `HOT_PATH_BUDGET_KB = 38`; the assignment line is untouched. **Verified the VALUE, not just an empty grep.**
- **Re-materialisation integrity:** `git diff --name-only` lists exactly the 7 territory files; `--ignore-cr-at-eol` gives an identical stat, so the 83-file delete-and-recheckout produced **zero** stray content churn.
- **Territory audit:** the complete changed set is exactly the 8 files across S1–S4's territories. `plan.md`, `install.ps1`, `install.sh`, `package.json`, `dcs/VERSION` all untouched. No forbidden-zone violation.
- **S2/S4 semantic agreement verified by EXECUTION, not prose:** ran `execute.md`'s snippet verbatim against the real archived IAP and compared to the gate's `approval_digests` on the same file — both produce the identical set, and the stamp is a member.
- Ran the documented snippet under **both Git Bash and PowerShell** (via a script file, to avoid quoting artifacts) — works correctly in both. No broken runbook command.
- Independently confirmed the two gate copies byte-identical and containing no CR at all.
- **Check 10 non-vacuity:** it scans 59 real files, reuses check 9's scoping (`vault/` and `.dcs/` correctly out of reach), and uses `read_bytes` so it does not skip on decode failure. Verified its stated premise with `npm pack --dry-run`: `.gitattributes` is absent from the `files` whitelist and does not ship.
- Audited the check-enumeration census: docstring items 1–11 match the code's `# --- N.` sections exactly, contiguous and accurate.
- Measured pre- vs post-incident suite counts by running HEAD's test files in a scratch mirror: gate 25 → 32, integrity 14 → 15.
- Verified **this incident's OWN approval marker survived** the re-materialisation — stamp `127cd46f…` is the first member of its digest set.

### observations — verbatim

- **S3's scope disclosure is acceptable in-territory tidying, not drift.** Its tasking required the docstring list to "include the new check"; adding only entry 10 would have left the enumeration reading 1–8 then 10 — incoherent and, under principle 15, a false census. Adding 9 and 11 makes it complete and true, stays inside its one file, and was disclosed.
- The 201 repro **no longer reproduces** for the mechanism that matters: the check gives the same number in two genuinely different checkouts of the same commit, and the archived stamp verifies again. Criterion 3b's residual raw-getsize gap is the explicitly-deferred `[IC]` item — `C:\DCS` still needs its post-merge re-materialisation.
- Criterion 2's predicted target of 84 will be met at the integration commit; the current 83 is the same set plus the untracked `.gitattributes`, confirmed in the clone test.
- **The writer/reader split is coherent by design:** the IC keeps stamping a raw-bytes digest (`plan.md` unchanged), and raw is always a member by construction — so the widening is read-side only and cannot produce a stamp the gate later rejects.
- The pre-existing `write_text` fixtures were correctly left alone — they remain self-consistent, and rewriting them would have been churn outside the tasking.

---

## Advisories and their resolution

Per `execute.md` v0.6.5, a `pass` carrying advisories is a normal, healthy
verdict: **the IC fixes them itself and folds them into the integration
commit.** All seven were resolved before the commit; none required a
fix-tasking or a re-verify.

| # | Advisory | Resolution |
|---|---|---|
| 1 | **`.gitattributes` is UNTRACKED.** `git commit -a` silently omits it, and every in-worktree criterion reads green either way. The officer demonstrated both halves: a clone of today's HEAD reproduces the full `83 i/lf w/crlf` defect; a clone including the file is clean at `84 i/lf w/lf`. | **`git add .gitattributes` explicitly** in the integration commit, and verified with `git show --stat` afterwards. This was the single highest-value finding of the review — it would have silently voided the entire deliverable. |
| 2 | Budget derivation both **arithmetically wrong and stale**: `ceil(37906/1024) + 1 = 38` — that expression is **39**, and 37,906 was the raw-CRLF basis this incident replaced. | Comment re-based onto the normalised measure: `ceil(37579/1024) + 1 = 38`, which is correct arithmetic *and* the current basis. The error is recorded in the comment rather than quietly overwritten. `HOT_PATH_BUDGET_KB` stays **38**. |
| 3 | "bites ~1.2 kB sooner than the 42 kB it replaces" — the gap is **4 kB**. | Corrected to 4 kB. |
| 4 | `CLAUDE.md`'s suite counts stale: `25 cases` → actually 32, `12 checks` → actually 15 (already wrong before this incident). | **The counts were removed rather than updated**, and replaced with an instruction to read each suite's own `N/M passed`. A case count is a derived fact with a lifetime; replacing one rotting number with another only resets the clock. |
| 5 | `plan.md:348-349` still describes the gate as computing "a plain sha256 of the file's bytes". | **Not fixed — registered.** The IC ruled `plan.md` forbidden at command point 2 precisely because its raw stamp is a member by construction. The *instruction* remains correct and safe; only the descriptive parenthetical is stale. Registered as a follow-up. |
| 6 | `approval_digests`' docstring claim that files differing by a real CR "must still hash apart" has a **narrow counterexample**: a CR immediately preceding a CRLF, since `lf()` folds `X\r\r\n` and `X\r\n` alike. One-way, and the officer's own sweep bounded it — no genuinely different logical content is ever accepted. | Docstring qualified with the exception, its one-way direction, the bound the sweep established, and the note that it is **git's own fold** that is lossy there, not this function. Mirrored to `.claude/hooks/`; copies re-verified byte-identical. |
| 7 | `execute.md` / `status.md` say "any of the three", but the set dedups to two for a pure-LF file. | Both reworded to "any **member** of that set — up to three… fewer when those forms coincide", naming the pure-LF case explicitly. |

**Files the IC touched applying advisories:** `tests/test_doctrine_integrity.py`
(2, 3), `dcs/hooks/dcs_gate.py` + `.claude/hooks/dcs_gate.py` (6),
`dcs/workflows/execute.md`, `dcs/workflows/status.md` (7), and **`CLAUDE.md`
(4) — which is outside every specialist territory.** `CLAUDE.md` is unguarded
in `.dcs/config.json` and this is IC work, but it is recorded here plainly
rather than left to be noticed in the diff.

**Re-verified after the advisory fixes** (the officer's pass stands; this
confirms the fixes broke nothing): `py_compile` OK on both gate copies, `diff`
empty, suites **15/15 · 32/32 · 10/10**, `HOT_PATH_BUDGET_KB = 38`, and no
tracked file contains CRLF.

## Criteria state at pass

| # | Criterion | State |
|---|---|---|
| 1 | `.gitattributes` present, definite `eol: lf` | **MET** |
| 2 | No `w/crlf` row | **MET** — `83 i/lf w/lf`, → 84 once `.gitattributes` is committed |
| 3a | The check is tree-independent | **MET** — identical `37579` in two genuinely different checkouts |
| 3b | Raw `getsize` agrees between trees | **[IC], at close** — `C:\DCS` still needs its post-merge re-materialisation |
| 4 | Gate verdict independent of line endings, as an invariant | **MET** — 13,120 cases, 0 violations; 1.19 M text pairs, 0 leakage |
| 5 | Regression test red against the old implementation | **MET** — reconstructed independently, 30/32 with exactly the two predicted failures |
| 6 | Archived stamp verifies again | **MET** — all three digests agree at `a5eec3b4` |
| 7 | A fresh clone is clean | **MET** — verified in a throwaway clone despite `core.autocrlf=true` |
| 8 | All three suites green | **MET** — 15/15, 32/32, 10/10 |
| 9 | `HOT_PATH_BUDGET_KB` value unchanged | **MET** — 38, assignment untouched |
| 10 | Owner end-to-end confirmation | **Pending — the close gate** |
| 11 | Version decided at merge | **[IC]**, at merge |
| 12 | Deploy marker | **[deploy period]** |
