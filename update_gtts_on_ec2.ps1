# PowerShell script to update gTTS implementation on EC2

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Updating gTTS Implementation on EC2" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Upload updated files
Write-Host "`nUploading updated gTTS synthesis module..." -ForegroundColor Yellow
scp -i ai-voice-key.pem backend/app/services/gtts_synthesis.py ubuntu@34.236.36.88:~/AI_For_Bharat/backend/app/services/

Write-Host "Uploading diagnostic scripts..." -ForegroundColor Yellow
scp -i ai-voice-key.pem diagnose_gtts.py ubuntu@34.236.36.88:~/AI_For_Bharat/
scp -i ai-voice-key.pem test_gtts_direct.py ubuntu@34.236.36.88:~/AI_For_Bharat/
scp -i ai-voice-key.pem DEBUG_GTTS_ISSUE.md ubuntu@34.236.36.88:~/AI_For_Bharat/

Write-Host "`n✓ Files uploaded successfully!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. SSH into EC2: ssh -i ai-voice-key.pem ubuntu@34.236.36.88"
Write-Host "2. Activate venv: source venv/bin/activate"
Write-Host "3. Run diagnostic: python3 diagnose_gtts.py"
Write-Host "4. Check backend logs: tail -f backend.log"
Write-Host "`nOr run diagnostic remotely:"
Write-Host "ssh -i ai-voice-key.pem ubuntu@34.236.36.88 'cd AI_For_Bharat && source venv/bin/activate && python3 diagnose_gtts.py'" -ForegroundColor Yellow
