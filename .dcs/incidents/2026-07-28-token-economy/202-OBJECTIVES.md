<!--
202-OBJECTIVES.md -- written by the IC together with the Owner, at the
start of EACH operational period (/dcs-plan). Re-drafted (new file content,
same filename) each time the incident re-enters the P-loop for another
period -- the prior period's 202 is preserved in 214-LOG.md's phase-
transition history and, once complete, in AAR.md's summary, not in this
file itself.
-->

# 202 — Objectives (Operational Period 1)

**Incident:** 2026-07-28-token-economy
**Period:** 1 (increments each time the incident returns to this step)

## Goal

Cut DCS's own token overhead everywhere `201-BRIEF.md` found it, without
trading away context-reset recovery, independent verification, or the
auditable command chain that make DCS safe to run unattended.

## Acceptance criteria (the Definition of Done)

1. `dcs/workflows/run.md` and `dcs/workflows/loop.md` stop `@`-including a
   phase workflow's full text (`new.md`, `plan.md`, `execute.md`,
   `close.md`) into required reading merely because that phase *might* run
   this invocation — each phase's material loads only where the
   `<process>` body already explicitly reads it at the point that phase is
   entered (both files already contain that explicit re-read instruction
   today, e.g. `run.md` step 3's "Read `new.md` and execute..." — the
   top-of-file eager include is redundant with it, not a second, different
   need). `doctrine.md` may stay eager (needed regardless of phase).
   Verified by: `grep -n '^@' dcs/workflows/run.md dcs/workflows/loop.md`
   showing no phase-workflow file remains in the unconditional block, and a
   trace of a single-phase invocation confirming that phase's material is
   still fully read at its own boundary (no omission).

