# DCS Doctrine — Appendix (provenance, field lessons, background)

This file is commentary, not constitution. `doctrine.md` is the normative
core — every MUST/NEVER/definition/threshold lives there and stands on its
own. This appendix exists for humans (and the ESG) who want the *why*:
which incident taught a rule, the ICS analogy behind a mechanism, the
longer version of a rationale that doctrine only gives one clause of.
Nothing here is `@`-included by any workflow or agent — if a rule matters
to how an agent behaves, it is already in the core.

### Field-lesson citation convention

Every field lesson in this appendix (and throughout the package) follows
one of three citation forms, depending on when the originating incident
occurred relative to the self-hosting boundary (2026-07-25, when DCS began
running its own incidents under its own process):

- **Post-self-hosting (date >= 2026-07-25):** the originating incident's
  slug in backticks — e.g., incident `decomposition-backlog-routing`.
  The slug matches the incident directory name under `.dcs/incidents/`.
- **Pre-self-hosting with known version (date < 2026-07-25):** the DCS
  version at the time of the incident — e.g., `v0.5.2`. The version alone
  is the identifier; no additional annotation is needed.
- **Pre-self-hosting without a known version or date:** the literal note
  `(predates self-hosting)`, which is the best-available identifier when
  neither an incident slug nor a version number is known.

Headings below mirror the core's section names so you can jump from a
core rule straight to its story.

## Why phases, not nesting

