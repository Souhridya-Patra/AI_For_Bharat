# Quick Start Guide - AI Voice Platform

## Prerequisites

- Python 3.9+ installed
- AWS account with credentials
- Internet connection

## Step 1: Set Up AWS Credentials

Choose one of these methods:

### Option A: Interactive Python Script (Easiest)

```powershell
python scripts/setup_credentials.py
```

This will:
- Prompt for your AWS Access Key ID
- Prompt for your AWS Secret Access Key
- Prompt for your AWS Region (default: ap-south-1)
- Create credentials files
- Test the connection

### Option B: PowerShell Script

```powershell
.\scripts\setup_credentials.ps1
```

### Option C: Manual Setup

1. Create directory: `C:\Users\YOUR_USERNAME\.aws\`

2. Create file: `credentials`
   ```ini
   [default]
   aws_access_key_id = YOUR_ACCESS_KEY_ID
   aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
   ```

3. Create file: `config`
   ```ini
   [default]
   region = ap-south-1
   output = json
   ```

## Step 2: Verify Credentials

```powershell
python scripts/check_aws_credentials.py
```

You should see:
```
✓ Successfully connected to AWS!
  - Account: 123456789012
  - User ARN: arn:aws:iam::...
```

## Step 3: Install Dependencies

```powershell
pip install boto3 botocore
```

## Step 4: Set Up AWS Infrastructure

```powershell
python scripts/setup_aws_infrastructure.py
```

This creates:
- S3 buckets for audio and models
- DynamoDB tables for voices, projects, and audit logs

Expected output:
```
✓ Created bucket: ai-voice-platform-audio
✓ Created bucket: ai-voice-platform-models
✓ Created table: voice_models
✓ Created table: projects
✓ Created table: audit_logs
✓ AWS Infrastructure setup completed successfully!
```

## Step 5: Install Backend Dependencies

```powershell
cd backend
pip install -r requirements.txt
```

## Step 6: Configure Backend

```powershell
# Copy environment template
cp .env.example .env

# Edit .env file (optional - defaults should work)
notepad .env
```

## Step 7: Start the API Server

```powershell
# From backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

## Step 8: Test the API

Open a new terminal and run:

```powershell
# Check health
curl http://localhost:8000/health

# Run demo (requires SageMaker endpoint)
python scripts/demo_hello_bharat.py
```

## Troubleshooting

### Error: "Unable to locate credentials"

**Solution**: Run `python scripts/setup_credentials.py` to configure AWS credentials.

### Error: "BucketAlreadyExists"

**Solution**: S3 bucket names must be globally unique. Edit `scripts/setup_aws_infrastructure.py` and change bucket names:
```python
S3_AUDIO_BUCKET = "ai-voice-platform-audio-YOUR_NAME"
S3_MODELS_BUCKET = "ai-voice-platform-models-YOUR_NAME"
```

### Error: "Access Denied"

**Solution**: Your AWS user needs these permissions:
- AmazonS3FullAccess
- AmazonDynamoDBFullAccess
- AmazonSageMakerFullAccess

Contact your AWS administrator or hackathon organizer.

### Error: "Module not found"

**Solution**: Install missing dependencies:
```powershell
pip install -r backend/requirements.txt
```

### API not responding

**Solution**: 
1. Check if server is running: `curl http://localhost:8000/health`
2. Check for port conflicts
3. Try a different port: `uvicorn app.main:app --port 8001`

## Next Steps

1. **Deploy XTTS-v2 Model to SageMaker**
   - See `docs/sagemaker_deployment.md`
   - This requires model files and GPU instances

2. **Test Voice Synthesis**
   ```powershell
   python scripts/demo_hello_bharat.py
   ```

3. **Build Frontend**
   - See `frontend/README.md` (coming soon)

4. **Deploy to Production**
   - See `docs/deployment.md`

## Getting Help

- Check `docs/AWS_SETUP_GUIDE.md` for detailed AWS setup
- Review error logs in terminal
- Check AWS Console for resource status
- Contact hackathon support for credential issues

## Quick Reference

### Important URLs
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Important Files
- Backend config: `backend/.env`
- AWS credentials: `~/.aws/credentials`
- AWS config: `~/.aws/config`

### Important Commands
```powershell
# Check credentials
python scripts/check_aws_credentials.py

# Setup infrastructure
python scripts/setup_aws_infrastructure.py

# Start API
cd backend && uvicorn app.main:app --reload

# Run demo
python scripts/demo_hello_bharat.py
```

---

**Ready to build!** 🚀
