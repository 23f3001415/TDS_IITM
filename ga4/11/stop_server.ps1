Set-Location $PSScriptRoot

foreach ($pidFile in @("uvicorn.pid", "cloudflared.pid")) {
    if (Test-Path $pidFile) {
        $pidValue = Get-Content $pidFile | Select-Object -First 1
        if ($pidValue) {
            Stop-Process -Id ([int]$pidValue) -Force -ErrorAction SilentlyContinue
        }
        Remove-Item $pidFile -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "Stopped server and tunnel (if running)."
