#!/bin/bash
# Script to test the full integration

echo "============================================================"
echo "Testing Full Integration"
echo "============================================================"

echo -e "\n[1/3] Testing synthesis endpoint with Tamil..."
curl -X POST http://localhost:8000/v1/synthesize \
  -H "Content-Type: application/json" \
  -d '{
    "text": "வணக்கம்",
    "voice_id": "default",
    "language": "ta",
    "speed": 1.0,
    "pitch": 0,
    "stream": false
  }' | jq '.'

echo -e "\n[2/3] Checking backend logs for gTTS activity..."
tail -30 backend.log | grep -E "\[GTTS\]|gTTS|Tamil|Telugu"

echo -e "\n[3/3] Checking if backend is using correct synthesis engine..."
tail -50 backend.log | grep -E "Using|Selected|engine"

echo -e "\n============================================================"
echo "Integration test complete"
echo "============================================================"
