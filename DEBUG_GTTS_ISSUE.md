# Debugging gTTS Audio Generation Issue

## Problem
gTTS is producing 0-second audio files or saying "exclamation mark" instead of the actual text.

## Possible Causes

### 1. Internet Connection Issue
gTTS requires internet connection to Google's TTS API. If EC2 instance can't reach Google servers, it will fail silently.

**Test:**
```bash
# From EC2 instance
curl -I https://translate.google.com
```

### 2. gTTS Not Properly Installed
The gTTS package might not be installed or might be the wrong version.

**Test:**
```bash
# From EC2 instance (in virtual environment)
source venv/bin/activate
pip show gTTS
python3 -c "from gtts import gTTS; print('gTTS imported successfully')"
```

### 3. Text Encoding Issues
Special characters or encoding problems might cause gTTS to fail.

### 4. Rate Limiting
Google might be rate-limiting requests from your IP.

## Diagnostic Steps

### Step 1: Check Backend Logs
When you try to synthesize Tamil/Telugu/Bengali text, check the backend logs for:
- `[GTTS] Synthesizing text with language=...`
- `[GTTS] Original text: ...`
- `[GTTS] Cleaned text: ...`
- `[GTTS] Generated audio: size=... bytes`

**Look for:**
- Very small audio size (< 1000 bytes) = problem
- Error messages from gTTS
- Network errors

### Step 2: Test gTTS Directly
Run the diagnostic script on EC2:

```bash
# From EC2 instance
source venv/bin/activate
python3 test_gtts_direct.py
```

This will:
- Test gTTS with multiple languages
- Show exact error messages
- Generate test MP3 files you can download and check

### Step 3: Check Generated Audio Files
If test files are generated, download one and check:

```bash
# From your local machine
scp -i ai-voice-key.pem ubuntu@34.236.36.88:~/AI_For_Bharat/test_ta.mp3 .
```

Then play it locally to see if it's valid audio.

### Step 4: Check Network Access
Verify EC2 can reach Google's servers:

```bash
# From EC2 instance
curl -v https://translate.google.com/translate_tts?ie=UTF-8&q=hello&tl=en&client=tw-ob
```

Should return audio data (binary).

## Solutions

### Solution 1: Install/Reinstall gTTS
```bash
source venv/bin/activate
pip uninstall gTTS -y
pip install gTTS==2.5.0
```

### Solution 2: Check Security Group
Ensure EC2 security group allows outbound HTTPS (port 443) to Google servers.

AWS Console → EC2 → Security Groups → Your SG → Outbound Rules
- Should have: All traffic OR HTTPS (443) to 0.0.0.0/0

### Solution 3: Use Alternative Text
Try simpler text without special characters:

```python
# Instead of: "வணக்கம் பாரதம்! இது ஒரு AI குரல் தளம்."
# Try: "vanakkam"
```

### Solution 4: Add Retry Logic
If Google is rate-limiting, add retry with exponential backoff.

## Expected Behavior

When working correctly, you should see:
```
[GTTS] Synthesizing text with language=ta, speed=1.0
[GTTS] Original text: 'வணக்கம் பாரதம்! இது ஒரு AI குரல் தளம்.'
[GTTS] Using gTTS language code: ta
[GTTS] Cleaned text: 'வணக்கம் பாரதம் இது ஒரு AI குரல் தளம்'
[GTTS] Creating gTTS object...
[GTTS] Writing audio to buffer...
[GTTS] Generated audio: size=15234 bytes, language=ta
```

Audio size should be > 5000 bytes for a typical sentence.

## Next Steps

1. Run `test_gtts_direct.py` on EC2
2. Share the output with me
3. Check backend logs when synthesizing
4. Verify network connectivity to Google

## Quick Fix: Fallback to Polly for All Languages

If gTTS continues to fail, we can configure Polly to handle all languages (with transliteration):

```bash
# Edit backend/.env
USE_AWS_POLLY=True
# Polly will use English voice for non-supported languages
```

This won't be perfect for Tamil/Telugu/etc., but it will work.
