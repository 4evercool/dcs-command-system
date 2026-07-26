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

## 8. Citations into a file the incident is editing

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

## 9. Byte representation is a defect family, not four accidents

By 2026-07-25 this project had been bitten four times by the same shape: **the
bytes on disk are not the bytes you reasoned about.**

| | what drifted | what it broke |
|---|---|---|
| `d604b4f` | a BOM from PowerShell `Set-Content` | `dcs_gate.py`'s shebang parse |
| 2026-07-22 | the same BOM class | the IAP hash comparison — hence `utf-8-sig` |
| `0428ac4` | ANSI-codepage double-encoding across 13 version bumps | `package.json` at 13.5 MB, `npm publish` E415 |
| `hot-path-budget-eol-sensitivity` | CRLF vs LF, from `core.autocrlf` with no policy | the approval marker, silently, for a *closed* incident |

Four instances, one question nobody was asking: **which representation is this
mechanism deciding on?** Every guard added along the way checked the failure it
was born from — the BOM/U+FFFD check cannot see double-encoding, and neither can
see line endings — which is §6's lesson arriving again from a new direction.

The general form is worth stating so the fifth instance is recognised early:
**if a hash, a size, or a comparison decides something, pin the representation
it decides on.** A repo-level policy (`.gitattributes`) pins the tree; a
normalisation inside the mechanism pins what ships. They are not substitutes —
`.gitattributes` is absent from `package.json`'s `files` whitelist and npm
performs no git checkout, so the policy protects a clone of this repo and
nothing downstream. **That single fact moved the incident from Type 3 to Type 1.**

### Enumerate a contract's readers before you change it

Four places computed a raw sha256 of `IAP.md`: the gate, `execute.md`,
`status.md`, and the stamper in `plan.md`. Fixing only the gate would have made
the two workflows **stricter than the mechanism they describe** — a hard stop on
a validly approved plan, on exactly the drift the gate had just been taught to
tolerate. The stamper was correctly left alone, because it writes a raw digest
which the widened set contains by construction; that asymmetry is what made the
change safe to land on a live gate mid-incident.

The tasking that migrated the readers ended with *"if you find a fourth reader
this tasking does not name, that is a deviation"* — because the population had
already been under-enumerated once.

### Measure the hazard before you design around it

That incident's 201 was planned around a vivid hazard: *the fix can invalidate
its own approval marker mid-execution*. The Logistics Chief dissolved it in three
measurements — the renormalise is a no-op here, untracked files are never
rewritten, and the Write tool emits LF so the artifacts were already in the
target representation. Confirmed afterwards in production: the marker still
matched after 83 files were re-materialised.

The real risk was somewhere else entirely — a *tracked duplicate* of the gate
hook at `.claude/hooks/dcs_gate.py`, which is what actually enforces, and which
no test asserted matched its payload copy. **A hazard you can picture is not
thereby the hazard you have.** Plan against the measured one.

### Two smaller ones from the same incident

- **An untracked deliverable is invisible to every in-tree check.** A clone of
  the then-HEAD reproduced the entire original defect while every criterion,
  measured inside the worktree, read green. `git commit -a` omits untracked
  files silently. Stage new files explicitly; verify with `git show --stat`.
- **Delete a rotting derived number; do not correct it.** `CLAUDE.md`'s suite
  counts had drifted from 25/12 to 32/15. Updating them resets the clock;
  removing them and pointing at each suite's own `N/M` output ends the class.
  Same reasoning retired a budget derivation whose arithmetic was simply wrong
  (`ceil(37906/1024)+1` is 39, not 38) and which had survived a prior review
  because the *value* was right and nobody evaluated the *formula*.

## 10. A count a model performs by reading prose is not a count

`halt-loop-unbounded` (2026-07-26) demonstrated this **on its own log,
three times, while building the fix for it.**

`execute.md` and `plan.md` both instruct the Dispatcher to count this
incident's stamped attempts by grepping `214-LOG.md` for `IAP APPROVED` /
`pre-stamp checklist PASSED`. Run against the live log at three successive
points, that instruction returned **3, then 4, then 6** — against **1,
then 3, then 4** real stamps. Nothing was wrong with the log. Ordinary
narrative entries *mention* the tokens: an entry explaining that a hash was
voided, an entry recording that the checklist passed, a Safety summary
quoting the line it is about. The substring is in all of them.

