# 🔧 Installation Fix for Windows

## Problem
Pydantic v2 requires Rust compilation which is failing on your system.

## Solution Options

### Option 1: Use Pre-Built Wheels (RECOMMENDED)

Try installing with pre-built wheels only:

```powershell
# Install packages one by one
python -m pip install fastapi==0.104.1 --only-binary :all:
python -m pip install uvicorn==0.24.0 --only-binary :all:
python -m pip install "pydantic<2.0" --only-binary :all:
python -m pip install boto3==1.34.34
python -m pip install soundfile==0.12.1
python -m pip install python-multipart==0.0.6
python -m pip install python-dotenv==1.0.0
```

### Option 2: Use Conda (FASTEST)

If you have Anaconda or Miniconda:

```powershell
# Create new environment
conda create -n bharat python=3.11 -y
conda activate bharat

# Install from conda-forge
conda install -c conda-forge fastapi uvicorn boto3 python-dotenv -y
pip install soundfile python-multipart pydantic==1.10.13
```

### Option 3: Use Python 3.11 (More Compatible)

Python 3.13 is very new and some packages don't have pre-built wheels yet.

```powershell
# Download Python 3.11 from python.org
# Install it
# Then create virtual environment:

py -3.11 -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r backend/requirements-hackathon.txt
```

### Option 4: Skip Pydantic Settings (QUICKEST FOR DEMO)

Use environment variables directly:

```powershell
# Install minimal packages
python -m pip install fastapi==0.104.1
python -m pip install uvicorn==0.24.0
python -m pip install boto3==1.34.34
python -m pip install soundfile==0.12.1
python -m pip install python-multipart==0.0.6
python -m pip install python-dotenv==1.0.0
```

Then I'll update the code to not use pydantic-settings.

## Recommended: Option 4 (Quickest)

Let me know and I'll update the config.py to work without pydantic-settings. This is the fastest way to get your demo working!

Just run:
```powershell
python -m pip install fastapi uvicorn boto3 soundfile python-multipart python-dotenv
```

Then I'll fix the config file.
