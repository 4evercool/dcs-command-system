---
tags: [dcs, decision]
updated: 2026-07-28
---

# Decision: decline the SQLite migration for `REGISTER.md`

**Decided:** 2026-07-28, ninth `/dcs-esg` session
**Status:** closed — declined, no register row
**Reopen if:** a concrete retrieval-cost measurement shows plain-text reads
are actually the bottleneck, or the worktree/merge model changes such that a
binary file no longer has to survive `git worktree` + `--no-ff` merge

## The question

Raised by the Owner during the `token-economy` stem, 2026-07-28: move
`REGISTER.md` (and other structured-enough files) to a real database, on the
reasoning that agents could then retrieve exactly the row they need instead of
reading surrounding context — simpler and cheaper. Worth recording as a live
proposal even though the case below argues against it; the disagreement
itself is the ESG-relevant fact, and three of `token-economy`'s six items
(`automation-layer-eager-reading`, `log-read-scoping-incomplete`,
`esg-artifact-bloat`) already chase the same underlying goal by other means.

## The decision

**Not building it.** Recorded here so it stays decided rather than being
rediscovered and relitigated the next time `REGISTER.md`'s size comes up.

## Why

**Selective reads already work on text, without a database.** `grep -n` for
an ID, or `Read` with an offset, already returns one row without loading the
rest of the file — this ESG session did exactly that against `REGISTER.md`
repeatedly while sweeping a 748-line, 76 KB file. A `SELECT * WHERE id=...`
returns the same underlying cell content (the same multi-paragraph
Territory/Outcome prose), just delimited differently. Storage format does not
shrink the answer; it changes how reliably a narrow query can be aimed — real,
but smaller than "reads unnecessary context" implies.

**`.dcs/incidents/**` is git-tracked and merged `--no-ff` at close — a
database breaks under exactly that model.** `214-LOG.md` is append-only text:
two worktrees each adding lines in disjoint time ranges merge cleanly under
git's line-based algorithm almost every time. A binary SQLite file has no
line-based merge — two independently-modified copies differ at the byte/page
level almost everywhere, so the first parallel incident touching the same
database file conflicts outright. This is not an inconvenience to engineer
around; it is incompatible with the worktree-isolation model doctrine's
"Parallel operation" section describes.

**`REGISTER.md` itself (`.gitignore`d, single copy, courtesy-locked — no
git-merge issue) still doesn't gain what the measurement shows is missing.**
The bloat `esg-artifact-bloat` measured was free-text cell content (Territory,
Intake source, Outcome), not absence of schema — the table already has 12
well-defined columns. A `TEXT` column holds the same paragraph at the same
length; the fix for unbounded prose is a content bound, independent of
storage engine. `token-economy`'s own pointer-not-copy mechanism (criterion 3)
already delivered that bound and measurably worked: `REGISTER.md` +
`STRATEGY.md` are 108,510 B this session, down from 158,542 B three sessions
ago.

**The migration's own footprint is large.** Every workflow that reads or
edits `REGISTER.md` (`new.md`, `plan.md`, `execute.md`, `close.md`, `esg.md`,
`deploy.md`, `status.md`, `loop.md`, `run.md` — effectively the whole
package) would need rewriting to issue SQL instead, every touching agent
charter would need the same, and `tests/test_doctrine_integrity.py`'s
regex/glob-based checks would need a parallel database-aware implementation.
`references/typing.md` names "a database schema migration" as the textbook
Type 1 trigger — this migration is plausibly larger than the six items
already bundled into `token-economy`.

**Current scale does not need indexed lookup.** The register holds on the
order of three dozen rows across this project's entire self-hosted history to
date. A full-text `grep` over a file this size is sub-second; "databases win
at scale" is true in general and not load-bearing here.

**A cheaper mechanism already exists in the package and gets most of the
stated benefit.** `DELEGATION.md` embeds one fenced `delegation-bounds` JSON
block inside an otherwise prose file — `schemas.md` itself calls it "the only
part workflows parse." The same pattern applied to `REGISTER.md` (a small
structured block per row, or one at the file level, with Notes/Outcome
staying free prose under a length bound) would give reliable, schema-checked
field access without losing git-diffability or breaking the merge model. It
would also have caught, at write time, the one concrete failure already on
record: an `Edit` call that embedded literal newlines into a table cell and
silently broke the table into stray paragraph text (`REGISTER.md`'s own
Notes, eighth `/dcs-esg`).

## What to do instead, if the pain returns

Re-measure whether reads or writes are the actual cost before reaching for a
new storage engine — this project's own sessions already default to targeted
`grep`/`Read` rather than whole-file loads, and the pointer-not-copy
mechanism (`token-economy` criterion 3) is the same idea applied at the
content layer. If a `delegation-bounds`-style fenced structured block for
`REGISTER.md` rows is ever wanted, that is a small, git-diffable, mergeable
step in the SQLite proposal's actual direction without its costs.

## Links

- [[Backlog]] item 21 — where this was raised, with the Dispatcher's
  assessment this decision is drawn from
- [[Decisions/cross-project-register-view]] — a similar "the cost is not the
  reading, it is the writing" argument against a different structural change