The failure is not sloppiness, and this is the part worth keeping. Each
of those three miscounts was produced by a careful reader following a
written instruction exactly. **The instruction was the defect** — it named
a command whose output does not mean what the rule needs it to mean, and
no amount of care recovers that. The Dispatcher counted correctly only at
the fourth stamp, by abandoning the prescribed `grep` for an anchored
pattern — that is, by using the field-position grammar the period had just
finished building.

Two consequences that generalize past this incident:

- **A rule whose enforcement is "run this command and read the number" is
  only as good as the command's precision.** Before writing such a rule,
  run its command against a *realistic* artifact — one with narration in
  it — not a clean example. This one had survived since v0.5.12 because it
  was only ever checked against logs too short to contain narration.
- **Self-application is the cheapest test available for a process rule,
  and it is nearly free.** This incident found the defect four times over
  without a single extra spawn, purely because the rule happened to apply
  to the artifact the session was already writing. When a rule governs an
  artifact DCS itself produces, run it on DCS's own artifacts before
  shipping it. See §6 ("A rule you exempt yourself from is not a rule") —
  this is its constructive twin.

The same incident produced a second instance of the family from the
opposite direction: the Logistics Chief derived requirement **L0-d** — a
log with no trailing newline turns a verbatim append into a splice onto
the last line — from the *shape* of the act, with no observed case. A
specialist implemented it, a test pinned it, and hours later the
incident's own `214-LOG.md` turned out to have no trailing newline and an
append against it failed. Derivation from structure beat waiting for the
field by less than a day.

## 11. A cut registry constrains aim, not prose — and only aim is a contract

`schemas-md-trim` (2026-07-26) ran the technique `doctrine-hot-path-trim`
invented: the Planning Chief enumerates every span to be cut, **measures**
each one instead of estimating, attaches a KEEP-list, and the specialist
executes the ledger rather than exercising fresh editorial judgement. It hit
the target on the first attempt again, with the pre-authorised reserve
untouched — two for two.

What the second run taught, which the first could not: **the two columns of a
cut registry have completely different force.**

- **"Before" is a contract.** Every one of the five positions matched its
  registered size exactly (one within 2 B, on blank-line accounting). That
  agreement *is* the evidence that the specialist cut the registered
  fragments and nothing else — which is why the tasking's deviation clause
  was keyed to it, and why no deviation was owed despite the other column
  diverging.
- **"After" is a forecast.** Replacement prose came out 26–87 B off the plan
  in both directions, netting −2,331 against a planned −2,349. Nothing was
  wrong: the length of a sentence someone has not written yet is not
  knowable, and a registry that pretended otherwise would manufacture
  deviations out of ordinary writing.

So: size the reserve against "after" drift, and trigger deviations only off
"before". A registry that treats both columns as binding will spend command
points on prose length; one that treats neither as binding stops being a
registry and becomes a suggestion.

### Label a historical measurement; do not recompute it

Same incident, and it is the sharper half of the lesson. The Safety Officer
found the guard's ratchet comment mixing raw-CRLF and normalised byte counts
with no basis named, and offered two fixes: label the old numbers, or convert
them. The IC chose **label**, and the reason generalises past this file — the
prior incident *genuinely measured raw*. Substituting normalised equivalents
would credit it with measurements it never took and mint three new derived
facts in place of one labelled basis.

The cost of the unlabelled number is worth recording precisely, because it is
larger than it looks. One figure — "1,189 B" — lived in six artifacts without
its basis. Unpicking it in a single period produced **three separate errors**:
the IAP attributed the growth to the wrong file, the mandated correction broke
the arithmetic of the sentence around it, and the tasking prompt inherited the
wrong attribution. See §2 ("Derived facts rot, and they travel") — this is
that lesson's worked example, and the antidote is one clause: name the basis
where the number is written.

## Links

- [[Post-mortems/energy-cost-model-rework]] — the incident behind v0.5.12
- [[Metrics/incident-metrics]] — the evidence base
- [[Backlog]] — including the rows `doctrine-hot-path-trim` discovered
