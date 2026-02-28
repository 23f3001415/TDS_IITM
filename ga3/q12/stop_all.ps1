param(
  [int]$Port = 8003
)

$ErrorActionPreference = "SilentlyContinue"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

if (Test-Path "runtime\cloudflared.pid") {
  $cfPid = [int](Get-Content "runtime\cloudflared.pid")
  Stop-Process -Id $cfPid -Force
}

if (Test-Path "runtime\uvicorn.pid") {
  $uvPid = [int](Get-Content "runtime\uvicorn.pid")
  Stop-Process -Id $uvPid -Force
}

$extraCf = Get-CimInstance Win32_Process |
  Where-Object { $_.Name -eq "cloudflared.exe" -and $_.CommandLine -like "*tunnel --url http://localhost:$Port*" }
foreach ($p in $extraCf) {
  Stop-Process -Id $p.ProcessId -Force
}

$extraUv = Get-CimInstance Win32_Process |
  Where-Object { $_.Name -eq "python.exe" -and $_.CommandLine -like "*-m uvicorn main:app*" -and $_.CommandLine -like "*--port $Port*" }
foreach ($p in $extraUv) {
  Stop-Process -Id $p.ProcessId -Force
}

Write-Host "Stopped tracked q12 processes (if they were running)."
