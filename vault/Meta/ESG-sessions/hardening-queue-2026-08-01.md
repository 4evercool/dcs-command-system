# Owner-directed queue from the hardening decision — 2026-08-01

Outside any incident, on the Owner's directive ("write it up and queue
the three incidents"), following the adopted decision
`vault/Decisions/non-anthropic-hardening.md` (harden DCS so
non-Anthropic operators cannot repeat the 2026-07-29 → 07-31 breaches;
principle: mechanism over prose).

Rows appended (all QUEUED, unranked — this act landed after the
fifteenth `/dcs-esg` had already ranked the review rows, so these await
the sixteenth):

- `close-integrity-guard-bundle` (H) — SHA-existence, non-English,
  artifact-completeness/tracked, SAFETY-JSON conformance, clean-tree,
  commit-message checks at close; fail-closed.
- `log-append-helper` (M, Type 1) — canonical timestamped 214-LOG
  append tool with operator identity.
- `independence-fail-closed-and-model-floor` (H) — no unattended close
  without an independently spawned Safety Officer; Delegation gains an
  approved-model list (generalizes Delegation v5's blanket
  auto_approve_type3 suspension into a per-model control).

Territory overlap with the review-queue rows is declared in each row's
Territory cell; the stems sequence them.
