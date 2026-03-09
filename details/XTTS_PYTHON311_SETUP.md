# 🎭 XTTS True Voice Cloning Setup Guide (Python 3.11)

## Overview
Your voice cloning feature is now **FULLY INTEGRATED** with XTTS-v2! This enables **true voice cloning** where your synthesized speech actually sounds like your cloned voice (not just Polly defaults).

Since XTTS requires Python 3.9-3.11 and your system has Python 3.12, you'll create a separate Python 3.11 environment.

## Why XTTS?
- ✅ **Professional Quality**: Rivals ElevenLabs ($99/month)
- ✅ **True Voice Cloning**: Actually uses your voice embeddings  
- ✅ **16+ Languages**: Hindi, English, Tamil, Telugu, and more
- ✅ **Natural Prosody**: Emotions, breathing, human-like intonation
- ✅ **FREE**: No API costs, runs locally

## Prerequisites
- Ubuntu/Linux server (your current setup)
- 4GB+ RAM
- 5GB+ disk space (for XTTS model download)

---

## Step-by-Step Setup

### 1. Install Python 3.11

Check if Python 3.11 is available:
```bash
python3.11 --version
```

If not installed:
```bash
# Add deadsnakes PPA (for Ubuntu)
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3.11-dev -y

# Verify installation
python3.11 --version
```

### 2. Create Python 3.11 Virtual Environment

```bash
cd ~/AI_For_Bharat

# Create new venv with Python 3.11
python3.11 -m venv venv_xtts

# Activate the new environment
source venv_xtts/bin/activate

# Verify correct version
python --version  # Should show Python 3.11.x
```

### 3. Install Required Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install core dependencies
pip install fastapi==0.109.2
pip install uvicorn==0.27.1
pip install boto3==1.34.51
pip install python-dotenv==1.0.1
pip install python-multipart==0.0.9

# Audio processing
pip install soundfile==0.12.1
pip install librosa==0.10.1
pip install pydub==0.25.1

# Multi-language TTS
pip install gTTS==2.5.0

# **XTTS-v2 (The key package!)**
pip install TTS==0.22.0
```

**Note**: First XTTS run will download ~1.8GB model. This is normal.

### 4. Update .env Configuration

Edit `backend/.env`:
```bash
nano backend/.env
```

Add/Update these lines:
```env
# Enable XTTS for true voice cloning
USE_XTTS=True
USE_XTTS_SAGEMAKER=False

# Keep existing services
USE_AWS_POLLY=True
USE_MOCK_SYNTHESIS=False

# Synthesis priority (xtts > polly > gtts)
SYNTHESIS_PRIORITY=xtts,polly,gtts

# AWS credentials (already configured)
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1

# DynamoDB table for cloned voices
DYNAMODB_VOICES_TABLE=ai-voice-platform-voices

# S3 bucket for voice models
S3_MODELS_BUCKET=ai-voice-platform-models
```

Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

### 5. Pull Latest Code

```bash
git pull origin main
```

### 6. Start Server with XTTS

```bash
# Make sure you're in venv_xtts
source ~/AI_For_Bharat/venv_xtts/bin/activate

# Start server
cd ~/AI_For_Bharat
python start_server.py
```

**First Run**: XTTS will download models (~1.8GB). Wait 3-5 minutes.

Expected output:
```
INFO - [XTTS] Initializing local XTTS-v2 model...
INFO - Downloading tts_models/multilingual/multi-dataset/xtts_v2...
INFO - [XTTS] Local XTTS-v2 model initialized successfully
INFO - Application startup complete
INFO - Uvicorn running on http://0.0.0.0:8000
```

---

## Testing Voice Cloning

### Test 1: Clone a Voice

1. Open frontend: `http://<YOUR_SERVER_IP>:8000`
2. Go to **"🎭 Clone Voice"** tab
3. Upload 6-10 second audio sample
4. Name it (e.g., "My Voice")
5. Click **"Clone This Voice"**
6. Note the voice ID: `voice_abc123def456`

### Test 2: Synthesize with Cloned Voice

1. Go to **"🎵 Text-to-Speech"** tab
2. Select your cloned voice from dropdown
3. Enter text: "नमस्ते! यह मेरी आवाज़ है।"
4. Language: Hindi
5. Click **"Synthesize Speech"**

**Expected**: Audio should sound like YOUR voice, not Polly!

Check logs for:
```
INFO - ✨ Using XTTS-v2 for CLONED voice: voice_abc123def456
INFO - [XTTS] Loading cloned voice: voice_abc123def456
INFO - [XTTS] Downloading cloned voice from S3: s3://...
INFO - [XTTS] Cloning voice from: /tmp/voice_abc123_reference.wav
INFO - [XTTS] Generated audio: size=245760 bytes
```

---

## Troubleshooting

### ImportError: No module named 'TTS'

**Problem**: TTS not installed in active venv  
**Solution**:
```bash
source ~/AI_For_Bharat/venv_xtts/bin/activate
pip install TTS==0.22.0
```

### Python version mismatch

