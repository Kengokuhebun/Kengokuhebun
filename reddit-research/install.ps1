# Windows installer for reddit-research. Run in PowerShell from this folder:
#   powershell -ExecutionPolicy Bypass -File .\install.ps1
# Everything used is free: uv (Python manager), Playwright, Arctic Shift, your own Reddit login.
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Installing uv (free Python installer from Astral)..."
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
}

Write-Host "Installing the rr command..."
uv tool install --force --python 3.12 "$here"
uv tool update-shell | Out-Null
$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"


if (Get-Command claude -ErrorAction SilentlyContinue) {
    Write-Host "Registering the MCP server with Claude Code (all projects)..."
    claude mcp remove reddit-research --scope user 2>$null | Out-Null
    claude mcp add reddit-research --scope user -- rr serve
    $skills = "$env:USERPROFILE\.claude\skills\reddit-research"
    New-Item -ItemType Directory -Force -Path $skills | Out-Null
    Copy-Item "$here\.claude\skills\reddit-research\SKILL.md" $skills -Force
    Write-Host "Installed the research playbook skill to $skills"
} else {
    Write-Host "Claude Code CLI not found. See README.md for Claude Desktop setup."
}

Write-Host ""
Write-Host "IMPORTANT: open a NEW PowerShell window first (this one doesn't know the rr command yet),"
Write-Host "or paste this here:  `$env:Path = `"`$env:USERPROFILE\.local\bin;`$env:Path`""
Write-Host ""
Write-Host "Next: sign the tool's browser into Reddit (one time):  rr login"
Write-Host "Then check everything:                                rr doctor"
