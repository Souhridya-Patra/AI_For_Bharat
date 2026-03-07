# 🎤 AI Voice Platform - For Judges

## Quick Access

**Live Demo:** http://YOUR_EC2_IP:3000

**API Documentation:** http://YOUR_EC2_IP:8000/docs

**GitHub Repository:** https://github.com/YOUR_USERNAME/ai-voice-platform

---

## How to Test

### Option 1: Web Interface (Recommended)

1. Open the demo URL in your browser
2. You'll see a text area with Hindi text pre-filled
3. Click "Synthesize Speech"
4. Audio will play automatically in ~500ms
5. Try different languages and speeds!

### Option 2: API Testing

Use the interactive API docs or curl:

```bash
curl -X POST "http://YOUR_EC2_IP:8000/v1/synthesize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "नमस्ते भारत!",
    "voice_id": "default",
    "language": "hi",
    "speed": 1.0
  }'
```

---

## Features to Test

1. **Hindi Synthesis** - Try the pre-filled example
2. **English (Indian)** - Click "English (Indian)" button
3. **Speed Control** - Adjust slider (0.5x to 2.0x)
4. **Multiple Languages** - Tamil, Telugu, Bengali, Marathi
5. **API Documentation** - Visit /docs endpoint

---

## What You're Seeing

- Real AWS Polly synthesis (not mock)
- Audio stored in S3
- Metadata in DynamoDB
- Sub-500ms latency
- Production-ready architecture

---

## Technical Details

**AWS Services:**
- Amazon Polly (Text-to-Speech)
- Amazon S3 (Storage)
- Amazon DynamoDB (Metadata)

**Architecture:**
- FastAPI backend
- RESTful API
- React-like frontend
- Deployed on AWS EC2

---

## Contact

Team SAAN | Leader: Souhridya Patra
Email: [your-email]
