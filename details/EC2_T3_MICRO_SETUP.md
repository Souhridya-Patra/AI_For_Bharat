# 🚀 EC2 Deployment - t3.micro Optimized

## Instance Selection

**Choose:** `t3.micro`
- Free tier eligible
- 2 vCPUs, 1 GB RAM
- Perfect for hackathon demo

---

## Modified Setup Commands

After connecting to EC2, use these optimized commands:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and essentials (Python 3.10 is pre-installed on Ubuntu 22.04)
sudo apt install -y python3-pip git libsndfile1

# Clone repository
git clone https://github.com/YOUR_USERNAME/ai-voice-platform.git
cd ai-voice-platform

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn boto3 soundfile python-multipart python-dotenv

# Alternative: Install without venv (use --break-system-packages)
# pip3 install --break-system-packages fastapi uvicorn boto3 soundfile python-multipart python-dotenv

# Configure AWS credentials
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

# Install screen
sudo apt install -y screen

# Start backend
screen -S backend
cd ~/ai-voice-platform
source venv/bin/activate  # Activate venv if you created one
python3 start_server.py
# Press Ctrl+A then D to detach

# Start frontend
screen -S frontend
cd ~/ai-voice-platform
source venv/bin/activate  # Activate venv if you created one
python3 start_frontend.py
# Press Ctrl+A then D to detach
```

---

## Performance Tips for t3.micro

### 1. Monitor Memory Usage
```bash
free -h  # Check available memory
```

### 2. If Services Crash
```bash
# Check logs
screen -r backend  # See backend logs
screen -r frontend  # See frontend logs
```

### 3. Restart if Needed
```bash
# Kill and restart
screen -X -S backend quit
screen -X -S frontend quit

# Start again
screen -S backend
cd ~/ai-voice-platform && python3 start_server.py
# Ctrl+A D

screen -S frontend
cd ~/ai-voice-platform && python3 start_frontend.py
# Ctrl+A D
```

---

## Expected Performance

### t3.micro Performance:
- **Synthesis latency:** 500-800ms (slightly slower than t2.medium)
- **Concurrent users:** 5-10 (fine for judging)
- **Stability:** Good for demo purposes

### This is Perfect for Hackathon Because:
- ✅ Free tier eligible
- ✅ Judges test one at a time
- ✅ Not expecting production-scale traffic
- ✅ Shows cost optimization skills

---

## If You Need Better Performance

### Option 1: Upgrade to t3.small
- Stop instance
- Change instance type to t3.small
- Start instance
- Cost: ~$0.02/hour

### Option 2: Use Spot Instance
- Launch as spot instance
- 70% cheaper
- May be interrupted (but unlikely during short demo)

---

## Cost Breakdown

### t3.micro:
- **Free tier:** 750 hours/month free (first 12 months)
- **After free tier:** $0.0104/hour = ~$7.50/month
- **For hackathon (1 week):** FREE or ~$1.75

### t3.small (if you upgrade):
- **Cost:** $0.0208/hour = ~$15/month
- **For hackathon (1 week):** ~$3.50

---

## ✅ Recommendation

**Use t3.micro for hackathon!**

Reasons:
1. Free tier eligible
2. Sufficient for demo
3. Shows cost awareness
4. Easy to upgrade if needed

---

## Complete Deployment Steps

1. **Launch EC2:**
   - Instance type: `t3.micro` ⭐
   - AMI: Ubuntu 22.04 LTS
   - Security groups: 22, 80, 8000, 3000
   - Key pair: Save it!

2. **Connect:**
   ```bash
   ssh -i your-key.pem ubuntu@YOUR_EC2_IP
   ```

3. **Setup:**
   - Follow commands above
   - Install dependencies
   - Configure AWS credentials

4. **Start Services:**
   - Backend in screen session
   - Frontend in screen session

5. **Test:**
   - Open `http://YOUR_EC2_IP:3000`
   - Synthesize speech
   - ✅ Works!

---

## Troubleshooting t3.micro

### Issue: Out of Memory
**Solution:** Restart services, they'll use less memory on fresh start

### Issue: Slow Response
**Solution:** This is normal for t3.micro, still under 1 second

### Issue: Service Crashes
**Solution:** Check logs, restart service

---

## You're Ready!

**Use t3.micro and follow the deployment steps!**

Your application will work perfectly for hackathon judging! 🚀
