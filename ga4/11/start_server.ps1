Set-Location $PSScriptRoot

# Start FastAPI server
$uvicorn = Start-Process -FilePath python -ArgumentList "-m","uvicorn","main:app","--host","0.0.0.0","--port","8000" -PassThru
$uvicorn.Id | Set-Content "$PSScriptRoot\\uvicorn.pid"

Start-Sleep -Seconds 2

# Expose publicly via Cloudflare quick tunnel
$cloudflared = Start-Process -FilePath cloudflared -ArgumentList "tunnel","--url","http://localhost:8000","--no-autoupdate" -RedirectStandardOutput "$PSScriptRoot\\cloudflared.out.log" -RedirectStandardError "$PSScriptRoot\\cloudflared.err.log" -PassThru
$cloudflared.Id | Set-Content "$PSScriptRoot\\cloudflared.pid"

Write-Host "Started uvicorn PID: $($uvicorn.Id)"
Write-Host "Started cloudflared PID: $($cloudflared.Id)"
Write-Host "Check $PSScriptRoot\\cloudflared.err.log for the public trycloudflare URL."
