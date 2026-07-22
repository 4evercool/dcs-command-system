<!--
REGISTER.md -- the incident portfolio. Owned by the Chief of Staff (main
session during /dcs-esg); also touched by /dcs-new (QUEUED -> ACTIVE),
/dcs-plan (Delegation auto-approval logging), and /dcs-close
(ACTIVE -> CLOSED) per their own workflow amendments. Every incident that
opens should end up with a row here, whether or not it started at a
/dcs-esg session.
-->

# REGISTER — Incident Portfolio

<!-- Status values: QUEUED | ACTIVE | PARKED | CLOSED
     PARKED = intentionally not running now (e.g. /dcs-loop's hard rule 1
     parking a Type 1 it will not run unattended, reason "awaits Owner")
     -- distinct from CLOSED, which means the incident finished. -->

| ID | Title | Type | Priority | Intake source | Opened | Closed | Outcome |
|---|---|---|---|---|---|---|---|
| {{slug}} | {{one-line title}} | {{5\|3\|1\|?}} | {{H\|M\|L or rank}} | {{Owner chat / audit_results id / vault tech-debt / ...}} | {{date, or "—" while still QUEUED}} | {{date, or "—"}} | {{one-line outcome, or "—" until closed}} |

## Notes

{{free text -- e.g. why an item is PARKED, links to relevant sitreps in SITREPS/}}
