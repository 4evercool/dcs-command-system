---
tags: [dcs, decision, delegation]
updated: 2026-07-28
---

# Decision: how `DELEGATION.md` reached v4, and why each bound moved (or didn't)

**Consolidated 2026-07-28** from `STRATEGY.md`'s `## Sessions` log (nine
`/dcs-esg` sessions, 2026-07-25 through 2026-07-27), as part of retroactively
applying the same pointer-not-copy discipline `token-economy` shipped for
`REGISTER.md` to `STRATEGY.md`'s own history. Nothing here is new
reasoning — this is the existing v1→v4 argument gathered into one place so
a reader doesn't have to reconstruct it from nine scattered session
entries, several of which only make sense in light of an earlier one.

## v1 → v2 (2026-07-25, founding session and the second session same day)

Granted at founding with the template's proposed bounds and
`deploy.auto_after_close: true`, **despite zero closed incidents of
evidence** — the Chief of Staff noted this explicitly: the bounds were
reasoned from the repo's structure, not from a track record.

`doctrine-hot-path-trim` (the first self-hosted incident) exercised
`auto_after_close` on its first real use, and the Owner overrode it.
**v2** reverted `deploy.auto_after_close` to `false` to match. Three
other amendments were proposed on real evidence at the same session and
declined — the ratchet-drift lesson from that incident went to
`vault/Meta/building-dcs-lessons.md` §8, not to the Delegation.

## v2 → v3 (2026-07-26, third session same day)

**`forbidden_topics` dropped `"installer"`.** This looks like a
reversal of v2's decision to keep such entries, but the reasoning
differs by case: v2 declined dropping `"version bump"` because it
misfired on an incidental phrase, and a misfiring topic-string bound
costs one Owner prompt — the safe direction. `"installer"` is
**structural**, not incidental: `CLAUDE.md:148` is the sentence that
*defines* Type 1, so any 201 that quotes it to justify its own typing
trips the bound by construction, on every such incident, forever.
Nothing was loosened — `install.ps1`/`install.sh` stayed in
`forbidden_globs` throughout, so a real installer change was always
caught by territory, never by this topic string alone. Measured once in
the field (`schemas-md-trim`) before the drop.

**Three bounds were deliberately left alone, evidence checked rather
than assumed:**
- `max_files` stayed 4 — territory sizes across the five incidents
  closed by then were 3, 11, 8, 11, 3, and **both** that exceeded 4 were
  Type 1, which no `auto_approve_type3` bound reaches anyway. Nothing to
  raise it on.
- `max_specialists` stayed 2, with a named open question:
  `schema-citation-guard` ran three specialist spawns (two taskings plus
  a fix-tasking after a halt), and whether a fix-tasking counts against
  the bound had never been decided. Flagged as mattering "the first time
  a Type 3 halts" — still unresolved as of the ninth session's own
  Sessions-log entry.
- The `deploy` object stayed untouched — two deploy trains had run by
  then, and **both** needed an Owner-authorised substitution of the
  verification step, which is precisely the shape of decision doctrine
  says must not be delegated.

## v3 held for four consecutive sessions on evidence, not caution

Across the sessions of 2026-07-26 (first) through 2026-07-27 (sixth),
`auto_approve_type3` **never fired once** — first because "no Type 3 has
closed" (true through the fourth session), then because the one Type 3
that *did* close (`direct-resolution-lane`'s sibling incidents) broke
both previously-untested bounds at once: `max_files` 4 against 7 files,
`max_specialists` 2 against 3 taskings. Each time, the Chief of Staff
offered the Owner the honest alternative — fit the bounds to the repo's
actual shape, or drop a grant that never fires — and each time the Owner
kept v3 unamended. The stated reasoning (fourth session): **a bound
firing and sending the IAP to Owner review *is* the mechanism working**;
a second attempt at a rule that had already failed once deserved Owner
eyes, not a wider gate.

The `deploy` object's own revisit condition fired the moment
`deploy-marker-blind` closed (fifth session) — but the evidence it was
waiting for (a deploy train running under the new content-shaped step 7)
had not yet arrived, because that same train was what *installed* step
7. Loosening `deploy.auto` at that point would have been deciding on
expectation, not observation.

## v3 → v4 (2026-07-27, seventh session same day)

**`deploy.auto` flipped `false` → `true`.** This is the amendment v3
itself had written the condition for, and by the seventh session the
condition was **satisfied, not merely fired**: the train that closed
just before this session ran clean — content witness exit 1 (4
differing) before install, exit 0 (47 identical) after, integration sha
pinned on both runs — with **no Owner-authorised substitution of the
verification step needed, the first time in five ships.** v3's own
stated ground for withholding delegation had been "a step that needs a
human decision on each use is precisely the step that must not be
delegated" — and step 7 no longer needed one.

**`auto_after_close` stayed `false`** — deliberately distinct from
`deploy.auto`. That is the specific setting the Owner's v2 override was
about; close-and-ship remain separate acts under v4 exactly as under v2.

`auto_approve_type3` was left alone again at the seventh and eighth
sessions — eight, then still eight, closed incidents without it ever
firing. The eighth session's sweep named a **shift in diagnosis** worth
recording precisely because it's easy to miscite as unchanged: through
the fourth session, the reason was "no Type 3 has closed"; by the
eighth, a Type 3 *had* closed, its bounds *held*, but the `"version
bump"` topic-string screen fired anyway (four consecutive false
positives across two incidents by then, zero true positives ever
recorded) — a different mechanism blocking auto-approval than the one
that used to. Same decision (keep the topic string — the noise costs one
Owner prompt, the safe direction, and a real installer change is caught
by `forbidden_globs` regardless), but the *reason* the grant still
hasn't fired had moved, and restating the old reason would have been
wrong rather than merely stale.

## What this file deliberately does not cover

Per-incident ranking decisions (why `X` was rank 1 over `Y` this
session) are not consolidated here — those are inherently transient
(the ranking changes every time a rank-1 incident closes) and the
supporting evidence for each already lives in that incident's own
`REGISTER.md` row and `AAR.md`. This file is scoped to the one thread
that is genuinely cumulative: the Delegation's own bounds, which each
carry forward everything decided about them before.
