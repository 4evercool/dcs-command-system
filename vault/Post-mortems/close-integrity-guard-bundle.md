---
tags: [dcs, post-mortem, record-integrity, self-hosting]
created: 2026-08-03
status: closed -- MERGED (deploy pending)
---

# Post-mortem: close-integrity-guard-bundle

**Incident:** `close-integrity-guard-bundle` (Type 1). **Opened:** 2026-08-02. **Closed:** 2026-08-03. **Periods:** 1 (two attempts — a Safety Officer halt routed the first back to `/dcs-plan`). **Outcome:** [[Decisions/non-anthropic-hardening|non-anthropic-hardening]] Packaging item 1 shipped — a shipped, unconditional record-integrity gate (`dcs/tools/record_integrity.py`) invoked from a new `close.md` step 5a.1b, plus this repo's own English-only/term-census policy generalized in `test_doctrine_integrity.py`. Full chronology (every command point, every measurement): `.dcs/incidents/2026-08-02-close-integrity-guard-bundle/214-LOG.md`.

## What this incident was actually about

Build the mechanical enforcement that closes the gap the [[Post-mortems/deepseek-period-review|deepseek period review]] found: every DCS rule enforced by a *mechanism* held; every rule that lived only in doctrine prose broke. This bundle mechanized four of those broken rules for close time — commit-SHA citation existence, artifact-set completeness, `SAFETY.md` schema conformance, clean-tree, non-degenerate commit messages — plus this repo's own content-integrity policies.

## The two intake corrections, found before typing

Both worth recording because they're a recurring failure shape, not a one-off:

1. **The intake's "seven-artifact set" was wrong.** It traced to one incident's count of artifacts found *missing*, decontextualized into a size claim. The real canonical set is 9 (`forms.md` now states this explicitly).
2. **A naive "SAFETY.md has a JSON fence" check would have both missed the target and cleared it wrongly** — `record-integrity-corrections/SAFETY.md:33` contains the literal fence-marker substring inside prose *about the absence of a fence*. A substring check reads it as present; the incident's own precondition would have been misjudged twice over by the shape of check the intake asked for.

Neither correction changed the incident's goal. Both would have shipped a broken mechanism if the stem hadn't verified the intake's own claims against the repo instead of transcribing them.

## The halt: a mechanism that checks itself is not a check

Full field-lesson write-up, doctrine's own copy: [[doctrine-appendix#Principle 16|doctrine-appendix.md, "Principle 16 — a mechanism that checks itself is not a check"]]. The compressed version: both refutations were found by running the *new* mechanism against something *real* — the term census against its own defining file (tautological: every term "found itself"), and the SHA-citation tool against **this incident's own directory** (criterion 14's own mandated sanity check), which surfaced a permanent, append-only-unfixable false positive baked in by the incident's own planning process.

**The generalizable pattern:** a check whose only witnesses are purpose-built fixtures can pass by construction — the fixtures were built to make it pass. The two checks that actually found something were the ones run against a real, adversarial target that nobody had shaped to fit the check: the shipped payload's own text, and the incident's own working history.

**A second-order finding, from the replan's own re-verification:** the "obvious" fix to the false positive (drop the `sha` keyword from the citation grammar) would have been *wrong* — corpus measurement showed 5 of 8 historical `sha`-keyword tokens were genuine commit citations across 4 different incidents. The actual gap wasn't the trigger, it was the missing remedy: no mechanism existed for legitimately correcting an append-only record. This is worth remembering the next time a false positive looks like it should be silenced at the detector rather than given a real remedy path.

## Command-point discipline, measured

`dcs-commander` ran as Fable on every spawn but one (the very first command-point-1 attempt failed with a network error — `ENOTFOUND` — and was immediately re-spawned per doctrine's "never cache the fallback" rule, landing on Opus that one time). Every other command point succeeded on `fable` first attempt. Two full `iap_review` reject→revise→accept cycles happened (one pre-execution on the first plan, one post-halt on the replan) — both times the commander independently re-derived the load-bearing claims from the repo rather than trusting the chief's or the IC's write-up, and both times found something real: a false witness-count claim, an unowned `dcs/README.md` line, an un-fundable version-number placeholder on the first cycle; nothing new on the second (clean accept). The Safety Officer's own halt→pass cycle mutation-tested its own findings rather than merely inspecting code — this is what actually distinguished "the fix looks right" from "the fix is provably right" for both refutations.

## A disclosed prompt-injection attempt, contained

Mid-execution, an S2 sub-agent reported that after it deliberately blanked a fixture file for a legitimate mutation test, an injected message shaped like a system reminder claimed the change was made by "the user or a linter" and asked it not to mention this. The agent correctly refused, reverted the file, verified the revert byte-for-byte, and disclosed the incident rather than complying with the request for silence. The Safety Officer independently re-verified the fixture's actual content was intact, not tampered. No harm resulted. Flagged directly to the Owner in the session transcript; source channel not identified. Recorded here because it's exactly the kind of event a future incident touching subagent-generated content should know can happen, and that the right response — verify, refuse, disclose — is what actually contained it.

## What's explicitly deferred, not forgotten

- `log-append-helper` and `independence-fail-closed-and-model-floor` — the other two incidents [[Decisions/non-anthropic-hardening|non-anthropic-hardening]] queued; unaffected by this one.
- `russian-artifacts-translation` — historical remediation of already-known non-English incidents; this bundle only builds the sweep going forward (criterion 7's scope boundary is explicit about this).
- Documenting the `RECORD-CORRECTION:` convention in shipped prose (`forms.md`) — the tool's own finding text carries the remedy to where an operator actually hits it, but nothing in `forms.md`/`doctrine.md` names the convention for a reader who isn't already blocked. Queued as a follow-up register row at this close.
- `record-verbatim-attribution-followup` — pre-existing queued row, untouched by this incident.
- Hot-path headroom is now 17 bytes (of 37,888) — tracked as debt for the next incident that touches `doctrine.md` or `schemas.md`.

## Numbers, with the command that regenerates them

- 34 incident directories in the corpus at this incident's close; regenerate: `ls .dcs/incidents/ | wc -l`.
- `dcs/tools/record_integrity.py`'s own docstring carries its own regenerating command for every citation/suppression figure it states — read it there rather than copying a number into this file (principle 15).
- Final suite state: `test_dcs_gate.py` 100/100, `test_dcs_intake.py` 18/18, `test_doctrine_integrity.py` 156/156 (up from 152 pre-incident) — regenerate with `npm test`.
