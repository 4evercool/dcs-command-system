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

## 6. A rule you exempt yourself from is not a rule

`CLAUDE.md` says: *write files with the Write/Edit tools, never
PowerShell `Set-Content`/`Out-File`* — because that emits a BOM, which
had already broken a hash comparison twice.

Every version bump for thirteen releases then used
`Get-Content package.json -Raw` + `WriteAllText`. Not the forbidden verb,
the same failure: PowerShell 5.1 reads with the system ANSI codepage, so
each bump decoded the description's em-dash as cp1251 and re-encoded it
as UTF-8. Three characters became six, six became twelve:

| commit | package.json |
|---|---|
| d5d8106 | 1,378 chars |
| 537177a | 4,356 |
| 6b72a63 | 139,473 |
| 6a57b97 | **6,322,630** |

`npm publish` failed at 13.5 MB. Three things made it survivable only by
luck: the file stayed **valid JSON**, so every parse succeeded; the
growth was in one field, so diffs looked ordinary; and the existing
encoding guard checked for BOM and U+FFFD, while double-encoded text is
**valid UTF-8**. Nothing measured size, so nothing noticed.

The same pass found the damage was not confined to `package.json`:
`dcs-ops-specialist.md` and `dcs-situation-analyst.md` carried mangled
em-dashes in their `description:` frontmatter — the text that renders in
the agent registry. It had been visible in session output for a dozen
versions and nobody, including me, registered it.

**Three transferable pieces:**

1. **A rule stated as a verb is a rule about the verb.** "Never use
   `Set-Content`" got followed literally while the underlying hazard —
   *any* PowerShell round-trip through a text file — went unaddressed.
   State the hazard, then the instances.
2. **Guards check the failure they were born from.** The encoding guard
   existed and passed throughout, because it was written after a BOM
   incident and looked for BOMs. Ask what *neighbouring* corruption the
   check would miss.
3. **Cheap invariants catch expensive drift.** "`package.json` < 8 kB"
   would have failed on the first bump. Any artifact with a stable
   expected size deserves one.

## 7. The author is not exempt

Within two days I: shipped a principle that duplicated an existing one in
weaker form; shipped a false field lesson and corrected it four minutes
later; instructed a session to fabricate a log entry; made artifact
hygiene a binding halt and caused **13 of 17 halts to fire on process
rather than code**; and the encoding failure above. Each was caught by
the system, by a session refusing a bad instruction, or by the Owner —
**none by me**. That is not modesty, it is the design argument: the
author is the least reliable reviewer of the author, which is why DCS
self-hosts. See [[Decisions/distribution-and-scheduling]] for what
self-hosting does and does not cover.

## Links

- [[Post-mortems/energy-cost-model-rework]] — the incident behind v0.5.12
- [[Metrics/incident-metrics]] — the evidence base
