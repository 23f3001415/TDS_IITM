param(
  [int]$Port = 8002
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

& "$root\start_api.ps1" -Port $Port
& "$root\start_tunnel.ps1" -Port $Port

$base = Get-Content "base_url.txt"
Write-Host ""
Write-Host "FINAL_BASE_URL=$base"
