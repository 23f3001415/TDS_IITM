param(
  [int]$Port = 8000
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

New-Item -ItemType Directory -Path "runtime" -Force | Out-Null

try {
  $health = Invoke-WebRequest -Uri "http://127.0.0.1:$Port/health" -UseBasicParsing -TimeoutSec 3
  if ($health.StatusCode -ne 200) {
    throw "API health check failed with status $($health.StatusCode)"
  }
} catch {
  Write-Host "ERROR: API is not running on port $Port. Start it first with .\start_api.ps1"
  exit 1
}

if (Test-Path "runtime\cloudflared.pid") {
  $oldPid = [int](Get-Content "runtime\cloudflared.pid")
  $old = Get-Process -Id $oldPid -ErrorAction SilentlyContinue
  if ($old) {
    Stop-Process -Id $oldPid -Force
    Start-Sleep -Milliseconds 500
  }
}

$cloudflared = (Get-Command cloudflared -ErrorAction SilentlyContinue).Source
if (-not $cloudflared) {
  $fallback = Join-Path $root "..\..\ga1\cloudflared.exe"
  if (Test-Path $fallback) {
    $cloudflared = (Resolve-Path $fallback).Path
  }
}
if (-not $cloudflared) {
  Write-Host "ERROR: cloudflared is not in PATH and fallback binary was not found."
  exit 1
}

$outLog = Join-Path $root "runtime\cloudflared.out.log"
$errLog = Join-Path $root "runtime\cloudflared.err.log"
Set-Content -Path $outLog -Value ""
Set-Content -Path $errLog -Value ""

Start-Process `
  -FilePath $cloudflared `
  -ArgumentList "tunnel", "--url", "http://localhost:$Port", "--no-autoupdate" `
  -WorkingDirectory $root `
  -RedirectStandardOutput $outLog `
  -RedirectStandardError $errLog | Out-Null

Start-Sleep -Seconds 2
$cfProc = Get-CimInstance Win32_Process |
  Where-Object {
    $_.Name -eq "cloudflared.exe" -and
    $_.CommandLine -like "*tunnel --url http://localhost:$Port*"
  } |
  Sort-Object ProcessId -Descending |
  Select-Object -First 1

if (-not $cfProc) {
  Write-Host "ERROR: cloudflared process was not found."
  Get-Content $errLog -Tail 80
  exit 1
}

$url = $null
$pattern = "https://[-a-z0-9]+\.trycloudflare\.com"
$deadline = (Get-Date).AddSeconds(35)
while ((Get-Date) -lt $deadline) {
  if (Test-Path $errLog) {
    $match = Select-String -Path $errLog -Pattern $pattern -AllMatches | Select-Object -First 1
    if ($match) {
      $url = $match.Matches[0].Value
      break
    }
  }
  Start-Sleep -Milliseconds 800
}

if (-not $url) {
  Write-Host "ERROR: Could not extract public tunnel URL from logs."
  Get-Content $errLog -Tail 120
  exit 1
}

$cfProc.ProcessId | Set-Content "runtime\cloudflared.pid"
$url | Set-Content "runtime\tunnel_url.txt"
"$url/comment" | Set-Content "endpoint_url.txt"

Write-Host "Tunnel is running:"
Write-Host "$url"
Write-Host "Submit URL:"
Write-Host "$url/comment"
Write-Host "CLOUDFLARED_PID=$($cfProc.ProcessId)"
