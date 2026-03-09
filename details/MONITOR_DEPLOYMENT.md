# 📊 Monitor Your Deployment

## Quick Health Checks

### 1. Check if Services are Running
```bash
screen -ls
```

**Expected output:**
```
There are screens on:
    12345.backend   (Detached)
    12346.frontend  (Detached)
2 Sockets in /run/screen/S-ubuntu.
```

---

### 2. Test Backend Health
```bash
curl http://localhost:8000/health
```

**Expected output:**
```json
{"status":"healthy"}
```

---

### 3. Test Synthesis Endpoint
```bash
curl -X POST "http://localhost:8000/v1/synthesize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "नमस्ते",
    "voice_id": "default",
    "language": "hi",
    "speed": 1.0
  }'
```

**Expected:** JSON response with audio_url

---

### 4. Check Frontend
```bash
curl http://localhost:3000
```

**Expected:** HTML content

---

## View Logs

### Backend Logs
```bash
screen -r backend
```

**What to look for:**
- ✅ "Application startup complete"
- ✅ "Uvicorn running on http://0.0.0.0:8000"
- ❌ Any error messages

**Exit:** Press `Ctrl+A` then `D`

---

### Frontend Logs
```bash
screen -r frontend
```

**What to look for:**
- ✅ "Frontend server running on http://localhost:3000"
- ❌ Any error messages

**Exit:** Press `Ctrl+A` then `D`

---

## System Resources

### Check Memory Usage
```bash
free -h
```

**What to look for:**
- Available memory should be > 100MB
- If swap is being used heavily, consider restarting services

---

### Check Disk Space
```bash
df -h
```

**What to look for:**
- Root partition (/) should have > 1GB free
- If low, clean up old files

---

### Check CPU Usage
```bash
top
```

**What to look for:**
- Python processes should be < 50% CPU when idle
- Press `q` to exit

---

## AWS Service Checks

### Test AWS Credentials
```bash
aws sts get-caller-identity
```

**Expected output:**
```json
{
    "UserId": "...",
    "Account": "736722722438",
    "Arn": "..."
}
```

---

### Check S3 Buckets
```bash
aws s3 ls
```

**Expected:** List of your S3 buckets

---

### Check DynamoDB Tables
```bash
aws dynamodb list-tables
```

**Expected:** List of your DynamoDB tables

---

## Common Issues & Solutions

### Issue: Backend not responding

**Check:**
```bash
screen -r backend
```

**Solution:**
```bash
# Restart backend
screen -X -S backend quit
screen -S backend
cd ~/ai-voice-platform
python3 start_server.py
# Ctrl+A D
```

---

### Issue: Frontend not loading

**Check:**
```bash
screen -r frontend
```

**Solution:**
```bash
# Restart frontend
screen -X -S frontend quit
screen -S frontend
cd ~/ai-voice-platform
python3 start_frontend.py
# Ctrl+A D
```

---

### Issue: Synthesis fails

**Check AWS credentials:**
```bash
aws sts get-caller-identity
```

**Check Polly access:**
```bash
aws polly describe-voices --language-code hi
```

**Solution:**
- Verify AWS credentials in ~/.aws/credentials
- Check IAM permissions for Polly, S3, DynamoDB

---

### Issue: Out of memory

**Check memory:**
```bash
free -h
```

**Solution:**
```bash
# Restart services to free memory
screen -X -S backend quit
screen -X -S frontend quit

# Wait 10 seconds
sleep 10

# Start again
screen -S backend
cd ~/ai-voice-platform && python3 start_server.py
# Ctrl+A D

screen -S frontend
cd ~/ai-voice-platform && python3 start_frontend.py
# Ctrl+A D
```

---

### Issue: Slow response times

**Check CPU:**
```bash
top
```

**Solution:**
- This is normal for t3.micro
- Response times of 500-800ms are expected
- Consider upgrading to t3.small if needed

---

## Performance Monitoring

### Track Request Latency

**From your local machine:**
```bash
time curl -X POST "http://YOUR_EC2_IP:8000/v1/synthesize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "नमस्ते",
    "voice_id": "default",
    "language": "hi",
    "speed": 1.0
  }'
```

**Expected:** 0.5-1.0 seconds total time

---

### Monitor Uptime

**Check how long services have been running:**
```bash
uptime
```

---

### Check Network Connectivity

**Test internet connection:**
```bash
ping -c 3 google.com
```