**Problem**: Still using Python 3.12  
**Solution**:
```bash
deactivate  # Exit old venv
source ~/AI_For_Bharat/venv_xtts/bin/activate
python --version  # Verify 3.11
```

### XTTS model download fails

**Problem**: Network timeout during 1.8GB download  
**Solution**:
```bash
# Download manually
python -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2')"
```

### Voice not found in DynamoDB

**Problem**: Cloned voice ID not in database  
**Solution**:
- Re-clone the voice
- Check `.env` has correct `DYNAMODB_VOICES_TABLE`
- Verify AWS credentials work: `aws dynamodb list-tables`

### Audio quality is poor

**Problem**: Reference audio has noise or is too short  
**Solution**:
- Use 8-10 seconds (not 6)
- Record in quiet environment
- Use good microphone
- Single speaker only
- Natural speech (not monotone reading)

### OUT OF MEMORY

**Problem**: Server runs out of RAM during XTTS synthesis  
**Solution**:
```bash
# Check RAM usage
free -h

# If <2GB available, consider:
# 1. Close other applications
# 2. Use smaller batch sizes
# 3. Upgrade server to 4GB+ RAM
# 4. Use SageMaker endpoint instead
```

---

## Performance

### Local XTTS Performance
- **Synthesis Time**: 3-8 seconds per request (CPU)
- **GPU**: 0.5-2 seconds (if available)
- **RAM Usage**: 2-3GB during synthesis
- **Disk**: 1.8GB for model cache
- **Quality**: ⭐⭐⭐⭐⭐ Professional-grade

### vs Polly/gTTS
| Feature | XTTS | Polly | gTTS |
|---------|------|-------|------|
| True Voice Cloning | ✅ Yes | ❌ No | ❌ No |
| Natural Prosody | ✅⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Emotion/Breathing | ✅ Yes | Limited | No |
| Cost | Free | $4/1M chars | Free |
| Speed | 3-8s | <1s | 1-2s |
| Languages | 16+ | 60+ | 100+ |
| Quality | Professional | Very Good | Basic |

---

## Advanced: SageMaker Deployment (Optional)

For **production** with faster synthesis (0.5-2s):

```bash
cd ~/AI_For_Bharat

# Deploy XTTS to SageMaker with GPU
python scripts/deploy_xtts_sagemaker.py
```

Cost: ~$0.60/hour (ml.g4dn.xlarge GPU instance)

Update `.env`:
```env
USE_XTTS=True
USE_XTTS_SAGEMAKER=True
XTTS_SAGEMAKER_ENDPOINT=xtts-v2-endpoint
```

---

## Maintenance

### Switch Between Environments

**Use XTTS (Python 3.11)**:
```bash
source ~/AI_For_Bharat/venv_xtts/bin/activate
python start_server.py
```

**Use Polly/gTTS only (Python 3.12)**:
```bash
source ~/AI_For_Bharat/venv/bin/activate
USE_XTTS=False python start_server.py
```

### Update XTTS

```bash
source ~/AI_For_Bharat/venv_xtts/bin/activate
pip install --upgrade TTS
```

---

## Verification Checklist

Before considering XTTS setup complete:

- [ ] Python 3.11 installed: `python3.11 --version`
- [ ] venv_xtts created and activated
- [ ] TTS==0.22.0 installed: `pip show TTS`
- [ ] .env has `USE_XTTS=True`
- [ ] XTTS model downloaded (~1.8GB in `~/.local/share/tts/`)
- [ ] Server starts without errors
- [ ] Cloned voice synthesis works
- [ ] Audio sounds like cloned voice (not Polly)
- [ ] Logs show "Using XTTS-v2 for CLONED voice"

---

## Quick Commands Reference

```bash
# Setup (one-time)
sudo apt install python3.11 python3.11-venv -y
cd ~/AI_For_Bharat
python3.11 -m venv venv_xtts
source venv_xtts/bin/activate
pip install TTS==0.22.0 librosa pydub gTTS fastapi uvicorn boto3 python-dotenv

# Daily usage
source ~/AI_For_Bharat/venv_xtts/bin/activate
cd ~/AI_For_Bharat
python start_server.py

# Check XTTS is active
curl http://localhost:8000/health | jq
# Look for: "xtts_enabled": true
```

---

## Next Steps

1. ✅ **Setup Python 3.11 environment**
2. ✅ **Install XTTS**
3. ✅ **Enable in .env**
4. ✅ **Test voice cloning**
5. 📊 **Monitor performance**
6. 🎬 **Start dubbing projects**!

---

## Support

### Documentation
- VOICE_CLONING_GUIDE.md - Clone voice workflow
- DUBBING_WITH_CLONED_VOICES.md - Use cloned voices for dubbing
- XTTS_DEPLOYMENT_GUIDE.md - Advanced deployment options

### Issues?
- Check logs: `tail -f server.log`
- Verify .env settings
- Test with simple example first
- GPU not required but speeds up 5-10x

---

**Team SAAN** | AWS AI for Bharat Hackathon 2026

🎭 **True voice cloning is now ready!** 🎤
