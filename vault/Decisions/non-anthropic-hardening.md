---
tags: [dcs, decision, hardening, model-trust]
created: 2026-08-01
status: adopted (Owner directive 2026-08-01, chat session; three incidents queued from it)
---

# Decision: harden DCS for non-Anthropic operators

**Trigger.** The external review of the 2026-07-29 → 07-31 period
(`vault/Post-mortems/deepseek-period-review.md`), in which a
DeepSeek-driven operator produced twelve merged incidents whose
mechanical guards all stayed green while the prose-only rules broke
systematically: fabricated commit references, backfilled logs, closes
with most artifacts missing or untracked, Russian-language artifacts
against the English mandate, an operative safety condition lost in a
trim, and repeated silent collapse of Safety independence ("agent spawn
blocked — IC performed Safety verification directly").

**The empirical finding this decision rests on.** Every rule enforced by
a mechanism held (all 13 IAP hashes genuine, all suites green, register
deploy evidence honest). Every rule that lived only in doctrine prose
broke. Trust in DCS is therefore calibrated per-operating-model, and the
design must stop assuming the operator's discipline.

**The principle.** Move each broken rule into one of three places:
1. a **mechanism** that enforces it (a guard that goes red),
2. a **tool** that makes the correct act the only convenient act,
3. an **Owner gate** that fires when independence is lost.

Never more prose: the English mandate was perfectly clear and was
ignored; exhortation spends hot-path budget on exactly the operators who
least read it.

## The measures, by breach class

### 1. Records derived, not authored

- **SHA-existence guard**: sweep `.dcs/incidents/**` for sha-like
  tokens, `git cat-file -t` each. Turns fabrication (the `b4af6e4`
  case) into a red guard.
- **Log-append helper**: a stdlib script (`dcs/hooks/dcs_log.py append
  <slug> "<text>"`) that stamps the real timestamp itself in one
  canonical format, recording operator identity per entry. Backfilling
  becomes bypass-visible; the four-timezone chaos disappears. Guard:
  N+ entries sharing one timestamp, or out-of-order entries, is red at
  close.
- **Facts-by-command in AARs**: any git-state claim quotes the command
  *and its output*; Safety re-runs a sample.

### 2. Close-time completeness gate (fail-closed)

Before the merge step: the seven-artifact set exists **and is tracked**;
SAFETY.md contains a parsing schema-#5 JSON block; `git status` is clean
under `.dcs/incidents/<slug>/` and `vault/` after the archive commit.
Red blocks the merge, fail-closed like the gate's zombie rule — a close
that loses records is unrepairable later. Would have prevented the
missing-artifact closes, the untracked provisioning artifacts, and the
sole-copy ESG-history exposure.

### 3. Content guards over artifacts

- **Non-English sweep** over `.dcs/incidents/**` and the shipped
  payload (Cyrillic / non-whitelisted scripts). Rule-with-its-guard
  norm: a doctrine change about artifacts ships its enforcement in the
  same incident.
- **Load-bearing-term census**: a curated list of operative terms
  (`guarded_paths`, `escalate_owner`, sentinel names, …) that must each
  appear somewhere in the shipped package — the package-level twin of
  the queued `revision-preservation-map` idea. Converts a trim's silent
  loss of a safety condition into a red guard.

### 4. Independence loss is a halt, not a footnote

Every fabrication and missing-artifact close in the period happened in
"IC performed Safety directly" mode. Rule change: **if the Safety
Officer cannot be spawned as an independent agent, the incident may not
close unattended** — it PARKs or goes to Owner `AskUserQuestion`.
Self-verified closes become an Owner-visible event. Additionally, the
verdict's `checked` array must contain regenerable commands, and the
close-time check re-runs a subset; a verdict whose checks don't
reproduce is a halt.

### 5. Operator identity and differential trust

- Phase-transition log entries record the operating model (structured,
  via the append helper — the period's logs did it informally and it
  was the only way the review could attribute the breach clusters).
- **Delegation model floor**: the Delegation of Authority gains an
  approved-model list; unattended operation and auto-approval bounds
  apply only when the session model is listed. An unlisted model gets
  v0.1 behavior — every gate an Owner gate. Costs nothing on Fable;
  automatically demotes an unlisted operator to supervised mode.

### 6. Harness-robustness rules

- Commit messages via `git commit -F <file>` (file written with the
  Write tool), never inline multi-line strings — prevents the 22
  `@`-corrupted messages. Cheap guard at close: scan the incident's
  commits for degenerate messages.
- Temp files under the incident dir or system temp, never composed
  `C:\...` argument strings (the U+F03A `C:temp_s1_*.patch` case). The
  clean-tree check catches the debris regardless of cause — refuse to
  close over an unexplained untracked file rather than enumerate
  mangling modes.

## Deliberately rejected

- **More/louder doctrine prose** — see the principle above.
- **In-workflow model-quality heuristics** ("if the model seems weak…")
  — one explicit Owner-controlled list in the Delegation, not scattered
  self-judgment by the model being judged.

## Packaging (queued 2026-08-01, unranked)

1. `close-integrity-guard-bundle` — measures 1 (SHA guard), 2, 3, 6's
   close-time checks. Territory: tests + close.md. Likely Type 1 (it
   *is* enforcement mechanism). **SHIPPED 2026-08-03, Type 1 confirmed
   (merge `b8921c0`, v0.8.0) — full write-up:
   [[Post-mortems/close-integrity-guard-bundle]].** The term census
   (below) rode with it, per the Owner's explicit override of the IC's
   recommendation to queue it separately. Not shipped as part of this
   row: measure 1's log-append helper (item 2, below, unaffected) and
   documenting the `RECORD-CORRECTION:` convention in shipped prose
   (queued as a fresh follow-up at this incident's own close).
2. `log-append-helper` — measure 1's tool + entry format with operator
   identity. `dcs/hooks/**` → Type 1.
3. `independence-fail-closed-and-model-floor` — measures 4 + 5's
   Delegation change. Doctrine + close.md + Delegation schema; likely
   Type 3, Owner-heavy by nature. **MERGED 2026-08-03 (deploy pending),
   typed 1 by `dcs-commander` at planning (verified 17-file blast
   radius exceeded Type 3's ceiling), Owner overrode to 3 — full
   write-up: this incident's own `AAR.md`.** Measure 4 (independence
   fail-closed) and measure 5 (Delegation model floor) both shipped in
   this one incident, as packaged. Not covered: `plan.md:130`'s
   no-DELEGATION.md fallback-to-`config.json` path has no model floor
   (flagged to the Owner at IAP approval, candidate follow-up row); the
   `approved_models` list itself is still empty pending a `/dcs-esg`
   session (this incident's criterion 10).

The term-census guard may ride with (1) or with the already-queued
`trim-content-loss-restoration` — decide at (1)'s stem.

Sequencing note: (1) and (2) overlap territory with review-queue rows
(`field-lesson-guard-vacuity`, `trim-content-loss-restoration`,
`close-md-lock-diagnostic-inert` — all touch
`tests/test_doctrine_integrity.py` or `close.md`). The territory check
at each stem sequences them; none should run concurrently with its
overlap partner.
