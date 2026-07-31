### Territory lock — the cost cluster (2026-07-26, resolved 2026-07-27)

> **The cluster is down to two rows, and neither blocks the other on the
> critical path.** `safety-halt-functional-scope` shipped 2026-07-27
> (merge `aab9f06`), and `halt-binding-status` was **parked at the same
> session** because the experiment it was sequenced behind returned its
> answer — see that row's Outcome cell. What remains is
> `deviation-path-proportionality` (rank 5) and
> `safety-officer-incremental-verify` (rank 7); they still share
> `dcs/workflows/execute.md` and `dcs/references/doctrine.md` with each
> other and with the parked row, so **no two of the three may be `ACTIVE`
> at once** — but only two are open, so the sequencing costs one wait, not
> four. `field-lesson-citations` (rank 10) still shares `doctrine.md` and
> `doctrine-appendix.md` with both.
>
> **A second cluster formed while this one dissolved**, and it is worth
> naming before it is rediscovered as a conflict: `check-14-hardening`
> (rank 3), `schemas-contract-format` (rank 4) and `json-examples-unparsed`
> (rank 11) all claim `tests/test_doctrine_integrity.py`. Same rule, same
> reason. `check-14-hardening` is ranked ahead of `schemas-contract-format`
> deliberately: it is small, it patches a guard shipped hours earlier while
> its design is still fresh, and doing it first clears the file rather than
> stalling behind a much larger incident.
>
> The paragraph below is the state while the four-row lock was live, kept
> as the record of why it existed.

Four rows now point at the same nerve and, more to the point, at the **same
files**: `safety-halt-functional-scope` (rank 2), `halt-binding-status`
(rank 3), `deviation-path-proportionality` (rank 4),
`safety-officer-incremental-verify` (rank 5).

Every one of them holds `dcs/references/doctrine.md`; three hold
`dcs/workflows/execute.md`; two hold `agents/dcs-safety-officer.md`.
**No two of them may be `ACTIVE` at once** — `/dcs-new` step 7b's territory
check enforces this mechanically, and this note exists so the reason is on the
record rather than rediscovered as a conflict. Open them one at a time, in rank
order.

**The lock was held 2026-07-26 22:14 → 2026-07-27 00:33 (+1100) and is now
RELEASED.** `safety-halt-functional-scope` merged at `aab9f06` and its
worktree is gone, so the six rows sequenced behind it may open in rank order:
`halt-binding-status`, `deviation-path-proportionality`,
`safety-officer-incremental-verify` (shared `doctrine.md`) and
`field-lesson-citations`, `schemas-contract-format`, `json-examples-unparsed`
(shared `tests/test_doctrine_integrity.py`). **The second group's collision
just got one member wider:** `check-14-hardening`, queued at this close, also
claims `tests/test_doctrine_integrity.py`. The paragraph below describes the
state while the lock was held and is kept as the record of why.

`safety-halt-functional-scope`
was `ACTIVE` in `C:\DCS-wt\safety-halt-functional-scope`, so the other three —
`halt-binding-status`, `deviation-path-proportionality`,
`safety-officer-incremental-verify` — stayed `QUEUED` until it closed. Its
territory grew at the stem beyond the three files listed above (it now also
claims `dcs/references/schemas.md` §5 and `tests/test_doctrine_integrity.py`),
which additionally blocks `field-lesson-citations` (shares
`doctrine.md`/`doctrine-appendix.md`), `schemas-contract-format` and
`json-examples-unparsed` (both share `tests/test_doctrine_integrity.py`). Seven
of the queued rows are therefore sequenced behind this one; that is the cost of
the cluster, and it is the reason the register carries the note rather than
leaving it to be discovered as a merge conflict.

**Budget interaction, unchanged in kind but tighter in degree.** The hot path
sits at 36,582 B against the 37 KB ceiling — **1,306 B of slack** — and
`doctrine.md` is in this incident's territory, as it is in all four of the
cluster's. Regenerate with `python -c "import pathlib;
d=pathlib.Path('dcs/references/doctrine.md').read_bytes().replace(b'\r\n',b'\n');
s=pathlib.Path('dcs/references/schemas.md').read_bytes().replace(b'\r\n',b'\n');
print(len(d)+len(s), 37*1024-len(d)-len(s))"` from the repo root.

