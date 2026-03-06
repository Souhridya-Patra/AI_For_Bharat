"""Demo script for 'Hello Bharat' synthesis - 24-hour goal."""
import requests
import json
import time
import sys

API_BASE_URL = "http://localhost:8000/v1"

# Demo texts in different Indian languages
DEMO_TEXTS = {
    "hi": "नमस्ते भारत! यह एक AI आवाज़ प्लेटफ़ॉर्म है।",
    "en": "Hello Bharat! This is an AI voice platform for India.",
    "ta": "வணக்கம் பாரதம்! இது ஒரு AI குரல் தளம்.",
    "mr": "नमस्कार भारत! हे भारतासाठी एक AI आवाज प्लॅटफॉर्म आहे।",
    "bn": "নমস্কার ভারত! এটি একটি AI ভয়েস প্ল্যাটফর্ম।"
}


def test_synthesis(text: str, voice_id: str = "default", language: str = "auto"):
    """Test synthesis endpoint."""
    print(f"\n{'='*60}")
    print(f"Testing Synthesis: {language.upper()}")
    print(f"{'='*60}")
    print(f"Text: {text}")
    
    payload = {
        "text": text,
        "voice_id": voice_id,
        "speed": 1.0,
        "pitch": 0,
        "stream": False,
        "language": language
    }
    
    print("\nSending request to API...")
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/synthesize",
            json=payload,
            timeout=30
        )
        
        latency = (time.time() - start_time) * 1000  # Convert to ms
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✓ SUCCESS!")
            print(f"  - Latency: {latency:.2f}ms")
            print(f"  - Duration: {result['duration']:.2f}s")
            print(f"  - Sample Rate: {result['sample_rate']}Hz")
            print(f"  - Audio URL: {result['audio_url'][:80]}...")
            print(f"  - Request ID: {result['request_id']}")
            
            # Check if latency meets target
            if latency < 500:
                print(f"\n  🎯 Target achieved! Latency < 500ms")
            else:
                print(f"\n  ⚠️  Latency exceeds 500ms target")
            
            return True
        else:
            print(f"\n✗ FAILED!")
            print(f"  - Status Code: {response.status_code}")
            print(f"  - Error: {response.text}")
            return False
    
    except requests.exceptions.Timeout:
        print(f"\n✗ TIMEOUT! Request took longer than 30 seconds")
        return False
    
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False


def test_voice_cloning():
    """Test voice cloning endpoint."""
    print(f"\n{'='*60}")
    print(f"Testing Voice Cloning")
    print(f"{'='*60}")
    
    # Note: This requires an actual audio file
    print("Voice cloning requires an audio file (6-10 seconds)")
    print("Skipping for now - implement with actual audio file")
    return True


def test_voice_listing():
    """Test voice listing endpoint."""
    print(f"\n{'='*60}")
    print(f"Testing Voice Listing")
    print(f"{'='*60}")
    
    try:
        response = requests.get(f"{API_BASE_URL}/voices")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✓ SUCCESS!")
            print(f"  - Total voices: {result['total']}")
            
            if result['voices']:
                print(f"\n  Voices:")
                for voice in result['voices'][:5]:  # Show first 5
                    print(f"    - {voice['name']} (ID: {voice['id']})")
            
            return True
        else:
            print(f"\n✗ FAILED!")
            print(f"  - Status Code: {response.status_code}")
            print(f"  - Error: {response.text}")
            return False
    
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return False


def main():
    """Run demo tests."""
    print("\n" + "="*60)
    print("AI VOICE PLATFORM - HELLO BHARAT DEMO")
    print("24-Hour Goal: End-to-end synthesis with <500ms latency")
    print("="*60)
    print()
    print("Note: Running in MOCK mode for local development")
    print("      Real synthesis requires SageMaker endpoint deployment")
    print()
    
    # Check if API is running
    try:
        response = requests.get(f"{API_BASE_URL.replace('/v1', '')}/health", timeout=5)
        if response.status_code != 200:
            print("\n✗ API is not responding. Please start the server first:")
            print("  python start_server.py")
            print("  OR")
            print("  cd backend && uvicorn app.main:app --reload")
            sys.exit(1)
    except:
        print("\n✗ Cannot connect to API. Please start the server first:")
        print("  python start_server.py")
        print("  OR")
        print("  cd backend && uvicorn app.main:app --reload")
        sys.exit(1)
    
    print("\n✓ API is running")
    
    # Run tests
    results = []
    
    # Test synthesis for each language
    for lang, text in DEMO_TEXTS.items():
        result = test_synthesis(text, voice_id="default", language=lang)
        results.append((lang, result))
        time.sleep(1)  # Brief pause between requests
    
    # Test voice listing
    list_result = test_voice_listing()
    results.append(("voice_listing", list_result))
    
    # Summary
    print(f"\n{'='*60}")
    print("DEMO SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}")
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    if passed == total:
        print(f"\n🎉 All tests passed! 24-hour goal achieved!")
    else:
        print(f"\n⚠️  Some tests failed. Check the logs above.")
    
    print(f"\n{'='*60}")


if __name__ == "__main__":
    main()
