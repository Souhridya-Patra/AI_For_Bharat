# 🚀 START HERE - Deployment Guide

## What You Have Now

✅ **Fully functional AI Voice Platform**
- Backend with AWS Polly integration
- Beautiful web interface
- Real voice synthesis working
- Support for 6+ Indian languages
- All code ready to deploy

---

## What You Need to Do

### 🎯 Goal
Deploy your application to AWS EC2 so judges can access it remotely via a public URL.

### ⏱️ Time Required
**20 minutes total**

---

## Step-by-Step Process

### 1️⃣ Launch EC2 Instance (5 min)

**What:** Create a virtual server on AWS  
**Why:** So your app runs 24/7 and judges can access it  
**How:** Follow **QUICK_DEPLOY.md** Step 1

**Quick version:**
1. Go to AWS Console → EC2 → Launch Instance
2. Choose: t3.micro (FREE)
3. Choose: Ubuntu 22.04
4. Add security rules: Ports 22, 80, 8000, 3000
5. Create/select key pair (save the .pem file!)
6. Launch and note the Public IP

---

### 2️⃣ Push Code to GitHub (2 min)

**What:** Upload your code to GitHub  
**Why:** Easy way to get code onto EC2  
**How:** Run this command

```powershell
.\push_to_github.ps1
```

Follow the prompts to enter your GitHub repo URL.

---

### 3️⃣ Deploy on EC2 (10 min)

**What:** Install and run your app on EC2  
**Why:** Make it accessible via public URL  
**How:** Follow **QUICK_DEPLOY.md** Step 3

**Quick version:**
```bash
# Connect to EC2
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# Install dependencies
sudo apt update && sudo apt install -y python3-pip git libsndfile1

# Clone and setup
git clone YOUR_GITHUB_REPO
cd ai-voice-platform
pip3 install fastapi uvicorn boto3 soundfile python-multipart python-dotenv

# Configure AWS credentials
mkdir -p ~/.aws
nano ~/.aws/credentials  # Add your credentials

# Start services
screen -S backend
python3 start_server.py
# Ctrl+A D

screen -S frontend
python3 start_frontend.py
# Ctrl+A D
```

---

### 4️⃣ Update Frontend URL (2 min)

**What:** Change API URL from localhost to EC2 IP  
**Why:** So frontend can talk to backend  
**How:** Run this command locally

```powershell
python update_frontend_url.py YOUR_EC2_IP
git add frontend/index.html
git commit -m "Update API URL"
git push

# Then on EC2:
git pull
screen -X -S frontend quit
screen -S frontend
python3 start_frontend.py
# Ctrl+A D
```

---

### 5️⃣ Test & Share (1 min)

**What:** Verify everything works  
**Why:** Make sure judges can use it  
**How:** Open in browser

```
http://YOUR_EC2_IP:3000
```

Try synthesizing speech. If it works, you're done! 🎉

---

## Files to Use

### For Deployment:
1. **QUICK_DEPLOY.md** ⭐ - Fastest deployment guide
2. **DEPLOY_TO_EC2_NOW.md** - Detailed deployment guide
3. **DEPLOYMENT_CHECKLIST.md** - Track your progress

### Helper Scripts:
- **push_to_github.ps1** - Push code to GitHub
- **update_frontend_url.py** - Update API URL

### For Judges:
- **FOR_JUDGES.md** - Instructions for judges
- **README_FOR_GITHUB.md** - Use as your GitHub README

---

## Which Guide Should I Follow?

### If you want FAST deployment:
👉 **QUICK_DEPLOY.md** (3 steps, 20 minutes)

### If you want DETAILED instructions:
👉 **DEPLOY_TO_EC2_NOW.md** (step-by-step with explanations)

### If you want a CHECKLIST:
👉 **DEPLOYMENT_CHECKLIST.md** (print and check off)

---

## Common Questions

### Q: Will this cost money?
**A:** No! t3.micro is FREE for 750 hours/month (first 12 months). AWS services cost ~$0.01 for the hackathon.

### Q: How long will deployment take?
**A:** 20 minutes if you follow the quick guide.

### Q: What if something goes wrong?
**A:** Check the troubleshooting section in DEPLOY_TO_EC2_NOW.md or QUICK_DEPLOY.md.

### Q: Do I need to keep my computer on?
**A:** No! Once deployed to EC2, it runs independently.

### Q: Can judges access it anytime?
**A:** Yes! It's available 24/7 at http://YOUR_EC2_IP:3000

---

## After Deployment

### Update these files with your EC2 IP:
1. FOR_JUDGES.md
2. README_FOR_GITHUB.md (if using)

### Share with judges:
```
Live Demo: http://YOUR_EC2_IP:3000
API Docs: http://YOUR_EC2_IP:8000/docs
GitHub: https://github.com/YOUR_USERNAME/ai-voice-platform
```

---

## Troubleshooting

### Can't connect to EC2?
- Check security group allows your IP
- Verify .pem file permissions

### Services not starting?
```bash
screen -r backend  # Check logs
screen -r frontend # Check logs
```

### Frontend can't reach backend?
- Verify you updated the API URL
- Check backend is running: `curl http://localhost:8000/health`

---

## Cost Breakdown

| Service | Cost |
|---------|------|
| EC2 t3.micro | FREE (750 hrs/month) |
| AWS Polly | ~$0.01 |
| S3 Storage | FREE (5GB) |
| DynamoDB | FREE (25GB) |
| **Total** | **~$0-2** |

---

## Timeline

| Task | Time |
|------|------|
| Launch EC2 | 5 min |
| Push to GitHub | 2 min |
| Deploy on EC2 | 10 min |
| Update URLs | 2 min |
| Test | 1 min |
| **Total** | **20 min** |

---

## Ready to Start?

### Option 1: Quick Deploy (Recommended)
```powershell
# Open QUICK_DEPLOY.md and follow the 3 steps
```

### Option 2: Detailed Deploy
```powershell
# Open DEPLOY_TO_EC2_NOW.md for step-by-step guide
```

### Option 3: Checklist Approach
```powershell
# Open DEPLOYMENT_CHECKLIST.md and check off items
```

---

## Need Help?

1. Check troubleshooting sections in guides
2. Review error messages carefully
3. Check AWS Console for instance status
4. Verify security group settings

---

## After Hackathon

**IMPORTANT:** Stop your EC2 instance to avoid charges!

```
AWS Console → EC2 → Select instance → Instance State → Stop
```

---

## You're Ready! 🚀

Your application is fully built and tested. Just 20 minutes of deployment work and judges can access it!

**Start with:** QUICK_DEPLOY.md

Good luck with your hackathon! 🎉

---

**Team SAAN | Leader: Souhridya Patra**  
AWS AI for Bharat Hackathon 2026
