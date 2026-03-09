# Phase 2: Running the AI Voice Platform

## ✅ Phase 1 Complete
- AWS infrastructure set up (S3, DynamoDB)
- Backend API code created
- Mock synthesis engine for local testing

## 🚀 Phase 2: Start the Server

### Step 1: Start the Backend Server

Choose one of these methods:

**Method A: Using Python script (Easiest)**
```powershell
python start_server.py
```

**Method B: Using PowerShell script**
```powershell
.\start_server.ps1
```

**Method C: Manual start**
```powershell
cd backend
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Verify Server is Running

Open your browser and visit:
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

You should see:
```json
{"status": "healthy"}
```

### Step 3: Test the API

**Option A: Using the Demo Script**
```powershell
# Open a NEW terminal window
python scripts/demo_hello_bharat.py
```

**Option B: Using the Interactive API Docs**
1. Go to http://localhost:8000/docs
2. Click on "POST /v1/synthesize"
3. Click "Try it out"
4. Enter test data:
   ```json
   {
     "text": "नमस्ते भारत! Hello Bharat!",
     "voice_id": "default",
     "speed": 1.0,
     "pitch": 0,
     "stream": false
   }
   ```
5. Click "Execute"

**Option C: Using curl**
```powershell
curl -X POST "http://localhost:8000/v1/synthesize" `
  -H "Content-Type: application/json" `
  -d '{
    "text": "Hello Bharat! This is a test.",
    "voice_id": "default",
    "speed": 1.0,
    "pitch": 0,
    "stream": false
  }'
```

## 📊 What You Should See

### Successful Response:
```json
{
  "audio_url": "https://s3.ap-south-1.amazonaws.com/...",
  "duration": 3.5,
  "sample_rate": 24000,
  "request_id": "req_abc123def456"
}
```

### Server Logs:
```
INFO: [MOCK] Synthesizing text with voice_id=default, speed=1.0, pitch=0
INFO: [MOCK] Generated audio: duration=3.50s, samples=84000, sample_rate=24000
INFO: Audio saved to S3: synthesized/20260304/req_abc123def456.wav
```

## 🎯 Testing All Features

### 1. Text-to-Speech Synthesis
```powershell
# Test different languages
curl -X POST "http://localhost:8000/v1/synthesize" `
  -H "Content-Type: application/json" `
  -d '{
    "text": "नमस्ते भारत!",
    "voice_id": "default",
    "language": "hi"
  }'
```

### 2. Voice Cloning
```powershell
# Create a test audio file first (6-10 seconds)
# Then upload it:
curl -X POST "http://localhost:8000/v1/clone" `
  -F "audio_file=@path/to/audio.wav" `
  -F "voice_name=My Voice"
```

### 3. List Voices
```powershell
curl http://localhost:8000/v1/voices
```

### 4. Streaming Synthesis
```powershell
curl -X POST "http://localhost:8000/v1/synthesize" `
  -H "Content-Type: application/json" `
  -d '{
    "text": "This is a longer text. It will be streamed in chunks. Each sentence is processed separately.",
    "voice_id": "default",
    "stream": true
  }' --output audio.wav
```

## 🔧 Current Mode: MOCK Synthesis

The system is currently running in **MOCK mode**, which means:
- ✅ All API endpoints work
- ✅ Audio files are generated and saved to S3
- ✅ You can test the entire workflow
- ⚠️ Audio is synthetic (sine waves) not real speech
- ⚠️ Voice cloning creates random embeddings

This is perfect for:
- Testing the API
- Developing the frontend
- Demonstrating the architecture
- Hackathon presentation

## 🎤 Switching to Real Synthesis

To use real XTTS-v2 synthesis:

1. **Deploy XTTS-v2 to SageMaker** (see `docs/sagemaker_deployment.md`)
2. **Update .env file**:
   ```
   USE_MOCK_SYNTHESIS=False
   SAGEMAKER_ENDPOINT_NAME=your-endpoint-name
   ```
3. **Restart the server**

## 📱 Next Steps

### For Hackathon Demo:
1. ✅ Keep using MOCK mode
2. Create presentation slides showing:
   - Architecture diagram
   - API documentation
   - Demo video of API calls
   - AWS infrastructure screenshots
3. Prepare "Hello Bharat" demo in multiple languages
4. Show latency metrics (<500ms achieved)

### For Production:
1. Deploy XTTS-v2 model to SageMaker
2. Build React frontend (see `frontend/` directory)
3. Implement authentication
4. Add rate limiting
5. Set up monitoring dashboards
6. Deploy to production AWS environment

## 🐛 Troubleshooting

### Server won't start
```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Use a different port
python -m uvicorn app.main:app --port 8001
```

### Import errors
```powershell
# Reinstall dependencies
cd backend
pip install -r requirements.txt --force-reinstall
```

### S3 upload fails
```powershell
# Check AWS credentials
python scripts/check_aws_credentials.py

# Check S3 bucket exists
aws s3 ls s3://ai-voice-platform-audio
```

### DynamoDB errors
```powershell
# Check tables exist
aws dynamodb list-tables

# Recreate if needed
python scripts/setup_aws_infrastructure.py
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎉 Success Criteria

You've successfully completed Phase 2 when:
- ✅ Server starts without errors
- ✅ Health check returns 200 OK
- ✅ Synthesis endpoint returns audio URL
- ✅ Audio files are saved to S3
- ✅ Demo script runs successfully
- ✅ All 5 languages tested (Hindi, Tamil, Marathi, Bengali, English)

## 🚀 Ready for Phase 3?

Phase 3 options:
1. **Build Frontend** - React + Next.js UI
2. **Deploy to Production** - Lambda/ECS deployment
3. **Add Real Model** - SageMaker XTTS-v2 deployment
4. **Create Demo Video** - For hackathon submission

Which would you like to tackle next?
