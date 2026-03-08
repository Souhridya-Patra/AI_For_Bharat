# PowerShell script to check backend logs on EC2

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Checking Backend Logs on EC2" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

Write-Host "`nFetching last 50 lines of backend logs..." -ForegroundColor Yellow
ssh -i ai-voice-key.pem ubuntu@34.236.36.88 'cd AI_For_Bharat && tail -50 backend.log'

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "To watch logs in real-time, run:" -ForegroundColor Yellow
Write-Host "ssh -i ai-voice-key.pem ubuntu@34.236.36.88 'cd AI_For_Bharat && tail -f backend.log'" -ForegroundColor Green
