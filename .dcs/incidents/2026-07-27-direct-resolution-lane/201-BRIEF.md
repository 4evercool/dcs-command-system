# 201 — Incident Brief

**Incident:** direct-resolution-lane
**Opened:** 2026-07-27
**Type:** 1

**Provenance, and what this version is.** The stem was worked on 2026-07-27 by
a third-party DCS review (bread_bot main session, Fable; two situation
analysts, evidence cited), and the brief was parked at
`.dcs/esg/QUEUED-201/2026-07-27-direct-resolution-lane.md` when `new.md` step 7b
refused to open on a territory conflict with `deploy-marker-blind`. This
version is that brief **re-verified against HEAD `69be722`, then narrowed by an
IC ruling.** Two fresh analysts were spent only on the condition the queue note
names as grounds to reopen a stem (*"unless the blast radius changed"*) —
`deploy-marker-blind` merged (`0843816`, integration `916bebc`) after the brief
was written and edited a file it cites. Nothing was re-derived from scratch.

**Scope was narrowed at command point 1 and this brief reflects the narrowed
scope.** The parked brief carried three manifestations under one asserted root
cause; the IC ruled that root cause is a *model* rather than a defect and split
it (doctrine principle 4, `new.md` step 4a). See "Decomposition" below for what
left and where it went.

## Symptom

**A Type 5 incident resolved off the register leaves its row `QUEUED` forever.**
`new.md` step 7a — the Type 5 express lane — completes an incident without ever
writing `.dcs/esg/REGISTER.md`, and the register's state enum has no terminal
state meaning *"resolved directly; no worktree ever existed"*. The gap is
two-layered: there is no write step **and** no target state to write. Because
"next from the register" intake explicitly permits a Type 5 to originate from a
`QUEUED` row, the path is reachable by design rather than by accident, and the
field census shows it is walked.

## Evidence

Re-verified at HEAD `69be722`; disposition marked per item.

- **HOLDS.** `dcs/workflows/new.md:132-153` (step 7a) has five substeps — inline
  tasking, one specialist, IC verification, chat-only AAR, done — and **none
  touches `REGISTER.md`**. Confirmed by direct read; the file is untouched by
  `916bebc`.
- **HOLDS.** `dcs/workflows/new.md:203-219` (step 7b substep 4a) is the **only**
  register write for a completing incident, and it is gated Type 3/1 only.
- **MOVED, claim intact.** The state enum in `dcs/templates/REGISTER.md` — six
  values, `QUEUED | ACTIVE | MERGED (deploy pending) | DEPLOYED | PARKED |
  KILLED`, none fitting a directly-resolved row. The parked brief cited lines
  25-49; `916bebc` rewrote the `DEPLOYED` bullet (3 → 7 lines) and the
  facts-only paragraph, so the block now runs **25-53** and facts-only
  **55-66**. The value list itself is textually unchanged. Regenerate:
  `git show 916bebc -- dcs/templates/REGISTER.md`.
- **HOLDS.** The path is reachable by design: `new.md:25-31` and `run.md:24-35`
  both allow `"next from the register"` intake to reach a Type 5 typing
  decision, and `run.md:54-57` then short-circuits out of the chain entirely
  (*"no plan/execute/close chain to continue"*). `loop.md` step 5 recognises
  only a clean close or a `PARKED` skip as register-affecting.
- **HOLDS.** No carrier for a direct-resolution convention exists anywhere in
  the shipped package:
  `grep -rniE "field repair|post-hoc|деплой не применяется" dcs/workflows/*.md dcs/references/doctrine.md dcs/references/doctrine-appendix.md`
  → exit 1, zero matches.
- **HOLDS — the harm, measured in the field.** Of 6 Type-5-typed rows in
  `C:\bread_bot\.dcs\esg\REGISTER.md`, **3 sit `QUEUED` indefinitely** and 3
  were closed only through a locally-invented *"DEPLOYED — deploy not
  applicable"* convention; none shows a register footprint produced by the
  express lane itself. Regenerate: parse that register's rows, filter the Type
  column for values starting `5`.
