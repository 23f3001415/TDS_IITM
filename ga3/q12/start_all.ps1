param(
  [int]$Port = 8003
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

& "$root\start_api.ps1" -Port $Port
& "$root\start_tunnel.ps1" -Port $Port

$endpoint = Get-Content "endpoint_url.txt"
Write-Host ""
Write-Host "FINAL_ENDPOINT=$endpoint"
