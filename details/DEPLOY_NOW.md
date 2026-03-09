# 🚀 Deploy NOW - Quick Guide

## Choose Your Deployment Method

### ⚡ FASTEST: Ngrok (5 minutes)
**Best for:** Quick testing, no AWS setup needed

1. Download ngrok: https://ngrok.com/download
2. Run backend: `python start_server.py`
3. In new terminal: `ngrok http 8000`
4. Copy the https URL
5. Update `demo.html` line 287: Change API_URL to your ngrok URL
6. Open `demo.html` in browser
7. Share the ngrok URL with judges!

**Pros:** Super fast, no AWS needed
**Cons:** URL changes each time, requires your PC running

---

### 🏆 BEST: AWS EC2 (30 minutes)
**Best for:** Professional deployment, permanent URL

#### Quick Steps:

1. **Launch EC2:**
   - Go to AWS Console → EC2
   - Launch Ubuntu t2.medium instance
   - Security groups: Allow ports 22, 80, 8000, 3000
   - Download key pair

2. **Connect:**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Run deployment script:**
   ```bash
   # Upload deploy_to_ec2.sh to EC2
   chmod +x deploy_to_ec2.sh
   ./deploy_to_ec2.sh
   ```

4. **Access:**
   - Frontend: `http://your-ec2-ip:3000`
   - API: `http://your-ec2-ip:8000/docs`

**Pros:** Professional, permanent, shows AWS skills
**Cons:** Takes 30 minutes, costs ~$0.05/hour

---

### 💻 ALTERNATIVE: Keep Running Locally

If judges will access during specific time:

1. Start backend: `python start_server.py`
2. Start frontend: `python start_frontend.py`
3. Use ngrok to expose: `ngrok http 3000`
4. Share ngrok URL
5. **Keep your PC running during judging!**

---

## What Judges Need

### Provide in Submission:

1. **Live Demo URL** - Where they can test
2. **API Docs URL** - Interactive documentation
3. **GitHub URL** - Source code
4. **Video** - 3-minute demo
5. **Instructions** - FOR_JUDGES.md

### Example Submission:

```
Demo URL: http://54.123.45.67:3000
API Docs: http://54.123.45.67:8000/docs
GitHub: https://github.com/yourusername/ai-voice-platform
Video: https://youtube.com/watch?v=xxxxx
```

---

## Testing Before Submission

1. Open your deployed URL
2. Click "Synthesize Speech"
3. Verify audio plays
4. Test all language examples
5. Check API docs work
6. Share URL with friend to test

---

## Emergency: If Deployment Fails

**Option 1:** Record a comprehensive video showing everything working

**Option 2:** Provide detailed setup instructions in README

**Option 3:** Offer to do live demo via video call

---

## Recommended: EC2 + Video

**Best approach:**
1. Deploy to EC2 (permanent URL)
2. Record video showing it working
3. Provide both in submission

This way judges can:
- Test themselves (EC2 URL)
- Watch video if URL has issues
- See your code (GitHub)

---

## Next Steps

1. Choose deployment method (EC2 recommended)
2. Deploy following steps above
3. Test the deployed URL
4. Update FOR_JUDGES.md with your URL
5. Record video
6. Submit!

---

**Time needed:**
- Ngrok: 5 minutes
- EC2: 30 minutes
- Video: 30 minutes
- **Total: 1 hour to fully deployed + video**

You're almost there! 🚀
