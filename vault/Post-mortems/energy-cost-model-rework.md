---
tags: [dcs, post-mortem, incident]
incident: 2026-07-23-energy-cost-model-rework
project: bread_bot
updated: 2026-07-25
---

# Post-mortem: energy-cost-model-rework

**31 hours. 54 files. 11,000 lines. 10 Safety halts, 4 revisions of
period 1, 3 periods, 3 escalations, a 285 kB log — and it spawned its own
blocker incident mid-flight.** It shipped correctly (merge `8aba0249`,
deployed), so this is a post-mortem about **cost**, not correctness.

Source of truth: that incident's own `214-LOG.md` and `AAR.md` in
bread_bot. Numbers: [[Metrics/incident-metrics]].

## The finding that matters

**Every individual mechanism behaved correctly.** The halts were right.
The rejects were right — one caught a check that would have fired a
mandatory *false* deviation on a perfectly good deploy, because it
demanded a merge commit's SHA equal a sealed SHA that `--no-ff` makes
impossible by construction. The blocker it spawned was a genuine
production-corrupting bug (two branches allocating the same migration
number, conflict-free at merge). Nothing misfired.

So the cost did not come from a broken mechanism, and **no amount of
additional downstream rigor would have helped** — more rigor is more
hours. It came from scope admitted at intake and never bounded
afterwards. That is why all three v0.5.12 fixes act at or before the
plan, not at verification.

## Three specific causes, each now mechanized

**1. The 201 contained four incidents.** Its Symptom opens with "the
energy model is wrong" *and* names three accompanying defects — one of
them actively corrupting production data. All four were absorbed into a
single Type 1. Typing was correct and irrelevant: **typing sets ceremony,
it has never set size.**
→ `new.md` step 4a: one incident, one defect; register the rest.

**2. The period cap never fired, and the log explains why in its own
words:** *"(c) не срабатывает — ревизии не считаются периодами"* —
revisions are not counted as periods. Four revisions inside period 1
walked straight through a cap built for exactly this shape.
→ Trigger (c) counts **attempts** (any stamped-and-executed IAP).

**3. Proven work sat unshipped**, argued by the incident's own AAR:
*"Period 1 produced a proven, Safety-passed fix… that fix then sat in a
branch. A fix that is not shipped fixes nothing, and the defect kept
corrupting production data the whole time."* Period 2 existed **only** to
make period 1 shippable.
→ Close-and-requeue is the default at a Safety pass.

## The halt pattern (a separate lesson)

Halts 3 and 4 closed the named refutations and surfaced **another
instance of the same class** each time. The IC eventually named it
exactly — *"R5 is a defect of **form**, not of site"*, and *"converges on
the 4th attempt provided an instrumental rather than site-based fix"* —
and the Owner's pivot to a general guard ended the rotation immediately.

**The read was right; it was late because nothing asked for it.** Hence
the mandatory convergence read from the second halt (v0.5.9), and
enumeration-shaped sweep criteria: name the command that enumerates the
population, never a list of sites.

## What would have happened with today's rules

The active corruption bug ships in ~2 hours as its own incident. The
model rework opens separately and bounded. The migration collision is
still discovered — that was real work — and still becomes its own
blocker. Roughly three small incidents, each shipping the day it is
fixed, with the cap firing at attempt 3 rather than never.

## Links

- [[Meta/building-dcs-lessons]] — the recurring meta-patterns this fed
- [[Backlog]] — what remains unaddressed
