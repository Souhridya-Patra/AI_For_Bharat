# 🚀 EC2 Deployment - Step by Step

## Step 1: Launch EC2 Instance (5 minutes)

### 1.1 Go to AWS Console
- Open: https://console.aws.amazon.com/ec2/
- Make sure you're in **us-east-1** region (top right)

### 1.2 Click "Launch Instance"

### 1.3 Configure Instance:

**Name:** `ai-voice-platform`

**Application and OS Images (AMI):**
- Select: **Ubuntu Server 22.04 LTS (Free tier eligible)**
- Architecture: 64-bit (x86)

**Instance type:**
- Select: **t2.medium** (recommended) or **t2.small** (cheaper)
- Note: t2.micro might be too slow

**Key pair:**
- Click "Create new key pair"
- Name: `ai-voice-key`
- Type: RSA
- Format: .pem (for SSH)
- Click "Create key pair" - **SAVE THIS FILE!**

**Network settings:**
- Click "Edit"
- Auto-assign public IP: **Enable**
- Firewall (security groups): **Create security group**
- Security group name: `ai-voice-sg`

**Add these rules:**
1. SSH (22) - Source: My IP (for you to connect)
2. HTTP (80) - Source: Anywhere (0.0.0.0/0)
3. Custom TCP (8000) - Source: Anywhere (0.0.0.0/0) - Backend API
4. Custom TCP (3000) - Source: Anywhere (0.0.0.0/0) - Frontend

**Storage:**
- 20 GB gp3 (default is fine)

### 1.4 Launch Instance
- Click "Launch instance"
- Wait 2-3 minutes for it to start
- Note the **Public IPv4 address** (e.g., 54.123.45.67)

---

## Step 2: Upload Your Code to GitHub (10 minutes)

Before connecting to EC2, let's get your code on GitHub:

### 2.1 Create GitHub Repository
1. Go to: https://github.com/new
2. Repository name: `ai-voice-platform`
3. Description: "AI Voice Platform for Indian Languages - AWS Hackathon"
4. Public repository
5. Click "Create repository"

### 2.2 Upload Code from Your PC

Open PowerShell in your project folder:

```powershell
cd H:\Coding\Bharat

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - AI Voice Platform"

# Add remote (replace with YOUR GitHub URL)
git remote add origin https://github.com/YOUR_USERNAME/ai-voice-platform.git

# Push
git branch -M main
git push -u origin main
```

**Note:** Replace `YOUR_USERNAME` with your actual GitHub username

---

## Step 3: Connect to EC2 (2 minutes)

### 3.1 Open PowerShell

### 3.2 Navigate to where you saved the key file:
```powershell
cd Downloads  # or wherever you saved ai-voice-key.pem
```

### 3.3 Connect via SSH:
```powershell
ssh -i ai-voice-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

Replace `YOUR_EC2_PUBLIC_IP` with your actual IP (e.g., 54.123.45.67)

**If you get "permissions error":**
```powershell
icacls ai-voice-key.pem /inheritance:r
icacls ai-voice-key.pem /grant:r "%username%:R"
```

Type "yes" when asked about authenticity.

---

## Step 4: Setup EC2 Environment (5 minutes)

Once connected to EC2, run these commands:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install -y python3.11 python3-pip git

# Install system dependencies
sudo apt install -y libsndfile1

# Clone your repository
git clone https://github.com/YOUR_USERNAME/ai-voice-platform.git
cd ai-voice-platform

# Install Python dependencies
pip3 install fastapi uvicorn boto3 soundfile python-multipart python-dotenv

# Configure AWS credentials
mkdir -p ~/.aws

# Create credentials file
cat > ~/.aws/credentials << 'EOF'
[default]
aws_access_key_id = YOUR_AWS_ACCESS_KEY
aws_secret_access_key = YOUR_AWS_SECRET_KEY
EOF

# Create config file
cat > ~/.aws/config << 'EOF'
[default]
region = us-east-1
output = json
EOF
```

**IMPORTANT:** Replace `YOUR_AWS_ACCESS_KEY` and `YOUR_AWS_SECRET_KEY` with your actual credentials!

