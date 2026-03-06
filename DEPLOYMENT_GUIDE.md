# 🚀 Deployment Guide for Judges
## Make Your Project Accessible for Remote Testing

---

## 🎯 Goal
Deploy your AI Voice Platform so judges can test it remotely without you being present.

---

## ⚡ RECOMMENDED: AWS EC2 Deployment (30 minutes)

This is the best option because:
- ✅ Judges can access via public URL
- ✅ Uses AWS (shows AWS expertise)
- ✅ Professional deployment
- ✅ Free tier eligible

### Step 1: Launch EC2 Instance

1. **Go to AWS Console** → EC2
2. **Click "Launch Instance"**
3. **Configure:**
   - Name: `ai-voice-platform`
   - AMI: Ubuntu Server 22.04 LTS (Free tier eligible)
   - Instance type: `t2.medium` (or t2.micro for testing)
   - Key pair: Create new or use existing
   - Security group: Create new with these rules:
     - SSH (22) - Your IP
     - HTTP (80) - Anywhere
     - Custom TCP (8000) - Anywhere
     - Custom TCP (3000) - Anywhere

4. **Launch instance**

### Step 2: Connect to EC2

```bash
# Download your key pair (.pem file)
# Then connect:
ssh -i "your-key.pem" ubuntu@your-ec2-public-ip
```

### Step 3: Setup Environment

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install git
sudo apt install git -y

# Clone your repository (after you upload to GitHub)
git clone https://github.com/yourusername/ai-voice-platform.git
cd ai-voice-platform

# Install dependencies
pip3 install fastapi uvicorn boto3 soundfile python-multipart python-dotenv
```

### Step 4: Configure AWS Credentials on EC2

```bash
# Configure AWS credentials
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter region: us-east-1
# Enter output format: json
```

### Step 5: Start Backend (Keep Running)

```bash
# Install screen to keep process running
sudo apt install screen -y

# Start screen session
screen -S backend

# Start backend
cd ~/ai-voice-platform
python3 start_server.py

# Detach from screen: Press Ctrl+A then D
```

### Step 6: Start Frontend (Keep Running)

```bash
# New screen session
screen -S frontend

# Start frontend
cd ~/ai-voice-platform
python3 start_frontend.py

# Detach from screen: Press Ctrl+A then D
```

### Step 7: Get Public URL

Your EC2 public IP: `http://your-ec2-ip:3000`

Example: `http://54.123.45.67:3000`

---

## 🌐 ALTERNATIVE: Ngrok (5 minutes - Quick & Easy)

If you don't want to deploy to AWS, use Ngrok to expose your local server:

### Step 1: Download Ngrok

1. Go to: https://ngrok.com/
2. Sign up (free)
3. Download ngrok for Windows

### Step 2: Setup Ngrok

```powershell
# Extract ngrok.exe
# Add your authtoken (from ngrok dashboard)
.\ngrok authtoken YOUR_AUTH_TOKEN
```

### Step 3: Expose Backend

```powershell
# Terminal 1: Start backend
python start_server.py

# Terminal 2: Expose backend
.\ngrok http 8000
```

Copy the public URL (e.g., `https://abc123.ngrok.io`)

### Step 4: Update Frontend

Edit `demo.html` and change:
```javascript
const API_URL = 'https://your-ngrok-url.ngrok.io/v1';
```

### Step 5: Expose Frontend

```powershell
# Terminal 3: Start frontend
python start_frontend.py

# Terminal 4: Expose frontend
.\ngrok http 3000
```

Copy the frontend URL and share with judges!

---

## 📦 BEST: Complete AWS Deployment Script

Let me create an automated deployment script:

