# 201 — Incident Brief

**Incident:** record-integrity-corrections
**Opened:** 2026-08-02
**Type:** 3

## Symptom

The Owner-directed external period review (`vault/Post-mortems/deepseek-period-review.md` §D, committed 2026-08-01) found that several already-closed DCS incidents contain false or missing factual claims in their own historical records: a fabricated merge-commit citation, a quote attributed to a file that never existed, and three incidents nearly devoid of their standard artifact set. The sixteenth `/dcs-esg` session (2026-08-02) ranked correcting these #1 in the queue — ahead of building the automated SHA-existence guard (`close-integrity-guard-bundle`, rank 2) that would otherwise be "born red" checking against uncorrected archives — and made this incident's own green-Safety close the written condition for reinstating `auto_approve_type3` (suspended to `false` in Delegation v5 specifically because these fabrications undermine principle 12's premise that IC-logged approvals are honest).

## Evidence

- `.dcs/incidents/2026-07-30-halt-enumeration-grammar-drift/214-LOG.md:37` cites "merge b4af6e4" as this incident's close. `git cat-file -t b4af6e4` fails ("Not a valid object name") and `git log --all --oneline` never mentions it anywhere in this repository's history — fabricated. The incident's code in fact merged to main via two real, independently verified commits instead: `f7e0cc9` (code + close commits) and `838adea` (artifact archive) (situation-analyst finding, git verification; independently re-verified by dcs-commander at command point 1).
- `.dcs/incidents/2026-07-30-workflow-file-trim-grandfathered/AAR.md:44` headers a JSON block "Safety Officer's final verdict (verbatim, from SAFETY.md)". No `SAFETY.md` exists for this incident on disk, and `git log --all --full-history -- "**/workflow-file-trim-grandfathered/SAFETY.md"` returns nothing in this repository's entire history — the "verbatim" attribution is fabricated by construction (situation-analyst findings, both independently confirmed; re-verified by dcs-commander).
- Artifact-completeness census (`ls` + `git log --all --full-history` per missing file, cross-checked against the standard 8-artifact incident set): `workflow-file-trim-grandfathered` holds only `AAR.md` (7 of 8 missing); `2026-07-29-check-14-hardening` and `2026-07-29-worktree-removal-self-conflict` each hold only `AAR.md` + `SAFETY.md` (6 of 8 missing each). Every missing artifact across all three is confirmed **never committed** to this repository under any branch — not moved, not deleted-but-recoverable — so honest annotation, not restoration, is the only available correction. By contrast, `halt-enumeration-grammar-drift`'s only other gap, `203-ORG.md`, is a doctrine-compliant logged skip ("203 skipped (default Type 3 activation)", its own `214-LOG.md:30`) — not a defect, and out of this incident's scope.
- `.dcs/esg/REGISTER.md:135`, `token-economy-advisory-fixes` row: State `DEPLOYED`, but its Branch cell still names `dcs/token-economy-advisory-fixes`, while `git branch -a --list "*token-economy*"` confirms the branch is genuinely gone — the cell contradicts the register's own DEPLOYED/FACTS-ONLY rules (`REGISTER.md:44-50, 68-79`) (both analysts, corroborating; re-verified by dcs-commander).
- **Stale as of this stem — dropped from scope**: the original finding "CHANGELOG.md has no 0.7.1 entry" (`deepseek-period-review.md` §D, committed `064bd5b`, 2026-08-01 07:46) was true when written but overtaken about four hours later, the same day, by an unrelated release-prep commit (`1b1bd81`, refined by `33c2dd4`) that added a complete, well-formed 0.7.1 entry at `CHANGELOG.md:117`. Both analysts and dcs-commander independently confirm the entry exists and predates this stem — **no CHANGELOG write is needed**; this line item is verified-resolved, not actioned.

## Reproduction path

not applicable: record-integrity correction, not a code bug. Every finding above is independently re-derivable from the commands the situation analysts ran and cited (`git cat-file -t <sha>`, `git log --all --full-history -- <path>`, `git branch -a --list <pattern>`, direct reads of the cited file:line) — see their full structured returns for exact command output.

## Blast radius (best guess at intake)

