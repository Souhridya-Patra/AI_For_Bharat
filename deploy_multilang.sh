#!/bin/bash
# Deploy multi-language support to EC2

echo "============================================================"
echo "Deploying Multi-Language Support"
echo "============================================================"
echo ""

# Pull latest code
echo "Pulling latest code..."
git pull
echo ""

# Install gTTS
echo "Installing gTTS..."
source venv/bin/activate
pip install gTTS==2.5.0
echo ""

# Kill all services
echo "Stopping services..."
sudo pkill -9 python3
screen -wipe
echo ""

# Start backend
echo "Starting backend..."
screen -dmS backend bash -c 'cd ~/AI_For_Bharat && source venv/bin/activate && python3 start_server.py'
sleep 3
echo "✓ Backend started"
echo ""

# Start frontend
echo "Starting frontend..."
screen -dmS frontend bash -c 'cd ~/AI_For_Bharat && source venv/bin/activate && python3 start_frontend.py'
sleep 2
echo "✓ Frontend started"
echo ""

# Verify
echo "Verifying services..."
screen -ls
echo ""

echo "============================================================"
echo "✓ Deployment Complete!"
echo "============================================================"
echo ""
echo "Your platform now supports 10 Indian languages!"
echo ""
echo "Test it at: http://YOUR_EC2_IP:3000"
echo ""
echo "Supported languages:"
echo "  - Hindi (AWS Polly)"
echo "  - English (AWS Polly)"
echo "  - Tamil (Google TTS)"
echo "  - Telugu (Google TTS)"
echo "  - Bengali (Google TTS)"
echo "  - Marathi (Google TTS)"
echo "  - Kannada (Google TTS)"
echo "  - Malayalam (Google TTS)"
echo "  - Gujarati (Google TTS)"
echo ""
