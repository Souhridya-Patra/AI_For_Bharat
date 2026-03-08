#!/usr/bin/env python3
"""Test the full synthesis flow to identify where the issue is."""
import sys
import requests
import json

print("=" * 70)
print("Full Flow Integration Test")
print("=" * 70)

# Test cases
test_cases = [
    {
        "name": "Hindi (Polly)",
        "text": "नमस्ते भारत",
        "language": "hi",
        "expected_engine": "polly"
    },
    {
        "name": "English (Polly)",
        "text": "Hello Bharat",
        "language": "en-IN",
        "expected_engine": "polly"
    },
    {
        "name": "Tamil (gTTS)",
        "text": "வணக்கம்",
        "language": "ta",
        "expected_engine": "gtts"
    },
    {
        "name": "Telugu (gTTS)",
        "text": "నమస్కారం",
        "language": "te",
        "expected_engine": "gtts"
    },
    {
        "name": "Bengali (gTTS)",
        "text": "নমস্কার",
        "language": "bn",
        "expected_engine": "gtts"
    },
]

API_URL = "http://localhost:8000/v1/synthesize"

for i, test in enumerate(test_cases, 1):
    print(f"\n[{i}/{len(test_cases)}] Testing: {test['name']}")
    print(f"Text: {test['text']}")
    print(f"Language: {test['language']}")
    print(f"Expected engine: {test['expected_engine']}")
    
    payload = {
        "text": test['text'],
        "voice_id": "default",
        "language": test['language'],
        "speed": 1.0,
        "pitch": 0,
        "stream": False
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Success!")
            print(f"  Audio URL: {result.get('audio_url', 'N/A')}")
            print(f"  Duration: {result.get('duration', 0):.2f}s")
            print(f"  Sample Rate: {result.get('sample_rate', 0)}Hz")
            
            # Check if duration is suspiciously short
            if result.get('duration', 0) < 0.5:
                print(f"  ⚠ WARNING: Duration is very short!")
            
        else:
            print(f"✗ Failed with status {response.status_code}")
            try:
                error = response.json()
                print(f"  Error: {json.dumps(error, indent=2)}")
            except:
                print(f"  Response: {response.text[:200]}")
    
    except requests.exceptions.Timeout:
        print(f"✗ Request timed out after 30 seconds")
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to backend")
        print(f"  Make sure backend is running: python3 start_server.py")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")

print("\n" + "=" * 70)
print("Test Complete")
print("=" * 70)
print("\nIf tests failed, check:")
print("1. Backend logs: tail -50 backend.log")
print("2. Backend is running: curl http://localhost:8000/health")
print("3. Virtual environment: source venv/bin/activate")
print("\nIf tests passed but frontend fails, check:")
print("1. Frontend is using correct API URL")
print("2. CORS is configured correctly")
print("3. S3 URLs are accessible")