- `.dcs/incidents/2026-07-30-halt-enumeration-grammar-drift/214-LOG.md` — append a correction entry for the fabricated merge citation
- `.dcs/incidents/2026-07-30-workflow-file-trim-grandfathered/` — correct the false verbatim-SAFETY.md attribution in `AAR.md`; annotate the other 6 missing artifacts as irrecoverable
- `.dcs/incidents/2026-07-29-check-14-hardening/` — annotate 6 missing artifacts as irrecoverable
- `.dcs/incidents/2026-07-29-worktree-removal-self-conflict/` — annotate 6 missing artifacts as irrecoverable
- `.dcs/esg/REGISTER.md` — one cell (`token-economy-advisory-fixes` Branch column)
- `CHANGELOG.md` — verification only; no write expected (see Evidence — item already resolved)

No existing convention prescribes how to append a correction to a *closed* incident's own artifacts (searched `doctrine.md`, `doctrine-appendix.md`, `close.md`, both the repo copy and the installed copy — confirmed byte-identical by `payload_check.py`, 50/50). The Planning Chief will need to design a minimal one as part of tactics, not just apply an existing template. Candidate analogs found: `DELEGATION.md`'s append-a-new-versioned-block convention (never edit a past version block in place); `REGISTER.md`'s REGISTER-LOCK takeover-note pattern.

## Prior art

- `doctrine-appendix.md:658-670`, field lesson "W4" (`register-field-repair-path`, 2026-07-27): a prior repair was itself misreported as "restored verbatim" from sources that did not in fact contain the text — the identical *shape* of false-verbatim-attribution defect as `workflow-file-trim-grandfathered`'s AAR, different incident and root cause.
- `vault/Meta/ESG-sessions/ninth-dcs-esg-2026-07-28.md:64-67`: a prior ESG sweep found and corrected a different DEPLOYED row's stale Branch cell in place, with no special ceremony beyond a one-line note — direct precedent for the `token-economy-advisory-fixes` fix.
- No prior incident has corrected a closed incident's own `214-LOG.md` or `AAR.md` after the fact (searched `vault/Post-mortems/`, `vault/Decisions/`, `vault/Meta/` directly) — this is the first of its kind, which is also why `close-integrity-guard-bundle` (register rank 2) is sequenced to start only after this one closes.

## Decomposition check (step 4a)

Four distinct record-integrity defects remain in scope after dropping the stale CHANGELOG item: (1) fabricated merge citation, (2) false verbatim-SAFETY.md quote, (3) three incidents' worth of irrecoverable-artifact annotation (treated as one class of correction, same disposition for each), (4) one stale register cell. Each is technically severable — different incidents, different proximate causes — but all were deliberately bundled into this single register row by the Owner-chairing ESG (sixteenth session, 2026-08-02) for a stated sequencing reason: this incident's own green-Safety close is Delegation v5's written `auto_approve_type3` reinstatement condition, and it must land as a whole before `close-integrity-guard-bundle` (rank 2) can be built without being "born red" against still-uncorrected archives. Splitting further would override that considered strategic decision without new information that justifies it — the one new finding (the CHANGELOG item's staleness) argues for *less* scope, not more decomposition. **Not decomposing.** Keeping as one incident, one register row; scope reduced by one line item (CHANGELOG — verified already resolved).

## Type + rationale

**Proposed type:** 3
**Rationale:** All findings re-verified first-hand (b4af6e4 not a git object yet cited at 214-LOG.md:37; zero full-history trace of the "verbatim" SAFETY.md behind AAR.md:44; artifact census exact across the three sparse incident dirs; REGISTER.md:135's Branch cell names a branch git no longer has; 0.7.1 already at CHANGELOG.md:117): four defect classes across ~6 files in five surfaces with a first-of-its-kind closed-record annotation convention to design puts this well past Type 5's ≤1-file/no-design bar and demands the Safety Officer that Type 5 lacks, while no Type 1 trigger fires — append-only, trivially reversible annotations to unshipped `.dcs/**` records touch no shared infrastructure and need no Logistics or deploy-ordering — and Type 3's activation (Planning Chief to design the convention, Safety Officer to independently verify, Owner IAP approval guaranteed since Delegation v5 sets `auto_approve_type3: false`) is exactly the ceremony fabrication corrections warrant. (IC=dcs-commander, fable)
**Owner confirmation:** confirmed as proposed (Type 3)

## Intake source (for /dcs-close to route back to)

`.dcs/esg/REGISTER.md` row `record-integrity-corrections` (M, rank 1) ← `vault/Post-mortems/deepseek-period-review.md` §D ← Owner-directed queue 2026-08-01, ranked at the sixteenth `/dcs-esg`, 2026-08-02 (`vault/Meta/ESG-sessions/sixteenth-dcs-esg-2026-08-02.md`).
