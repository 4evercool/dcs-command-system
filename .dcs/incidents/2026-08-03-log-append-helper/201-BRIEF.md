<!--
201-BRIEF.md — written by the IC from dcs-situation-analyst findings, once,
at the stem (/dcs-new). Never edited after typing is confirmed except to
append a note if a later period's assessment reveals the original blast
radius was wrong (append, don't rewrite — 214-LOG.md is the append-only
one, but this file's Symptom/Evidence should stay a true record of what was
known at intake).
-->

# 201 — Incident Brief

**Incident:** log-append-helper
**Opened:** 2026-08-03
**Type:** 1

## Symptom

Every 214-LOG.md phase-transition entry across the incident portfolio is hand-typed by whichever session is at that transition, with no programmatic writer anywhere in the codebase. This produces two observable defect classes, both named in the intake and both independently confirmed on disk: (a) identical-timestamp batches — a session backfills several transitions after the fact and stamps them all with one repeated value (up to 12 entries sharing one timestamp in several closed incidents; two incidents where all 75 entries carry only a bare date with no time-of-day at all); and (b) inconsistent timestamp conventions, both across the portfolio (at least five distinct bracket shapes in use) and within a single incident's own log (two incidents mix formats or offsets inside one file, one of them genuinely cross-timezone). Because dcs_gate.py's entry grammar (`ENTRY_PREFIX`) is content-agnostic inside the brackets, none of this currently defeats the mechanical halt-ceiling counter — it defeats only auditability and honest reconstruction of what happened when, which is exactly the gap this incident's proposed tool and companion guard are meant to close.

## Evidence

- status-md-enum-drift/214-LOG.md lines 7-17 — 11 consecutive entries share one identical bracket `[2026-07-31T12:00:00+00:00]` (situation-analyst corpus scan, re-verified on disk).
- doctrine-hot-path-trim and hot-path-budget-eol-sensitivity — every one of 75 entries in each file reads only a bare date (`[2026-07-25]`), no time-of-day at all (situation-analyst corpus scan).
- worktree-path-propagation/214-LOG.md lines 5-14 — mixes `+1100`/`+11:00` formatting and two lines carry no bracketed timestamp at all, which dcs_gate.py's own grammar silently absorbs as continuation text rather than separate entries (situation-analyst, direct file + code read).
- halt-enumeration-grammar-drift/214-LOG.md lines 25-38 — 13 entries at `+03:00`, one later entry at `+11:00`: a genuine cross-offset mix inside one incident's own log (situation-analyst).
- Corpus scan of all 33 `.dcs/incidents/*/214-LOG.md` files found at least five distinct timestamp-bracket shapes in use portfolio-wide (situation-analyst). Correction to the intake's own framing: the post-mortem's literal "four conventions" phrase (`vault/Post-mortems/deepseek-period-review.md` §D) in fact describes SAFETY.md verdict headers, not 214-LOG.md — carried forward rather than repeated uncritically.
- `dcs_gate.py:106` `ENTRY_PREFIX = r'^\[[^\]]*\]\s+'` is content-agnostic inside the brackets; `render_entry()` (`dcs_gate.py:158-168`) is the only entry-string-building helper anywhere in the codebase and is called only by `rollback_entry()`/`rollback_act()` (and once more, transitively, in the deny message at `dcs_gate.py:743`), never to append an ordinary transition entry. No `dcs_log.py` exists today (situation-analyst, code read + directory listing; independently re-verified by dcs-commander at command point 1).
- `grep -n 214-LOG dcs/workflows/*.md` — 48 mentions across exactly 7 workflow files (plan.md 13, execute.md 14, close.md 8, new.md 4, status.md 4, loop.md 3, run.md 2); init.md, deploy.md, esg.md have none (situation-analyst; call-site count independently re-verified by dcs-commander at command point 1).
- Both existing hooks (`dcs_gate.py`, `record_integrity.py`) are stdlib-only with zero third-party imports, and `record_integrity.py` already imports `dcs_gate.py` dynamically via `importlib.util` specifically to avoid a second, drifting copy of the grammar — the reuse pattern a new tool should follow (situation-analyst).
- `record_integrity.py`'s five current close-time criteria contain no timestamp-order or duplicate-timestamp check; the proposed companion guard has no prior implementation anywhere (situation-analyst).
- Both DEPLOYED sibling incidents from the same hardening decision (`close-integrity-guard-bundle`, merge `779773b`; `independence-fail-closed-and-model-floor`, merge `f67f6d0`) were diffed against their own first parents and confirmed to leave `dcs_gate.py`, the 214-LOG.md template, and operator-identity recording untouched — this incident's scope is not preempted (situation-analyst).
- One related, independent-root-cause gap surfaced in passing and was split out per `new.md` step 4a rather than folded in here: `record_integrity.py` already added a fourth sentinel-shaped token (`RECORD-CORRECTION:`) invisible to `test_doctrine_integrity.py` check 12's three-token census and undocumented in shipped prose (both situation-analysts, independently). Routed to `vault/Backlog.md` item 31 (L priority, latent, no active harm — below the register bar per CLAUDE.md's vault routing rule, v0.6.13), not opened as its own register row.