- **SUPERSEDED, and this is the material change since the parked brief.** It
  said `tests/test_doctrine_integrity.py` "checks 1–14 contain no checks over
  … `REGISTER.md` text". The suite is now **checks 1–16**
  (`python tests/test_doctrine_integrity.py` → `82/82 passed`), and **check 15
  reaches `dcs/templates/REGISTER.md` directly and by name.** Its own PASS line:
  `deploy-evidence: declaring population is non-empty, spans ['dcs/'], and has 1
  paragraphs across 1 files: ['dcs/templates/REGISTER.md']`. That sole declaring
  paragraph is the `DEPLOYED` definition at `dcs/templates/REGISTER.md:39-45` —
  **immediately adjacent to the enum block this incident must edit.** Three
  sub-rules bind it: the file is pinned in the population by name as *"the
  halt-2 anti-erasure floor"*; Rule A requires that paragraph to cite
  `deploy.md` step 7 by the live step number; **Rule C allows at most one
  declaring paragraph per file.** A new state whose prose contrasts itself with
  `DEPLOYED` in one of check 15's three recognised rule shapes (definitional
  dash/colon; *only-after / once / when / if*; arrow) would turn check 15 red.
- **NEW.** `dcs/references/forms.md:22` restates the six states verbatim
  (`QUEUED / ACTIVE / MERGED / DEPLOYED / PARKED / KILLED`) and sits in **no
  check's population** — a new state makes it stale silently. Absent from the
  parked brief's blast radius.
- **NEW.** `dcs/workflows/close.md:239` asserts as settled fact that *"the
  register's terminal state for a shipped incident is `DEPLOYED`, reached later
  via `/dcs-deploy`"*. A new terminal state sits beside that sentence rather
  than replacing it, but the sentence must remain true.
- **NEW — precedent for the fix, and its limit.** A register state written by
  more than one workflow has precedent: `PARKED` is written by both
  `dcs/workflows/esg.md:85` and `dcs/workflows/loop.md:48,66,121`. A state
  **added to the enum after the fact** has **no** precedent — all six were
  established together in the v0.3 design.
- **HOLDS.** The hot-path budget applies if `doctrine.md` is touched:
  `doctrine.md` 23,387 B + `schemas.md` 13,296 B = **36,683 B** against a 37 kB
  ceiling — **1,205 B of slack**. Regenerate:
  `python -c "import pathlib; d=pathlib.Path('dcs/references/doctrine.md').read_bytes().replace(b'\r\n',b'\n'); s=pathlib.Path('dcs/references/schemas.md').read_bytes().replace(b'\r\n',b'\n'); print(len(d)+len(s), 37*1024-len(d)-len(s))"`.
  `HOT_PATH_BUDGET_KB` moved from line 112 to
  `tests/test_doctrine_integrity.py:142`.
- **HOLDS.** Baseline green at HEAD, each count read from its own line:
  `python tests/test_doctrine_integrity.py` → `82/82`;
  `python tests/test_dcs_gate.py` → `100/100`;
  `python tests/test_dcs_intake.py` → `10/10`.

**One analyst disagreement, recorded rather than resolved.** Analyst A placed
`tests/test_doctrine_integrity.py` inside the blast radius; Analyst B held it is
**not edited**, only *satisfied* — check 15 constrains how `REGISTER.md` may be
worded rather than needing a change. **The IC settled it on B's side and made it
a hard bound** (see Constraints).

## Reproduction path

Not a runtime bug; reproduced by reading, re-walked at HEAD `69be722`:

1. Trace `"next from the register"` intake (`new.md` step 1) into a Type 5
   typing decision and step 7a's completion. No step in 7a references
   `.dcs/esg/REGISTER.md`, so the row read as `QUEUED` is never written back.
2. Read `dcs/templates/REGISTER.md:25-53`. Six states; none is terminal for
   work resolved without a worktree.
3. Grep the package for a field-repair or post-hoc convention: zero hits. The
   only real-world instances were invented outside the package
   (`C:\bread_bot\.dcs\esg\REGISTER.md` rows 89-90).

## Blast radius (best guess at intake — the Planning Chief refines it)

**In, per the IC's narrowing:**

- `dcs/templates/REGISTER.md` — the new terminal state in the enum block
- `dcs/workflows/new.md` — the register write in step 7a's completion
- `dcs/references/forms.md` — the literal six-state enumeration at line 22
- `dcs/workflows/close.md` — keeping line 239's assertion honest
- `dcs/references/doctrine.md` and `dcs/references/typing.md` — only if the
  convention genuinely needs a doctrine or typing carrier; **the hot path has
  1,205 B of slack**, so this is a cost, not a free addition
