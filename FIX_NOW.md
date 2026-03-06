# 🚀 Quick Fix - Get Running in 2 Minutes

## The Problem
Pydantic v2 requires Rust compilation which is failing on Windows.

## The Solution
Use a simpler config without Pydantic.

## Run This Command

```powershell
python quick_fix_install.py
```

This will:
1. Install only essential packages (no Pydantic compilation)
2. Replace config.py with a simpler version that uses environment variables directly
3. Get your server ready to run

## Then Start Server

```powershell
python start_server.py
```

## That's It!

Your AI Voice Platform will be running with AWS Polly for real voice synthesis.

---

## What This Does

The quick fix:
- ✅ Installs FastAPI, Uvicorn, Boto3, SoundFile
- ✅ Skips Pydantic (uses plain Python classes instead)
- ✅ Keeps all functionality working
- ✅ Uses your .env file for configuration
- ✅ AWS Polly still works perfectly

## Alternative: Manual Installation

If the script doesn't work, run these commands manually:

```powershell
# Install packages
python -m pip install fastapi
python -m pip install uvicorn
python -m pip install boto3
python -m pip install soundfile
python -m pip install python-multipart
python -m pip install python-dotenv

# Copy simple config
copy backend\app\config_simple.py backend\app\config.py

# Start server
python start_server.py
```

## Verify It Works

```powershell
# In new terminal
python scripts/demo_hello_bharat.py
```

You should hear "नमस्ते भारत!" synthesized with AWS Polly!

---

**This is the fastest way to get your hackathon demo working!**
