# ✅ Deployment Checklist

## Pre-Deployment

- [ ] Application works locally
- [ ] AWS credentials configured
- [ ] GitHub account ready
- [ ] .pem key file saved securely

---

## EC2 Setup

- [ ] Launched t3.micro instance
- [ ] Ubuntu 22.04 LTS selected
- [ ] Security group configured (22, 80, 8000, 3000)
- [ ] Key pair created/selected
- [ ] Instance is "Running"
- [ ] Public IP noted: ________________

---

## Code Upload

- [ ] Pushed code to GitHub
- [ ] Repository URL: ________________
- [ ] Can access repo in browser

---

## EC2 Configuration

- [ ] Connected via SSH
- [ ] System updated (`sudo apt update`)
- [ ] Python 3 installed (pre-installed on Ubuntu 22.04)
- [ ] pip3 installed
- [ ] git installed
- [ ] libsndfile1 installed
- [ ] Repository cloned
- [ ] Python dependencies installed
- [ ] AWS credentials configured in ~/.aws/
- [ ] Credentials tested (`aws sts get-caller-identity`)

---

## Frontend Update

- [ ] Ran `update_frontend_url.py` locally
- [ ] Committed changes
- [ ] Pushed to GitHub
- [ ] Pulled changes on EC2

---

## Service Startup

- [ ] screen installed
- [ ] Backend started in screen session
- [ ] Backend detached (Ctrl+A D)
- [ ] Frontend started in screen session
- [ ] Frontend detached (Ctrl+A D)
- [ ] Both services running (`screen -ls`)

---

## Testing

- [ ] Health check works: `curl http://localhost:8000/health`
- [ ] Frontend loads: `http://YOUR_EC2_IP:3000`
- [ ] Can enter text
- [ ] Can select language
- [ ] Synthesis works
- [ ] Audio plays
- [ ] API docs accessible: `http://YOUR_EC2_IP:8000/docs`

---

## Documentation Update

- [ ] Updated FOR_JUDGES.md with EC2 IP
- [ ] Updated SUBMISSION_README.md with EC2 IP
- [ ] Committed and pushed changes
- [ ] Verified URLs work

---

## Submission Preparation

- [ ] Live demo URL ready
- [ ] API documentation URL ready
- [ ] GitHub repository public
- [ ] README.md complete
- [ ] Video script ready (VIDEO_SCRIPT.md)
- [ ] Presentation outline ready (PRESENTATION_OUTLINE.md)
- [ ] Blog post planned

---

## Final Checks

- [ ] Demo URL works from different device
- [ ] All languages work
- [ ] Speed control works
- [ ] Example buttons work
- [ ] Audio quality good
- [ ] Latency acceptable (<1 second)
- [ ] No errors in console

---

## Submission

- [ ] Prototype URL submitted
- [ ] GitHub repository URL submitted
- [ ] Video pitch recorded and uploaded
- [ ] Blog post written
- [ ] Presentation created
- [ ] All materials submitted

---

## Post-Submission

- [ ] EC2 instance still running for judging period
- [ ] Monitoring for any issues
- [ ] Ready to demo if needed

---

## After Hackathon

- [ ] EC2 instance STOPPED (to avoid charges)
- [ ] Backup important data
- [ ] Document learnings

---

## Emergency Contacts

**AWS Support:** https://console.aws.amazon.com/support/
**GitHub Support:** https://support.github.com/

---

## Quick Commands

### Check services:
```bash
screen -ls
```

### View logs:
```bash
screen -r backend  # Ctrl+A D to exit
screen -r frontend # Ctrl+A D to exit
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

### Test API:
```bash
curl http://localhost:8000/health
```

---

## Notes

**EC2 Public IP:** ________________

**GitHub Repo:** ________________

**Demo URL:** http://________________:3000

**API Docs:** http://________________:8000/docs

**Submission Date:** ________________

**Hackathon End Date:** ________________

---

## Status

**Current Phase:** ________________

**Last Updated:** ________________

**Issues:** ________________

---

Print this checklist and check off items as you complete them! ✅
