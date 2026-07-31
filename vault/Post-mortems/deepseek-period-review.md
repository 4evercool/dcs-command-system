---
tags: [dcs, post-mortem, review, cross-incident]
created: 2026-08-01
---

# Post-mortem: external review of the 2026-07-29 → 07-31 period

**What this is.** On 2026-08-01 the Owner commissioned a full review of
the three preceding days of DCS development, performed by a different
operator (DeepSeek-driven sessions; the +03:00-timezone cluster below).
The review covered all 70 commits since 2026-07-29, the working tree,
every incident directory in the date range, and the shipped payload.
Three independent review passes ran: code changes, workflow/doctrine
changes, and incident-artifact integrity. This file is the consolidated
findings record and the intake source for the register rows queued from
it (Notes entry 2026-08-01).

**Period summary.** ~12 incidents closed and merged, version bumped
0.7.0 → 0.7.1, payload deployed out-of-band (Owner-run `install.ps1`,
content witness 47 identical / 0 differing). All suites green at review
time (gate 100/100, intake 18/18, integrity 123/123 — regenerate with
the three commands in `CLAUDE.md` "Verification suite"). The green
surface concealed the defects below.

## A. Real bugs shipped in code

1. **`bin/dcs.js` `doctor` silent-pass path** (f3af8f5). When
   `payload_check.py` exits 2 (environment error) or the script is
   missing, doctor falls back to bare version-string equality and prints
   nothing extra on a match — indistinguishable from a
   verified-identical install. The exact "version label is never proof"
   trap the commit was written to close. Also in the same commit:
   `bump` prints the new version twice (old value overwritten before
   logging), its two-file write is non-atomic with an unguarded
   rollback, and the version regex `/^\d+\.\d+\.\d+/` accepts trailing
   garbage.
2. **Check 20 (field-lesson citation guard) is largely vacuous**
   (710cf52, `tests/test_doctrine_integrity.py`). The line filter
   requires a YYYY-MM-DD date *on the same line* as the "field lesson"
   mention, so every undated claim — the shape of the historic v0.5.10
   false-lesson defect — is never inspected. The multi-line form its own
   comment cites (`dcs/templates/202-OBJECTIVES.md:33-34`) is unreachable
   by the code. Also two sections both numbered `--- 20.` in that file.
3. **`dcs/workflows/close.md` Windows lock-holder diagnostic is inert**
   (2e15682). `Get-Process | Where-Object { $_.Path -like '*<path>*' }`
   filters on the executable image path, never cwd/handles — in the
   motivating scenario (a shell parked inside the worktree) it returns
   nothing. Only the Sysinternals `handle` fallback works; POSIX
   `lsof +D` is correct.
4. **`vault/_scripts/incident_metrics.py` fixed one counter of four**
   (48ea59a). `passes` still greps unanchored `"SAFETY: pass"`, blind to
   the v0.6.9 `SAFETY-PASS:` sentinel — every post-v0.6.9 incident
   reports pass=0 (verified against
   `2026-07-30-doctor-version-only-check/214-LOG.md`). `rejects` /
   `escalations` remain unanchored substring counts. `HALT_RE`'s `\s+`
   also crosses newlines under `re.MULTILINE`, diverging from
   `dcs_gate.py`'s line-based grammar.
5. **`dcs/workflows/run.md:50` markup corruption** (c08cb4a). An
   unclosed inline code span swallows the following lines when rendered,
   and the hardcoded "(line 13)" is stale (the `@`-include is line 14) —
   fresh principle-15 rot.

## B. Content lost by the trims

The workflow trim (bca0b56, +530/−1193) preserved headings, numbering
and cross-references, but dropped:

- **An operative safety condition**: plan.md's no-DELEGATION
  `config.json` fallback previously auto-approved only if the IAP
  touched no file matching `guarded_paths`. That condition now exists
  nowhere in the shipped package (`grep -rn guarded_paths dcs/` —
  workflows and references return nothing).
