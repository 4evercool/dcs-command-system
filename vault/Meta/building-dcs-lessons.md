---
tags: [dcs, meta, lessons]
updated: 2026-08-02
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

### And the limit of labelling: a basis protects the reader, not the decision

The same incident then demonstrated where that antidote stops, by falling
into the gap itself — which is why this paragraph exists rather than a
tidier version of the rule.

Its criterion 10 waived a version bump on the grounds that the version was
unpublished. The figure behind that came from an `npm view` run **two and a
half hours earlier**, and it was cited three times — 201, AAR, deploy sitrep
— each time **correctly labelled** "measured during the previous incident's
deploy". Labelling did its whole job: no reader was misled about provenance.
The version had been published 90 minutes before the IAP was stamped anyway,
and the release went out twice under one number.

So the rule has two halves, and only the first is widely understood:

- **Writing a number:** name its basis. Protects anyone who reads it later.
- **Resting a decision on a number:** re-run the command. A label tells you
  where a fact came from; it says nothing about whether it is still true,
  and an acceptance criterion is a decision, not a reader.

The tell is grammatical and easy to check: a criterion phrased as a **claim
about present state** ("X is unpublished", "the registry stands at N", "the
deployed marker is M") is asserting something the process must verify at the
moment it matters. A criterion phrased as an **invariant to establish** ("the
command returns empty", "the sets are equal") already carries its own check.
Lint 3a enforces the second shape for population sweeps; nothing yet enforces
it for single external facts. See [[Backlog]] item 13.

## 12. The paper trail caught what no mechanism did — four times in one incident

From `schema-citation-guard` (2026-07-26), the incident whose whole subject is
claims nobody re-measures. Every defect below was found by **a seat reading a
whole artifact**, and none of them was reachable by any guard DCS owns.

| # | Found by | What |
|---|---|---|
| 1 | IC, command point 2 | The 202 said "six charters already carry an anchor" — five do. The sixth, `dcs-commander.md`, was in the 202's own list of *un*anchored citations, one line above. |
| 2 | Dispatcher, accepting S1 | Criterion 8 named two errors in one CHANGELOG sentence; the fix removed one. Logged **before** Safety ran, deliberately unfixed, so the officer would reach it independently. It did. |
| 3 | Safety Officer, second run | The Dispatcher's own criterion-9 annotation gave the wrong *cause*: it said the surface list was short "for the same reason" as the count. The predecessor's grep **did** find `doctrine.md`; it was missing from the prose list for an unrelated reason. |
| 4 | Dispatcher, at close | The officer's advisory claimed a backtick in `` `schemas.md` #6 `` "evades even a naive grep", and the IC repeated it in a directive. Tested at close: the pattern's optional backtick absorbs it and the form **matches**. Two verifiers asserted a mechanism without running it. |

**The pattern is not "everyone makes mistakes."** It is that each error was
made by the seat *most* qualified to catch it, in its own area, and was caught
only downstream by someone reading rather than skimming. #2 and #4 are the
instructive pair: in #2 a seat found its own side's defect and chose to write
it down instead of quietly fixing it, which is what let the adversarial check
be a real test rather than a formality. In #4 the adversarial seat produced
the unverified claim, and only the habit of testing before transcribing kept
it out of the vault.

**Consequence for how DCS is built:** the value of the artifact chain is not
audit — it is that a claim written down becomes attackable by the next reader,
whereas a claim passed in a summary is inherited. Every one of the four
survived at least one hand-off before dying. This argues for the existing rule
that the IC transcribes structured returns verbatim, and against any future
convenience that would let a seat pass along a paraphrase.

**Two return-form deviations in the same incident** (a specialist naming a
divergence in `evidence` instead of returning `deviation`; another returning
no structured block at all, so the territory bound had to be established
forensically by the officer via `find -newermt`) are the same shape from the
producer's side — see [[Backlog]] item 14.

## 13. A rule that lives only in a prompt decays measurably

Lesson #1 says prose fails and mechanisms hold. This is the sharpest instance
so far, because for once the decay was **measured** rather than inferred, and
the rule that decayed was one written to fix this very failure mode.

v0.6.5 gave the Safety Officer's charter an explicit default: an
artifact-hygiene finding is an `advisories[]` entry, not a `halt`, unless it
clears one of three named bars. It shipped at `6a57b97`, 2026-07-25T14:19:21
+1100 (`git log -1 --format=%ad --date=iso-strict 6a57b97`), and the installed
copy under `~/.claude/` carried it the same afternoon.

It did not take. On the incident that supplied the evidence
(`C:\bread_bot\.dcs\incidents\2026-07-25-prod-tools-drift`), the
`advisories[]` channel was used **zero times across eleven officer spawns** —
`grep -c "advisor" .dcs/incidents/2026-07-25-prod-tools-drift/SAFETY.md` → 0 —
while eight of ten halts carried no functional defect by the officers' own
words, and **five of those eight postdate the install**. Anchored halt
timestamps: `grep -n "^\[.*\] SAFETY: halt" …/214-LOG.md`.

Three things are worth carrying forward.

**A prompt is not a carrier.** The charter said the right thing, in the right
place, to the exact agent that had to apply it, and eleven fresh spawns in a
row did not apply it. Nothing observed the rule, so nothing noticed it was
unobserved. `safety-halt-functional-scope` gave it check 14, which parses the
charter at run time and holds every citing surface to the charter's own live
step number, bar count and default verdict token — the check-13 shape, because
this rule has no executing module to import from the way check 12 has
`dcs_gate.py`.

**Find out whether the rule exists before designing the fix.** The register row
named the symptom ("8 of 10 halts found no functional defect") and read as
*there is no rule*. There was one. The distinction changed the incident's whole
shape — from "write a bar" to "give the existing bar a carrier" — and it was
settled by reconnaissance, not by argument. Two analysts disagreed about it,
and the disagreement was closed by one command rather than by picking the more
confident analyst.

**A fix can reintroduce the disease one file over.** The period's own new prose
put an un-regenerable number into `doctrine-appendix.md`. The Safety Officer
caught it, could not reproduce the number by any query it tried, called it "the
same class of defect this incident was opened to remove, reproduced in one file
off to the side" — **and still rated it an advisory**, because no acceptance
criterion covered the appendix text and stopping a merge over a number in a
historical note is exactly the spend the incident existed to end. That is the
bar working on its own author, which is the only test of a bar that means
anything.

### Two smaller ones, both about trusting an input

**A command decision is an input, not a fact.** At command point 4 the IC
reported a typo (`10\10` in `CHANGELOG.md:98`) that does not exist —
`grep -nF '10\10' CHANGELOG.md` returns nothing. The Dispatcher did not apply
the directive and recorded the omission. The scepticism DCS aims at specialist
self-reports applies upward too: a seat's authority is over the decision, not
over the facts it cites.

**Estimated timestamps are a derived fact like any other.** Several
`214-LOG.md` entries in that incident were stamped by estimate rather than by
clock and ran roughly 53 minutes ahead of the truth, anchored against
`git show -s --format=%ad c0fea95`. The log is append-only, so the drift was
recorded as a correction rather than tidied away — which is what append-only is
for. `close.md` step 3's rule about the real clock exists for precisely this,
and it was broken by the seat that transcribes the log.

## 14. A detector keyed on surface form cannot enumerate a population defined by role — and each narrowing looks like progress from inside

**Evidence: `deploy-marker-blind`, 2026-07-27. Five Safety Officer spawns,
four halts, three of them one class.** The diff is nine files; the cost was
not in the diff.

The incident's defect was *two statements of one contract disagreeing*. Three
detectors were built to catch that class, and **each was defeated by a
narrower surface assumption than the last**:

| Attempt | Detector | Defeated by |
|---|---|---|
| 1 | criterion 5's enumerator | **vocabulary** — the halting line read *"deployed marker was read"* and matched none of its four patterns |
| 2 | check 15's declaring predicate | **token** — `CLAUDE.md` states dispositions in exit-code words and contains **zero** `DEPLOYED` tokens |
| 3 | check 15's rule B comparator | **markup** — it required a *backticked* `` `DEPLOYED` `` in its window, and the site wrote it bare as a table label |

**The trap is that each narrowing is locally reasonable and looks like
progress.** Attempt 2 was a deliberate *tightening*, adopted for a good
reason (the loose predicate produced false positives) and defended with real
evidence — the specialist proved the tightened version still reddened
against the pre-incident tree. It was still one step further from role and
one step closer to form.

**What actually resolved it was not a fourth attempt.** The Owner ruled:
*narrow the guard's claim to what it demonstrably enforces.* Rule B was
removed rather than repaired, because a contradiction can **cite the source
correctly while naming none of its classes** — unreachable by a class-name
comparator *by construction*, not merely under-engineered.

**The transferable rule:**

> **A guard that under-claims truthfully is worth more than one that
> over-claims greenly.** The harm is never the missing coverage — it is the
> green PASS line telling the next maintainer the coverage exists.

Three of the final verdict's five advisories were that same defect one level
down: a PASS line printing *"plus the named root files"* while both were
deleted; a docstring merging two rules with different scopes; a CHANGELOG
sentence stating one rule two ways in one paragraph. **The class recurs in
the prose describing the fix as readily as in the thing being fixed.**

**When you next reach for a recognizer:** ask what the population is defined
*by*. If the answer is a role and your predicate is a string, you are
choosing how far the gap will be, not whether there is one. Answering
*"this is not reachable by a recognizer in this idiom"* in
`vault/Decisions/` is a legitimate outcome. Carried forward as
[[Backlog]] item 17.

## 15. Split one contract across two owners and the defect lands on the seam

Same incident, and it is almost too clean. Revision 1 partitioned the
contract's prose surfaces across two specialists: one held
`dcs/workflows/deploy.md`, the other held `dcs/templates/REGISTER.md` and
the rest. Both did their taskings correctly.

**Halt 2 landed exactly on the seam.** One widened `REGISTER.md`'s
`DEPLOYED` definition to admit a new route and left the facts-only block
*thirteen lines below it* stating the old route as a necessary condition;
the other's `deploy.md` cited that un-widened rule as authority. Neither
specialist could see the other's return — that is the design — so neither
could see the contradiction they jointly created.

Revision 2 gave **all six declaring files to one hand**, and the Planning
Chief said plainly why it was spending three of four specialists rather than
four: *the only credible fourth is a second prose owner, and that is the
failure mode.*

**Two corollaries worth keeping:**

- **The IC used the fourth slot anyway — read-only.** A reconciliation pass
  with **no territory**, running after the editors and before Safety, doing
  the officer's own manual read early. It earned it: it re-implemented the
  declaring predicate itself to enumerate the nine paragraphs a tightening
  had excluded, and reproduced the baseline result rather than reading about
  it. **A fourth pair of eyes is safe; a fourth pair of hands on one
  contract is not.**
- **Sequencing was the fix, not a performance compromise.** The guard had to
  be written *after* the prose it parses. Building the two against different
  snapshots of one contract is the same failure at a different scale.

**Partition by file is necessary and not sufficient.** Disjoint territories
prevent write conflicts; they do nothing about a *semantic* seam running
through a contract that spans them. When the artifact being changed is one
contract, the question is not "are these globs disjoint" but "does this
contract have one author this period".

## 16. Narrowing scope at the stem widened what could run beside it

*From `direct-resolution-lane`, 2026-07-27. One period, two specialists, one
attempt, zero deviations, zero halts — and the cheapest thing it did happened
before any specialist ran.*

The brief carried three manifestations under one asserted root cause: *"the
register state machine and every workflow that writes it were designed
exclusively for full-lifecycle incidents."* The IC ruled that sentence a
**model, not a defect**, and split on principle 4.

**The argument against splitting was concrete and it was wrong in an
interesting way.** It ran: three incidents would each edit the same enum, which
is worse than one. That does not follow — **one incident creates the state and
the others consume it**, so the enum is edited once regardless. But the
rebuttal only holds if the state's definition is general enough to be consumed
without amendment, which is why the IC turned it into a **hard bound** rather
than an aspiration: the definition may name no type, no workflow step, no lane.
A scope argument became a design constraint, and the Safety Officer later
verified by reading that both split-out rows are served unchanged.

**Then the narrowing paid a second time, in a currency nobody was tracking.**
Both chiefs recommended making `doctrine.md` and `typing.md` *forbidden* rather
than *conditional*, on the reasoning that no doctrine rule was changing and the
hot path had 1,205 B of slack. Accepting it dropped two files from the
territory — and recomputing the portfolio collision from the Territory column
showed the incident now blocked **three** queued rows instead of six. **Ranks 5,
7 and 12 were freed by a decision made for an unrelated reason.**

The generalisable part: **territory width is a portfolio cost, not just an
incident cost**, and it is invisible unless someone recomputes the collision
after the IAP narrows. `plan.md` step 5a refines the register's territory
already; what it does not do is re-derive *which rows that unblocks*. Both times
this session computed a blocked-rows list by hand it was wrong — once in each
direction — and both times the fix was to intersect the Territory column
mechanically instead.

## 17. Hand the verifier what you already found

*Same incident.* At step 5 the Dispatcher found a false claim in `CHANGELOG.md`
— it named the wrong paragraph as check 15's declaring one — and deliberately
did **not** fix it before spawning the Safety Officer, passing it forward as a
claim to verify instead.

The officer re-derived the predicate from source rather than accepting the
finding, confirmed it, and then found **three things the Dispatcher had
missed** — including that a specialist's own evidence reported a post-state as
its own baseline (`4 → 4` where the genuine count went `3 → 4`).

**The temptation is real and worth naming**: fixing it first would have been one
edit, and the verdict would have come back clean. It would also have been a
verdict on a tree the officer had not actually been asked to judge. A verifier
handed a pre-cleaned artifact returns a cheaper answer and a weaker one, and the
cost of the honest route was zero — the finding was an advisory either way, and
the IC fixed it after the verdict under `execute.md` step 9's advisory rule.

Related, and the sharper version of the same point: the officer's charter says
specialist self-reports are never listed as the check itself, only as the claim
being checked. **That rule should extend to the IC's own findings**, and here it
did.

## 18. A revision that fixes one criterion can silently unfix another

*From `register-field-repair-path`, 2026-07-27. One period, two revisions,
two halts, zero specialist deviations — and both halts were about the
plan's own paperwork, not the convention it shipped.*

**Halt 1 was an old acquaintance in new clothes.** A tasking asserted
"0.6.10 is unpublished" as fact, inherited verbatim from a sibling
incident's AAR. It was true when that incident closed and false 49 minutes
before this one's own 201 was drafted — the Owner published in between,
and nothing in the chain (two situation analysts, a Planning Chief, two
command-point spawns) ran `npm view` to check. This is §2 and §11's
"resting a decision on a number" clause, measured a second time: writing a
number and *resting a decision* on it are different obligations, and only
the first was met.

**Halt 2 is the sharper, newer lesson.** Fixing halt 1 meant rewriting
`IAP.md`'s objectives section. The rewrite carried forward criteria 1-4
and wrote the new criterion 6 — and silently dropped criterion 5's
already-Safety-verified "Criterion 5, answered" section, which lived in
the same file but was not what the rewrite's attention was on. Nothing
mechanical could have caught it: the plan's own protection for
already-verified work was a pinned sha256 of two *payload* files
(`dcs/templates/REGISTER.md`, `dcs/workflows/esg.md`), and criterion 5's
deliverable was IAP *prose* — outside the pin's pathspec by construction,
and outside `dcs_gate.py`'s reach too, since `.dcs/**` is unguarded. The
false claim that the pin covered "criteria 1-5" rode through the rewrite,
an IC self-review, and an Owner approval before the Safety Officer's full
re-read of the file caught it.

**Then the repair repeated the shape it was fixing.** Told the missing
text was "fully recoverable verbatim" from two named sources, the IC
restored a section and reported it as a verbatim recovery. It was not: a
tree-wide grep for the section's distinctive phrases found it in exactly
one file — the just-written `IAP.md` — and both cited sources hold only a
one-clause summary and a differently-worded partial paraphrase. The
*content* was right (the Safety Officer independently re-derived and
confirmed every claim in it against the actual files), but the *claim
about where it came from* was exactly as unverified as halt 1's claim
about the registry. An assertion of fidelity is a fact like any other —
principle 15 applies to "I copied this correctly" as much as to a byte
count.

**The transferable rule, in two parts:**

> A revision scoped to one criterion must still prove it preserved every
> other criterion's already-satisfied content — map each one to the
> section that carries it, in the file as it now stands, before
> re-stamping. "I only touched criterion 6" is a claim about intent; the
> map is the check on the result.
>
> A restoration claimed as "verbatim" is a citation like any other and
> must resolve the same way `grep -c -F` must return exactly the sources
> named — before the claim is written, not after a reviewer asks.

**One small aside, same incident:** a citation to a register row
(`trivial-work-inline-lane`) survived, unchanged, through a 201, an IAP,
and a register row's own quotation of itself — for hours after that row
was `KILLED` and folded into another one at an ESG sweep. A row id is a
derived fact too; nothing re-checks a citation against current portfolio
state once it is written down, the same gap §16's territory-recomputation
lesson names for a different column.

**A second small aside, discovered writing this very AAR:** "the pin only
covers payload files, so `.dcs/**` prose fixes need no re-approval" turned
out to be false in a way the pin's own gap did not predict. Fixing the
advisories above meant editing `IAP.md` again, post-pass, and the
Dispatcher assumed that was harmless bookkeeping. `dcs_gate.py`'s actual
execution-phase logic (read from source, not from memory of what it
"should" do) checks `marker_valid()` **unconditionally** for any target
outside `.dcs/**` — the `guarded_paths`/`unguarded_paths` exemption only
matters *inside* the halt-ceiling sub-check, reached only once the marker
is already valid. An invalid marker denies every other edit outright,
`vault/**` included, regardless of what `config.json` lists it as. The
next Edit call (to this very file) was denied, correctly, for exactly the
reason the mismatch predicts. **A rule read from a docstring's *intent*
("`.dcs/**` bookkeeping is unenforced") is not the same rule as the code's
actual branching** — the intent is true of `.dcs/**` specifically, and
the Dispatcher generalised it to "post-pass paperwork changes are
unenforced," which the source does not say and does not do.

## 19. A regeneration command must be able to establish the fact it sits beside

*From `criterion-unmeasured-fact`, 2026-07-28 — the incident that added
lint 4a check 3b (measured claims), one period, zero halts, zero
deviations. The lesson is not the fix; it is what the Safety Officer found
while verifying it.*

**The fourth field instance of the class was found by the fix's own
verifier, in a store the fix cannot reach.** Verifying check 3b, the
officer ran the establishing command itself — `npm view
dcs-command-system versions` — and found
`vault/Decisions/fable-review-roadmap.md:24-25` asserting "0.6.10 remains
unpublished (registry at 0.6.9)" while the registry already held 0.6.10.
That line even carried a "regeneration command" — *read the row's State
cell and `git log main..dcs/direct-resolution-lane`* — which **reads
in-tree state to back an out-of-tree claim**. It looks principle-15
compliant (a command sits beside the fact), and it can never establish
the fact. The test is not "is there a command beside it" but **"can this
command, run now, make this sentence true or false"** — check 3b's (i)
encodes exactly that for 202 criteria (`the command that establishes the
fact`), and reviewers of vault/register prose should apply the same test
by hand.

**The lint guards the lifecycle path only.** Check 3b fires at tasking
lint on 202 criteria; the MEASURED CLAIM template block fires at
authoring; the chief's charter fires at plan review. Vault notes,
register cells and sitreps stay unguarded — their stale external claims
get corrected only when someone next runs a live measurement, as happened
here. That boundary is honest and should be stated, not papered over: an
unguarded store accumulates exactly the claims the guarded path now
rejects.

**Dogfooding is a cheap false-positive test.** The incident applied its
own rule to its own paperwork before landing it: the 202's five criteria
contain zero unmeasured external facts (the one external-looking
criterion carries `grep -n "^## Unreleased" CHANGELOG.md`, an in-tree
read), and the verification plan bound the trigger's reach at "at most
one of five may fire" — the officer measured 0 of 5. A new
classification rule should always be pointed at the incident that ships
it; it is the one corpus guaranteed to be fresh.

## 20. A fix's own author should not author its own acceptance fixtures

*From `deviation-path-proportionality`, 2026-07-28 — one period, one
attempt (four stamps), three Safety halts, one escalation
(triggers b/c/e folded into one Owner decision), zero specialist
deviations, final verdict pass with zero refutations. The fix shipped is
[[Backlog#11|the deviation-arbitration cheap route]] itself; the lesson
is what it took three tries to notice about how DCS verifies its own
fixes.*

**Three consecutive fix-taskings each closed the specific hole a halt
named and opened a different one in the same admission boundary, because
the same agent that wrote the fix also wrote the test that passed it.**
Halt 1 found two independent scoping defects in `plan.md`'s new `## 6c.`
boundary. The fix-tasking closed both — and, in the same pass, widened a
third clause to admit a case it never constructed a fixture for. Halt 2
caught that. The Owner sanctioned a "raised-altitude" retry: one
per-artifact invariant instead of an enumerated branch list, with
mandatory validation against both cited field measurements before the
fix-tasking could report `done`. It followed the instruction faithfully,
validated exactly what it was told to validate, passed — and had, in
widening the boundary to admit one real case, silently admitted a second
one nobody had reviewed (a brand-new tasking file, for which the
boundary's own "provably didn't change" claim was vacuously false). Halt
3 caught that too. Same class, three times: not a wording bug repeating,
but a structural blind spot — a fixture set designed by the same
reasoning that designed the boundary inherits that reasoning's blind
spots by construction, and no amount of "validate more thoroughly this
time" instruction closes a gap the drafter cannot see is there.

**What actually broke the pattern was two changes at once, not a fourth
guess at the wording.** First, the fixture population moved from
specialist-authored to IC-authored — eleven must-admit / must-reject /
must-catch-by-execution cases, specified before the fix-tasking was
spawned, which the specialist could extend but not substitute, weaken,
or drop. Second, and this is the sharper finding: **the recurring
"these three lint checks are provably unneeded here, skip them" claim
was deleted outright**, once it was noticed that running the checks
costs nothing under the incident's own success metric — its acceptance
criterion counted only agent spawns and Owner round-trips, and lint
execution is neither. Three of the incident's four refutations were, in
different clothes, that same skip-claim being wrong about a case its
author hadn't considered. A check that always executes cannot be
vacuously skipped; there was no economic reason to keep the optimization
once someone asked what it was actually buying.

**The mechanical halt-ceiling counter and the doctrinal escalation
triggers protect against the same runaway loop from two different
distances, and only one of them held up under this incident's own
weight.** Every `## 6c.` re-stamp is a fresh `IAP-APPROVED:` sentinel,
and `dcs_gate.py`'s `halt_cycles()` re-anchors on that sentinel — so a
halt → fix → re-stamp → halt cycle never approached the per-attempt
ceiling on its own; this incident's own live tally read `0`–`1`
throughout, against three real halts. What actually fired, correctly,
both times, was doctrine's log-wide accounting that no re-stamp resets:
trigger (b) (second halt on the same objective, counted across the whole
`214-LOG.md`) and trigger (c) (cumulative `IAP-APPROVED:` count against
`esg.max_periods_before_review`, which this incident's four stamps
reached exactly). Both escalated to the Owner as designed, and the
Owner's "continue" at round 2 was logged as a decision, not treated as a
reset — doctrine's own stated distinction, exercised for real. The gap
this surfaces is narrow but real: the *cheap route's own* re-stamp
undercuts the *mechanical* ceiling that is supposed to bound cheap
iteration, even though the *doctrinal* ceiling still holds. Flagged for
`/dcs-esg`, not fixed here — this incident's own standing constraint
forbade touching `dcs_gate.py`.

**A "post-pass advisory correction that touches `IAP.md`" was not a rare
edge case this incident merely fixed — it happened repeatedly inside the
incident's own execution.** Every one of the IC's four bookkeeping
re-stamps (recording a corrected criterion-3 table, three times over)
was exactly the case `register-field-repair-path` first surfaced and
this incident's criterion 1 was widened mid-flight to cover. Dogfooding
a fix inside the same incident that ships it is not always available,
but here it was forced by circumstance rather than chosen, and it is the
sharpest confirmation the fix's own field measurements got.

## 21. The verifier's own record is not exempt from the rule it just wrote

*From `token-economy`, 2026-07-28 — Type 1, one period, one attempt, zero
specialist deviations, Safety verdict pass with zero refutations, six
advisories. The fix shipped is
[[Backlog#21|criterion 4's by-reference citation mechanism]] itself; the
lesson is what happened the very first time that mechanism's own
precondition was tested for real.*

**Criterion 4 built a rule that a Safety Officer may cite a prior
same-period verdict's `checked[]` entry by reference instead of
re-deriving it, but only for a subject it has independently reconfirmed
unchanged with a named command — never trusted from the written record
alone.** In the same period that rule was designed, wired end to end,
and dry-run tested against a past incident's `SAFETY.md`, the verdict
*this period's own Safety Officer wrote* contained a `checked[]` entry
that was simply false: "confirmed `new.md` and `plan.md` are absent from
`git status`" — `plan.md` was one of the period's 15 modified files,
legitimately edited by a different specialist for an unrelated criterion.
The Safety Officer did not catch its own error (self-review is not what
adversarial verification means), and no specialist was positioned to —
the claim was about the *union* of the diff, not any one territory.

**What caught it was `dcs-commander` applying the Safety Officer's own
standard one level up, at the very next command point.** Command point 4
does not exist to rubber-stamp a `pass`; this incident's own commander
re-ran all three guards independently, then read `plan.md`'s actual diff
because the verdict's own claim was checkable in one command. It found
the claim false, then checked whether the *invariant the claim was
defending* — that criterion 3's territory-glob-writing logic in
`plan.md` step 5a was untouched — still held. It did, because the
specialist's edits sat at unrelated line numbers. The false clause was
therefore a **record defect, not a deliverable defect**: the pass stands
on its merits, re-verified directly, not on the strength of the sentence
that happened to be wrong.

**Why this is not a near miss to shrug off.** Had a *second* Safety
Officer spawn existed this period (it did not — one clean pass, no
fix-tasking cycle), and had it cited this exact `checked[]` entry by
reference under the very rule shipped this period, it would have
propagated a false claim into a new verdict without re-checking it —
compounding the error under the label of the mechanism built to prevent
exactly that. The rule's own text already forbids citing anything in a
fix-tasking's `files_touched`; it says nothing about a citation source
that is itself wrong through simple author error, because nobody had
tested that path yet. This period did, by accident, on its first day.

**Candidate hardening, not built here:** either (a) a by-reference
citation must itself be accompanied by the officer re-running the one
command that would falsify it (turning "cite" into "cite and spot-check",
which partially defeats the savings the rule exists for), or (b) treat
this as evidence that verification records need a cheap, mechanical
cross-check — not a re-derivation, just confirming a stated file-absence
claim against `git status` — before any later reader may rely on it by
reference. Option (b) costs one grep per citation, not a full re-run, and
targets exactly the failure mode observed: a false *absence* claim, which
is the cheapest kind of claim to mechanically check and the kind this
incident's own record got wrong. **Not queued as its own row** — folded
into the follow-up incident `token-economy` registered at close for its
four remaining one-line advisory fixes; this is a fifth, and the only one
that touches a mechanism rather than a phrasing.

## 22. A shipped discipline is not a habit — its own author can violate it in the very next step

*From `token-economy`'s close and deploy, 2026-07-28. The Owner caught
this one, not any mechanism: "I thought we also agreed to change the
outcome field to reference existing files?"*

**Criterion 3 replaced `REGISTER.md`'s Outcome cell with a one-line
pointer, specifically to stop exactly the pattern it had grown under:
narrative restated inline instead of cited from where it already lives.**
At close, the Dispatcher applied that mechanism correctly — `token-economy`'s
own row got "see AAR.md Outcome," one line, nothing more. At the very
next command, `/dcs-deploy`, writing the same cell again to record the
ship, the Dispatcher appended a full paragraph of deploy-verification
narrative directly after that pointer — reproducing the pre-fix shape in
the same cell it had just fixed, one command later.

**No mechanism caught this, because none was built to.** Criterion 3's
own verification (this period's Safety Officer, `dcs-commander`'s
re-check) tested the *shipped rule's text* and its *first application*,
both of which were correct at the time they were checked. Nothing
re-checks a rule's *second* application, by its own author, after the
incident that built it has closed — the paper trail that would normally
catch a specialist's mistake (Safety Officer, commander, lint) has no
seat left running once `/dcs-close` finishes. The only reviewer left is
the Owner reading the artifact directly, which is what happened here.

**Why this is not the same as Backlog item 20 (workflow prose degrading)
or Meta §21 (a verifier's own checked-item being wrong).** Those are
about a *written rule* decaying or a *verification claim* being false.
This is neither: the rule was correct, freshly shipped, and correctly
applied once — the failure is that applying it correctly once did not
generalize to the very next time the same author touched the same field,
one command later, with no distance and no excuse of a stale mental
model. A rule shipped in `dcs/templates/REGISTER.md` binds a future
Planning Chief or Ops Specialist reading the template; it does not, by
itself, bind the Dispatcher's own next keystroke.

**Candidate hardening, not built here:** a mechanical check that a
`REGISTER.md` row's `Outcome`/`Territory`/`Intake source` cell, once
collapsed to a `see <file>.md ...` pointer, stays exactly that — a single
line matching the pointer pattern, nothing appended after it — would
have caught this at write time without needing a reviewer to notice.
Cheap to check (one regex per cell, at any point something writes to
`REGISTER.md`), and it targets the actual failure mode: not "does the
rule exist" but "does this specific write obey it."

## 23. A `.dcs/esg/` read is a derived fact with a lifetime, same as any other

*From `STRATEGY.md`'s fifth `/dcs-esg` session, 2026-07-27, consolidated
into Meta 2026-07-28 while retroactively compacting that file's Sessions
log.*

A session swept the portfolio at its start and reported to the Owner
that a just-shipped row still awaited deploy, and that it named a branch
`git show-ref` could not find. Neither reading was wrong when taken —
both were **stale**: a deploy train ran in the interval between the read
and the report, transitioning the row and deleting the branch. The
register was correct throughout; the session's own memory of it wasn't.

**The generalization is the same one principle 15 already states for
code and prose, applied to the ESG's own state:** `REGISTER.md` and
`STRATEGY.md` are exactly the files a *parallel* session is most likely
to be writing while another session reads them (that is the entire
point of v0.3's parallel-operation model), so a value read from either
at the top of a session is a snapshot, not a fact — it needs re-reading
immediately before it is acted on, not merely at sweep time. The session
that hit this treated it correctly: withdrawn from its own agenda rather
than quietly corrected and moved past, so the pattern is visible to the
next reader instead of erased.

## 24. A budget that only prose enforces gets overrun by the very mechanism meant to hold it

*From `workflow-budget-enforcement`, 2026-07-28.*

`CLAUDE.md` stated a ~250-line workflow-file budget from early in this
project's self-hosted life. Nothing measured it. The gap survived **two
`/dcs-esg` declines** (5th and 6th sessions, 2026-07-27 — sharper
evidence each time, still not queued), then cost two ad hoc IC rulings
in one incident (`deploy-marker-blind`: a 265-line ceiling, then a
pre-authorised band to 275) — and the file **still drifted past that
ruling** to 282 in the very next commit that touched it, because the
ruling was prose too, just prose with a number in it. Only a mechanical
check stopped the drift; the third and fourth ad hoc measurements
(`criterion-unmeasured-fact`'s Safety advisory, this incident's own
stem) were the same lesson landing a third and fourth time before it
was acted on. Directly confirms Meta 1 ("prose fails; mechanisms
hold") against a rule this project wrote about *itself* and still did
not mechanize for two ESG cycles.

**Two design choices worth carrying forward, both counter-intuitive on
first look:**

- **Zero headroom, not slack, when grandfathering existing debt.** The
  instinct when a check would otherwise redden four already-over-budget
  files is to grant a little room to breathe. That instinct is exactly
  what produced the defect this incident fixes — `deploy.md`'s ceiling
  drifted 265 → 275 → 282 through two successive small grants, each one
  individually reasonable. Pinning the grandfather ceiling at each
  file's *exact* current size, with the comment stating it is debt (not
  a new normal), removes the slack that a future well-intentioned "just
  a little more" would otherwise consume.
- **A check that has only ever been seen green is not yet trusted.** The
  Planning Chief mandated two demonstrated red-path failures in the
  implementing tasking (not merely "the check exists and passes") before
  the Safety Officer would treat criterion 1 as met — and the Officer
  went further, independently reddening the check **eight ways**,
  including two nobody had asked for (a *compliant* file crossing 250; a
  grandfathered file growing by exactly one line). This project's own
  suite had already paid for the alternative twice — a Rule B removed at
  a halt for over-claiming coverage it couldn't deliver, a comparator
  built only after someone thought to forge a mapping past it. Green
  proves the code runs; only an engineered red proves the comparator
  points the right way.

**A secondary, process-level finding:** the Logistics Chief's plan
named a deliverable (an atomic version bump, since the new check ships
inside `tests/`, which npm's `files` whitelist includes) that mapped to
no tasking — both existing ones explicitly forbade the files it
touched. Caught at the mechanical tasking-lint pass (`plan.md` 4a check
2, orphaned deliverables) before it reached command point 2, not
discovered mid-execution. The lint step existed for exactly this shape
of gap and worked on the first incident to produce one since it was
written down.

## 25. A specialist's project root must be the worktree, not the main checkout

**When:** `token-economy-advisory-fixes` (2026-07-30) — Type 3, four
one-line text fixes, 4 specialists in parallel.

**What happened:** specialists were given `Project root: C:\dcs` (the main
checkout) in their tasking prompts. All four applied their edits to
`C:\dcs\...` instead of `C:\DCS-wt\token-economy-advisory-fixes\...`.
The Dispatcher caught this at integration-commit time (the worktree had
no modified files), copied the four files from main checkout to worktree,
committed there, and restored the main checkout with `git checkout --`.

**Why it matters:** the worktree *is* the incident's world until merge
(v0.3, principle 6). Edits in the main checkout are edits to the
integration branch outside the gate — `dcs_gate.py` had an ACTIVE file
in the worktree but the target files were in the main tree, so the gate
could not block them. Two sessions editing the same file in parallel
would have noticed only at merge time.

**Resolved** `worktree-path-propagation` (2026-07-30), commit `16e4307`:
the fix is now **mechanical**, not just procedural. Three changes applied:
(1) `agents/dcs-ops-specialist.md` — `worktree_root` input + territory-
resolution rule in `<process>` step 3; (2) `dcs/workflows/execute.md` step
4 — instruction to compute `worktree_root` from `git worktree list
--porcelain` and pass it to every specialist; (3) `dcs/templates/
204-TASKING.md` — `## Worktree root` field with `{{worktree_root}}`
placeholder. The original procedural fix («the Dispatcher must pass the
worktree path») was documented here but never applied to code, leaving a
gap between the vault lesson and the running system — exactly the kind of
drift this lesson's own existence should have prevented.

**Also this incident:** the Agent tool's safety classifier
(`deepseek-v4-pro`) was intermittently unavailable, blocking specialist
and Safety Officer spawns across multiple model tiers. One specialist
tasking (S3 — a one-sentence text insertion, fully specified by the
Planning Chief) was applied by the Dispatcher directly. The Safety
Officer independently verified the result and did not refute it. The
lesson is not "Dispatcher-as-specialist is acceptable" — it is that the
gate's project-root mismatch above made the Dispatcher's direct edit
*ungated* for the same reason the specialists' edits were: the ACTIVE
file lived in a different tree from the files being edited.

## 26. A mechanical fix for worktree-path propagation shipped, and the very next specialist still edited the wrong tree

**When:** `provisioning-script-upstreaming` (2026-07-30) — Type 1, the incident immediately following `worktree-path-propagation`'s deploy.

**What happened:** S1 (dcs-ops-specialist) edited `C:\DCS\dcs\workflows\new.md` and `C:\DCS\dcs\workflows\execute.md` — the main checkout — despite the 204 tasking stating `Worktree root: C:\DCS-wt\provisioning-script-upstreaming`. S1's `files_touched` accurately reported the main-checkout paths, so the specialist was truthful about what it touched but edited the wrong tree. S2, in the same period with the same tasking format, correctly edited the worktree. The bug is intermittent — it does not reproduce on every spawn.

**How it was caught:** the Dispatcher ran `git -C <worktree> diff --stat` after S1 returned and saw zero modified files; `git -C <main> diff --stat` showed the changes. The fix was mechanical (copy files, revert main) but the gate did not block the main-checkout edits because `.dcs/ACTIVE` lives in the worktree while the specialist targeted the main tree — the gate's root-resolution logic had no ACTIVE file in the main checkout's tree.

**What's different from §25:** §25 documented the *absence* of a mechanical fix and the project-root mismatch in the specialist prompt. This incident ran *after* the fix deployed — `dcs/templates/204-TASKING.md` carries the `## Worktree root` field, `dcs/workflows/execute.md` step 4 instructs computing `worktree_root` from `git worktree list --porcelain`. The fix is present in the running system and the defect still reproduced, once, on the first specialist spawn after deploy. The second specialist correctly resolved to the worktree.

**Candidate hardening, not built here:** verify the specialist's `files_touched` paths all resolve to the worktree root before accepting a `done` return — one `grep` per path against the worktree prefix. A path outside the worktree is a deviation regardless of whether the specialist self-reported as `done`. This check is cheap (no re-spawn, no re-verification) and catches the failure mode mechanically rather than waiting for a human to notice a zero-diff worktree.

## 27. A column-width wrap instruction is not a specification when two mechanical constraints interact — and `awk`'s `length()` counts bytes, not characters, on this host

**When:** `trim-content-loss-restoration` (2026-08-01) — Type 1, restoring content two prior trim commits had dropped, under an inviolable line/byte budget.

**What happened, part one:** a tasking for `close.md` needed to insert a citation into a budget-saturated file while satisfying two independent mechanical constraints at once — merge-guard check 20 (a field-lesson identifier must fall on the flagged line or the one immediately after) and a discriminating `grep` (a specific string must stay unbroken on one line). The Planning Chief's first two attempts gave the specialist a column-width bound ("<= 76 columns", then "<= 78 columns") rather than dictated lines. `dcs-commander`, reviewing at command point 2, simulated every width from 60 to 78 and found only ONE (71, for `close.md`; 78, for two blocks in `execute.md`) satisfied both constraints simultaneously — every neighbouring width failed one or the other. Two IAP-review rejects were spent finding this. The third revision dictated literal lines with per-line character counts, and passed.

**What happened, part two:** once lines were dictated by character count, the taskings' own evidence commands (`awk ... {print length($0)}`) were verified against them — and failed, on a byte-exact, correctly-transcribed candidate. `LANG`/`LC_ALL`/`LC_CTYPE` are unset in this environment's Git Bash, so GNU Awk counts **bytes**, not **characters**; every dictated line containing U+2014 EM DASH (3 bytes, 1 character) read 2 higher than its dictated count. Both taskings' own instructions ("a different sequence means a line was re-flowed; report it rather than adjusting") turned a *correct* transcription into a *mandated false deviation*. This fired doctrine's escalation trigger (f) (third IAP reject in one period) — but the IC's own diagnosis, verified by constructing a byte-exact candidate tree and running it against the real merge guard before the third review even started, found the plan's *content* had been correct since revision two; only the evidence-command *specifications* were an environmental artifact. The Owner reviewed the 209 sitrep and chose "continue with 6 named fixes" over re-scoping or decomposing — correctly, since neither of doctrine's other two trigger-(f) diagnoses (wrong objectives, narrow chief information diet) applied.

**A related encoding trap in the same incident:** a dictated Python one-liner using `subprocess.run(..., text=True)` to prove a test-file edit was comment-only (via `ast.dump` equality) printed `AST DIFFERS` on this host — `text=True` decodes with `locale.getpreferredencoding()`, which is `cp1251` here, not UTF-8, mangling the same class of non-ASCII character. Decoding raw bytes with an explicit `.decode('utf-8')` fixed it and confirmed the edit really was comment-only.

**Why it matters:** two Windows-hosted, locale-dependent decoding defaults (`awk`'s byte-counting `length()`, Python's `subprocess.run(text=True)` platform-preferred-encoding) independently produced false negatives against correct work, in the same incident, both triggered by the same single non-ASCII character. Neither is a DCS defect — both are host-environment facts a cross-platform tasking author cannot assume away. **Candidate hardening, not built here:** any tasking dictating a per-line length check or a text-mode subprocess read should either specify the expected values in the host's actual counting unit (bytes, verified live) or force UTF-8 explicitly (`LANG=en_US.UTF-8 awk ...`, `.decode('utf-8')` on raw bytes) rather than trusting a locale default that varies by host.

## 28. Qualifying a ref lookup to a namespace is not the same as making it disambiguation-free — and a security-relevant advisory earned its own incident rather than a silent fold-in

**When:** `release-provenance-guard` (2026-08-01) — Type 3, the incident
building DCS's own npm publish-time provenance gate (`dcs/VERSION` and
`package.json` version-synced, a matching git tag at `HEAD`, and a
truthful `CHANGELOG.md` entry, checked in `prepublishOnly`).

**What happened, part one:** the first Safety Officer verdict halted on
`check_tag_at_head` resolving the tag via a plain `git rev-parse
tag^{commit}` — no namespace qualification at all — so a branch or
remote ref named `vV` satisfied the check with zero real tags present.
The fix-tasking qualified the lookup to `refs/tags/` with `--verify`,
closing that hole; the re-verification pass confirmed it (the exact halt
fixture now correctly exits `1`). But the same Safety Officer, re-running
its own adversarial sweep rather than trusting the fix as done, found the
qualification was not actually disambiguation-free: `git rev-parse
--verify refs/tags/<tag>^{commit}` still runs the *qualified string*
through git's full refname resolution table, which includes `refs/heads/
<refname>` — so a branch literally named `refs/tags/<tag>` (the
already-namespaced string, not the bare tag name) still satisfies the
check with zero real tags. Reproduced independently twice more (by
`dcs-commander` at command point 4, before ruling on it, and originally
by the Safety Officer that found it) before either party accepted it as
real.

**What happened, part two:** the commander ruled the residual hole an
advisory, not a halt — unreachable by accident (no convention, refspec,
or fetch produces that branch name; anyone who could create it could tag
for real instead, so it grants no capability) — but then declined to
apply `execute.md`'s own default of folding pass-time advisories into the
9b integration commit. Its reasoning: the fix rewrites the load-bearing
line of the exact security guard the period just spent two Safety passes
verifying, so folding it in post-verdict would ship an unverified change
under an already-spent pass — "the exact pattern that produced this
period's first halt." It routed the fix to a follow-up incident
(`tag-refname-disambiguation-hole`, QUEUED) instead, keeping the proven
gate merging on schedule.

**How it was caught:** entirely by the Safety Officer's own discipline of
building fixtures from scratch rather than accepting a fix as closing the
class it was tasked against — the fix-tasking's evidence requirements
asked for the *named* fixture (branch named plainly `vV`) to pass, and it
did; nothing forced re-probing the qualified-string form. The officer
probed it anyway, unprompted, because the *general shape* (a ref
namespace admitting an unexpected literal name) was still open even
though the *named* instance was closed.

**Why it matters:** "qualify the lookup to a namespace" reads like it
should be the complete, disambiguation-free fix — the mental model most
engineers reach for is "restricting to `refs/tags/` means only tags can
match." It doesn't hold once the qualification is applied *as a string
prefix fed back into a tool that still disambiguates*, rather than as a
constraint on *which resolution rule fires*. The disambiguation-free form
is a lookup with no fallback table at all (`git show-ref --verify
refs/tags/<tag>`, exact full refname only) — qualifying the input to
`rev-parse` is not equivalent to bypassing `rev-parse`'s own resolution
logic. Separately: this incident's "fold advisories into 9b" default
almost absorbed an unverified security-line edit into a commit riding on
a verdict that never saw it — caught only because the commander reasoned
past the written default rather than applying it literally.

**Candidate hardening, not built here:** (1) any future git-ref existence
check in this codebase should default to `show-ref --verify` for
exact-refname matching, never a qualified string passed to `rev-parse`;
(2) `execute.md` step 9's advisory-folding default should carve out
advisories whose fix touches a line the current period's own Safety
verification just certified — see Backlog #29 for the concrete text
change, not applied here to avoid editing a hot-path workflow file as a
side effect of an unrelated incident's close.

## 29. An incident's own intake description is a derived claim too — and can be corrected by the specialist work it commissions

**When:** `record-integrity-corrections` (2026-08-02) — Type 3, one period,
correcting four record-integrity failures from an external review (a fifth,
a missing CHANGELOG entry, turned out already resolved by an unrelated
commit and was dropped at the stem), under a "append corrections, never
edit" mandate that was the whole point of the incident.

**What happened:** the register row that queued this incident stated the
defect as "`halt-enumeration-grammar-drift` cites nonexistent merge
`b4af6e4` (no merge of its code exists — 48ea59a is linear on main)." The
first half is true; the second half is not. `48ea59a` genuinely has one
parent and is not itself a merge — but the incident's own specialist,
instructed to re-derive rather than paraphrase, found the code DID reach
main via two real merge commits (`f7e0cc9`, `838adea`); `48ea59a` simply
reached main *through* one of them. The appended correction states this
accurately, quietly contradicting the very register row that commissioned
it. The Safety Officer caught the discrepancy unprompted — nothing in the
202 asked it to re-check the register row's own prose — and filed it as an
advisory (no acceptance criterion covered it, and the IAP never authorised
editing the register mid-incident), with the fix deferred to the close's
own ACTIVE→MERGED register write, where the row is legitimately touched
anyway.

**Why it matters:** every intake description, however carefully sourced,
is a claim with a lifetime like any other principle-15 fact — including
the ones that commission an incident to fix claims with a lifetime.
Writing "verify, don't trust" into a 202/204 does not exempt the *writer*
of that 202/204 from the same rule for their own framing. A smaller-scale
echo of Meta §21 ("the verifier's own record is not exempt from the rule it
just wrote"), landing on the *intake* side of the pipeline instead of the
*verification* side.

**Also this incident:** an Ops Specialist completed its tasking correctly
— three new files, right content, every constraint honoured — and returned
a long, accurate, well-evidenced prose report with no `schemas.md #4` JSON
block anywhere in it. Task-correctness and schema-compliance are
independent axes; a specialist can score full marks on the first and zero
on the second. The Dispatcher declined to hand-transcribe JSON from the
prose (constructing the record a specialist was supposed to hand over is
exactly the shortcut this incident existed to discourage) and instead
spawned a second, narrowly-scoped instance — explicitly read-only,
forbidden from re-touching any file — whose only job was to confirm the
existing state and emit the missing block. Cheap (no re-work, no risk to
already-correct files) and cleanly distinct from a doctrine-9b "revision"
(the tasking never changed; only the return's form did).

**Candidate hardening, not built here:** a specialist return with a
`status` line and real evidence but no parseable JSON block is currently
caught only by the Dispatcher noticing prose where a fence was expected —
nothing mechanical flags it before the IC reads the whole response. A
one-line grep for a JSON-shaped fence in the raw return, run immediately
after any `dcs-ops-specialist`/`dcs-planning-chief`/`dcs-safety-officer`
spawn, would catch this class before the Dispatcher has to notice it by
eye.

## Links

- [[Post-mortems/energy-cost-model-rework]] — the incident behind v0.5.12
- [[Metrics/incident-metrics]] — the evidence base
- [[Backlog]] — including the rows `doctrine-hot-path-trim` discovered