2. **(revised, period 1 — see Chief feedback)** The five current sites
   where a workflow or agent charter deals with `214-LOG.md` outside
   `execute.md:227`'s already-scoped `verdict_disposition` spawn and
   `close.md:44`/`:69`'s legitimate full-history AAR reads —
   `plan.md:38` ("read `214-LOG.md` and confirm a `command: typed` entry
   exists"), `plan.md:573` (the pre-stamp checklist's equivalent check),
   `execute.md:25` ("`214-LOG.md` must contain both a `command: typed` and
   a `command: iap_review` entry"), `agents/dcs-commander.md:63`
   (unbounded "period history from 214-LOG.md" feeding the
   deviation/verdict_disposition spawns), and `agents/dcs-safety-officer.md`
   (which names no `214-LOG.md` handling at all today, despite a live
   instance of it reading the file in full:
   `.dcs/incidents/2026-07-27-register-field-repair-path/SAFETY.md:141`) —
   each become a bounded check (an existence/grep-style check naming the
   exact command, or the same "current period + last ~20 lines" bound
   `execute.md` already uses for `verdict_disposition`), never an
   instruction implying a full-file read. `run.md:101`'s IAP-stamp count
   and `loop.md:102`'s pause-state confirmation are bounded the same way
   (a `grep -c`-shaped count; a bounded tail/grep) as part of criterion 1's
   tasking, not this one. Verified by re-running `rg -U -n
   "(read|reads|reading|contain|contains|history|inspect|full)[^.]{0,80}
   214-LOG\.md|214-LOG\.md[^.]{0,90}(in full|must contain|read|history)"
   dcs/workflows/*.md agents/*.md` (current output already logged in
   `214-LOG.md` this period — this corrected enumerator replaces the
   Dispatcher's original regex, which missed `plan.md:573`,
   `execute.md:25`, and `agents/dcs-commander.md:63`) and confirming every
   in-scope hit is now phrased as a bounded check, plus
   `agents/dcs-safety-officer.md` now states one explicitly. Blast radius
   refines to `agents/dcs-commander.md` joining the tasked set (verified
   count via the four taskings' combined territory, deduped: **15 files**
   — composition changed, not size: `dcs/references/doctrine.md`,
   `dcs/workflows/new.md`, and `dcs/templates/214-LOG.md` drop out with
   criterion 5 (below), while `agents/dcs-commander.md` and
   `dcs/workflows/deploy.md` join for criteria 2 and 3 — a sanctioned
   refinement of the 201 estimate, not scope growth).

3. `REGISTER.md` keeps `Territory` as a bare glob list — no rationale
   prose — while a row's `State` is `ACTIVE` (`new.md` step 7b's
   territory-conflict check reads this column directly across every
   `ACTIVE` row for an O(1) scan, so it must stay inline and cheap). The
   moment a row leaves `ACTIVE` (`MERGED`/`DEPLOYED`/`PARKED`/`KILLED`/
   `RESOLVED`), `Territory`, `Outcome`, and `Intake source` collapse to a
   one-line pointer into that incident's own already-authoritative record
   (`IAP.md`'s partition table for territory, `AAR.md`'s Outcome section
   for outcome, the original citation for intake) rather than restating
   it — performed at the same write point `close.md` step 5a.3 /
   `deploy.md` / `esg.md`'s park/kill handling already touch that row, not
   a separate archival pass. **Caps are numbers, not adjectives: Territory,
   Outcome, and Intake source collapse to exactly one line each once
   terminal.** `STRATEGY.md`'s `## Sessions` log caps each entry at **5
   lines or fewer** (date, one-line decisions, Delegation version in
   force, optional pointer — the template's own shape, and `esg.md`'s own
   existing instruction, "one-line summary of the decisions made," that
   current practice has drifted from at ~64 lines/entry). Substantial
   decision rationale routes to **the project's own decision store, if
   its `CLAUDE.md` documents one** (doctrine's "Relationship to
   project-specific protocols") — `esg.md`/`STRATEGY.md` are shipped
   payload and must stay project-agnostic (this project's own `CLAUDE.md`:
   "Ship no project facts"); naming a specific path like `vault/Decisions/`
   directly in the shipped text would itself violate that rule, even
   though this repo's own vault happens to satisfy it at runtime.
   `dcs/workflows/esg.md` gains all of these rules explicitly — it names
   none of them today (confirmed by reading it in full this period).
   Verified by: (a) re-running this period's column-attribution method
   (`awk -F'|'` summing field byte-lengths per column; `wc -c`/section-extent
   for `STRATEGY.md`'s `## Sessions` — both recorded in `214-LOG.md` this
   period) against a sample of newly-terminal rows / newly-superseded
   session entries, confirming Territory/Outcome/Intake-source stay at one
   line and Sessions entries at 5 lines or fewer; (b) `new.md` step 7b's
   territory-conflict check still passing correctly against a live
   `ACTIVE`-row scenario post-fix (unchanged by this criterion — confirmed
   read-only); (c) `grep -rni vault dcs/workflows/esg.md
   dcs/templates/STRATEGY.md dcs/templates/REGISTER.md dcs/workflows/close.md
   dcs/workflows/deploy.md` returns nothing, confirming no project-specific
   path was shipped. Actually compacting this project's
   own existing bloated rows/sessions below the current combined figure
   (regenerate via `wc -c .dcs/esg/REGISTER.md .dcs/esg/STRATEGY.md`,
   don't trust this session's own 118,525 + 59,711 = 178,236 B reading) is
   **[IC]** work performed at this incident's close, using the mechanism
   specialists build — specialists are barred from `.dcs/**`.

4. Within one operational period, a second or third Safety Officer spawn no
   longer re-derives every acceptance criterion and re-runs the entire
   verification suite from scratch when a prior spawn this same period
   already verified content that provably has not changed since —
   `agents/dcs-safety-officer.md` currently has no such allowance (step 2
   says only "re-run the tests yourself, independently," unconditionally,
   confirmed by reading the charter in full this period). The new
   mechanism must not weaken principle 7 or the binding nature of a halt: a
   Safety Officer must still independently re-verify anything a
   fix-tasking pass touched, and may never accept a specialist's or an
   earlier verdict's claim of "unchanged" without checking that the claim
   itself is true — a subsequent verdict block MAY cite a prior
   same-period verdict's `checked[]` entry by reference instead of
   restating it, but only for content it independently re-confirmed is
   unchanged, never as a substitute for that re-confirmation. Verified by a
   repro modeled on 201's baseline (`register-field-repair-path`'s
   `SAFETY.md`: 21,415 B, 3 verdict blocks in one period) showing reduced
   redundant restatement on a comparable multi-spawn period, plus a
   demonstration that a genuine change is still independently caught.

5. **DROPPED this period — number reserved, not renumbered (matching
   schemas.md's own convention of reserving a number so existing citations
   keep pointing here).** Original text: "`doctrine.md` is not
   unconditionally reread in full at every phase transition within what is
   provably the SAME uninterrupted session — but every fresh spawn... still
   reads it in full at its own boundary, via a mechanism that positively
   distinguishes 'same session, continuing' from 'fresh spawn / possible
   reset'... If no tactic can make that distinction safely,
   `objectives_feedback` must say so and this criterion drops for the
   period rather than trading principle 5's resilience guarantee for
   savings." **The Planning Chief invoked exactly this escape hatch**: it
   tested the actual mechanism this period (reading `dcs/workflows/run.md`
   returns its `@`-include lines as literal text — the Read tool does not
   resolve them, so nothing can be made conditional on that path; a disk
   marker records that someone read the file at time T, never that THIS
   context holds it; a model self-report about its own context is exactly
   the "assume continuity" the criterion forbids, and silently wrong across
   an auto-compaction). No tasking targets `doctrine.md` this period as a
   result — it is in no specialist's territory. Consolation finding,
   independently valuable: the 4× reload does not occur on the `/dcs-run`
   path at all (confirmed same investigation), so the item's automation-layer
   share is already addressed by criterion 1 with no continuity assumption
   needed. **Flagged to the Owner at IAP approval** — this removes one of
   the six items the Owner explicitly directed be covered in this incident;
   dropping it is authorized by this criterion's own pre-stated condition,
   not a unilateral scope cut.

6. `dcs/references/schemas.md`'s `evidence` (#4), `checked`/`refutations`/
   `advisories` (#5), and the tasking object's `evidence_required` (#2)
   fields, plus `agents/dcs-ops-specialist.md`, `agents/dcs-safety-officer.md`,
   `agents/dcs-planning-chief.md`, and `dcs/templates/204-TASKING.md`,
   explicitly state the same brevity rule criterion 3 applies to
   `REGISTER.md`/`STRATEGY.md` — cite the decisive excerpt or a file:line
   location, never paste a full unabridged transcript — matching the
   existing convention for `summary` ("one paragraph") and `rationale`
   ("one line"). This is the same underlying defect as criterion 3 (no
   rule anywhere requires citing a location over pasting content), applied
   to a different set of files. Verified by `grep -niE "verbos|concise|
   terse|paraphrase|paste|full output|unabridged|one line|one paragraph"
   agents/dcs-*.md dcs/references/schemas.md dcs/templates/204-TASKING.md`
   showing the new rule text present in all five locations.

## Out of scope this period

- DCS's enforcement and release surface: `dcs/hooks/dcs_gate.py`,
  `tests/test_dcs_gate.py`, `install.ps1`, `install.sh`, `package.json` —
  no item's fix touches these (201-BRIEF.md, Blast radius).
- `doctrine.md` itself: criterion 5 (its per-phase reread frequency)
  dropped this period — see criterion 5's own entry above for why. Further
  reducing its absolute size was already out of scope regardless (addressed
  by a prior incident, `doctrine-hot-path-trim`, and guarded by the
  hot-path budget test) — `doctrine.md` is in no tasking's territory this
  period.
- Resolving whether `@`-include resolution is single- or multi-level is
  investigative context for the Chief's tactics, not a goal in itself —
  criterion 1's fix (remove the eager block) sidesteps the question rather
  than needing to resolve it.
- The atomic `dcs/VERSION`/`package.json` version bump this change will
  eventually need is existing close-time/merge-gate bookkeeping
  (`test_doctrine_integrity.py`), not a criterion here.

## Chief feedback (filled in after /dcs-plan spawns the Planning Chief)

Both chiefs returned period 1; full detail in `214-LOG.md`'s
2026-07-28T14:39:34 entry, not restated here. Summary: criterion 5 dropped
(escape hatch invoked — no tactic can safely distinguish "same session" from
"fresh spawn/possible reset" with tools available); criterion 2 corrected
(enumerator under-counted its own population by 3 sites, now fixed, blast
radius +1 file); criterion 3 corrected (numeric caps added, shipped-package
phrasing fixed to stay project-agnostic). No criterion was found
unmeasurable/untestable as originally scoped. Logistics Chief confirms full
payload install (`install.ps1`/`/dcs-deploy`) is the only deploy shape, no
schema/env/migration concerns, and flags the hot-path budget (719 B
headroom) as the one ship-stopper risk — mitigated by criterion 5's drop
(removes `doctrine.md` from every territory) and criterion 6's tasking
already re-measuring the budget before returning.
