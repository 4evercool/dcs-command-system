# /dcs-deploy — 2026-08-04 (second train this date)

Two-row train, shipped under full v0.1 Owner gate (Delegation v6
`deploy.auto: true` but `approved_models` absent — model floor failed;
same disposition as the `log-append-helper` train earlier this date).

- **`field-lesson-guard-vacuity`** (merges `8f6b1ea` + `64a4a01`) —
  deploy had been **HELD by Owner direction** since its post-close
  review found the repair weakened check 20; the hold was lifted by the
  Owner at this train's go/no-go, with the gating fix on the same train.
- **`field-lesson-guard-bare-date-weakening`** (merge `c092c03`) — the
  gating fix: strict `_FL_ID_RE`, fourth-sentinel census, citation
  rewording; Safety PASS period 1 attempt 2.

Portfolio at train time: clean tree, no orphan worktrees, no stale
actives; one dangling branch deliberately kept
(`dcs/revision-preservation-map-abandoned-2026-07-31` — will never
ship, kept as the abandoned-work reference).

Content witness (`python tests/payload_check.py`): before
`install.ps1` — 48 identical / 5 differing (the train's own payload
files: doctrine-appendix, doctrine, forms, execute, plan); after — 53
identical / 0 differing / 0 repo-only / 0 installed-only, at
integration tip `1988b99`. Clean ship; DCS 0.8.0 remains the installed
version label (no version bump rode this train — the witness, not the
label, is the ship evidence). Both branches deleted; DEPLOY-LOCK taken
and released.

Now actionable downstream: `vault/Backlog.md` item 31's final strike at
the next `/dcs-esg` sweep (discharge already recorded in its banner),
and rank 2 `verdict-rerun-em-dash-gap` gained a second live confirmation
at this incident's close (see its 209 sitrep).
