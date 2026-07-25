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

## 7. Citations into a file the incident is editing

From `doctrine-hot-path-trim` (2026-07-25), the first self-hosted incident,
which took **two Safety halts** — neither against the work, both against the
bookkeeping that recorded it.

The incident moved prose out of `doctrine.md` into `doctrine-appendix.md` and
logged where each passage went, citing appendix **line ranges**. Those citations
were correct when written and wrong when read: the same incident appended 114
lines to that file and shifted every line past 45. The Safety Officer opened the
cited ranges and found unrelated text.

**Cite by content anchor, not by line range.**

```bash
grep -n -F "Principle 15 — the test-inversion lesson." dcs/references/doctrine-appendix.md
```

An anchor **is** the substance; a line number is a fact *derived about* the
substance, with a lifetime. The anchor resolves in any tree, survives arbitrary
edits above it, and when it does break it returns zero hits **loudly** instead of
silently resolving to the wrong paragraph. This is principle 15 applied to
citations specifically, and it is worth stating separately because "write the
derivation, not the result" does not obviously imply "do not write line numbers".

Three qualifications, each learned the hard way in the same incident:

- **Anchors have their own failure mode: markdown hard-wrapping.** A phrase
  spanning a line break matches nothing under line-based `grep`. One anchor here
  (`three times in one incident`) returned 0 hits for exactly that reason. Choose
  anchors **within a single physical line**, and uniqueness-check each one
  (`grep -c -F` must return `1`) before writing it down. An anchor matching twice
  is as useless as a rotted line number.
- **Anchors eliminate rot, not under-coverage.** A row can still name too few
  anchors — which is precisely what the second halt was. What the scheme actually
  buys is that the population becomes *enumerable* and each member becomes a
  one-command binary check; an officer could then exercise all 19 in a single
  script rather than discovering one defect per verify cycle. Do not overclaim it
  as making the class "unrepresentable" — this incident did, and its own Safety
  Officer corrected it.
- **A corrective can be worse than the defect it fixes.** The first correction
  narrowed a citation from `116-135` to `128-135` on a prior officer's
  observation, and broke a coverage that had been *correct*. Officer → IC →
  Dispatcher, each faithfully transcribing the one before, none re-deriving
  against the source — lesson 2's chain, occurring inside the remedy written for a
  lesson-2 defect. **The seat applying a corrective owes the same re-derivation as
  the seat that found the defect.**

Two smaller notes from the same incident, both about *where* things live:

- **Check where a corrective lands before choosing a disposition.** This one named
  `214-LOG.md`, under `.dcs/**`, which specialists are barred from by
  construction — so `execute.md`'s "fix-taskings" path was unavailable and the IC
  had to name the Dispatcher as executor. The disposition menu assumes a
  specialist can act; sometimes none can.
- **A byte-count acceptance criterion is line-ending-sensitive on Windows.**
  `core.autocrlf=true` with no `.gitattributes` means a fresh worktree measures
  larger than a long-lived checkout of the same commit — 319 B here, against a
  43,008 B ceiling. Name the tree in the criterion, measure in the worktree
  (conservative), and treat the sensitivity as its own defect rather than folding
  it in.

## Links

- [[Post-mortems/energy-cost-model-rework]] — the incident behind v0.5.12
- [[Metrics/incident-metrics]] — the evidence base
- [[Backlog]] — including the rows `doctrine-hot-path-trim` discovered
