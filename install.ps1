# DCS install: copy the DCS package from this repo (canonical) into ~/.claude (installed copy).
# Idempotent; overwrites installed files with repo versions. Run after every committed change.
$ErrorActionPreference = "Stop"
$repo = $PSScriptRoot
$claude = Join-Path $env:USERPROFILE ".claude"

robocopy (Join-Path $repo "dcs") (Join-Path $claude "dcs") /E /XD __pycache__ /NFL /NDL /NJH /NJS | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy payload failed: $LASTEXITCODE" }

Copy-Item (Join-Path $repo "agents\dcs-*.md") (Join-Path $claude "agents\") -Force

Get-ChildItem -Directory (Join-Path $repo "skills") -Filter "dcs-*" | ForEach-Object {
    robocopy $_.FullName (Join-Path $claude "skills\$($_.Name)") /E /NFL /NDL /NJH /NJS | Out-Null
    if ($LASTEXITCODE -ge 8) { throw "robocopy skill $($_.Name) failed: $LASTEXITCODE" }
}

$version = (Get-Content (Join-Path $repo "dcs\VERSION")).Trim()
Write-Host "DCS $version installed to $claude"
Write-Host "NOTE: projects hold their own copy of dcs_gate.py in <project>\.claude\hooks\ -- re-run /dcs-init (or copy dcs\hooks\dcs_gate.py manually) in each onboarded project after a hook change."
$global:LASTEXITCODE = 0
