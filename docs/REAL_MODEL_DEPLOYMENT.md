# Real Model Deployment Guide

## Overview

For the hackathon, we have 3 deployment options for real voice synthesis:

1. **Option A: Coqui TTS on EC2** (Recommended for hackathon - Fast setup)
2. **Option B: XTTS-v2 on SageMaker** (Production-grade but complex)
3. **Option C: Use Existing TTS API** (Fastest - Use AWS Polly or external API)

## Option A: Coqui TTS on EC2 (RECOMMENDED)

This is the fastest way to get real voice synthesis working for your hackathon demo.

### Why This Option?
- ✅ Real voice synthesis (not mock)
- ✅ Can deploy in 30 minutes
- ✅ Works with existing API code
- ✅ Supports Indian languages
- ✅ No complex SageMaker setup needed
- ✅ Cost-effective for hackathon (~$0.10/hour)

### Step 1: Launch EC2 Instance

```powershell
# Create EC2 instance with GPU (for best quality)
aws ec2 run-instances `
  --image-id ami-0c55b159cbfafe1f0 `
  --instance-type g4dn.xlarge `
  --key-name your-key-pair `
  --security-group-ids sg-xxxxxxxx `
  --subnet-id subnet-xxxxxxxx `
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=voice-synthesis-server}]'

# Or use t3.xlarge for CPU-only (slower but cheaper)
# --instance-type t3.xlarge
```

### Step 2: Install Coqui TTS on EC2

SSH into your EC2 instance and run:

```bash
# Update system
sudo apt-get update
sudo apt-get install -y python3-pip python3-dev ffmpeg

# Install Coqui TTS
pip3 install TTS

# Install additional dependencies
pip3 install fastapi uvicorn soundfile numpy

# Test installation
tts --list_models
```

### Step 3: Create TTS Server on EC2

Create a file `tts_server.py` on EC2:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from TTS.api import TTS
import numpy as np
import base64
import io
import soundfile as sf

app = FastAPI()

# Initialize TTS model
print("Loading TTS model...")
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=True)
print("Model loaded!")

class SynthesisRequest(BaseModel):
    text: str
    language: str = "en"
    speaker_wav: str = None  # Base64 encoded audio for voice cloning

@app.post("/synthesize")
async def synthesize(request: SynthesisRequest):
    try:
        # Generate audio
        if request.speaker_wav:
            # Voice cloning mode
            wav = tts.tts(
                text=request.text,
                speaker_wav=request.speaker_wav,
                language=request.language
            )
        else:
            # Default voice
            wav = tts.tts(
                text=request.text,
                language=request.language
            )
        
        # Convert to base64
        buffer = io.BytesIO()
        sf.write(buffer, wav, 22050, format='WAV')
        buffer.seek(0)
        audio_base64 = base64.b64encode(buffer.read()).decode()
        
        return {
            "audio": audio_base64,
            "sample_rate": 22050,
            "duration": len(wav) / 22050
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Step 4: Start TTS Server

```bash
# Run server
python3 tts_server.py

# Or run in background
nohup python3 tts_server.py > tts_server.log 2>&1 &
```

### Step 5: Update Your Backend

Update `backend/app/services/synthesis_engine.py` to use the EC2 TTS server:

```python
# Add this method to VoiceSynthesisEngine class
def _call_ec2_tts(self, text: str, language: str = "en") -> np.ndarray:
    """Call TTS server on EC2."""
    import requests
    import base64
    
    ec2_url = "http://YOUR_EC2_IP:8001/synthesize"
    
    response = requests.post(ec2_url, json={
        "text": text,
        "language": language
    })
    
    if response.status_code == 200:
        data = response.json()
        audio_bytes = base64.b64decode(data['audio'])
        
        # Convert to numpy array
        buffer = io.BytesIO(audio_bytes)
        audio, sr = sf.read(buffer)
        
        return audio
    else:
        raise RuntimeError(f"TTS server error: {response.text}")
```

### Step 6: Test

```powershell
# Test EC2 TTS server directly
curl -X POST "http://YOUR_EC2_IP:8001/synthesize" `
  -H "Content-Type: application/json" `
  -d '{"text": "Hello Bharat!", "language": "en"}'

# Test through your API
curl -X POST "http://localhost:8000/v1/synthesize" `
  -H "Content-Type: application/json" `
  -d '{"text": "नमस्ते भारत!", "voice_id": "default", "language": "hi"}'
```

## Option B: Use AWS Polly (FASTEST)

AWS Polly is Amazon's text-to-speech service with Indian language support.

### Advantages
- ✅ No deployment needed
- ✅ Works immediately
- ✅ Supports Hindi, Tamil, Telugu
- ✅ Pay per use
- ✅ High quality

### Implementation

Update `backend/app/services/synthesis_engine.py`:

```python
def _use_aws_polly(self, text: str, language: str = "en") -> np.ndarray:
    """Use AWS Polly for synthesis."""
    import boto3
    
    polly = boto3.client('polly', region_name=settings.aws_region)
    
    # Map language codes to Polly voices
    voice_map = {
        "en": "Joanna",
        "hi": "Aditi",  # Hindi
        "ta": "Aditi",  # Tamil (use Hindi voice)
        "te": "Aditi",  # Telugu (use Hindi voice)
    }
    
    voice_id = voice_map.get(language, "Joanna")
    
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='pcm',
        VoiceId=voice_id,
        SampleRate='24000'
    )
    
    # Read audio stream
    audio_bytes = response['AudioStream'].read()
    
    # Convert to numpy array
    audio = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
    
    return audio
```

### Enable Polly

```powershell
# Update .env
USE_MOCK_SYNTHESIS=False
USE_AWS_POLLY=True

# Restart server
python start_server.py
```

## Option C: XTTS-v2 on SageMaker (Production)

This is the most complex but production-ready option.

### Requirements
- SageMaker endpoint with GPU instance
- Model files (several GB)
- Custom inference container
- More setup time (2-4 hours)

### Quick Setup (if you have time)

1. **Download XTTS-v2 model**
```bash
pip install TTS
python -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2')"
```

2. **Create SageMaker model package**
```python
# See scripts/deploy_to_sagemaker.py (we'll create this)
```

3. **Deploy endpoint**
```bash
python scripts/deploy_to_sagemaker.py
```

## Recommendation for Hackathon

**Use Option A (Coqui TTS on EC2) or Option B (AWS Polly)**

### Why?
1. **Time**: Can be set up in 30 minutes
2. **Cost**: ~$0.10-0.50/hour for EC2 or pay-per-use for Polly
3. **Quality**: Real voice synthesis
4. **Reliability**: Proven technology
5. **Demo-ready**: Works immediately

### For Judges
- Show real voice synthesis
- Demonstrate Indian language support
- Prove low latency
- Show scalability potential

## Cost Comparison

| Option | Setup Time | Cost/Hour | Quality | Indian Languages |
|--------|-----------|-----------|---------|------------------|
| Mock | 0 min | $0 | Synthetic | ✅ |
| AWS Polly | 5 min | $0.004/request | High | ✅ Hindi |
| EC2 + Coqui | 30 min | $0.10-0.50 | Very High | ✅ All |
| SageMaker | 2-4 hours | $0.70+ | Highest | ✅ All |

## Next Steps

1. Choose your option (I recommend Option A or B)
2. Follow the setup guide above
3. Test with demo script
4. Update .env to disable mock mode
5. Restart server and test

Would you like me to create the complete implementation for Option A (EC2) or Option B (Polly)?
