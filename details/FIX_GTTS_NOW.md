# Fix gTTS Audio Issue - Quick Guide

## What I Fixed

1. **Improved text preprocessing** in `gtts_synthesis.py`:
   - Removes standalone punctuation that gTTS reads literally
   - Normalizes excessive punctuation (!!!! → !)
   - Better logging to diagnose issues

2. **Created diagnostic tools**:
   - `diagnose_gtts.py` - Comprehensive test script
   - `test_gtts_direct.py` - Simple gTTS test
   - `DEBUG_GTTS_ISSUE.md` - Detailed troubleshooting guide
   - `GTTS_TROUBLESHOOTING.md` - Step-by-step solutions

## What You Need to Do NOW

### Option 1: Upload and Test (Recommended)

**On Windows (PowerShell):**
```powershell
.\update_gtts_on_ec2.ps1
```

**Then SSH and run diagnostic:**
```bash
ssh -i ai-voice-key.pem ubuntu@34.236.36.88
cd AI_For_Bharat
source venv/bin/activate
python3 diagnose_gtts.py
```

### Option 2: Manual Upload

```bash
# Upload updated files
scp -i ai-voice-key.pem backend/app/services/gtts_synthesis.py ubuntu@34.236.36.88:~/AI_For_Bharat/backend/app/services/
scp -i ai-voice-key.pem diagnose_gtts.py ubuntu@34.236.36.88:~/AI_For_Bharat/

# SSH and test
ssh -i ai-voice-key.pem ubuntu@34.236.36.88
cd AI_For_Bharat
source venv/bin/activate
python3 diagnose_gtts.py
```

### Option 3: Quick Remote Test

```bash
ssh -i ai-voice-key.pem ubuntu@34.236.36.88 'cd AI_For_Bharat && source venv/bin/activate && python3 diagnose_gtts.py'
```

## What the Diagnostic Will Tell You

The script will test:
1. ✓ Is gTTS installed?
2. ✓ Can EC2 reach Google's servers?
3. ✓ Does basic English synthesis work?
4. ✓ Do Indian languages work?
5. ✓ Do full sentences work?

## Most Likely Issues

### Issue 1: Internet Connectivity (90% chance)
**Symptom:** Can't reach Google Translate
**Fix:** Check EC2 security group allows outbound HTTPS (port 443)

### Issue 2: gTTS Not Installed (5% chance)
**Symptom:** Import error
**Fix:** 
```bash
source venv/bin/activate
pip install gTTS==2.5.0
```

### Issue 3: Rate Limiting (3% chance)
**Symptom:** Very small audio files (< 1000 bytes)
**Fix:** Wait a few minutes, try again

### Issue 4: Text Encoding (2% chance)
**Symptom:** "Text is empty after cleaning"
**Fix:** Try simpler text without special characters

## After Running Diagnostic

### If All Tests Pass ✓
The issue is likely in the integration. Check:
1. Backend logs: `tail -f backend.log`
2. Restart backend: `sudo systemctl restart ai-voice-backend`
3. Test from frontend again

### If Tests Fail ✗
Share the diagnostic output with me. It will show exactly what's wrong.

## Quick Test from Frontend

1. Open: http://34.236.36.88:3000
2. Select "Tamil" language
3. Enter: "vanakkam"
4. Click "Synthesize Speech"
5. Check backend logs immediately: `tail -20 backend.log`

## Expected Working Logs

```
[GTTS] Synthesizing text with language=ta, speed=1.0
[GTTS] Original text: 'vanakkam'
[GTTS] Using gTTS language code: ta
[GTTS] Cleaned text: 'vanakkam'
[GTTS] Creating gTTS object...
[GTTS] Writing audio to buffer...
[GTTS] Generated audio: size=8234 bytes, language=ta
Detected MP3 format from gTTS, size=8234 bytes
Audio saved to S3: synthesized/20260307/req_xxx.mp3
```

## If Still Not Working

Run this and share the output:
```bash
cd AI_For_Bharat
source venv/bin/activate
python3 diagnose_gtts.py > diagnostic_output.txt 2>&1
cat diagnostic_output.txt
```

Also share:
```bash
tail -50 backend.log > backend_logs.txt
cat backend_logs.txt
```

## Emergency Fallback

If you need the demo to work NOW and can't fix gTTS:

**Use Polly for everything:**
```bash
# Edit backend/.env
USE_AWS_POLLY=True
# Restart backend
sudo systemctl restart ai-voice-backend
```

This will use AWS Polly for all languages. It won't sound perfect for Tamil/Telugu/etc., but it will work reliably.

## Files Created

- `backend/app/services/gtts_synthesis.py` - Updated with better preprocessing
- `diagnose_gtts.py` - Comprehensive diagnostic script
- `test_gtts_direct.py` - Simple gTTS test
- `DEBUG_GTTS_ISSUE.md` - Detailed debugging guide
- `GTTS_TROUBLESHOOTING.md` - Step-by-step solutions
- `update_gtts_on_ec2.ps1` - PowerShell upload script
- `update_gtts_on_ec2.sh` - Bash upload script

## Next Steps

1. Upload files to EC2 (use PowerShell script)
2. Run diagnostic script
3. Share output if issues persist
4. Test from frontend

Good luck! The diagnostic will tell us exactly what's wrong.
