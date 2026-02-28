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

# Cleanup any extra matching processes started manually.
$extraCf = Get-CimInstance Win32_Process |
  Where-Object { $_.Name -eq "cloudflared.exe" -and $_.CommandLine -like "*tunnel --url http://localhost:8000*" }
foreach ($p in $extraCf) {
  Stop-Process -Id $p.ProcessId -Force
}

$extraUv = Get-CimInstance Win32_Process |
  Where-Object { $_.Name -eq "python.exe" -and $_.CommandLine -like "*-m uvicorn main:app*" -and $_.CommandLine -like "*--port 8000*" }
foreach ($p in $extraUv) {
  Stop-Process -Id $p.ProcessId -Force
}

Write-Host "Stopped tracked q2 processes (if they were running)."
