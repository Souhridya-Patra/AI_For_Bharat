# 🔧 Fix Python 3.12 Installation Issues

## Problem

You're getting a Rust compilation error when installing Pydantic with Python 3.12+. This happens because newer versions of Pydantic require Rust to compile.

## Solution

Use an older version of FastAPI that works with Pydantic v1 (no Rust required).

---

## Quick Fix (Recommended)

### Option 1: PowerShell Script
```powershell
.\install_python312.ps1
```

### Option 2: Python Script
```powershell
python install_python312.py
```

---

## Manual Installation

If the scripts don't work, install packages manually:

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install packages one by one
python -m pip install fastapi==0.109.2
python -m pip install uvicorn==0.27.1
python -m pip install boto3
python -m pip install soundfile
python -m pip install python-multipart
python -m pip install python-dotenv
```

---

## What Changed?

We're using:
- **FastAPI 0.109.2** (instead of latest) - works with Pydantic v1
- **Pydantic v1** (automatically installed) - no Rust required

Your application code already supports this (no changes needed)!

---

## Verify Installation

```powershell
python -c "import fastapi; print(f'FastAPI: {fastapi.__version__}')"
python -c "import uvicorn; print(f'Uvicorn: {uvicorn.__version__}')"
python -c "import boto3; print('boto3: OK')"
python -c "import soundfile; print('soundfile: OK')"
```

Expected output:
```
FastAPI: 0.109.2
Uvicorn: 0.27.1
boto3: OK
soundfile: OK
```

---

## Start the Server

```powershell
python start_server.py
```

---

## Alternative: Use Python 3.10

If you continue having issues, consider using Python 3.10 instead:

1. Download Python 3.10 from: https://www.python.org/downloads/
2. Install it
3. Use it for this project:
   ```powershell
   py -3.10 -m pip install -r backend/requirements-python312.txt
   py -3.10 start_server.py
   ```

---

## Why This Happens

- **Python 3.12+** is very new
- **Pydantic v2** (used by latest FastAPI) requires Rust compilation
- **Windows** doesn't have Rust by default
- **Solution:** Use older FastAPI version with Pydantic v1

---

## Troubleshooting

### Issue: soundfile fails to install

**Solution:** Install libsndfile first
```powershell
# Download from: http://www.mega-nerd.com/libsndfile/
# Or use conda:
conda install -c conda-forge libsndfile
```

### Issue: boto3 fails to install

**Solution:** Install with --no-cache-dir
```powershell
python -m pip install --no-cache-dir boto3
```

### Issue: Still getting Rust errors

**Solution:** Clear pip cache and try again
```powershell
python -m pip cache purge
python -m pip install --no-cache-dir fastapi==0.109.2
```

---

## For EC2 Deployment

On Ubuntu 22.04 (EC2), this issue doesn't occur because:
- Python 3.10 is pre-installed
- Linux has better package support
- No Rust compilation issues

So your deployment will work fine!

---

## Summary

✅ **Local Development:** Use install_python312.ps1  
✅ **EC2 Deployment:** No changes needed (Python 3.10)  
✅ **Your Code:** Already compatible (no changes needed)  

---

## Next Steps

1. Run: `.\install_python312.ps1`
2. Verify: `python -c "import fastapi; print(fastapi.__version__)"`
3. Start: `python start_server.py`
4. Test: Open http://localhost:8000/docs

---

**You're all set! The installation should work now.** 🚀