**Test AWS connectivity:**
```bash
ping -c 3 s3.amazonaws.com
```

---

## Automated Monitoring Script

Create a monitoring script:

```bash
cat > ~/monitor.sh << 'EOF'
#!/bin/bash

echo "=== AI Voice Platform Health Check ==="
echo ""

echo "1. Services Status:"
screen -ls | grep -E "backend|frontend"
echo ""

echo "2. Backend Health:"
curl -s http://localhost:8000/health
echo ""
echo ""

echo "3. Memory Usage:"
free -h | grep Mem
echo ""

echo "4. Disk Usage:"
df -h | grep "/$"
echo ""

echo "5. AWS Credentials:"
aws sts get-caller-identity --query Account --output text 2>/dev/null || echo "AWS credentials not configured"
echo ""

echo "=== Health Check Complete ==="
EOF

chmod +x ~/monitor.sh
```

**Run it:**
```bash
~/monitor.sh
```

---

## Set Up Automatic Restart (Optional)

Create a cron job to restart services daily:

```bash
crontab -e
```

Add this line:
```
0 4 * * * screen -X -S backend quit && screen -X -S frontend quit && sleep 10 && screen -dmS backend bash -c 'cd ~/ai-voice-platform && python3 start_server.py' && screen -dmS frontend bash -c 'cd ~/ai-voice-platform && python3 start_frontend.py'
```

This restarts services at 4 AM daily.

---

## Logs Location

### Backend Logs
```bash
# View in screen session
screen -r backend
```

### Frontend Logs
```bash
# View in screen session
screen -r frontend
```

### System Logs
```bash
# View system logs
sudo journalctl -xe
```

---

## Security Checks

### Check Open Ports
```bash
sudo netstat -tulpn | grep LISTEN
```

**Expected:**
- Port 22 (SSH)
- Port 8000 (Backend)
- Port 3000 (Frontend)

---

### Check Failed Login Attempts
```bash
sudo grep "Failed password" /var/log/auth.log | tail -10
```

---

### Update Security Patches
```bash
sudo apt update
sudo apt list --upgradable
```

---

## Backup Important Data

### Backup AWS Credentials
```bash
cp ~/.aws/credentials ~/credentials.backup
cp ~/.aws/config ~/config.backup
```

### Backup Application Code
```bash
cd ~/ai-voice-platform
git status
git log -1
```

---

## Emergency Procedures

### If Everything Fails

1. **Stop all services:**
   ```bash
   screen -X -S backend quit
   screen -X -S frontend quit
   ```

2. **Reboot EC2:**
   ```bash
   sudo reboot
   ```

3. **Reconnect after 2 minutes:**
   ```bash
   ssh -i your-key.pem ubuntu@YOUR_EC2_IP
   ```

4. **Restart services:**
   ```bash
   cd ~/ai-voice-platform
   screen -S backend
   python3 start_server.py
   # Ctrl+A D
   
   screen -S frontend
   python3 start_frontend.py
   # Ctrl+A D
   ```

---

## Contact AWS Support

If you encounter AWS-specific issues:

1. Go to: https://console.aws.amazon.com/support/
2. Create a support case
3. Select: Technical support
4. Describe your issue

---

## Monitoring Checklist

Run this checklist every few hours during hackathon:

- [ ] Services running (`screen -ls`)
- [ ] Backend healthy (`curl http://localhost:8000/health`)
- [ ] Frontend accessible (open in browser)
- [ ] Memory available (`free -h`)
- [ ] Disk space available (`df -h`)
- [ ] No errors in logs (`screen -r backend`, `screen -r frontend`)
- [ ] AWS credentials valid (`aws sts get-caller-identity`)

---

## Quick Reference

```bash
# Check services
screen -ls

# View backend logs
screen -r backend  # Ctrl+A D to exit

# View frontend logs
screen -r frontend  # Ctrl+A D to exit

# Test backend
curl http://localhost:8000/health

# Test frontend
curl http://localhost:3000

# Check memory
free -h

# Check disk
df -h

# Restart backend
screen -X -S backend quit
screen -S backend
cd ~/ai-voice-platform && python3 start_server.py
# Ctrl+A D

# Restart frontend
screen -X -S frontend quit
screen -S frontend
cd ~/ai-voice-platform && python3 start_frontend.py
# Ctrl+A D
```

---

## You're All Set! 🎉

Your deployment is monitored and ready for the hackathon!

Keep this guide handy during the judging period.
