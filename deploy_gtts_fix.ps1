# PowerShell script to deploy gTTS fix to EC2

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Deploying gTTS Fix to EC2" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

Write-Host "`n[1/4] Uploading fixed backend files..." -ForegroundColor Yellow
scp -i ai-voice-key.pem backend/app/services/gtts_synthesis.py ubuntu@34.236.36.88:~/AI_For_Bharat/backend/app/services/
scp -i ai-voice-key.pem backend/app/api/synthesis.py ubuntu@34.236.36.88:~/AI_For_Bharat/backend/app/api/

Write-Host "`n[2/4] Uploading test scripts..." -ForegroundColor Yellow
scp -i ai-voice-key.pem test_full_flow.py ubuntu@34.236.36.88:~/AI_For_Bharat/
scp -i ai-voice-key.pem restart_backend.sh ubuntu@34.236.36.88:~/AI_For_Bharat/
scp -i ai-voice-key.pem check_integration.sh ubuntu@34.236.36.88:~/AI_For_Bharat/

Write-Host "`n[3/4] Making scripts executable..." -ForegroundColor Yellow
ssh -i ai-voice-key.pem ubuntu@34.236.36.88 'chmod +x ~/AI_For_Bharat/*.sh'

Write-Host "`n[4/4] Restarting backend..." -ForegroundColor Yellow
ssh -i ai-voice-key.pem ubuntu@34.236.36.88 'cd AI_For_Bharat && bash restart_backend.sh'

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

Write-Host "`nWhat was fixed:" -ForegroundColor Yellow
Write-Host "1. Text preprocessing - removes standalone punctuation"
Write-Host "2. Duration calculation - correct for MP3 files"
Write-Host "3. Better logging - easier to debug"

Write-Host "`nTest now:" -ForegroundColor Yellow
Write-Host "1. Open: http://34.236.36.88:3000"
Write-Host "2. Select 'Tamil' language"
Write-Host "3. Enter: வணக்கம்"
Write-Host "4. Click 'Synthesize Speech'"

Write-Host "`nOr test via API:" -ForegroundColor Yellow
Write-Host 'ssh -i ai-voice-key.pem ubuntu@34.236.36.88 "cd AI_For_Bharat && source venv/bin/activate && python3 test_full_flow.py"' -ForegroundColor Green

Write-Host "`nWatch logs:" -ForegroundColor Yellow
Write-Host 'ssh -i ai-voice-key.pem ubuntu@34.236.36.88 "tail -f AI_For_Bharat/backend.log"' -ForegroundColor Green
