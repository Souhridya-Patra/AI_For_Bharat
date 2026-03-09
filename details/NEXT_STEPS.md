# Next Steps - gTTS Integration Issue

## Good News! 🎉

The diagnostic shows gTTS is working perfectly:
- ✓ All languages generating valid audio
- ✓ File sizes are correct (30-40KB)
- ✓ MP3 format is valid
- ✓ Internet connectivity is good

## The Problem

Since gTTS works standalone but fails in your app, the issue is in the **integration** between your FastAPI backend and gTTS.

## What to Do Now

### Step 1: Restart Backend with Updated Code

```bash
cd ~/AI_For_Bharat
source venv/bin/activate
bash restart_backend.sh
```

This will:
- Stop the old backend process
- Start backend with the updated gTTS code
- Verify it's running

### Step 2: Test the Full Integration

```bash
cd ~/AI_For_Bharat
source venv/bin/activate
python3 test_full_flow.py
```

This will test all languages through the API endpoint and show you exactly where it fails.

### Step 3: Check Backend Logs

While testing from the frontend, watch the logs in real-time:

```bash
tail -f backend.log
```

Look for lines with `[GTTS]` - they will show:
- What text is being received
- What language is selected
- What audio is generated
- Any errors

### Step 4: Test from Frontend

1. Open: http://34.236.36.88:3000
2. Select "Tamil" language
3. Enter: "வணக்கம்"
4. Click "Synthesize Speech"
5. Watch the backend logs

## Common Integration Issues

### Issue 1: Backend Not Restarted
**Symptom:** Old code still running
**Fix:** Kill all Python processes and restart
```bash
pkill -f "uvicorn.*main:app"
cd ~/AI_For_Bharat
source venv/bin/activate
python3 start_server.py
```

### Issue 2: Wrong Virtual Environment
**Symptom:** gTTS not found when backend runs
**Fix:** Make sure backend is running in venv
```bash
which python3  # Should show: /home/ubuntu/AI_For_Bharat/venv/bin/python3
```

### Issue 3: S3 Upload Failing
**Symptom:** Audio generated but not playable
**Fix:** Check S3 permissions and region
```bash
# Check backend/.env
cat backend/.env | grep -E "AWS_REGION|S3_BUCKET"
# Should show: AWS_REGION=ap-south-1
```

### Issue 4: Duration Calculation Wrong
**Symptom:** 0-second audio
**Fix:** Check `backend/app/api/synthesis.py` line ~90
```python
# For MP3 from gTTS, duration calculation is different
# We need to parse the MP3 file to get actual duration
```

## Detailed Debugging

### Check What Engine Is Being Used

```bash
# Test Tamil synthesis
curl -X POST http://localhost:8000/v1/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text":"வணக்கம்","voice_id":"default","language":"ta","speed":1.0,"pitch":0,"stream":false}'

# Check logs immediately
tail -20 backend.log | grep -E "Using|Selected|GTTS|Polly"
```

You should see:
```
Using Google TTS for language: ta
[GTTS] Synthesizing text with language=ta
```

If you see "Using AWS Polly" instead, the routing is wrong.

### Check Audio File on S3

```bash
# List recent files
aws s3 ls s3://ai-voice-platform-audio/synthesized/ --recursive | tail -5

# Download and check one
aws s3 cp s3://ai-voice-platform-audio/synthesized/20260307/req_xxx.mp3 test_s3.mp3
file test_s3.mp3
# Should say: "Audio file with ID3 version 2.4.0"

# Check size
ls -lh test_s3.mp3
# Should be > 5KB
```

### Check Frontend Request

Open browser console (F12) and look at the Network tab when you click "Synthesize Speech":
- Request URL should be: http://34.236.36.88:8000/v1/synthesize
- Request payload should show your text and language
- Response should have audio_url

## Expected Working Flow

1. Frontend sends request with Tamil text
2. Backend receives: `{"text":"வணக்கம்","language":"ta",...}`
3. Synthesis engine routes to gTTS (not Polly)
4. gTTS generates MP3 audio (30-40KB)
5. Audio uploaded to S3
6. S3 URL returned to frontend
7. Frontend plays audio

## If Still Not Working

Run all diagnostic commands and share output:

```bash
cd ~/AI_For_Bharat
source venv/bin/activate

# 1. Test gTTS directly (we know this works)
python3 diagnose_gtts.py > diag1.txt 2>&1

# 2. Test full integration
python3 test_full_flow.py > diag2.txt 2>&1

# 3. Get backend logs
tail -100 backend.log > diag3.txt

# 4. Test one synthesis and capture logs
curl -X POST http://localhost:8000/v1/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text":"வணக்கம்","voice_id":"default","language":"ta","speed":1.0,"pitch":0,"stream":false}' \
  > diag4.txt 2>&1

# Wait 2 seconds
sleep 2

# Get logs from that request
tail -30 backend.log > diag5.txt

# Share all diag*.txt files
cat diag*.txt
```

## Quick Commands Reference

```bash
# Restart backend
bash restart_backend.sh

# Test integration
python3 test_full_flow.py

# Watch logs
tail -f backend.log

# Test one synthesis
curl -X POST http://localhost:8000/v1/synthesize -H "Content-Type: application/json" -d '{"text":"வணக்கம்","voice_id":"default","language":"ta","speed":1.0,"pitch":0,"stream":false}'

# Check backend health
curl http://localhost:8000/health

# Check what's running
ps aux | grep python
```

## Most Likely Solution

Based on the diagnostic results, I suspect the issue is:

1. **Backend not restarted** - Old code still running
2. **Duration calculation** - MP3 duration not calculated correctly
3. **S3 URL** - Audio uploaded but URL not accessible

Run the restart script and test again. The updated code should fix the text preprocessing issue.
