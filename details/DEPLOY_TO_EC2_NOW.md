# 🚀 Deploy to EC2 - Complete Guide

## Prerequisites Checklist

✅ AWS Account with credentials
✅ Application working locally
✅ GitHub repository ready (or will create)

---

## Step 1: Launch EC2 Instance

### 1.1 Go to EC2 Console
- Open AWS Console → EC2 → Launch Instance

### 1.2 Configure Instance
```
Name: ai-voice-platform
AMI: Ubuntu Server 22.04 LTS
Instance Type: t3.micro (FREE TIER)
Key Pair: Create new or use existing (SAVE THE .pem FILE!)
```

### 1.3 Configure Security Group
Create security group with these rules:

| Type | Port | Source | Description |
|------|------|--------|-------------|
| SSH | 22 | My IP | SSH access |
| HTTP | 80 | 0.0.0.0/0 | Web access |
| Custom TCP | 8000 | 0.0.0.0/0 | Backend API |
| Custom TCP | 3000 | 0.0.0.0/0 | Frontend |

### 1.4 Launch Instance
- Click "Launch Instance"
- Wait for instance to be "Running"
- Note the Public IPv4 address

---

## Step 2: Connect to EC2

### 2.1 Open PowerShell/Terminal

### 2.2 Set Key Permissions (Windows PowerShell)
```powershell
icacls "your-key.pem" /inheritance:r
icacls "your-key.pem" /grant:r "%username%:R"
```

### 2.3 Connect via SSH
```bash
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

---

## Step 3: Setup EC2 Environment

Copy and paste these commands one by one:

### 3.1 Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 3.2 Install Dependencies
```bash
sudo apt install -y python3-pip git libsndfile1
```

### 3.3 Upload Your Code

**Option A: Via GitHub (Recommended)**
```bash
# First, push your code to GitHub from your local machine
# Then on EC2:
git clone https://github.com/YOUR_USERNAME/ai-voice-platform.git
cd ai-voice-platform
```

**Option B: Via SCP (Direct Upload)**
```bash
# From your local machine (PowerShell):
scp -i your-key.pem -r H:\Coding\Bharat ubuntu@YOUR_EC2_IP:~/ai-voice-platform
```

### 3.4 Install Python Dependencies
```bash
cd ~/ai-voice-platform
pip3 install fastapi uvicorn boto3 soundfile python-multipart python-dotenv
```

### 3.5 Configure AWS Credentials
```bash
mkdir -p ~/.aws

cat > ~/.aws/credentials << 'EOF'
[default]
aws_access_key_id = YOUR_AWS_ACCESS_KEY
aws_secret_access_key = YOUR_AWS_SECRET_KEY
EOF

cat > ~/.aws/config << 'EOF'
[default]
region = us-east-1
output = json
EOF
```

**Replace YOUR_AWS_ACCESS_KEY and YOUR_AWS_SECRET_KEY with your actual credentials!**

### 3.6 Update Frontend API URL

Edit the frontend to use EC2 IP instead of localhost:
```bash
cd ~/ai-voice-platform
nano frontend/index.html
```

Find this line:
```javascript
const API_URL = 'http://localhost:8000/v1';
```

Change to:
```javascript
const API_URL = 'http://YOUR_EC2_PUBLIC_IP:8000/v1';
```

Also update the health check URL:
```javascript
const response = await fetch('http://localhost:8000/health');
```

Change to:
```javascript
const response = await fetch('http://YOUR_EC2_PUBLIC_IP:8000/health');
```

Save and exit (Ctrl+X, Y, Enter)

---

## Step 4: Start Services

### 4.1 Install Screen
```bash
sudo apt install -y screen
```

### 4.2 Start Backend
```bash
screen -S backend
cd ~/ai-voice-platform
python3 start_server.py
```

Press `Ctrl+A` then `D` to detach (backend keeps running)

### 4.3 Start Frontend
```bash
screen -S frontend
cd ~/ai-voice-platform
python3 start_frontend.py
```

Press `Ctrl+A` then `D` to detach (frontend keeps running)

---

## Step 5: Test Deployment

### 5.1 Test Backend
```bash
curl http://YOUR_EC2_PUBLIC_IP:8000/health
```

Should return: `{"status":"healthy"}`

### 5.2 Test Frontend
Open in browser:
```
http://YOUR_EC2_PUBLIC_IP:3000
```

### 5.3 Test Synthesis
1. Enter text in Hindi
2. Click "Synthesize Speech"
3. Audio should play!

---

## Step 6: Update FOR_JUDGES.md

Update the URLs in `FOR_JUDGES.md`:
```markdown
**Live Demo:** http://YOUR_EC2_PUBLIC_IP:3000
**API Documentation:** http://YOUR_EC2_PUBLIC_IP:8000/docs
```

---

## Troubleshooting

### Check if services are running:
```bash
screen -ls
```

### View backend logs:
```bash
screen -r backend
# Press Ctrl+A then D to exit
```

### View frontend logs:
```bash
screen -r frontend
# Press Ctrl+A then D to exit
```

### Restart backend:
```bash
screen -X -S backend quit
screen -S backend
cd ~/ai-voice-platform && python3 start_server.py
# Ctrl+A D
```

### Restart frontend:
```bash
screen -X -S frontend quit
screen -S frontend
cd ~/ai-voice-platform && python3 start_frontend.py
# Ctrl+A D
```

### Check AWS credentials:
```bash
aws sts get-caller-identity
```

---

## Cost Information

### t3.micro Costs:
- **Free Tier:** 750 hours/month FREE (first 12 months)
- **After Free Tier:** $0.0104/hour = ~$7.50/month
- **For Hackathon (1 week):** FREE or ~$1.75

### Remember to STOP instance after hackathon!
```bash
# From AWS Console:
EC2 → Instances → Select instance → Instance State → Stop
```

---

## Quick Commands Reference

```bash
# Check services
screen -ls

# View logs
screen -r backend    # Ctrl+A D to exit
screen -r frontend   # Ctrl+A D to exit

# Restart services
screen -X -S backend quit && screen -S backend
screen -X -S frontend quit && screen -S frontend

# Check memory
free -h

# Check disk space
df -h

# Test API
curl http://localhost:8000/health
```

---

## ✅ Success Checklist

- [ ] EC2 instance launched (t3.micro)
- [ ] Security groups configured (22, 80, 8000, 3000)
- [ ] Connected via SSH
- [ ] Dependencies installed
- [ ] Code uploaded
- [ ] AWS credentials configured
- [ ] Frontend API URL updated
- [ ] Backend running in screen
- [ ] Frontend running in screen
- [ ] Health check passes
- [ ] Frontend loads in browser
- [ ] Speech synthesis works
- [ ] FOR_JUDGES.md updated with URLs

---

## You're Ready! 🎉

Your application is now live and accessible to judges!

**Share this URL with judges:**
```
http://YOUR_EC2_PUBLIC_IP:3000
```

**API Documentation:**
```
http://YOUR_EC2_PUBLIC_IP:8000/docs
```

Good luck with your hackathon! 🚀
