"""Test all API endpoints to verify everything works."""
import requests
import json
import time
import sys

API_BASE = "http://localhost:8000"

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def print_success(text):
    """Print success message."""
    print(f"✓ {text}")

def print_error(text):
    """Print error message."""
    print(f"✗ {text}")

def test_health():
    """Test health endpoint."""
    print_header("1. Testing Health Endpoint")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            print_success(f"Health check passed: {response.json()}")
            return True
        else:
            print_error(f"Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Cannot connect to server: {e}")
        return False

def test_root():
    """Test root endpoint."""
    print_header("2. Testing Root Endpoint")
    try:
        response = requests.get(f"{API_BASE}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"API: {data['message']}")
            print_success(f"Version: {data['version']}")
            print_success(f"Status: {data['status']}")
            return True
        else:
            print_error(f"Root endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_synthesis():
    """Test synthesis endpoint."""
    print_header("3. Testing Synthesis Endpoint")
    
    test_cases = [
        ("English", "Hello Bharat! This is a test of the AI voice platform.", "en"),
        ("Hindi", "नमस्ते भारत! यह एक परीक्षण है।", "hi"),
        ("Tamil", "வணக்கம் பாரதம்!", "ta"),
    ]
    
    results = []
    for lang, text, lang_code in test_cases:
        print(f"\nTesting {lang}...")
        print(f"Text: {text}")
        
        payload = {
            "text": text,
            "voice_id": "default",
            "speed": 1.0,
            "pitch": 0,
            "stream": False,
            "language": lang_code
        }
        
        start_time = time.time()
        try:
            response = requests.post(
                f"{API_BASE}/v1/synthesize",
                json=payload,
                timeout=30
            )
            latency = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Synthesis successful")
                print(f"  - Latency: {latency:.2f}ms")
                print(f"  - Duration: {data['duration']:.2f}s")
                print(f"  - Sample Rate: {data['sample_rate']}Hz")
                print(f"  - Request ID: {data['request_id']}")
                
                if latency < 500:
                    print(f"  🎯 Target achieved! (<500ms)")
                
                results.append(True)
            else:
                print_error(f"Synthesis failed: {response.status_code}")
                print(f"  Error: {response.text}")
                results.append(False)
        
        except Exception as e:
            print_error(f"Error: {e}")
            results.append(False)
        
        time.sleep(0.5)  # Brief pause between requests
    
    return all(results)

def test_voices_list():
    """Test voice listing endpoint."""
    print_header("4. Testing Voice List Endpoint")
    try:
        response = requests.get(f"{API_BASE}/v1/voices", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Voice list retrieved")
            print(f"  - Total voices: {data['total']}")
            if data['voices']:
                print(f"  - Voices:")
                for voice in data['voices'][:3]:
                    print(f"    • {voice['name']} (ID: {voice['id']})")
            return True
        else:
            print_error(f"Voice list failed: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def test_streaming():
    """Test streaming synthesis."""
    print_header("5. Testing Streaming Synthesis")
    
    payload = {
        "text": "This is a test of streaming synthesis. It should return audio in chunks. Each sentence is processed separately.",
        "voice_id": "default",
        "speed": 1.0,
        "pitch": 0,
        "stream": True
    }
    
    try:
        print("Requesting streaming synthesis...")
        response = requests.post(
            f"{API_BASE}/v1/synthesize",
            json=payload,
            stream=True,
            timeout=30
        )
        
        if response.status_code == 200:
            chunks = 0
            total_bytes = 0
            
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    chunks += 1
                    total_bytes += len(chunk)
            
            print_success(f"Streaming synthesis successful")
            print(f"  - Chunks received: {chunks}")
            print(f"  - Total bytes: {total_bytes:,}")
            return True
        else:
            print_error(f"Streaming failed: {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("AI VOICE PLATFORM - ENDPOINT TESTING")
    print("=" * 60)
    print("\nTesting all API endpoints...")
    
    # Check if server is running
    print("\nChecking if server is running...")
    try:
        requests.get(f"{API_BASE}/health", timeout=2)
        print_success("Server is running")
    except:
        print_error("Server is not running!")
        print("\nPlease start the server first:")
        print("  python start_server.py")
        sys.exit(1)
    
    # Run tests
    results = {
        "Health Check": test_health(),
        "Root Endpoint": test_root(),
        "Synthesis": test_synthesis(),
        "Voice List": test_voices_list(),
        "Streaming": test_streaming()
    }
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    print(f"\nTests Passed: {passed}/{total}\n")
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")
    
    if passed == total:
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("\nYour AI Voice Platform is working correctly!")
        print("\nNext steps:")
        print("  1. Run: python scripts/demo_hello_bharat.py")
        print("  2. Visit: http://localhost:8000/docs")
        print("  3. Build the frontend or deploy to production")
        print("=" * 60)
        sys.exit(0)
    else:
        print("\n" + "=" * 60)
        print("⚠️  SOME TESTS FAILED")
        print("=" * 60)
        print("\nPlease check the errors above and:")
        print("  1. Verify AWS credentials are configured")
        print("  2. Check that S3 buckets exist")
        print("  3. Review server logs for errors")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTests cancelled by user.")
        sys.exit(1)
