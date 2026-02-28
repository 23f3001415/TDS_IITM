param(
  [int]$Port = 8000
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

New-Item -ItemType Directory -Path "runtime" -Force | Out-Null

if (Test-Path "runtime\uvicorn.pid") {
  $oldPid = [int](Get-Content "runtime\uvicorn.pid")
  $old = Get-Process -Id $oldPid -ErrorAction SilentlyContinue
  if ($old) {
    Stop-Process -Id $oldPid -Force
    Start-Sleep -Milliseconds 500
  }
}

if (-not $env:OPENAI_API_KEY) {
  Write-Host "WARN: OPENAI_API_KEY is not set in this shell. Fallback sentiment mode will be used."
}

$outLog = Join-Path $root "runtime\uvicorn.out.log"
$errLog = Join-Path $root "runtime\uvicorn.err.log"
Set-Content -Path $outLog -Value ""
Set-Content -Path $errLog -Value ""

Start-Process `
  -FilePath "python" `
  -ArgumentList "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$Port" `
  -WorkingDirectory $root `
  -RedirectStandardOutput $outLog `
  -RedirectStandardError $errLog | Out-Null

# Resolve actual uvicorn python process id.
Start-Sleep -Seconds 1
$uvicornProc = Get-CimInstance Win32_Process |
  Where-Object {
    $_.Name -eq "python.exe" -and
    $_.CommandLine -like "*-m uvicorn main:app*" -and
    $_.CommandLine -like "*--port $Port*"
  } |
  Sort-Object ProcessId -Descending |
  Select-Object -First 1

if (-not $uvicornProc) {
  Write-Host "ERROR: Could not find uvicorn process."
  Get-Content $errLog -Tail 50
  exit 1
}

$deadline = (Get-Date).AddSeconds(20)
$healthy = $false
while ((Get-Date) -lt $deadline) {
  try {
    $resp = Invoke-WebRequest -Uri "http://127.0.0.1:$Port/health" -UseBasicParsing -TimeoutSec 3
    if ($resp.StatusCode -eq 200) {
      $healthy = $true
      break
    }
  } catch {
  }
  Start-Sleep -Milliseconds 700
}

if (-not $healthy) {
  Write-Host "ERROR: API did not become healthy on port $Port."
  Get-Content $errLog -Tail 80
  exit 1
}

$uvicornProc.ProcessId | Set-Content "runtime\uvicorn.pid"
Write-Host "API is running at http://127.0.0.1:$Port"
Write-Host "UVICORN_PID=$($uvicornProc.ProcessId)"