**Hygiene, observed at this incident's stem and owned by no row:**
`C:\DCS-wt\schema-citation-guard\` is an empty directory left on disk after
that incident's close removed its worktree — absent from `git -C C:\DCS
worktree list`, so it is an orphaned husk, not a worktree. Zero-loss to remove
(`rmdir "C:\DCS-wt\schema-citation-guard"`); left in place only because the
`/dcs-run` session that found it was rooted there. Belongs to the next
`/dcs-esg` agenda item (f).

> **Taken to the 2026-07-27 ESG as agenda item (f); the Owner chose removal and
> the removal FAILED. Recorded as not-removed, per the facts-only rule.**
> `Remove-Item C:\DCS-wt\schema-citation-guard` returned *"The process cannot
> access the file … because it is being used by another process"*, and
> `Get-ChildItem C:\DCS-wt` still lists it. Diagnosed rather than escalated
> (audit rule 5): the directory is **empty**, holds no tracked or untracked
> file, and is not a registered worktree — so there is **zero loss** and
> nothing to preserve. The holder is the ESG session itself: its shell is
> rooted in that directory and the harness restores that working directory
> after every command, so the process asked to delete it is the process holding
> it. Not forced, and no equivalent route attempted.
>
> **Still owed, and it is a one-liner from any other terminal** (or it frees
> itself when that session ends): `rmdir "C:\DCS-wt\schema-citation-guard"`.
> Carry it to the next `/dcs-esg` agenda item (f) if it is still on disk. The
> lesson worth keeping is smaller than the paragraph: **a session rooted inside
> the worktree container cannot clean that container**, which is one more reason
> `CLAUDE.md`'s "run DCS incidents from a session rooted in `C:\DCS`" is a rule
> and not a preference.

`schemas-md-trim` (rank 1) is sequential ahead of all four for a different
reason — not territory but **budget**: the hot path closed
`halt-loop-unbounded` at 34 B of slack, and each of these four is expected to
add to `doctrine.md`. It shares `tests/test_doctrine_integrity.py` with
`field-lesson-citations` (rank 8), which therefore also waits.

**Owner decision recorded at this incident's stem:** the live `prod-tools-drift`
in bread_bot is finished under the *old* rules; the new ceiling is not applied
retroactively. That incident is in another project and outside this one's
territory by principle 6.

Hygiene, observed while gathering evidence and not owned by any row:
`C:\bread_bot-wt\baking-plan-demand-and-units\` is on disk but absent from
`git -C C:\bread_bot worktree list` — an orphaned directory left after that
incident's close removed the worktree. Belongs to bread_bot's next ESG.

Founded 2026-07-25 at the first `/dcs-esg` session for `C:\DCS` (the DCS
package repo, self-hosted). Register founded empty, then populated with the
five rows above from the founding session's intake sweep of
`vault/Backlog.md` — the intake source `CLAUDE.md` documents ("candidates
for `/dcs-esg` to queue, **not** a register").

**`hot-path-budget-eol-sensitivity` shipped out-of-band, and the register says
so deliberately.** A `/dcs-deploy` train was opened 2026-07-25 and found the
work **already live**: `~/.claude/dcs/VERSION` read **0.6.8** (written 17:54,
after the close), so step 4's reconciliation excluded the row from the train
rather than re-shipping it. DCS did not perform this deploy and the row must not
read as though it had — that is the facts-only rule applied to the register
(field lesson 2026-07-23, recorded in this file's own header).

Verification before recording it, rather than trusting the marker: **the whole
payload was compared, not sampled** — all 31 files under `dcs/`, all 6
`agents/dcs-*.md`, all 10 `skills/dcs-*/SKILL.md` — none missing, none extra,
zero content differences, and the installed `dcs_gate.py` contains
`approval_digests`, so the v0.6.8 gate fix is genuinely live. The deployed
content corresponds to merge `70c1188`, which set VERSION 0.6.8. Regenerate with
`python <scratch>/payload_check.py` or by diffing `C:\DCS\dcs` against
`~/.claude/dcs`.

The train shipped nothing, changed nothing, and released its lock. Its only
lasting acts were this row's transition and deleting the spent branch.

**`hot-path-budget-eol-sensitivity` held the whole tree while it ran.** It was
typed **1** at its stem (up from the register's Type 3 assumption): the analysts
showed `.gitattributes` is absent from `package.json`'s `files` whitelist while
`dcs/hooks/dcs_gate.py` ships, so a tree-only fix would leave every downstream
project with a gate that hashes raw bytes — and the gate's approval hash is
*already* broken for the closed incident (stamp matches the git blob, not the
on-disk file). Its territory therefore includes the gate and its guarding tests,
and **item 5, the `git add --renormalise` pass, touches every tracked text file
by construction.** No other incident may open until it closes. That is recorded
here rather than in a five-path territory column that would be untrue.

**Territory conflicts among the queued rows** (principle 6, portfolio-wide) —
recomputed at the 2026-07-25 ESG:

- **Ranks 1 and 2 collide** on `tests/test_doctrine_integrity.py`:
  `hot-path-budget-eol-sensitivity` changes how the hot path is *measured*,
  `schemas-md-trim` changes what is measured and re-seats the ratchet.
  Strictly sequential, and in that order — trimming against a ruler with no
  stable definition is how `doctrine-hot-path-trim` ended up re-deriving its
  ratchet at the merge. `/dcs-new` step 7b's check enforces this once rank 1
  is `ACTIVE`.
- **Ranks 3, 4 and 5 are mutually disjoint and disjoint from 1–2**
  (`bin/`+`package.json`; `doctrine.md`+`appendix`+`dcs-safety-officer.md`;
  `dcs/hooks/dcs_intake.py`+`.gitignore`), so any of them could legitimately
  run in parallel in its own worktree.

**Delegation interaction (v2 bounds):** three queued rows can never
auto-approve, all expected rather than anomalous —
`intake-nudge-telemetry` (`dcs/hooks/**`), `version-bump-command`
(`bin/**`, `package.json`, and the `"version bump"` topic), and any row whose
close bumps the version, since `CLAUDE.md` requires that to be atomic and
`package.json` is a `forbidden_glob`. `version-bump-command` carries type `?`
deliberately: `CLAUDE.md` types installer changes as Type 1 and a release-tooling
command sits close to that line, but typing is a command point and is never
delegated, so it gets decided at that incident's own stem rather than presumed
here.

`cross-project-register-view` is carried with type `?` deliberately: it is
queued as a decision to be made, and the expected outcome is a
`vault/Decisions/` entry rather than a code change. Its type gets set at its
own stem, if it ever opens.

**`package-json-description-corruption`** was flagged by OPS-1 while executing
rank 1, from inside its own territory, and correctly left untouched. Measured
2026-07-25: `wc -c package.json` = 6,322,630 B; the `description` field is
2,942,431 characters of mojibake. Pre-existing at HEAD (`git show
HEAD:package.json | wc -c` = 6,322,584, the delta being CRLF normalisation), so
not caused by this incident. Ranked **H** because `package.json` is the npm
release surface and `npm publish` would ship it. Territory is `package.json`
alone, which rank 1 currently holds for its version bump, so this stays `QUEUED`
until rank 1 closes.

**Ranks reconciled with `STRATEGY.md` at the 2026-07-25 ESG.** They had drifted
three ways after the first incident: rank 1 was deployed, two mid-incident
discoveries were never in the strategy list, and two rows both claimed rank 3.
The list and this table now agree; `REGISTER.md` remains the operational truth
if they diverge again.

**`hot-path-budget-eol-sensitivity`** was discovered at plan time inside
`doctrine-hot-path-trim` and registered rather than absorbed (principle 4,
one incident one defect — it has its own root cause and could ship alone).
`core.autocrlf=true` with no `.gitattributes` means a fresh worktree checks
out CRLF while the long-lived main checkout holds LF, and
`test_doctrine_integrity.py`'s budget check reads raw `os.path.getsize`.
Measured 2026-07-25: main checkout 41,444 B, fresh worktree 41,763 B — the
same commit, a 319 B spread, against a 43,008 B ceiling. Regenerate with
`wc -c dcs/references/doctrine.md dcs/references/schemas.md` in each tree.
Territory is disjoint from rank 1's (`.gitattributes` is new;
`test_doctrine_integrity.py` overlaps only in that both incidents touch that
file — rank 1 touches the `HOT_PATH_BUDGET_KB` constant only, this one would
touch the check's measurement logic, which rank 1 is explicitly forbidden).
Because that is a same-file overlap the glob-level check cannot see, this row
stays `QUEUED` until rank 1 closes.