---

## Step 5: Start Services (3 minutes)

### 5.1 Install Screen (to keep processes running)
```bash
sudo apt install -y screen
```

### 5.2 Start Backend
```bash
# Create screen session for backend
screen -S backend

# Start backend
cd ~/ai-voice-platform
python3 start_server.py

# Detach from screen: Press Ctrl+A, then press D
```

### 5.3 Start Frontend
```bash
# Create screen session for frontend
screen -S frontend

# Start frontend
cd ~/ai-voice-platform
python3 start_frontend.py

# Detach from screen: Press Ctrl+A, then press D
```

### 5.4 Verify Services Running
```bash
# Check if services are running
curl http://localhost:8000/health
curl http://localhost:3000
```

---

## Step 6: Test Your Deployment (2 minutes)

### 6.1 Get Your Public URL
Your EC2 public IP: `http://YOUR_EC2_IP:3000`

Example: `http://54.123.45.67:3000`

### 6.2 Open in Browser
1. Open your browser
2. Go to: `http://YOUR_EC2_IP:3000`
3. You should see your AI Voice Platform!
4. Click "Synthesize Speech"
5. Audio should play!

### 6.3 Test API Docs
Go to: `http://YOUR_EC2_IP:8000/docs`

---

## Step 7: Make Services Auto-Start (Optional but Recommended)

If EC2 restarts, services will stop. Let's make them auto-start:

```bash
# Create systemd service for backend
sudo tee /etc/systemd/system/ai-voice-backend.service > /dev/null << EOF
[Unit]
Description=AI Voice Platform Backend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ai-voice-platform
ExecStart=/usr/bin/python3 start_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create systemd service for frontend
sudo tee /etc/systemd/system/ai-voice-frontend.service > /dev/null << EOF
[Unit]
Description=AI Voice Platform Frontend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ai-voice-platform
ExecStart=/usr/bin/python3 start_frontend.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start services
sudo systemctl daemon-reload
sudo systemctl enable ai-voice-backend
sudo systemctl enable ai-voice-frontend
sudo systemctl start ai-voice-backend
sudo systemctl start ai-voice-frontend

# Check status
sudo systemctl status ai-voice-backend
sudo systemctl status ai-voice-frontend
```

---

## ✅ Deployment Complete!

### Your URLs:
- **Frontend:** `http://YOUR_EC2_IP:3000`
- **API Docs:** `http://YOUR_EC2_IP:8000/docs`
- **API Health:** `http://YOUR_EC2_IP:8000/health`

### Share with Judges:
```
Live Application: http://YOUR_EC2_IP:3000
API Documentation: http://YOUR_EC2_IP:8000/docs
GitHub: https://github.com/YOUR_USERNAME/ai-voice-platform
```

---

## 🔧 Useful Commands

### Check if services are running:
```bash
screen -ls  # List all screen sessions
screen -r backend  # Attach to backend (Ctrl+A D to detach)
screen -r frontend  # Attach to frontend
```

### View logs:
```bash
sudo journalctl -u ai-voice-backend -f
sudo journalctl -u ai-voice-frontend -f
```

### Restart services:
```bash
sudo systemctl restart ai-voice-backend
sudo systemctl restart ai-voice-frontend
```

### Stop services:
```bash
sudo systemctl stop ai-voice-backend
sudo systemctl stop ai-voice-frontend
```

---

## 💰 Cost Estimate

**t2.medium:** ~$0.05/hour = ~$1.20/day = ~$36/month
**t2.small:** ~$0.025/hour = ~$0.60/day = ~$18/month

**For hackathon (1 week):** ~$8-10 total

**Remember to STOP the instance after hackathon to avoid charges!**

---

## 🎯 Next Steps

1. ✅ Test your deployed URL
2. ✅ Share URL with a friend to verify
3. ✅ Update FOR_JUDGES.md with your URL
4. ✅ Record video showing deployed version
5. ✅ Submit to hackathon!

---

**Your fully functional application is now live! 🚀**
