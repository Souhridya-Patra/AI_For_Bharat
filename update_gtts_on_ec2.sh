#!/bin/bash
# Script to update gTTS implementation on EC2

echo "============================================================"
echo "Updating gTTS Implementation on EC2"
echo "============================================================"

# Upload updated files
echo "Uploading updated gTTS synthesis module..."
scp -i ai-voice-key.pem backend/app/services/gtts_synthesis.py ubuntu@34.236.36.88:~/AI_For_Bharat/backend/app/services/

echo "Uploading diagnostic scripts..."
scp -i ai-voice-key.pem diagnose_gtts.py ubuntu@34.236.36.88:~/AI_For_Bharat/
scp -i ai-voice-key.pem test_gtts_direct.py ubuntu@34.236.36.88:~/AI_For_Bharat/
scp -i ai-voice-key.pem DEBUG_GTTS_ISSUE.md ubuntu@34.236.36.88:~/AI_For_Bharat/

echo ""
echo "✓ Files uploaded successfully!"
echo ""
echo "Next steps:"
echo "1. SSH into EC2: ssh -i ai-voice-key.pem ubuntu@34.236.36.88"
echo "2. Activate venv: source venv/bin/activate"
echo "3. Run diagnostic: python3 diagnose_gtts.py"
echo "4. Restart backend: sudo systemctl restart ai-voice-backend"
echo ""
echo "Or run all at once:"
echo "ssh -i ai-voice-key.pem ubuntu@34.236.36.88 'cd AI_For_Bharat && source venv/bin/activate && python3 diagnose_gtts.py'"
