# 🎯 Demo Quick Reference - One Page

## Before Judges Arrive

```powershell
# 1. Start server
python start_server.py

# 2. Open browser
start http://localhost:8000/docs

# 3. Test it works
python scripts/demo_hello_bharat.py
```

---

## Method 1: Interactive API (EASIEST)

**Show judges:** `http://localhost:8000/docs`

**Guide them:**
1. Click `POST /v1/synthesize`
2. Click "Try it out"
3. Paste this:
```json
{
  "text": "नमस्ते भारत! यह एक AI आवाज़ प्लेटफ़ॉर्म है।",
  "voice_id": "default",
  "language": "hi",
  "speed": 1.0,
  "pitch": 0,
  "stream": false,
  "post_process": true
}
```
4. Click "Execute"
5. Click the audio_url to hear Hindi speech

---

## Method 2: Live Demo (MOST IMPRESSIVE)

**Copy-paste these commands:**

```powershell
# Hindi
curl -X POST "http://localhost:8000/v1/synthesize" -H "Content-Type: application/json" -d "{\"text\":\"नमस्ते भारत! यह एक AI आवाज़ प्लेटफ़ॉर्म है।\",\"voice_id\":\"default\",\"language\":\"hi\"}"

# English (Indian)
curl -X POST "http://localhost:8000/v1/synthesize" -H "Content-Type: application/json" -d "{\"text\":\"Hello Bharat! This platform supports multiple Indian languages.\",\"voice_id\":\"default\",\"language\":\"en-IN\"}"

# Fast speech
curl -X POST "http://localhost:8000/v1/synthesize" -H "Content-Type: application/json" -d "{\"text\":\"This is fast speech\",\"voice_id\":\"default\",\"language\":\"en\",\"speed\":1.5}"
```

**Then:** Copy audio_url from response → Paste in browser → Play audio

---

## What to Say (30 Seconds)

"We built an AI voice platform for Indian languages using AWS. It uses AWS Polly for real voice synthesis, stores audio in S3, and uses DynamoDB for metadata. It supports Hindi, English with Indian accent, and other regional languages. Latency is under 500ms. Let me show you."

---

## Key Features to Highlight

✅ Real voice synthesis (AWS Polly)
✅ Hindi with Indian accent (Aditi voice)
✅ Multiple Indian languages
✅ Speed control (0.5x to 2.0x)
✅ RESTful API with docs
✅ AWS infrastructure (Polly, S3, DynamoDB)
✅ Latency < 500ms
✅ Production-ready architecture

---

## Judge Questions - Quick Answers

**"Does it really work?"**
→ "Yes, let me synthesize Hindi right now" [Show demo]

**"Why AWS Polly?"**
→ "Fast to deploy, production-ready, cost-effective. Architecture is modular - can swap in custom models later."

**"What about scale?"**
→ "AWS Polly auto-scales. API is stateless. S3 and DynamoDB scale automatically."

**"Cost?"**
→ "~$25/month for 1000 users. Demo cost: $0.17 total."

**"Other languages?"**
→ "Supports Hindi, English (Indian), Tamil, Telugu, Bengali, Marathi. Can add more voices."

---

## Emergency Fixes

**Server crashed:**
```powershell
python start_server.py
```

**Synthesis failing:**
```powershell
python scripts/check_aws_credentials.py
```

**Nothing works:**
→ Show API docs, explain architecture, show code

---

## Success Checklist

- [ ] Server running
- [ ] API docs open in browser
- [ ] Tested one synthesis
- [ ] Demo commands ready to copy-paste
- [ ] Confident and ready!

---

## You've Got This! 🚀

Your platform works. You know how to demo it. Just be confident and show them what you built!

**Team SAAN** | **Souhridya Patra** | **AWS AI for Bharat**
