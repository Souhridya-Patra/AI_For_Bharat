#!/bin/bash
# Script to restart backend and verify it's working

echo "============================================================"
echo "Restarting Backend Service"
echo "============================================================"

# Check if backend is running as systemd service
if systemctl is-active --quiet ai-voice-backend; then
    echo "Stopping systemd service..."
    sudo systemctl stop ai-voice-backend
    sleep 2
    echo "Starting systemd service..."
    sudo systemctl start ai-voice-backend
    sleep 3
    echo "✓ Service restarted"
    sudo systemctl status ai-voice-backend --no-pager
else
    echo "Backend not running as systemd service"
    echo "Checking for running Python processes..."
    
    # Kill any existing backend processes
    pkill -f "uvicorn.*main:app" || echo "No existing processes found"
    sleep 2
    
    # Start backend in background
    echo "Starting backend..."
    cd ~/AI_For_Bharat
    source venv/bin/activate
    nohup python3 start_server.py > backend.log 2>&1 &
    sleep 3
    echo "✓ Backend started"
fi

echo ""
echo "Checking backend health..."
curl -s http://localhost:8000/health | jq '.'

echo ""
echo "Checking backend logs for startup messages..."
tail -20 backend.log

echo ""
echo "============================================================"
echo "Backend restart complete"
echo "============================================================"
echo ""
echo "Test from frontend: http://34.236.36.88:3000"
echo "Or test with curl:"
echo 'curl -X POST http://localhost:8000/v1/synthesize -H "Content-Type: application/json" -d '"'"'{"text":"வணக்கம்","voice_id":"default","language":"ta","speed":1.0,"pitch":0,"stream":false}'"'"''
