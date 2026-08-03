<!--
Fixture for tests/test_doctrine_integrity.py section 23 case (vi) --
prose-fence/. Exercises dcs/tools/record_integrity.py's criterion 3
(SAFETY.md real-fence-parsing check): this incident directory is named
2026-08-10-prose-fence, strictly after SAFETY_FENCE_EFFECTIVE_DATE
(2026-08-03), so it is IN SCOPE and the fence check must actually run.
The "Checked" item below deliberately mentions a fence only in prose,
mid-sentence, mirroring the real naive-substring trap at
.dcs/incidents/2026-08-02-record-integrity-corrections/SAFETY.md:33
("no ` ```json ` fence ...", inside prose about the ABSENCE of fences) --
except that real file is dated ON the pin and so is out of scope by date
alone; this fixture is dated AFTER the pin specifically so the fence
parser itself, not the date gate, is what must correctly find no genuine
fenced block here. A substring search for "```json" WOULD wrongly match
this file; a real parser (looking for a fenced block whose own line
starts with the delimiter) must not be fooled, and the absence of any
genuine verdict fence in an in-scope incident must itself be a finding.
Other files in this directory carry a one-line pointer back to this
comment. This directory is this incident's own uncommitted product, not
historical evidence: do not edit in place, add a new fixture directory
instead (principle 15).
-->

# SAFETY.md -- Safety Officer Verdict (fixture: prose-fence)

**Incident:** prose-fence (fixture)
**Verdict:** pass

## Refutations

None.

## Advisories

None.

## Checked

1. This fixture deliberately carries no genuine verdict fence -- the
   text ```json``` appears here only as a naive-substring trap, inside a
   sentence, never as a real ```-delimited fenced code block starting a
   line. A parser that merely searches for the substring "```json" would
   wrongly treat this file as carrying a fence; a real fence parser must
   not be fooled by it, and must instead report this in-scope incident's
   missing verdict fence as a finding.
