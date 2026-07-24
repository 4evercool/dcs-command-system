---
tags: [dcs, meta, lessons]
updated: 2026-07-25
---

# Meta: lessons about building DCS

Patterns in the **construction** of DCS, distinct from the rules DCS
enforces. These are for whoever is improving the system next — including
the version of me that wrote a defective rule four minutes after writing
a correct one.

## 1. Prose fails; mechanisms hold

Every rule written only as prose was violated in the field, usually
within hours, usually by a session acting reasonably on a reading the
prose permitted:

| Rule as prose | What happened | What actually held |
|---|---|---|
| "Dispatchers must consult the IC at command points" | skipped 3× on day one | pre-stamp checklist + entry gates reading the log |
| "Revisions are fresh spawns, never resumed agents" | violated twice *after* it was written down | the gate denying `SendMessage` |
| "No code before an approved plan" | — | a PreToolUse hook (never violated) |

The rule with no violations is the one that was mechanical from the
start. When a rule matters, ask what file or command could refuse to
proceed without it, and put it there. Prose is documentation of a
mechanism, not a substitute for one.

## 2. Derived facts rot, and they travel

Doctrine principle 15 was learned three separate ways in two days:

- a census of code sites, correct when measured, wrong by the next commit
- *"the Fable quota is exhausted in this session"* — measured once, then
  cited as a standing condition for hours after it had restored
- **my own**: I read a zero-byte agent transcript, concluded the spawn
  was dead, and instructed a session to log a failed attempt that had
  never happened. The session refused, measured, and corrected me.

The tell is always the same: a fact with a **lifetime** recorded without
one, then transcribed in good faith at every hop until it lands somewhere
durable with no memory of having been a measurement.

## 3. Measure the thing, not a proxy for it

My dead-spawn error again, in general form. I had three pieces of
circumstantial evidence (zero bytes, no growth, a real earlier failure)
and none of them measured the actual question: *did a decision block come
back?* Confident causal stories assembled from proxies are the most
expensive kind of wrong, because they read as diligence.

## 4. Ask what the rule costs when it is wrong

Two rules shipped over-strict and had to be scoped back within a day:

- the deploy clean-check blocked on *any* dirty file, including
  `.claude/` churn a deploy never ships → scoped to the deploy payload
- the worktree audit called every foreign worktree an orphan, including
  the deploy script's own → scoped to DCS-owned worktrees

Both were "safe" in the abstract and produced friction plus a wrong
answer in practice. A gate that fires on the wrong thing teaches people
to route around gates.

## 5. The system's own failures are its best specification

Almost every mechanism in DCS is named after the incident that produced
it. Nothing in the design was speculative and survived; the parts that
lasted came from watching something break. When adding a mechanism with
no incident behind it, be suspicious — that is the shape of ceremony.

## 6. The author is not exempt

Within one day I: shipped a principle that duplicated an existing one in
weaker form; shipped a false field lesson and corrected it four minutes
later; and instructed a session to fabricate a log entry. Each was caught
by the system or by the Owner, not by me. **This is why DCS self-hosts** —
see [[Decisions/distribution-and-scheduling]] for what that does and does
not cover.

## Links

- [[Post-mortems/energy-cost-model-rework]] — the incident behind v0.5.12
- [[Metrics/incident-metrics]] — the evidence base
