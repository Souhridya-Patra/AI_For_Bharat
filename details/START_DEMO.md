# 🚀 Start Demo - Quick Guide

## For Judges / Testing

### Step 1: Start Backend (Terminal 1)
```powershell
python start_server.py
```

Wait for: `INFO: Application startup complete`

### Step 2: Start Frontend (Terminal 2)
```powershell
python start_frontend.py
```

Browser will open automatically to: `http://localhost:3000`

### Step 3: Test It!

**In the web interface:**
1. Text is pre-filled with Hindi example
2. Click "Synthesize Speech"
3. Wait ~500ms
4. Audio plays automatically!

**Try different languages:**
- Click "Hindi Example" button
- Click "English (Indian)" button
- Click "Tamil Example" button

---

## What You'll See

### Beautiful Web Interface
- Clean, modern design
- Easy to use
- Real-time synthesis
- Audio plays in browser
- No S3 URL errors!

### Features to Show
- Multiple Indian languages
- Speed control (0.5x to 2.0x)
- Real AWS Polly synthesis
- Sub-500ms latency
- Professional quality audio

---

## Troubleshooting

### If server won't start:
```powershell
# Check if port is in use
netstat -ano | findstr :8000

# Kill process if needed
taskkill /PID [process-id] /F

# Restart
python start_server.py
```

### If frontend won't start:
```powershell
# Use different port
# Edit start_frontend.py, change PORT = 3001
python start_frontend.py
```

### If synthesis fails:
```powershell
# Check AWS credentials
python scripts/check_aws_credentials.py

# Check server logs in Terminal 1
```

---

## For Hackathon Submission

### What to Submit:
1. **GitHub**: All code
2. **Video**: 3-min demo (use VIDEO_SCRIPT.md)
3. **Blog**: Technical post (use blog outline)
4. **Presentation**: 10-12 slides (use PRESENTATION_OUTLINE.md)

### Demo URL:
- Local: http://localhost:3000
- Or deploy to AWS and use public URL

---

## Quick Demo Script

**30 seconds:**
"This is our AI Voice Platform for Indian languages. Watch - I type Hindi text, click synthesize, and hear natural speech in under 500ms. We support 6+ Indian languages using AWS Polly, S3, and DynamoDB. It's 10x cheaper than alternatives and production-ready."

---

**You're ready to demo! 🎉**