The deeper reason DCS reaches for ICS at all: in a real incident, the
first unit on scene doesn't wait for a fully-staffed command post before
acting, and a large incident doesn't collapse into one person doing
everything either — it activates only the sections the scale demands
(this is where DCS's "scalable activation" principle comes from). ICS
solves the same problem software agent orchestration has: how do you get
disciplined division of labor without a live, ever-present supervisor.
Claude's inability to nest subagents is what forces the ICS chain of
command into a **temporal** shape instead of a live one — chiefs don't
supervise specialists in real time, they hand off a tasking and read a
report later, the same way a shift's day-chief hands off to the
night-chief through a logbook, not a phone call.

## Transfer of command

The ICS original: the person who first reports "I see fire on that
distillation tower" is never required to be the incident commander — the
first unit on scene takes the report and runs initial actions, and
command transfers to the qualified IC when they arrive. This matters
because it is the whole justification for why DCS doesn't insist the main
session itself be the smartest available model: exactly as a report can
come from whoever's on shift, a Dispatcher on any model tier can take the
initial report and run the mechanics, while the actual command judgment
transfers to a qualified seat (Fable, or the strongest tier that's
actually available) the moment a real decision is needed. The prohibition
on the Dispatcher ever quietly deciding for itself exists because that is
precisely the shortcut a tired shift-lead is tempted to take in real ICS
too — "I'll just make the call myself, no need to loop in the IC for
this one" — and it is exactly how authority erodes in both domains.

**Model availability rationale.** Why re-testing at every command point is
mandatory rather than a convenience: quota limits are time-windowed and
restore, and any incident that runs for hours routinely outlives the
window that produced an earlier failure. "Fable is exhausted" is
therefore a **derived fact with a lifetime** (principle 15) — true when
measured, false when read — and once it is written into an append-only
log it reads as a standing condition to every later command point that
never re-checks it, silently demoting the seat for the rest of the
incident. The cost asymmetry behind always trying the preferred tier
first: a spawn that fails again costs one wasted spawn, which is
trivially cheaper than running every remaining command point at a lower
tier than the Owner is paying for. The announce rule has its own small
rationale too: a command-point agent writes nothing by design (the
single-writer rule), so its working time is indistinguishable from a
hang unless the Dispatcher says out loud that it is spawning.

**Field lesson 2026-07-24 (quota vs. transcript, predates self-hosting).** The rule that
liveness is measured by the decision, never by a proxy, comes from one
incident that produced both halves of the failure mode in a single
sitting. A command-point spawn on Fable was genuinely killed by quota
exhaustion partway through; that was correctly diagnosed as dead and
re-spawned on `opus`. Later in the same incident a different spawn was
misdiagnosed as dead from a zero-byte transcript, when it had in fact
already returned a complete `reject` verdict — the transcript file
simply had not flushed yet, a harness artifact, not evidence of death.
Acting on that second misdiagnosis would have written a fabricated
failed-attempt entry into the append-only 214 — exactly the derived-fact
error principle 15 forbids, this time inside a log nothing can retract.

## The working principles

**Principle 15 — no derived facts (field lesson 2026-07-24, v0.5.2).** The
motivating incident existed to stop two branches silently allocating the
same migration number. Inside it, an unmeasured assertion travelled `IC
prose → Safety Officer prose → Dispatcher-relayed tasking → committed code
comment`, faithfully transcribed at every hop — **three times in one
incident, once by each seat, including the IC and the Dispatcher.** No hop
was dishonest; each seat had a named upstream source and no reason to
doubt it. The Safety Officer caught two of the three, one of them its own.

Two details are the reason this became a principle rather than a project
pitfall. First, the third instance could not be *corrected*: two competent
independent measurements returned different counts (48 and 56) because
they used different predicates for "carries a version token", so the
remedy was to **delete the number** and describe the shape instead.
Second, the same incident independently re-derived the same law in two
other forms — its ADR banned pinned commit hashes after a reference tree
rotted from `060132b0` to `f21fdd42` within hours of being written into
the plan, and the host project's own `CLAUDE.md` had *already* banned
hardcoded numbers in docs after a schema version, a plugin count, and a
test count all rotted. Three rediscoveries, three local bans, no general
rule — which is what a doctrine principle is for.

The enforcement choice was deliberate and is the incident's other lesson:
the mechanism that shipped worked because it produced a **git conflict**,
while the intuitive alternative (a monotonic counter) merged cleanly and
double-allocated. A doctrine paragraph alone is the monotonic counter. So
principle 15 lives in the Safety Officer's process, an adversarial seat
that already caught two instances with no rule telling it to look.

**Principle 14 — goal drift (field lesson 2026-07-22, v0.3.2).** The
original incident that motivated this trigger: a multi-period incident's
202 objectives, redrafted at the start of period 3, had quietly grown
acceptance criteria that traced to nothing in the 201's original Symptom
section — a plausible-sounding feature had been folded in because it was
adjacent to the code being touched, not because the incident was ever
supposed to deliver it. Nobody involved thought they were doing anything
wrong in the moment; each individual 202 revision looked like a reasonable
next step from the previous one. The lesson: an incident is supposed to
*converge* on its original goal, not *accrete* new ones period over
period, and the only reliable tripwire for that drift is comparing each
new 202 against the 201 verbatim, not against the previous period's 202
(which is exactly the document that's already drifted).

**Principle 4 — the cost of over-scope.** Why Type 1's full-org
authorization for unbounded scope is a genuine risk and not a formality:
nothing downstream can undo an over-scoped 201. The halts, rejects, and
escalations built into the P-loop all still fire correctly against an
over-scoped incident — but firing correctly costs hours each time, so the
mistake survives being caught, it just gets caught expensively. The
"model, not defect" trap this principle guards against: a goal like
"rethink how X is accounted" names an ongoing condition rather than a
fixable defect, exactly the shape of goal that keeps growing scope no
matter how tightly the incident is typed.

**Principle 4 — the missing bar between "decompose" and "register" (field
lesson 2026-07-28, v0.6.13, incident `decomposition-backlog-routing`).**
This principle's own text told step 4a to register *every* split-out
defect, unconditionally — the rule that prevents scope creep inside one
incident said nothing about the portfolio-level creep that follows: a
register absorbing every decomposed defect and every ESG-swept intake
item as a first-class row regardless of size. A third-party review of a
different project (bread_bot), recorded during `direct-resolution-lane`'s
own stem, 2026-07-27, found the gap and split it into two readings — one
on the *triviality* axis, one on the *priority* axis — before either was
typed. Both named the same two call sites (`new.md` step 4a, `esg.md`
step 2's sweep) for the same complaint, and were folded into one row at
the sixth `/dcs-esg`, 2026-07-27, on the reading that a missing bar is one
defect, not two, no matter how many axes describe its absence. Deciding
*where* the bar sits was itself measured, not assumed: the incident's own
three live-symptom register rows were all Type 3 at priority `L`, so a
Type-5-shaped triviality test — the more intuitive-sounding bar — would
have caught none of them, and priority is what shipped instead. The fix
keeps the rule inside this package's own "ship no project facts"
constraint by routing through "the project's own `CLAUDE.md`" rather than
a hardcoded surface, with unconditional registration preserved as the
fallback for a project that documents no lighter one.

**Principle 6 — one session, one project, in full.** The mechanism behind
"territory never leaves its own project": every DCS artifact — config,
`ACTIVE`, incidents, register, delegation, worktrees — resolves relative
to the project root that holds the `.dcs/` directory, so a session rooted
in repo A can only ever open and act against A's own portfolio; repo B's
work has to be its own incident, from a session rooted in B. The failure
mode this closes: the gate cannot judge a tree it has no `.dcs/` for, so
by default it allows every target outside the project, which makes a
cross-project territory silently ungated rather than loudly rejected —
`plan.md` lint check 8 exists specifically to refuse that at plan time,
before it is ever discovered by a specialist editing outside the gate's
reach rather than being left for the specialist to discover the hard way.
The portfolio-wide disjoint-territory rule pays for itself again at merge
time: it keeps every concurrent incident's `git merge --no-ff` into main
trivially clean, with no cross-incident conflict to resolve.

**Principle 9b — why single-shot, not resumed.** Two reasons, both
structural, and both explain why a revision is always a fresh spawn
rather than a resumed agent. First, a resumed agent's reasoning lives in
a transcript that no incident artifact records, so its information diet
stops being auditable and principle 5's guarantee — the directory is the
only channel that survives a reset — quietly breaks. Second, a resumed
specialist still holds its OLD tasking, so an amended territory gets
edited against the stale one: a partition violation invisible to the
gate, because each individual edit still looks in-bounds for the tasking
the agent remembers, even though the tasking itself has moved on. This
rule was prose twice before it became a mechanism (`dcs_gate.py` denying
`SendMessage` while an incident is active), and prose did not hold either
time.

**Principle 13 — the four-revisions field lesson (predates self-hosting).** The loophole the
"attempt" definition exists to close: counting operational periods alone
let one incident run four revisions inside a single period 1, correctly
logging under the old wording that trigger (c) "does not fire — revisions
are not counted as periods." A 31-hour thrash inside that one period
never tripped the escalation cap that exists to catch exactly that kind
of grinding non-convergence. Each further revision pass was cheap to
justify in isolation — it always looks like one more small fix — but each
one buys, at most, one instance fixed, at the cost of a full
execute-plus-verify cycle; trigger (f)'s three-rejects rule closes the
matching loophole on the plan side: three rejects in one period means the
objectives, the chief's information diet, or the incident's size is
wrong, not that the plan needs one more pass.

**Principle 13 — the halt-ceiling field lesson (v0.6.9).** The gap this
ceiling closes: trigger (b) already required a convergence read from the
second halt on, but that read only ever fired inside the case the
period-boundary escalation check actually walks — and the fix-tasking
branch of the execute workflow runs its own halt to fix-tasking to
re-verify cycle *inside* a single attempt, never crossing into a re-plan
or a new period, so nothing upstream of this ceiling was ever watching
that inner loop. One incident rode exactly that gap to ten halts across
two attempts and sixteen hours forty minutes of continuous, un-closed
execution; a related incident that did eventually close carried the same
shape further before it was done — over thirty hours and a log file
approaching 300 KB. Eight of the ten halts in the first incident carried
no functional defect at all: the reviewing officer was re-litigating form
(a stale count, a phrasing, a docstring) each time, which is exactly the
same-class whack-a-mole the trigger (b) convergence read exists to name
— except the read was never triggered, because trigger (b) only counted
halts *between* attempts, and this loop never left its attempt. By the
fourth iteration the owner had stopped reviewing each halt individually
and granted a blanket "proceed" covering everything still to come, which
is the human failure mode a mechanical ceiling is meant to make
unnecessary: ten halts deep, "continue" had become a reflex, not a
review. The earlier fix for the sibling gap — the attempt-counting rule
that closed the loophole where several re-plans of one period never
tripped trigger (c) — solved the *outer* loop and left this *inner* one
completely open; the ceiling here is that rule's missing half, not a
separate idea.

These five figures — the ten halts, the sixteen hours forty minutes, the
over thirty hours, the ~300 KB log, and the eight of ten — are historical
counts from the incidents that produced this lesson, not numbers this
file recomputes; read each as **as of the incident's own close — it
moves**. The halt count specifically regenerates, for any incident's own
log, with:

`python .claude/hooks/dcs_gate.py --halt-count <incident-dir>`

The recipe is the counter itself, not a re-derived regex, because a second
implementation of the count is exactly the same class of divergence this
principle exists to name: the earlier `grep -cE` recipe disagreed with the
real counter on part of the fixture set, because it ignored the reset
anchors — principle 15 applied to itself, and missed the first time. No
count is quoted here because the old recipe was deleted with this edit,
which leaves the disagreement with nothing to regenerate it from. The
other four figures have no artifact left to regenerate from post-close and
carry the annotation instead.

**Principle 15 — transfer between seats, not only durable artifacts (field
lesson 2026-07-28, v0.6.11, incident `deviation-path-proportionality`).**
Principle 15 already forbade a derived fact surviving, unregenerated, inside
a durable artifact; this incident found the same failure one step earlier,
inside a single period, between seats that write nothing themselves — a fact
a prior seat had already established was retyped from memory by the next
seat relaying it forward, instead of being cited by file reference or
regenerating command. A third-party review of DCS, recorded 2026-07-27 — the
day before this incident opened — identified the seat most exposed to that
pattern, the Dispatcher, which relays between nearly every spawn, as the
dominant defect source: "9 of `prod-tools-drift`'s 10 halts were not about
the code" (**as of the incident's own close — it moves**). That is a
different predicate — "not about the code" — from the eight-of-ten figure
just above ("no functional defect"), independently counted over the same ten
halts; `prod-tools-drift` is itself a different project's incident, with no
regenerating command this repo can run against it, so the two counts
disagreeing by one is not a discrepancy to chase down here — it is a small,
live case of the exact drift this principle exists to stop.

**Principle 13 — the sentinel threat model (v0.6.9 revision 2).**
Revision 1 of this ceiling used a bare-substring match and failed in
both directions the same class of bug can fail: **T1**, false reset —
ordinary narration that happens to contain a sentinel word (a halt
entry's own summary quoting `IAP-APPROVED`, a status line describing
what a period does) zeroed the tally though nothing was actually
re-approved; and **T2**, false anchor-miss — a genuine re-approval or
pass, logged in natural prose rather than the exact grammar, failed to
lift the wall though the event was real. Both close the same way: a
sentinel counts only as the first field of its `214-LOG.md` entry, never
as a substring anywhere in it, and `plan.md`/`execute.md` write that
exact grammar structurally, not as one phrasing among several. A third
class, **T3**, is a deliberately fabricated, well-formed sentinel line
with no real event behind it. For `IAP-APPROVED:` this is closed: the
anchor only counts while its captured hash prefixes the stamped
`IAP-APPROVED` marker the gate independently verifies, so forging the
log line alone changes nothing. `SAFETY-PASS:` has no equivalent
binding — no hash-verified artifact records a Safety verdict — so a
session that deliberately writes a well-formed `SAFETY-PASS:` line does
lift the wall. Hash-binding it is not currently possible, and removing
the anchor would brick the close of every incident this ceiling is
meant to let finish. The IC accepted this residual and required it
recorded here rather than silently relitigated: such a line is a
**false Safety verdict sitting in an append-only log, visible in
`git diff`** — escalation material for whoever reviews the merge, not a
path this mechanism is designed to support.

**Same residual, extended (period 1 revision 3): the timestamp made
mandatory, and the boundary named directly.** The remainder T3 leaves is
not only the fabricated-sentinel case above but also its mirror image: a
line that verbatim reproduces a genuine anchor entry — timestamp and
token both, in full — is byte-for-byte indistinguishable from the real
entry, and no line-by-line parser can ever tell the two apart from the
bytes alone. That is exactly why the grammar (`dcs_gate.py`'s `GRAMMAR_LINE`) requires
such a quotation to be indented off column zero when it appears inside a
body: "An entry begins at column zero with a mandatory bracketed
timestamp; any other line is a continuation, never a sentinel, and
quoting a whole prior entry inside a body requires indenting it off
column zero." An unindented copy of a whole anchor entry is, by that same
definition, a new entry, not a quotation of an old one. This is the same accepted T3 residual already recorded above for
`SAFETY-PASS:`, extended rather than reopened as a separate deal.

One further gap belongs in this same residual, named here so it is not
rediscovered as a finding (Safety Officer 3, period 1): `ENTRY_PREFIX`
accepts **any** bracketed field, including an empty one — `[] SAFETY-PASS:
…` at column zero does anchor, though `GRAMMAR_LINE` says "timestamp".
The divergence runs the **opposite** way to the one that caused revision
2's halt: what the prose publishes is strictly contained in what the code
enforces, so an author who follows the prose always writes a line the
parser accepts, and the "follow the documentation, get denied" symptom
cannot occur. Narrowing the pattern to a non-empty field was considered
and declined at command point 4: it buys cosmetic strictness at the price
of a fourth verification cycle, in an incident whose whole subject is that
such cycles were unbounded. Revision
3 also made the bracketed timestamp **mandatory**, where revision 2 left
it merely conventional: IC addendum 4's own rollback act, dictated as a
bare `SAFETY-PASS:` body with no timestamp, would otherwise anchor as a
level-0 act the moment a second author quoted that dictated body verbatim
without also supplying the timestamp — a plan-level defect, not a
mistake by the specialist who first hit it, and the reason the timestamp
is a hard requirement now rather than an optional nicety.

**Principle 13 — anchor absent means zero, not unbounded.** When the
counter finds no `IAP-APPROVED:` or `SAFETY-PASS:` anchor at all in
`214-LOG.md`, it starts the tally at the top of the log rather than
refusing to count or erroring out — which, for a log with no anchor, is
the same thing as starting at zero. Four reasons converge on that
reading rather than any other: the mechanism's scope is exactly the
grammar's scope, so a log that has never written an anchor has also
never written the sentinel the ceiling counts, and there is nothing to
be unbounded about; the state self-heals at the very next stamped
`IAP-APPROVED`, the same act that resets a non-empty tally, so an absent
anchor is never a *permanent* zero; it is the mechanical expression of a
decision already made at the Owner level — the ceiling does not apply
retroactively, so a log with no anchor owes no count from before this
mechanism existed; and it is the only reading that keeps the deny
message's promise true after a payload rollback, when a rolled-back
`plan.md` stops writing the `IAP-APPROVED:` line the gate would
otherwise look for. Practically, this is why every `214-LOG.md` written
before this revision — in this repository and in every npm consumer's
own project — behaves safely on first contact: it has no sentinel of
any kind, so the walk finds no anchor, and the tally opens at zero
instead of at "every halt since the log began."

**Principle 13 — the convergence-read lesson (moved from
`execute.md`).** Field lesson 2026-07-24 (predates self-hosting): an IC produced exactly this
read — unprompted and correctly — only at the fourth halt, and the
Owner's pivot to a general guard ended the incident's rotation
immediately. The read was right; it was late because nothing asked for
it.

**Principle 15 — the test-inversion lesson.** A regression test asserting
that two live branches still collide is green only for as long as the
defect survives: fixing the defect — the entire purpose of the incident
the test was written for — turns the test red, so the artifact meant to
prevent a regression ends up actively punishing the repair. This is why
the rule pins to immutable evidence and to the invariant rather than the
instance: a fixture, a frozen blob, or a commit SHA cannot un-collide
itself out from under the test the way a live branch pair can.

**Principle 15 — the v0.6.5 mechanization (field lesson 2026-07-26,
incident `safety-halt-functional-scope`).** v0.6.5 gave the Safety
Officer's charter an explicit default: an artifact-hygiene finding is an
`advisories[]` entry, not a `halt`, unless it clears one of three named
bars (`agents/dcs-safety-officer.md` step 6). The charter justified that
default with a qualitative census — "the large majority of Safety halts
across all incidents to date were process/artifact findings" — which
was itself a derived fact (the specific numbers were
unverifiable, per the field lesson below)
with no regenerating command beside it, principle 15 applied to the
sentence that introduced the advisory/refutation split. When this
incident tried to regenerate it, **no query over the surviving
`214-LOG.md` artifacts reconstructed 17** — several were tried, by the
incident and again independently by its Safety Officer, and they
disagreed with each other as well as with the census. The population
predates the sentinel grammar that would let it be recounted, so there
is no command to put beside the number. It was therefore deleted
outright rather than replaced with a second unverifiable figure,
because the argument for the
default (a binding halt costs a full execute-and-verify cycle; spending
it on a docstring misallocates the one mechanism that can stop a merge)
never needed the census to hold — the count was decoration on a
structural argument, not load-bearing.

The same incident closed a second, independent divergence: principle 15
itself still read "Enforced by the Safety Officer's checklist (principle
7), not by discipline" after v0.6.5 shipped, a phrasing that named no
default and, read next to the charter's actual step 6, sounded like
every finding is still binding. Doctrine and charter answered "what does
the officer do by default with a hygiene finding" differently until this
edit — doctrine now names the default and points at the charter step
that enforces it, so the two documents give the same answer read back to
back.

## The lifecycle (Planning P mapped to software)

**Why the default is close/merge/ship, not "keep going until everything's
done."** A Safety-passed period holds *proven* work — it cleared
adversarial verification — and holding the incident open past that point
doesn't protect anything; it just keeps that proven work unmerged and
unshipped, fixing nothing, until the rest of the scope eventually catches
up. Registering the remainder as a follow-up incident, with this
incident's own AAR standing in for its 201 evidence, costs one extra
document and buys back everything a Safety-passed period earned: it ships
now instead of waiting on an unrelated part of the scope.

## Relationship to project-specific protocols

The core rule ("DCS agents honor a project's own pre-flight protocols
inside their DCS role") was written against three concrete examples worth
keeping on record as illustrations of the pattern, not because DCS itself
knows anything about these specific protocols:

- A project that documents "query the vault before a non-trivial fix" —
  a `dcs-planning-chief` planning tactics on that project reads the
  relevant vault domain pages before proposing tactics, the same way any
  agent working in that codebase would.
- A project that documents "query the action_log before debugging" — a
  `dcs-situation-analyst` doing stem-phase intel queries it as part of
  gathering evidence for the 201, rather than reconstructing history from
  code alone.
- A project that documents "query the codegraph before a cross-file
  edit" — an ops specialist about to touch a function other code calls
  checks callers/callees first, per that project's own rule, before
  writing its 214 return.

In every case DCS discovers the protocol the same way a new human
contributor would: by reading the target project's `CLAUDE.md`. DCS never
ships assumptions about what a given project's memory system, evidence
trail, or call-graph tooling looks like.

**Field lesson 2026-07-24 (charter defect, not agent failure, predates self-hosting).** A
concrete case behind the codegraph example above: a project made
call-graph queries mandatory before cross-file edits, and
`dcs-ops-specialist` — the only role that edits code — had no such tool
granted in its charter. It correctly fell back to `grep` and flagged the
gap in its return rather than silently claiming the mandated step had
been done. The corrective was to widen the charter, not to fault the
agent for a tool nobody had granted it.

## Automation layers

The rationale for why deploy delegation (`auto_after_close`, v0.4) is
allowed to exist at all: it is aimed specifically at an Owner who has
already watched enough routine, in-bounds ships go out correctly that
requiring their explicit go/no-go on each one has stopped teaching them
anything and started being pure latency. The safeguard that makes this
non-reckless is that delegation only ever narrows *prompts*, never
*evidence* — every ship still produces the exact same append-only log,
hash-bound approval, and register row it would have if the Owner had
typed "yes" themselves; delegation removes a keystroke, not a record.

The broader point the whole automation-layers design leans on: unattended
operation is legitimate specifically *because* the Delegation of Authority
is a written, Owner-signed artifact reviewed at a standing ESG session —
`/dcs-loop` is not DCS deciding for itself what counts as routine, it is
DCS mechanically enforcing a definition of "routine" the Owner already
wrote down. Strip away the Delegation and `/dcs-loop` degrades gracefully
to "pause at every approval," which is the honest behavior for "nothing
has been delegated yet," not a bug.

## Parallel operation

**Field lesson 2026-07-23 (worktree audit scoping, v0.4.2).** A worktree
audit run against a real project found four worktrees beyond the incident
ones the audit was designed to check: three belonging to the agent
harness itself (created under `.claude/worktrees/`, detached HEAD, names
that look generated rather than chosen) and one belonging to the deploy
script's own temporary checkout. The pre-v0.4.2 version of the audit had
no notion of "foreign" — it treated every worktree on disk as DCS's to
account for, so all four were flagged as orphans with a proposed
`git worktree remove` command. Deleting the harness's own worktrees out
from under it, or a deploy script's worktree mid-flight, would have been
actively destructive, not merely a false positive. The fix was to give
the audit a scoping test (DCS-owned = under the DCS container, or has a
`dcs/*` branch checked out; everything else is foreign) and make foreign
worktrees categorically un-flaggable, un-removable-by-DCS, mentioned at
most as a one-line footnote. The general lesson carried forward: a tool
that walks "everything on disk" needs an explicit ownership boundary
before it's safe to point cleanup suggestions at what it finds, because
disk state is shared with things that aren't the tool's business.

**Why "one worktree per division of the fire line" as the framing.** The
ICS image is literal: a wildfire's divisions are physically separate
ground, each worked by its own crew without micromanaging every other
division's moves, because the incident's overall plan already assigned
disjoint terrain. A DCS worktree is the same idea applied to a
filesystem: once the portfolio-level territory partition (principle 6)
has assigned disjoint file globs to concurrent incidents, each incident's
worktree can be worked without coordinating every edit with the others,
because the plan already guarantees they can't collide. "Main checkout as
staging area" and "deploy train as demobilization" follow the same
literal-ICS-image habit: staging is where resources marshal *before* being
released back to general availability (shipped), and demobilization is
the formal, accounted-for act of standing resources down — never an
ad hoc walk-off.

**Why three separate surfaces catch a stray worktree, not one.** The
worktree audit is detection, not correction — by design it never deletes
anything, because an automated cleanup routine that's wrong once destroys
someone's in-progress work with no recovery path. Correction is deliberately
routed through a slower, human-gated surface (the ESG's finish/park/kill
decision) specifically so that "this looks stale" and "this is safe to
delete" are never the same judgment call. The gate's `.dcs/CLOSED` zombie
rule is the last line of defense for the case where both of the first two
surfaces get skipped — a worktree that nobody audited and nobody parked
still can't be quietly reused for source edits, because the gate denies
unconditionally the moment `.dcs/CLOSED` exists in that root, IAP marker
or not. This is doctrine's only deliberately fail-closed exception to
"the gate only reads the approval marker" (principle 11) — a closed
incident's directory should never accidentally become a live one again.

**Relocated: the "three surfaces" summary sentence (incident
`close-integrity-guard-bundle`, 2026-08-02).** `doctrine.md`'s own
"Parallel operation" section, immediately after the worktree-audit
checklist, used to carry a one-sentence restatement of the point just
made above, moved here verbatim to fund principle 16's (close-time record
integrity) hot-path cost:

> Three surfaces make an audit finding an actual fix: the audit finds it;
> `/dcs-esg` agenda item (f) is where the Owner decides (finish/park/kill),
> and **parking always removes the worktree**; the gate's `.dcs/CLOSED`
> zombie rule makes one that slipped past both unusable meantime (principle
> 11's one deliberate fail-closed exception).

No compressed remnant was left in the core: every fact this sentence
stated survives independently elsewhere — "parking always removes the
worktree" is principle 10's own "(v0.3) No dangling incidents or
worktrees ... close/park/kill all remove it"; the `.dcs/CLOSED`
zombie-rule/principle-11 link is stated at the worktree audit's own step 5
("`dcs_gate.py`'s zombie rule (principle 11) denies guarded edits while it
exists"); and the "last line of defense" framing is the fuller paragraph
immediately above. The one detail with no other home is the specific
`/dcs-esg` agenda item letter (f) that owns the finish/park/kill decision,
preserved here rather than dropped.

**Project-supplied provision hook provenance (incident `provisioning-script-upstreaming`, 2026-07-30).** The `.dcs/provision` hook point generalises a pattern first developed in the bread_bot project (commit `4ae52377`), where a worktree-provisioning script automated environment setup for each new incident worktree. Three bread_bot incidents exercised the pattern independently before it was upstreamed into DCS as a general convention:

- **`cost-dynamics-labor-toggle`** — the provision script installed project-specific tooling the incident's specialists needed before their first operational period.
- **`cost-dynamics-per-product`** — the same script was re-invoked on a second worktree and proved the idempotency requirement in practice: a re-run mid-incident (after a worktree reset) did no harm.
- **`tools-prod-db-guards`** — the script was absent from a worktree created before the pattern was formalised, confirming the "absent = skip" behaviour: the incident ran normally, and the missing provision was noted in the log as a non-blocking observation rather than a failure.

The review-to-register chain that brought this upstream: a third-party review of bread_bot (2026-07-27) identified the provision pattern as a candidate for DCS itself rather than a project-local convention; the finding entered the register, was prioritised at the ESG, and became this incident. The convention DCS adopts is the minimal contract the three incidents all converged on: a single script at a known path, two arguments, three exit behaviours, and idempotency — nothing project-specific, nothing DCS ships.

## Structured return schemas

**Why every return is fixed JSON, not prose (principle 9).** A fixed
schema is what lets an IC catch the gap between "I did the task" and "I
did *a* task" — free-form prose lets a specialist narrate completion
without ever committing to the specific, checkable claims (files
touched, tests run, real command output) that let the IC or the Safety
Officer test the claim against reality. The schema forces that
commitment at return time, before the gap has a chance to calcify into
the record as an unexamined success.

**Why a single writer per artifact.** Subagents return their JSON block
rather than writing `203`/`204`/`IAP`/`SAFETY`/`AAR` files themselves, so
there is exactly one writer per numbered artifact: the IC, transcribing
per `references/forms.md`. That single choke point is what lets the IC
reject a malformed or incomplete return before it becomes doctrine for
the rest of the period — a subagent writing straight to disk could
commit a bad return to the record with nobody positioned to catch it
first.

**The contract-declaration format (incident `schemas-contract-format`,
period 1).** Before this incident, `schemas.md` was contract-shaped only
by convention — a `Returned by` line plus a fields table with one field
per row — and two sections quietly broke that convention: #3 had neither
a `Returned by` line nor a fields table at all (it was documented purely
by its JSON example), and #6 joined several distinct field names into one
table cell with `/` (`type` / `verdict` / `disposition`), which is
unreadable to anything mechanical because a cell holding three names
isn't a list of one field, it's a merge conflict nobody resolved. #2 had
a second, independent ambiguity: its `Returned by` line names two agents
(`dcs-planning-chief` and, for deploy concerns, `dcs-logistics-chief`),
which is honest about who writes *some* schema, but not about which agent
owns *this* section's own field list.

The fix treats "`Returned by` line naming exactly one producer, plus a
fields table with exactly one field per row" as the format itself, already
true by construction for #1/#4/#5, and completes it for the three that
didn't fit: #3 gained its own `Returned by` line and table (its schema was
always `dcs-logistics-chief`'s alone); #2 gained an explicit `Contract
producer:` sentence naming `dcs-planning-chief` only, so a reader — human
or mechanical — never has to infer which of the two named agents owns the
table below; #6 lost every slash-joined cell by adding a `Command point`
column and giving each field its own row, so `disposition` (used at both
`deviation` and `verdict_disposition`, with a different enum each time)
and `type`/`verdict` (each used at exactly one point) are no longer
conflated into one ambiguous row. `esg_activation` — the one field that
rides with any decision rather than belonging to a single point — carries
the point-column value `any` rather than an enumerated list (its
optionality lives in the Type column, beside every other type qualifier),
by design: it is the one field in the table that is genuinely
cross-cutting, not a fourth point hiding under a fifth name.

The same shape was mirrored into each `agents/dcs-*.md` charter's own
`<output_contract>`, closing a real drift in the same edit:
`agents/dcs-safety-officer.md`'s contract prose had never been updated to
mention `advisories` after `schemas.md` gained the field at v0.6.5
(commit `6a57b97`; regenerate both sides of the drift with
`git show 6a57b97 -- agents/dcs-safety-officer.md dcs/references/schemas.md`)
— the charter and the schema it implements had quietly
disagreed about the shape of a `pass` verdict since that commit, caught
only because this incident audited every charter's contract block against
its schemas.md section side by side.

### D1: Command-point liveness provenance (incident `hot-path-budget-emergency-trim`, 2026-07-30)

Original text moved from `doctrine.md` "A command point is never a silent wait" sub-section to keep the hot path below budget. The compressed version preserves the header, the announcement rule, and the dead-spawn rule while removing the liveness-proxy enumeration and shortening the "ask the session" instruction.

> Original bullet 2 full text:
> **An empty or errored return is a FAILED spawn, not a slow one.** A spawn that ends with no decision block — quota exhausted, API error, early termination — is dead; the decision will never arrive. Re-spawn immediately on the next tier and log **both** attempts (the failure and the seat that answered). Never wait indefinitely on a corpse, never resume it (principle 9b), and never let a dead spawn become the reason the Dispatcher decides alone. **Liveness is measured by the decision, never by a proxy** — not transcript size, not file mtimes, not silence, all harness artifacts. **Ask the session what the agent returned; never infer it from the filesystem.**

The removed material is the proxy enumeration ("not transcript size, not file mtimes, not silence, all harness artifacts"), the explicit parenthetical "(the failure and the seat that answered)", and the word "indefinitely". The core rule — liveness is measured by the decision, ask the session, never infer from the filesystem — is preserved in compressed form.

### D2: Principle 13 sentinel mechanics provenance (incident `hot-path-budget-emergency-trim`, 2026-07-30)

Original v0.6.9 per-attempt ceiling text moved from `doctrine.md` principle 13, trigger (b). The compressed version replaces this with a one-sentence reference to `dcs_gate.py`'s `halt_cycles()` and `GRAMMAR_LINE`. The convergence-read rule (v0.5.9) and all other triggers (a, c, d, f) remain in the core unchanged.

> Original v0.6.9 text:
> (v0.6.9) A per-attempt ceiling on trigger (b) closes a hole `execute.md`'s fix-tasking branch has **by construction**: that branch runs its own halt → fix-tasking → re-verify loop *inside* a single attempt, and nothing before this ceiling ever counted it. The unit of count is one such iteration, logged in `214-LOG.md` as a `SAFETY-HALT:` sentinel per `dcs_gate.py`'s published grammar (`GRAMMAR_LINE`): "An entry begins at column zero with a mandatory bracketed timestamp; any other line is a continuation, never a sentinel, and quoting a whole prior entry inside a body requires indenting it off column zero." `dcs_gate.py` is the counter; `esg.max_halts_per_attempt` (default 3) is the ceiling, and reaching it is a mechanical denial, not a warning — it promotes the inner loop into the outer attempt count trigger (c) already tracks. Exactly two sentinels reset the tally: `IAP-APPROVED: <hash>` (written by `plan.md`), an anchor only while `<hash>` prefixes the stamped `IAP-APPROVED` the gate already verified — the marker is the authority, the log line only fixes its position in time; and `SAFETY-PASS:` (written by `execute.md`), so a passed period can still close. A sentinel quoted inside a sentence is never an anchor; the Owner answering "continue" is a decision, not a reset

The doctrine-appendix.md already carries the extended field-lesson narratives for this ceiling (see "Principle 13 — the halt-ceiling field lesson" and "Principle 13 — the sentinel threat model" above); this entry records the exact prose divested from the hot path.

### D3: v0.1 constraints historical narrative provenance (incident `hot-path-budget-emergency-trim`, 2026-07-30)

Original historical evolution text moved from `doctrine.md` "v0.1 constraints" section. The compressed version retains the current-state summary only.

> Original text:
> **One incident active at a time** *(superseded by v0.3)* — `.dcs/ACTIVE` is the lock; `/dcs-new` refuses a second incident while one is active. **(v0.3)** Now **one incident per worktree**: `.dcs/ACTIVE` is per-worktree (git-ignored, never merges) — one seat, one `ACTIVE` file, one incident, scoped to whichever tree the session is rooted in. The no-two-incidents-anywhere constraint moves to the register's territory partition (principle 6; "Parallel operation" below).

The removed material is the v0.1-era description of `.dcs/ACTIVE` as "the lock" and `/dcs-new` refusing a second incident, plus the transition language "(superseded by v0.3)" and "Now". The current rule (one incident per worktree) is preserved in compressed form.

### D4: Worktree audit step 5 — platform diagnostic commands provenance (incident `hot-path-budget-emergency-trim`, 2026-07-30)

Original platform-specific diagnostic commands moved from `doctrine.md` step 5 of the worktree audit checklist. Produced by incident `worktree-removal-self-conflict` (v0.7.0). The core rule (diagnose before escalating, cd to esg_root) remains in doctrine.md; the platform-specific commands are here.

> Original platform diagnostic text:
> POSIX: `lsof +D <path>` or `fuser -v <path>`; Windows: `powershell "Get-Process | Where-Object { $_.Path -like '*<path>*' }"` (or Sysinternals `handle <path>` if installed)

## Workflow field lessons (restored, incident `trim-content-loss-restoration`)

Incident `workflow-file-trim-grandfathered` (commit `bca0b56`, 2026-07-31) trimmed four workflow files to the 250-line ceiling and deleted the field lessons below outright instead of routing them here, which is where CLAUDE.md's "Where lessons go" convention sends the provenance of a rule; the rules themselves stayed in the workflows and only the stories were lost; each entry quotes the deleted prose verbatim and regenerates with `git show bca0b56^:dcs/workflows/<file>`; all three lessons predate self-hosting with no recorded version, so each carries the `predates self-hosting` identifier per the citation convention above; and the figures inside the quotations are historical counts from the incidents that produced them, not numbers this file recomputes, to be read as of that incident's own close, because it moves.

### W1: plan.md step 4a preamble — the tasking lint is not a command point (field lesson 2026-07-23, predates self-hosting)

> Field lesson 2026-07-23: an entire IAP review cycle (the IC's second REJECT on one incident) was consumed by defects in this list, and the IC's own verdict was that both were *Dispatcher transcription errors, not the chief's*.
> — predates self-hosting; regenerate with `git show bca0b56^:dcs/workflows/plan.md`, old lines 139-142.

### W2: plan.md lint check 3a — a census is not an enumeration (field lesson 2026-07-24, predates self-hosting)

> Field lesson 2026-07-24: an incident took **four Safety halts** on one objective, each closing the named instances and revealing another of the same class, because the criterion enumerated sites instead of asserting an invariant.
> — predates self-hosting; regenerate with `git show bca0b56^:dcs/workflows/plan.md`, old lines 170-173.

### W3: execute.md step 9b — a fix that is not shipped fixes nothing (field lesson 2026-07-24, predates self-hosting)

> Field lesson 2026-07-24, in the incident's own AAR: period 1 produced a Safety-passed fix for a bug that was actively corrupting production data, and *"that fix then sat in a branch. A fix that is not shipped fixes nothing, and the defect kept corrupting production data the whole time"* — a second period existed only to make the first one shippable.
> — predates self-hosting; regenerate with `git show bca0b56^:dcs/workflows/execute.md`, old lines 430-435.

W1's rule still lives at `plan.md` step 4a's preamble, W2's at `plan.md` lint check 3a, and W3's at `execute.md` step 9b and in this appendix's "## The lifecycle (Planning P mapped to software)" section above.

### W4: plan.md's `## 6c.` amendment path — a preservation map, not just a boundary check (field lesson 2026-07-27, incident `register-field-repair-path`)

> That incident's own `AAR.md` records two instances from a single repair.
> A rewrite of `IAP.md` fixing a criterion-6 halt silently dropped the
> already-Safety-verified "Criterion 5, answered" section (`AAR.md`:67-72)
> — the plan's only protection was a pinned hash over payload files, and
> criterion 5's deliverable was `.dcs/**` prose, outside both the pin and
> `dcs_gate.py`'s reach. The repair that restored the section then repeated
> the same defect shape one level up: reported as "restored verbatim" from
> two cited sources, when neither source in fact contained the text — a
> reconstruction misdescribed as a recovery (`AAR.md`:82-89). Full
> write-up: `vault/Meta/building-dcs-lessons.md` §18.
> — incident `register-field-repair-path`, 2026-07-27.

A 2026-07-31 attempt at this same fix, branch
`dcs/revision-preservation-map-abandoned-2026-07-31` @ `497dcd4`, shipped
prose plus a phrase-grep check that only confirmed `plan.md` mentioned
"preservation map" — it never inspected any incident's actual map. Prior
art only, superseded by this incident's mechanical check
(`dcs/tools/preservation_map.py`, `schemas.md` #9 (preservation map)).

### Principle 16 — a mechanism that checks itself is not a check (field lesson 2026-08-02/03, incident `close-integrity-guard-bundle`)

> Period 1's Safety Officer halted on two refutations, both found by doing
> the same thing: running the new close-time gate against real, live
> targets instead of only its own fixtures. (1) The load-bearing-term
> census scanned `tests/` as part of its own population — and lived in
> `tests/`. Every census term was a literal string inside the file that
> defined it, so `_term_missing` was provably always `[]`: the check would
> have passed with every other file in the package deleted. The fix was
> not a better term list; it was excluding the census's own defining file
> from the population it checks, by resolved-path identity, so a rename
> cannot silently re-open the hole. (2) Running the new tool against this
> incident's own directory — the sanity check criterion 14 exists
> specifically to force — found a *permanent, unremediable* finding: an
> earlier planning entry had to quote `"sha 3df43fc8"` verbatim to explain
> an accepted false-positive class, and `214-LOG.md` is append-only, so
> the citation could never be un-written. The shipped suppression
> mechanism could not clear it: it fired on a mere prose *mention* of its
> own sentinel (a false positive in the other direction) while being
> structurally unable to clear a genuinely corrected citation at all. A
> mechanism whose own governing incident cannot pass it is not a
> deployable mechanism, however correct its unit tests look in isolation.
>
> `dcs-commander` ruled `replan`, not `fix_taskings`, because the honest
> fix — a grammar-recognized `RECORD-CORRECTION:` **entry** (never a
> body-anywhere substring match) that **names its target** and clears
> every occurrence of that token **anywhere in the file** — revises what
> the Definition of Done actually promises (an append-only-compatible
> remedy exists), not merely how it is implemented. The re-verification
> pass also caught a related trap: two test cases asserted a criterion-3
> "finding" that was satisfied by unrelated criterion-2 noise (every
> fixture in this incident is untracked, so criterion 2 always fires) —
> correct by accident, not by construction. Full chronology, every claim
> independently re-measured at each command point rather than trusted:
> `.dcs/incidents/2026-08-02-close-integrity-guard-bundle/214-LOG.md`.
> — incident `close-integrity-guard-bundle`, 2026-08-02/03.

Principle 16's rule ("a close runs a mechanical record-integrity check
... unconditionally, not behind a project's opt-in") lives at
`doctrine.md`; this is its provenance. The generalizable lesson, stated
once so a future guard-writing incident does not have to rediscover it:
**a check that can pass by construction (self-reference, or a shared
side-effect from a sibling check) is not evidence of anything — run the
new mechanism against something real, especially the incident that built
it, before trusting a green suite.**