- `CHANGELOG.md` at ship

**Explicitly out:** `tests/test_doctrine_integrity.py` (see Constraints);
`dcs/workflows/esg.md`, `dcs/workflows/run.md`, `dcs/workflows/loop.md` and
`dcs/references/schemas.md` (dropped with manifestations (b) and (c));
`dcs/workflows/status.md` (a pre-existing defect, registered separately).

**One honest caveat for plan time, flagged rather than buried.** `run.md:54-57`
and `loop.md` step 5 both describe Type 5 as register-neutral. If making step 7a
write the register leaves either of those texts false, the coherent fix for (a)
touches them, and the IC's drop list would need revisiting. That is a
**plan-time refinement to raise before the IAP is stamped**, not a licence to
widen during execution — widening past an approved IAP's blast radius is
escalation trigger (a).

## Constraints inherited from command point 1

1. **The new state's definition must be scenario-neutral** — terminal for *any*
   resolution that never opened a worktree/deploy lifecycle — so the split-out
   manifestations later consume it without reopening the enum. This is a hard
   requirement for the 202 to inherit, not a preference.
2. **`tests/test_doctrine_integrity.py` stays out of territory.** If check 15
   goes red, the remedy is rewording `REGISTER.md`. Editing the check is a
   deviation, full stop.

## Decomposition (`new.md` step 4a) — ruled at command point 1

The parked brief carried three manifestations on a single-root-cause argument.
The IC ruled **split**, on grounds worth keeping: the asserted root cause —
*"the register state machine and every workflow that writes it were designed
exclusively for full-lifecycle incidents"* — **is a model, and principle 4
disposes of models by name**: open the first concrete defect the model causes,
and route the model to `STRATEGY.md`. It also dismantled the strongest argument
for keeping them together — that three incidents would each edit the same enum.
They would not: **one incident creates the state and the others consume it**,
which is why constraint 1 above exists.

Split out, each with this brief's evidence already gathered:

- **(b)** field repairs have no registration path → `register-field-repair-path`
- **(c)** no inline-diff-plus-post-hoc-row sizing branch →
  `trivial-work-inline-lane`, cross-referenced to `decomposition-backlog-routing`
  (rank 9), which claims the same two sites for the same complaint on the
  priority axis rather than the triviality axis
- the `dcs/workflows/status.md:102-103` enum drift (`QUEUED / ACTIVE / PARKED /
  CLOSED`, **already wrong today**) → `status-md-enum-drift`

Sibling split at the original stem and already queued:
`decomposition-backlog-routing` (rank 9).

**Brief size:** the parked brief measured 8,067 B, inside step 4a's ~7–11 KB
range, so the size smell did not itself indicate over-scope — the model test
did.

## Type + rationale

**Type 1.** Decided at the original stem by an IC (bread_bot main session,
Fable) and **confirmed by the Owner via `AskUserQuestion`, 2026-07-27**; the
register records that it must not be re-litigated unless the blast radius
changed. It changed, and it changed **upward** (check 15 now binds the central
file; three further carriers found), and Type 1 is already the ceiling — so the
change cannot move the type, and `typing.md`'s *"type up, not down"* is
satisfied. **Re-confirmed at command point 1 for the narrowed scope on its own
merits** (IC = `dcs-commander`, fable): a new terminal state in the shipped
portfolio state machine is a new cross-cutting concern, which is `typing.md`'s
Type 1 trigger by name. Counter-precedent considered at the original stem:
`safety-halt-functional-scope` ran seven doctrine/workflow files as a clean
Type 3 because it touched no enforcement surface — true here too (no gate code,
no install scripts).

## Intake source (for `/dcs-close` to route back to)

Third-party DCS review, 2026-07-27, bread_bot main session (Fable),
Owner-directed "Phase 1". Opened from `REGISTER.md` at **rank 1** — the Owner's
call at the fifth `/dcs-esg`, 2026-07-27. Escalation trigger (e) was raised at
command point 1 (IC-requested ESG activation) and the Owner decided
**continue**, declining to convene now; the 209 is at
`.dcs/esg/SITREPS/direct-resolution-lane-p0.md`, and the three new rows plus the
model are **owed to the next sweep**.
