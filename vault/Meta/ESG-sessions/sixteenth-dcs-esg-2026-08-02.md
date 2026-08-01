# Sixteenth `/dcs-esg`, 2026-08-02 — hardening arc ranked, sequencing-first rank 1

Chair: Owner. Chief of Staff: main session (Fable).

## Portfolio at close of session

32 DEPLOYED, 20 QUEUED (ranked 1–20, contiguous), 1 PARKED
(`halt-binding-status`), 10 KILLED, 4 RESOLVED, nothing ACTIVE, nothing
deploy-pending, no pending sitreps. Regenerate from the State column:
`awk -F'|' '/^\| [a-z][a-z0-9-]* \|/ {s=$6; gsub(/^ +| +$/,"",s); sub(/ \(.*/,"",s); print s}' .dcs/esg/REGISTER.md | sort | uniq -c`.

Since the fifteenth session (yesterday): `trim-content-loss-restoration`
(Type 1, was rank 1 — six restoration sites, witness 50/0 at `998bcd4`),
`revision-preservation-map` (restarted, ran clean to DEPLOYED) and
`release-provenance-guard` (out-of-queue Owner incident; premise
corrected and slug renamed from `tarball-tag-guard` at its stem) all
shipped; `doctor-silent-pass-and-bump-defects` resolved as Type 5 (Owner
override of the commander's proposed 3) with a new `tests/test_dcs_cli.py`.

## Decisions

1. **Rank 1 = `record-integrity-corrections` — a sequencing argument,
   accepted:** (a) its close is Delegation v5's written reinstatement
   condition for `auto_approve_type3`; (b) it must land before the
   hardening SHA-existence guard (`close-integrity-guard-bundle`,
   rank 2), or that guard is born red on the still-uncorrected archives
   (the fabricated `b4af6e4` citation).
2. **Ranking accepted wholesale (1–20).** Hardening rows at 2–4;
   restoration follow-ups at 6/12/13; `release-provenance-guard`'s two
   at 8/10 (`tag-refname-disambiguation-hole` carries an explicit
   Owner-sign-off-at-open marker — it was queued straight from a
   command point and has never been typed or confirmed).
3. **Evidence branch kept**:
   `dcs/revision-preservation-map-abandoned-2026-07-31` stays — its
   `497dcd4` is cited in the fifteenth session's records, and deleting
   the ref would eventually hand the commit to GC, stranding citations
   exactly when the SHA-existence guard starts checking them.

## Also noted

- `russian-artifacts-translation`'s premise re-verified against the
  `incident-artifacts-english-mandate` field repair (`4bc90b7`): the
  repair changed the *rule*, translated nothing — the row stands.
- `vault/_scripts/register-view-plan.md` was superseded by events: the
  view exists and runs as a PostToolUse hook (output
  `.dcs/esg/register-view.html`, 67 rows / 0 unparsed on every register
  edit this session) — differing from the plan's spec (which targeted
  `vault/register-view.html` via a manual script). The plan file is
  committed as the design record; whether the plan-vs-built divergence
  needs reconciling is left for whoever owns the tooling next.
- Delegation v5 unchanged; both post-v5 deploys ran clean under its
  deploy authority.

## Worktree audit

Clean: one worktree (main checkout), no orphans, no husks, no stale
actives. One deliberate non-default: the kept evidence branch above,
recorded here so the next audit does not re-flag it cold.
