# ⚡ Quick Deploy - 3 Steps

## Step 1: Launch EC2 (5 min)

1. Go to: https://console.aws.amazon.com/ec2
2. Click "Launch Instance"
3. Configure:
   - **Name:** ai-voice-platform
   - **AMI:** Ubuntu Server 22.04 LTS
   - **Instance type:** t3.micro
   - **Key pair:** Create new (save the .pem file!)
   - **Security group:** Create new with these ports:
     - SSH (22) - My IP
     - HTTP (80) - Anywhere
     - Custom TCP (8000) - Anywhere
     - Custom TCP (3000) - Anywhere
4. Click "Launch Instance"
5. Wait for status: "Running"
6. Copy the **Public IPv4 address**

---

## Step 2: Push to GitHub (2 min)

```powershell
# Run this in PowerShell:
.\push_to_github.ps1
```

When prompted:
- Enter your GitHub repo URL
- Enter commit message (or press Enter for default)

---

## Step 3: Deploy on EC2 (10 min)

### 3.1 Connect to EC2
```powershell
ssh -i your-key.pem ubuntu@YOUR_EC2_IP
```

### 3.2 Run Setup Commands
```bash
# Update system
sudo apt update && sudo apt install -y python3-pip git libsndfile1

# Clone your repo
git clone https://github.com/YOUR_USERNAME/ai-voice-platform.git
cd ai-voice-platform

# Install dependencies
pip3 install fastapi uvicorn boto3 soundfile python-multipart python-dotenv

# Configure AWS credentials
mkdir -p ~/.aws
cat > ~/.aws/credentials << 'EOF'
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
EOF

cat > ~/.aws/config << 'EOF'
[default]
region = us-east-1
output = json
EOF
```

### 3.3 Update Frontend URL
```bash
# Exit EC2 temporarily (Ctrl+D)
# On your local machine:
python update_frontend_url.py YOUR_EC2_IP

# Push changes
git add frontend/index.html
git commit -m "Update API URL for EC2"
git push

# Back on EC2:
git pull
```

### 3.4 Start Services
```bash
# Install screen
sudo apt install -y screen

# Start backend
screen -S backend
python3 start_server.py
# Press Ctrl+A then D

# Start frontend
screen -S frontend
python3 start_frontend.py
# Press Ctrl+A then D
```

---

## Step 4: Test (1 min)

Open in browser:
```
http://YOUR_EC2_IP:3000
```

Try synthesizing speech!

---

## Step 5: Update FOR_JUDGES.md (1 min)

Replace `YOUR_EC2_IP` with your actual IP in:
- FOR_JUDGES.md
- SUBMISSION_README.md

Commit and push:
```bash
git add .
git commit -m "Add deployment URLs"
git push
```

---

## ✅ Done!

Your application is now live and ready for judges!

**Share this URL:**
```
http://YOUR_EC2_IP:3000
```

---

## Troubleshooting

### Can't connect to EC2?
- Check security group allows SSH from your IP
- Verify .pem file permissions

### Services not starting?
```bash
# Check logs
screen -r backend
screen -r frontend
```

### API not responding?
```bash
# Test health endpoint
curl http://localhost:8000/health
```

### Need to restart?
```bash
screen -X -S backend quit
screen -X -S frontend quit
# Then start again
```

---

## Cost

**t3.micro:** FREE (750 hours/month free tier)
**AWS Services:** ~$0.01 for hackathon

**Total: FREE** 🎉

---

## After Hackathon

**STOP your EC2 instance:**
```
AWS Console → EC2 → Select instance → Instance State → Stop
```

---

Need detailed instructions? See: **DEPLOY_TO_EC2_NOW.md**
