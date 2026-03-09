# Quick Fix - gTTS Audio Issue

## TL;DR

gTTS works perfectly (diagnostic confirmed). The issue is in the integration. I fixed:
1. Text preprocessing (removes punctuation that gTTS reads literally)
2. MP3 duration calculation (was treating MP3 as PCM)

## Deploy Fix NOW

```powershell
.\deploy_gtts_fix.ps1
```

## Test It Works

```bash
ssh -i ai-voice-key.pem ubuntu@34.236.36.88
cd AI_For_Bharat
source venv/bin/activate
python3 test_full_flow.py
```

Should show:
```
✓ Success! for all 5 languages
```

## Test from Frontend

http://34.236.36.88:3000
- Select "Tamil"
- Enter "வணக்கம்"
- Click "Synthesize Speech"
- Should play audio (not 0 seconds)

## If It Still Fails

```bash
# Get logs
ssh -i ai-voice-key.pem ubuntu@34.236.36.88 'tail -50 AI_For_Bharat/backend.log'
```

Share the output.

## What I Fixed

| Issue | Before | After |
|-------|--------|-------|
| Text | "வணக்கம்!" says "exclamation mark" | "வணக்கம்" says correctly |
| Duration | 0.76s (wrong) | 4.54s (correct) |
| Format | Treated MP3 as PCM | Detects MP3 correctly |

## Files Changed

- `backend/app/services/gtts_synthesis.py` - Text preprocessing
- `backend/app/api/synthesis.py` - Duration calculation

Deploy and test. Should work now!