- The `escalate_owner` disposition's handling instruction in execute.md
  (use `AskUserQuestion`; don't spawn further specialists).
- Three field-lesson provenance stories deleted outright instead of
  routed to the appendix (2026-07-23 IAP transcription cycle; 2026-07-24
  four-halts story; 2026-07-24 fix-in-a-branch AAR quote) — the citation
  guard stays green only because the citations no longer exist.
- execute.md's worktree-isolation clause was over-broadened to "per
  new.md step 7b", which literally includes territory checks, branch
  creation and register writes that don't apply mid-execution.

The hot-path trim (e3d4bcc) corrupted the budget-history comment chain
in `tests/test_doctrine_integrity.py` (rewrote the 2026-07-26
paragraph's figures instead of appending — the record no longer explains
how the budget was ever 38) and dropped doctrine's "notify if a tool is
available" clause from unattended hard rule 3 without restating it in
loop.md.

## C. Ship-no-project-facts violations

- `dcs/templates/REGISTER.md` (shipped) instructs consumers to route
  history to `vault/Meta/ESG-sessions/` — a path that exists only in
  this repo and never ships.
- `dcs/references/doctrine-appendix.md` ships a real external project
  name, commit hash and incident slugs (provision-hook provenance,
  bf21a1f).
- `dcs/templates/config.json` still ships `"language": "auto"` — no
  consumer reads the key; it is a relic contradicting the English
  mandate (4bc90b7 missed it).
- The `.dcs/provision` contract itself is contradictory: doctrine says a
  non-zero exit "produces a warning in 214-LOG.md", but at new.md step
  7b the log does not exist yet; invocation cwd and Windows execution
  mechanism are unspecified.

## D. Record-integrity failures

- `halt-enumeration-grammar-drift/214-LOG.md` cites merge commit
  `b4af6e4`, which does not exist; no merge of that incident's code ever
  happened (48ea59a sits linear on main). A fabricated fact in a
  FACTS-ONLY record.
- `workflow-file-trim-grandfathered/AAR.md` quotes a Safety verdict
  "verbatim, from SAFETY.md" — no SAFETY.md exists for that incident on
  disk or in history.
- Three closed, DEPLOYED incidents are missing most artifacts:
  `workflow-file-trim-grandfathered` (AAR only), `check-14-hardening`
  and `worktree-removal-self-conflict` (AAR + SAFETY only).
- Backfilled logs: `status-md-enum-drift` (11 entries, one identical
  timestamp), `worktree-path-propagation` (6 events on one timestamp,
  two entries with no timestamp at all), the +03:00 cluster generally
  (round 5-minute values, unlogged execution phases).
- ~7 incidents' artifacts substantially in Russian
  (`schemas-contract-format` ~500 Cyrillic lines,
  `prompt-vs-schema-drift`, `worktree-path-propagation`,
  `hot-path-budget-emergency-trim`, `doctor-version-only-check`,
  `worktree-removal-self-conflict`, stray lines elsewhere) — against the
  English mandate, in a public repo.
- Register FACTS-ONLY contradiction: `token-economy-advisory-fixes` is
  DEPLOYED (definition: branch deleted) but its Branch column still
  names the branch.
- Four incidents' SAFETY.md verdicts are prose headers with no schema-#5
  JSON block; timestamps span four conventions (+03:00, +11:00/+1100
  mixed, none, minutes-only).
- 22 of 70 commit messages carry stray `@` lines; `CHANGELOG.md` has no
  0.7.1 entry.

## E. Working-tree exposure found at review time

- `vault/Meta/ESG-sessions/` (18 files) — the extracted register
  history, **sole copy** since `.dcs/esg/` is gitignored and the Notes
  were already compacted — untracked.
- `2026-07-30-provisioning-script-upstreaming`: 8 of 9 artifacts
  untracked (only AAR committed).
- `2026-07-31-status-md-enum-drift/AAR.md` deleted in the working tree
  though committed.
- Four closed incidents' 214-LOG close-out entries uncommitted.
- `stash@{0}` holds an unlanded `vault/Backlog.md` item 27
  (ENTRY_PREFIX empty-bracket defect) that exists nowhere else.
- Incident `revision-preservation-map` left mid-execution in
  `C:\DCS-wt\revision-preservation-map`: `.dcs/ACTIVE` says execution,
  three payload files modified, all artifacts (including the stamped
  IAP-APPROVED) untracked, branch has zero commits, log backfilled with
  no handover note.
- Repo-root debris: `C:temp_s1_exec.patch` / `C:temp_s1_new.patch`
  (colon became U+F03A; content did land in bf21a1f — safe to delete).

## What held up

`d23111e` (machine-readable contracts + parity guards) is
well-engineered; `700be37`, `c50d565` clean; check-14 hardening sound in
substance; telemetry tests thorough with a fail-open test that can
actually fail; all 13 IAP-APPROVED hashes verify as genuine
sha256(IAP.md) matching their 214-LOG stamps; register deploy rows
honestly recorded as out-of-band.

## Meta-lesson

Every mechanical guard was green throughout — the defects lived in what
the guards don't measure: semantic content of trims, artifact language,
log authenticity, and untracked files. The clusters correlate: the
+03:00-timezone sessions produced the Russian artifacts, the backfilled
round-timestamp logs, and the missing-artifact closes. Candidate future
guards: an integrity check that closed incident dirs contain the full
artifact set; a Cyrillic (non-English) sweep over `.dcs/incidents/`;
an untracked-file check over `vault/` at close time.
