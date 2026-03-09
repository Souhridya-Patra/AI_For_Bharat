# Enable Real Voice Synthesis for Hackathon

## 🎯 Goal
Switch from mock synthesis to real voice synthesis so judges can test your platform.

## ⚡ Quick Start (5 Minutes)

### Option: AWS Polly (RECOMMENDED FOR HACKATHON)

AWS Polly is Amazon's text-to-speech service. It's perfect for hackathons because:
- ✅ No deployment needed
- ✅ Works immediately  
- ✅ Real voice synthesis
- ✅ Supports Hindi (Aditi voice)
- ✅ High quality neural voices
- ✅ Pay per use (~$0.004 per request)
- ✅ No GPU instances needed

### Step 1: Enable AWS Polly

```powershell
python scripts/enable_polly.py
```

This automatically updates your `.env` file to:
```ini
USE_MOCK_SYNTHESIS=False
USE_AWS_POLLY=True
```

### Step 2: Restart Server

```powershell
# Stop current server (Ctrl+C)
# Then restart:
python start_server.py
```

### Step 3: Test Real Synthesis

```powershell
# Run demo
python scripts/demo_hello_bharat.py

# Or test directly
curl -X POST "http://localhost:8000/v1/synthesize" `
  -H "Content-Type: application/json" `
  -d '{
    "text": "नमस्ते भारत! यह एक वास्तविक आवाज़ है।",
    "voice_id": "default",
    "language": "hi"
  }'
```

### Step 4: Verify

You should see in the logs:
```
INFO: Using AWS Polly for real voice synthesis
INFO: [POLLY] Synthesizing text with language=hi, speed=1.0
INFO: [POLLY] Generated audio: duration=3.50s, sample_rate=24000
```

## ✅ That's It!

Your platform now has real voice synthesis!

## 🎤 Supported Voices

### Hindi (Best for "AI for Bharat")
```json
{
  "text": "नमस्ते भारत! यह एक AI आवाज़ प्लेटफ़ॉर्म है।",
  "language": "hi"
}
```
Voice: Aditi (Female, Indian accent)

### English (Indian)
```json
{
  "text": "Hello Bharat! This is an AI voice platform.",
  "language": "en-IN"
}
```
Voice: Aditi (Female, Indian English)

### English (US)
```json
{
  "text": "Hello! This is a test.",
  "language": "en"
}
```
Voice: Joanna (Female, US accent)

### Other Indian Languages
Tamil, Telugu, Bengali, Marathi all use the Aditi (Hindi) voice.

## 🎛️ Features

### Speed Control
```json
{
  "text": "This is fast speech",
  "speed": 1.5,
  "language": "en"
}
```
Supported: 0.5x to 2.0x

### Streaming
```json
{
  "text": "Long text here. Multiple sentences. Will stream.",
  "stream": true,
  "language": "en"
}
```

## 💰 Cost

AWS Polly pricing:
- Neural voices: $16 per 1 million characters
- Standard voices: $4 per 1 million characters

For hackathon demo:
- ~100 requests × 100 characters = 10,000 characters
- Cost: ~$0.16 total
- Essentially free for demo purposes!

## 🔍 Troubleshooting

### Error: "Unable to locate credentials"
```powershell
python scripts/check_aws_credentials.py
```

### Error: "Access Denied"
Your AWS user needs `AmazonPollyFullAccess` permission.

### No audio generated
Check server logs for errors. Ensure AWS credentials are valid.

### Wrong voice/language
Check the language code in your request. Use "hi" for Hindi, "en" for English.

## 📊 For Judges

When demonstrating to judges:

1. **Show Real Synthesis**
   - "This uses AWS Polly, Amazon's neural text-to-speech"
   - "Not mock data - real voice synthesis"

2. **Demonstrate Hindi**
   ```
   Text: "नमस्ते! मैं एक AI आवाज़ हूँ।"
   Language: Hindi
   Voice: Aditi (Indian female voice)
   ```

3. **Show Speed Control**
   - Normal: 1.0x
   - Fast: 1.5x
   - Slow: 0.75x

4. **Explain Scalability**
   - "Currently using AWS Polly"
   - "Can switch to custom XTTS-v2 model for more control"
   - "Architecture supports both"

## 🚀 Advanced: Custom Model (Optional)

If you have time and want even better quality:

### Option A: Coqui TTS on EC2
See `docs/REAL_MODEL_DEPLOYMENT.md` - Option A

### Option B: XTTS-v2 on SageMaker
See `docs/REAL_MODEL_DEPLOYMENT.md` - Option C

## 📝 Summary

✅ **Enabled**: Real voice synthesis with AWS Polly  
✅ **Quality**: High-quality neural voices  
✅ **Languages**: Hindi, English (Indian & US)  
✅ **Cost**: ~$0.16 for entire hackathon demo  
✅ **Setup Time**: 5 minutes  
✅ **Judge-Ready**: Professional voice synthesis  

## 🎉 You're Ready!

Your AI Voice Platform now has real voice synthesis and is ready for the hackathon judges to test!

---

**Questions?** Check the logs or run:
```powershell
python scripts/test_all_endpoints.py
```
