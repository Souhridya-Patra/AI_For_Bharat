# gTTS Audio Generation Troubleshooting Guide

## Current Issue
- gTTS producing 0-second audio files
- Audio saying "exclamation mark" instead of actual text
- Only affects non-Polly languages (Tamil, Telugu, Bengali, Marathi, etc.)

## Quick Diagnosis

### Step 1: Run Diagnostic Script
```bash
# On EC2 instance
cd ~/AI_For_Bharat
source venv/bin/activate
python3 diagnose_gtts.py
```

This will test:
1. gTTS installation
2. Internet connectivity to Google
3. Basic English synthesis
4. Indian language synthesis
5. Full sentence synthesis

### Step 2: Check Backend Logs
```bash
# On EC2 instance
tail -f backend.log
```

Look for lines starting with `[GTTS]` when you try to synthesize.

### Step 3: Test from Frontend
1. Open frontend: http://34.236.36.88:3000
2. Select "Tamil" language
3. Enter simple text: "vanakkam"
4. Click "Synthesize Speech"
5. Check backend logs immediately

## Common Issues and Solutions

### Issue 1: "Cannot reach Google Translate"
**Symptom:** Diagnostic script fails at step 2
**Cause:** EC2 instance can't access Google's servers
**Solution:**
```bash
# Check security group allows outbound HTTPS
# AWS Console → EC2 → Security Groups → Outbound Rules
# Should have: Type=HTTPS, Port=443, Destination=0.0.0.0/0
```

### Issue 2: "gTTS is NOT installed"
**Symptom:** Import error when running diagnostic
**Cause:** gTTS not installed in virtual environment
**Solution:**
```bash
source venv/bin/activate
pip install gTTS==2.5.0
```

### Issue 3: "Audio is very small (< 1000 bytes)"
**Symptom:** Audio generated but file is tiny
**Cause:** gTTS returned error page instead of audio
**Solution:**
- Check if Google is rate-limiting your IP
- Try with VPN or different IP
- Add retry logic with delays

### Issue 4: "Text is empty after cleaning"
**Symptom:** Error in backend logs
**Cause:** Text preprocessing removed all content
**Solution:**
- Check what text is being sent from frontend
- Verify encoding is UTF-8
- Try simpler text without special characters

### Issue 5: Backend logs show "exclamation mark"
**Symptom:** Audio literally says "exclamation mark"
**Cause:** gTTS reading punctuation as text
**Solution:**
- Updated `gtts_synthesis.py` now preprocesses text
- Removes standalone punctuation
- Normalizes excessive punctuation

## Verification Steps

### 1. Verify gTTS Works Standalone
```python
from gtts import gTTS
import io

tts = gTTS(text="வணக்கம்", lang="ta", lang_check=False)
buffer = io.BytesIO()
tts.write_to_fp(buffer)
buffer.seek(0)
audio = buffer.read()

print(f"Audio size: {len(audio)} bytes")
# Should be > 5000 bytes

# Save and test
with open('test.mp3', 'wb') as f:
    f.write(audio)
```

### 2. Verify Network Access
```bash
# Test direct API call
curl -o test.mp3 "https://translate.google.com/translate_tts?ie=UTF-8&q=hello&tl=en&client=tw-ob"

# Check file size
ls -lh test.mp3
# Should be > 5KB

# Play it (if you have audio player)
# Or download and play locally
```

### 3. Verify Backend Configuration
```bash
# Check .env file
cat backend/.env | grep -E "USE_AWS_POLLY|USE_MOCK"

# Should show:
# USE_MOCK_SYNTHESIS=False
# USE_AWS_POLLY=True
```

### 4. Verify Synthesis Engine Routing
Check backend logs for:
```
[ENGINE] Selected XTTS-v2 for ta (ultra-realistic synthesis)
# OR
Using Google TTS for language: ta
```

Should see "Using Google TTS" for Tamil/Telugu/Bengali/etc.

## Advanced Debugging

### Enable Detailed Logging
Edit `backend/app/services/gtts_synthesis.py`:
```python
# Add at top of synthesize() method
logger.setLevel(logging.DEBUG)
```

### Test with curl
```bash
# Test synthesis endpoint directly
curl -X POST http://localhost:8000/v1/synthesize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "வணக்கம்",
    "voice_id": "default",
    "language": "ta",
    "speed": 1.0,
    "pitch": 0,
    "stream": false
  }'
```

### Check S3 Upload
If audio is generated but not playable:
```bash
# Check S3 bucket
aws s3 ls s3://ai-voice-platform-audio/synthesized/ --recursive

# Download a file
aws s3 cp s3://ai-voice-platform-audio/synthesized/20260307/req_xxx.mp3 test.mp3

# Check file type
file test.mp3
# Should say: "Audio file with ID3 version 2.4.0"
```

## Fallback Options

### Option 1: Use Polly for All Languages
If gTTS continues to fail, configure Polly to handle everything:

Edit `backend/.env`:
```bash
USE_AWS_POLLY=True
# Polly will use English voice for unsupported languages
```

Pros: Reliable, works offline
Cons: Won't sound natural for Tamil/Telugu/etc.

### Option 2: Use XTTS (if available)
XTTS provides better quality but requires more setup:
```bash
USE_XTTS=True
```

### Option 3: Mock Mode for Testing
For demo purposes only:
```bash
USE_MOCK_SYNTHESIS=True
```

## Expected Working Output

When everything works correctly, you should see:

```
[GTTS] Synthesizing text with language=ta, speed=1.0
[GTTS] Original text: 'வணக்கம் பாரதம்! இது ஒரு AI குரல் தளம்.'
[GTTS] Using gTTS language code: ta
[GTTS] Cleaned text: 'வணக்கம் பாரதம் இது ஒரு AI குரல் தளம்'
[GTTS] Creating gTTS object...
[GTTS] Writing audio to buffer...
[GTTS] Generated audio: size=15234 bytes, language=ta
Detected MP3 format from gTTS, size=15234 bytes
Final audio: format=mp3, size=15234 bytes
Audio saved to S3: synthesized/20260307/req_xxx.mp3
```

Audio file should be:
- Size: > 5000 bytes for typical sentence
- Format: MP3 with ID3 tags
- Playable in any audio player

## Still Not Working?

If you've tried everything above and it still doesn't work:

1. Share the output of `diagnose_gtts.py`
2. Share backend logs when attempting synthesis
3. Share any error messages from frontend console
4. Verify EC2 instance has internet access: `curl -I https://google.com`

## Contact
For hackathon support, reach out with:
- Diagnostic script output
- Backend logs (last 50 lines)
- Frontend error messages
- EC2 instance details
