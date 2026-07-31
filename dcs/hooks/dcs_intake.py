#!/usr/bin/env python3
"""UserPromptSubmit hook: make DCS opt-in visible at the start of a session.

The problem this closes (v0.6.0): DCS only engages when someone types a
`/dcs-*` command. A session that simply starts editing bypasses the whole
system -- the approval gate is deliberately silent when no incident is
active (that silence is what keeps DCS zero-overhead for non-incident
work), so nothing ever mentions that an incident was an option. The
result is that the discipline applies exactly when someone remembers it,
which is the failure mode DCS exists to remove.

This hook injects ONE short note on the FIRST prompt of a session in a
DCS-onboarded project:

- No active incident -> tell the session to offer `/dcs-run` if the
  request is a bug fix or feature, and to just proceed otherwise. The
  classification is left to the model rather than to keyword matching
  here: phrasing varies, languages vary, and a wrong keyword rule would
  either nag constantly or stay silent when it matters.
- Active incident -> report its slug, type and phase. A fresh session
  otherwise has no idea an incident is mid-flight in this tree, and the
  gate's denial message is a poor way to find out.

Deliberately ADVISORY, never blocking: it cannot deny, and it fires once
per session, not once per prompt. Over-gating buys friction, not safety
-- most work in a repo (docs, config, tooling, questions) legitimately
needs no incident, and a nag on every prompt would be trained away
within a day.

Fails open on every error, like every other DCS hook.
"""
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

MAX_AGE_SECONDS = 12 * 3600  # marker files older than this are reaped


def find_project_root(start):
    """Walk up from cwd looking for .dcs/ (the same discovery the gate
    hook uses for a relative target)."""
    env_root = os.environ.get("CLAUDE_PROJECT_DIR")
    if env_root and (Path(env_root) / ".dcs").is_dir():
        return Path(env_root).resolve()
    cur = Path(start).resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / ".dcs").is_dir():
            return candidate
    return None


def already_seen(session_id, project_root):
    """Once per (session, project). Marker lives in the system temp dir --
    never inside the project, which must not be dirtied by a hook."""
    key = hashlib.sha256(
        (str(session_id) + "|" + str(project_root)).encode("utf-8")
    ).hexdigest()[:24]
    marker = Path(tempfile.gettempdir()) / ("dcs_intake_" + key)
    if marker.exists():
        return True
    try:
        marker.write_text("1", encoding="utf-8")
        _reap(marker.parent)
    except OSError:
        pass  # cannot write a marker -> at worst the note repeats
    return False


def _reap(tmpdir):
    """Best-effort cleanup so markers don't accumulate forever."""
    import time
    now = time.time()
    try:
        for p in tmpdir.glob("dcs_intake_*"):
            try:
                if now - p.stat().st_mtime > MAX_AGE_SECONDS:
                    p.unlink()
            except OSError:
                pass
    except OSError:
        pass


def emit(context):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }))
    sys.exit(0)


def record_telemetry(session_id, project_root, event_type):
    """Append one JSON line to .dcs/esg/intake-telemetry.log.
    Fails open -- a telemetry write is never worth breaking the hook."""
    try:
        prefix = hashlib.sha256(
            (str(session_id) + "|" + str(project_root)).encode("utf-8")
        ).hexdigest()[:12]
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": prefix,
            "event_type": event_type,
            "project_root": str(project_root),
        }
        log_dir = Path(project_root) / ".dcs" / "esg"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / "intake-telemetry.log"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except OSError:
        pass


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    try:
        project_root = find_project_root(payload.get("cwd") or os.getcwd())
        if project_root is None:
            sys.exit(0)  # not a DCS-onboarded project

        session_id = payload.get("session_id") or "unknown-session"
        if already_seen(session_id, project_root):
            sys.exit(0)  # one note per session, not per prompt

        active = project_root / ".dcs" / "ACTIVE"
        if active.is_file():
            raw = active.read_text(encoding="utf-8-sig").strip()
            parts = [p.strip() for p in raw.split("|")]
            slug, inc_type, phase = (parts + ["?", "?", "?"])[:3]
            record_telemetry(session_id, project_root, "active_reported")
            emit(
                "[DCS] An incident is ACTIVE in this tree: {slug} "
                "(Type {t}, phase {p}). The approval gate is armed and will "
                "deny source edits that fall outside its approved IAP. Run "
                "/dcs-status before starting anything unrelated, and resume "
                "the incident with the command /dcs-status names.".format(
                    slug=slug, t=inc_type, p=phase
                )
            )

        record_telemetry(session_id, project_root, "nudge_offered")
        emit(
            "[DCS] This project is DCS-onboarded; no incident is currently "
            "active. If what the Owner just asked for is a bug fix or a "
            "feature -- anything that changes source code -- ASK, in one "
            "line, whether to open it as an incident (`/dcs-run "
            "<one-line description>`) before you start editing. If it is a "
            "question, an exploration, a trivial or single-file change, or "
            "work on docs/tooling, just proceed: no incident needed, and do "
            "not raise this again. DCS is opt-in per task and the Owner may "
            "always decline. Ask once; never re-litigate the answer."
        )
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)  # fail open -- a nudge is never worth breaking a turn


if __name__ == "__main__":
    main()
