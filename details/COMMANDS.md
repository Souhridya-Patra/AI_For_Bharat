# Command Reference - AI Voice Platform

Quick reference for all commands to run the AI Voice Platform.

## 🚀 Initial Setup

### 1. Configure AWS Credentials
```powershell
# Interactive setup (easiest)
python scripts/setup_credentials.py

# Or check existing credentials
python scripts/check_aws_credentials.py

# Or use AWS CLI
aws configure
```

### 2. Create AWS Infrastructure
```powershell
# Create S3 buckets and DynamoDB tables
python scripts/setup_aws_infrastructure.py
```

### 3. Install Dependencies
```powershell
# Install backend dependencies
cd backend
pip install -r requirements.txt
```

## 🏃 Running the Server

### Start Server
```powershell
# Method 1: Using Python script (recommended)
python start_server.py

# Method 2: Using PowerShell script
.\start_server.ps1

# Method 3: Manual start
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Method 4: Different port
python -m uvicorn app.main:app --reload --port 8001
```

### Stop Server
```
Press Ctrl+C in the terminal
```

## 🧪 Testing

### Run All Tests
```powershell
# Test all endpoints
python scripts/test_all_endpoints.py

# Run demo
python scripts/demo_hello_bharat.py
```

### Test Individual Endpoints

#### Health Check
```powershell
curl http://localhost:8000/health
```

#### Synthesize Speech
```powershell
curl -X POST "http://localhost:8000/v1/synthesize" `
  -H "Content-Type: application/json" `
  -d '{
    "text": "Hello Bharat!",
    "voice_id": "default",
    "speed": 1.0,
    "pitch": 0,
    "stream": false
  }'
```

#### Clone Voice
```powershell
curl -X POST "http://localhost:8000/v1/clone" `
  -F "audio_file=@audio.wav" `
  -F "voice_name=My Voice"
```

#### List Voices
```powershell
curl http://localhost:8000/v1/voices
```

#### Delete Voice
```powershell
curl -X DELETE "http://localhost:8000/v1/voices/voice_abc123"
```

## 🌐 Access URLs

```
API Base:        http://localhost:8000
API Docs:        http://localhost:8000/docs
ReDoc:           http://localhost:8000/redoc
Health Check:    http://localhost:8000/health
```

## 🔧 Configuration

### View Current Config
```powershell
# View .env file
cd backend
type .env

# Or on Linux/Mac
cat .env
```

### Edit Config
```powershell
# Windows
notepad backend\.env

# Or use any text editor
code backend\.env
```

### Important Settings
```ini
# Use mock synthesis (no SageMaker needed)
USE_MOCK_SYNTHESIS=True

# AWS Region
AWS_REGION=ap-south-1

# Debug mode
DEBUG=True
```

## 📊 AWS Commands

### Check S3 Buckets
```powershell
# List buckets
aws s3 ls

# List files in bucket
aws s3 ls s3://ai-voice-platform-audio/

# Download file
aws s3 cp s3://ai-voice-platform-audio/file.wav ./
```

### Check DynamoDB Tables
```powershell
# List tables
aws dynamodb list-tables

# Describe table
aws dynamodb describe-table --table-name voice_models

# Scan table (view all items)
aws dynamodb scan --table-name voice_models
```

### Check SageMaker Endpoints
```powershell
# List endpoints
aws sagemaker list-endpoints

# Describe endpoint
aws sagemaker describe-endpoint --endpoint-name xtts-v2-endpoint
```

## 🐛 Troubleshooting Commands

### Check Python Version
```powershell
python --version
# Should be 3.9 or higher
```

### Check Installed Packages
```powershell
pip list | findstr fastapi
pip list | findstr boto3
```

### Reinstall Dependencies
```powershell
cd backend
pip install -r requirements.txt --force-reinstall
```

### Check Port Usage
```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill process on port (if needed)
# Find PID from above command, then:
taskkill /PID <PID> /F
```

### View Server Logs
```
# Logs appear in the terminal where server is running
# Look for errors starting with "ERROR:" or "Traceback"
```

### Test AWS Connection
```powershell
# Test credentials
python scripts/check_aws_credentials.py

# Test S3 access
aws s3 ls

# Test DynamoDB access
aws dynamodb list-tables
```

## 📦 Package Management

### Update Dependencies
```powershell
cd backend
pip install --upgrade -r requirements.txt
```

### Add New Package
```powershell
# Install package
pip install package-name

# Add to requirements.txt
pip freeze | findstr package-name >> requirements.txt
```

## 🔄 Git Commands (if using version control)

```powershell
# Initialize repo
git init

# Add files
git add .

# Commit
git commit -m "Initial commit"

# Push to GitHub
git remote add origin https://github.com/yourusername/ai-voice-platform.git
git push -u origin main
```

## 🚢 Deployment Commands

### Docker (if using)
```powershell
# Build image
docker build -t ai-voice-platform .

# Run container
docker run -p 8000:8000 ai-voice-platform

# Stop container
docker stop <container-id>
```

### AWS Lambda (if deploying)
```powershell
# Package application
cd backend
pip install -t package -r requirements.txt

# Create deployment package
cd package
zip -r ../deployment.zip .
cd ..
zip -g deployment.zip app/

# Deploy
aws lambda update-function-code `
  --function-name ai-voice-platform `
  --zip-file fileb://deployment.zip
```

## 📝 Development Commands

### Format Code
```powershell
# Install black
pip install black

# Format code
black backend/
```

### Lint Code
```powershell
# Install flake8
pip install flake8

# Lint code
flake8 backend/
```

### Type Checking
```powershell
# Install mypy
pip install mypy

# Check types
mypy backend/
```

## 🎯 Quick Commands for Demo

```powershell
# 1. Start server
python start_server.py

# 2. In new terminal - test everything
python scripts/test_all_endpoints.py

# 3. Run demo
python scripts/demo_hello_bharat.py

# 4. Open browser
start http://localhost:8000/docs
```

## 💡 Useful Aliases (Optional)

Add to PowerShell profile (`$PROFILE`):

```powershell
# Quick start server
function Start-VoiceAPI {
    python start_server.py
}

# Quick test
function Test-VoiceAPI {
    python scripts/test_all_endpoints.py
}

# Quick demo
function Demo-VoiceAPI {
    python scripts/demo_hello_bharat.py
}

# Aliases
Set-Alias voice Start-VoiceAPI
Set-Alias test-voice Test-VoiceAPI
Set-Alias demo-voice Demo-VoiceAPI
```

Then use:
```powershell
voice      # Start server
test-voice # Run tests
demo-voice # Run demo
```

## 📚 Help Commands

```powershell
# Python help
python --help

# Pip help
pip --help

# AWS CLI help
aws help
aws s3 help
aws dynamodb help

# Uvicorn help
uvicorn --help
```

---

**Tip**: Keep this file open in a separate window for quick reference!
