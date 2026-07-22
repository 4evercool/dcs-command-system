#!/usr/bin/env node
/* DCS installer CLI — copies the package payload into ~/.claude (the
 * installed copy). Node stdlib only, no dependencies.
 *
 * Commands:
 *   dcs install     copy dcs/, agents/dcs-*.md, skills/dcs-* into ~/.claude
 *   dcs uninstall   remove exactly those from ~/.claude
 *   dcs doctor      compare installed vs package version; check python
 *   dcs version     print package version
 *
 * Testing hooks (env): DCS_PKG_ROOT overrides the payload source dir,
 * DCS_CLAUDE_DIR overrides the ~/.claude target dir.
 */
"use strict";
const fs = require("fs");
const os = require("os");
const path = require("path");
const { spawnSync } = require("child_process");

const PKG_ROOT = process.env.DCS_PKG_ROOT || path.join(__dirname, "..");
const CLAUDE_DIR =
  process.env.DCS_CLAUDE_DIR || path.join(os.homedir(), ".claude");

function pkgVersion() {
  try {
    const v = fs
      .readFileSync(path.join(PKG_ROOT, "dcs", "VERSION"), "utf8")
      .trim();
    if (v) return v;
  } catch (e) {
    /* fall through to package.json */
  }
  return JSON.parse(
    fs.readFileSync(path.join(PKG_ROOT, "package.json"), "utf8")
  ).version;
}

function copyFiltered(src, dest) {
  fs.cpSync(src, dest, {
    recursive: true,
    force: true,
    filter: (p) => !p.split(path.sep).includes("__pycache__"),
  });
}

function listDcsSkills(root) {
  const skillsDir = path.join(root, "skills");
  if (!fs.existsSync(skillsDir)) return [];
  return fs
    .readdirSync(skillsDir, { withFileTypes: true })
    .filter((d) => d.isDirectory() && d.name.startsWith("dcs-"))
    .map((d) => d.name);
}

function install() {
  const payload = path.join(PKG_ROOT, "dcs");
  if (!fs.existsSync(payload)) {
    console.error(`error: payload not found at ${payload}`);
    process.exit(1);
  }
  fs.mkdirSync(path.join(CLAUDE_DIR, "agents"), { recursive: true });
  fs.mkdirSync(path.join(CLAUDE_DIR, "skills"), { recursive: true });

  copyFiltered(payload, path.join(CLAUDE_DIR, "dcs"));

  const agentsSrc = path.join(PKG_ROOT, "agents");
  for (const f of fs.readdirSync(agentsSrc)) {
    if (f.startsWith("dcs-") && f.endsWith(".md")) {
      fs.copyFileSync(
        path.join(agentsSrc, f),
        path.join(CLAUDE_DIR, "agents", f)
      );
    }
  }

  for (const name of listDcsSkills(PKG_ROOT)) {
    copyFiltered(
      path.join(PKG_ROOT, "skills", name),
      path.join(CLAUDE_DIR, "skills", name)
    );
  }

  console.log(`DCS ${pkgVersion()} installed to ${CLAUDE_DIR}`);
  console.log(
    "Next: in a Claude Code session, run /dcs-init inside a project to " +
      "onboard it (creates .dcs/ and wires the PreToolUse approval gate)."
  );
  console.log(
    "NOTE: onboarded projects hold their own copy of dcs_gate.py in " +
      "<project>/.claude/hooks/ -- re-run /dcs-init (or copy " +
      "dcs/hooks/dcs_gate.py manually) in each project after upgrading."
  );
}

function uninstall() {
  const targets = [path.join(CLAUDE_DIR, "dcs")];
  const agentsDir = path.join(CLAUDE_DIR, "agents");
  if (fs.existsSync(agentsDir)) {
    for (const f of fs.readdirSync(agentsDir)) {
      if (f.startsWith("dcs-") && f.endsWith(".md"))
        targets.push(path.join(agentsDir, f));
    }
  }
  for (const name of listDcsSkills(CLAUDE_DIR)) {
    targets.push(path.join(CLAUDE_DIR, "skills", name));
  }
  let removed = 0;
  for (const t of targets) {
    if (fs.existsSync(t)) {
      fs.rmSync(t, { recursive: true, force: true });
      removed++;
    }
  }
  console.log(`DCS uninstalled from ${CLAUDE_DIR} (${removed} items removed).`);
  console.log(
    "Project-side files (.dcs/, .claude/hooks/dcs_gate.py, settings.json " +
      "hook wiring) are NOT touched -- remove those per project if desired."
  );
}

function doctor() {
  const pkg = pkgVersion();
  let installed = "(not installed)";
  try {
    installed = fs
      .readFileSync(path.join(CLAUDE_DIR, "dcs", "VERSION"), "utf8")
      .trim();
  } catch (e) {
    /* not installed */
  }
  console.log(`package version:   ${pkg}`);
  console.log(`installed version: ${installed}`);
  if (installed !== pkg) {
    console.log("-> versions differ; run: dcs install");
  }
  const py = spawnSync("python", ["--version"], { encoding: "utf8" });
  if (py.error || py.status !== 0) {
    console.log(
      "WARNING: `python` not found on PATH -- the gate hook " +
        "(dcs_gate.py) needs Python 3.8+; the approval gate will not " +
        "enforce without it."
    );
  } else {
    console.log(`python:            ${(py.stdout || py.stderr).trim()} (ok)`);
  }
}

function postinstall() {
  // Auto-install on `npm install`, guarded: never fail the npm install,
  // never run where it makes no sense.
  if (process.env.DCS_SKIP_POSTINSTALL) {
    console.log("DCS: postinstall skipped (DCS_SKIP_POSTINSTALL set).");
    return;
  }
  if (process.env.CI) {
    console.log("DCS: postinstall skipped (CI environment).");
    return;
  }
  if (!fs.existsSync(CLAUDE_DIR)) {
    console.log(
      `DCS: ${CLAUDE_DIR} not found -- skipping auto-install. ` +
        "Once Claude Code is set up, run: dcs install"
    );
    return;
  }
  try {
    install();
  } catch (e) {
    console.warn(
      `DCS: auto-install failed (${e.message}). ` +
        "Your npm install is fine; run `dcs install` manually."
    );
  }
}

const cmd = process.argv[2] || "install";
switch (cmd) {
  case "install":
    install();
    break;
  case "postinstall":
    postinstall();
    break;
  case "uninstall":
    uninstall();
    break;
  case "doctor":
    doctor();
    break;
  case "version":
  case "--version":
  case "-v":
    console.log(pkgVersion());
    break;
  default:
    console.error(
      `unknown command: ${cmd}\nusage: dcs [install|uninstall|doctor|version]`
    );
    process.exit(1);
}