## Reproduction path

1. Open `.dcs/incidents/2026-07-31-status-md-enum-drift/214-LOG.md`, lines 7-17: identical bracket repeated 11 times across a full incident lifecycle's worth of distinct transitions.
2. Open `.dcs/incidents/2026-07-30-worktree-path-propagation/214-LOG.md`, lines 5-14: two timestamp formattings and two timestamp-less lines in one file.
3. `find dcs/hooks -iname 'dcs_log*'` returns nothing — no append helper exists; `grep -n 'def ' dcs/hooks/dcs_gate.py` shows `render_entry()` is only ever called by the rollback path.
4. `grep -n 'def ' dcs/tools/record_integrity.py` lists five close-time criteria, none touching timestamp order or duplication.

## Blast radius (best guess at intake)

- `dcs/hooks/dcs_log.py` (new file — the append tool itself)
- `dcs/hooks/dcs_gate.py` (grammar authority — read/import only expected; `ENTRY_PREFIX` is already content-agnostic, likely no edit needed)
- `dcs/templates/214-LOG.md` (format line needs an operator-identity field)
- `dcs/references/forms.md` (documents the artifact's rationale/format)
- `dcs/references/doctrine.md` (principle 13's `GRAMMAR_LINE` citation — must stay byte-exact per the merge guard's verbatim-quote check)
- `dcs/tools/record_integrity.py` (natural home for the new close-time "N+ same-timestamp / out-of-order" criterion; already parses entries via `split_log_entries()`)
- `tests/test_doctrine_integrity.py` (check 12's "log grammar" sweep and the load-bearing-term census would need a new check)
- `dcs/workflows/{new,plan,execute,close,run,loop,status}.md` (~20 call sites currently instructing hand-written appends, 48 total 214-LOG mentions)

## Prior art

`vault/Decisions/non-anthropic-hardening.md` (2026-08-01, Owner-adopted) — measure 1's "Log-append helper" bullet and packaging item 2 name this exact incident, already split out from the sibling `close-integrity-guard-bundle` (which explicitly shipped without this scope: "measure 1's log-append helper (item 2, below, unaffected)"). Empirical source: `vault/Post-mortems/deepseek-period-review.md` §D's "Backfilled logs" bullet, naming `status-md-enum-drift` and `worktree-path-propagation` by example — both re-verified on disk by this stem's own analysts. No prior implementation attempt exists for either the append tool or the companion guard anywhere in the repository. One architecturally reusable precedent: `record_integrity.py`'s dynamic `dcs_gate.py` import pattern, and `dcs_intake.py`'s `record_telemetry()` (stdlib-only, stamps `datetime.now(timezone.utc).isoformat()`, appends one record per event, fails open) — the closest existing shape for a new stamping/appending hook, though 214-LOG.md's format is prose-line rather than JSON-line.

## Type + rationale

**Proposed type:** 1
**Rationale:** Verified blast radius spans ~13 files — a new shipped hook becoming the single writer for phase transitions across 7 workflows (48 call-site mentions confirmed on disk), a new check in the merge-time guard test_doctrine_integrity.py, a new close-time criterion in record_integrity.py, and a format change to the shipped 214-LOG.md template beside doctrine's byte-exact GRAMMAR_LINE citation — which is past Type 3's ~4-file ceiling and matches typing.md's Type 1 trigger "a new cross-cutting concern like the DCS gate hook itself"; I concur with the register row's Type 1 note but on these grounds rather than its dcs/hooks/** blanket, since CLAUDE.md's literal rule names dcs_gate.py, its guarding tests, and the installer, and this brief expects no dcs_gate.py edit at all. (IC=dcs-commander, fable)
**Owner confirmation:** confirmed as proposed (AskUserQuestion, 2026-08-03)

## Intake source (for /dcs-close to route back to)

"next from the register" — `.dcs/esg/REGISTER.md` row `log-append-helper` (rank 3, M priority as queued; that row's own Type cell already read "1 (`dcs/hooks/**` — CLAUDE.md types hook changes Type 1)"); originating decision `vault/Decisions/non-anthropic-hardening.md` measure 1 + packaging item 2, Owner-directed queue 2026-08-01.
