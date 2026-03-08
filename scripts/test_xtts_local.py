"""Quick test script for XTTS-v2 local synthesis.

This script tests XTTS-v2 voice synthesis locally to verify installation.
"""
import sys
import os

def test_xtts_local():
    """Test XTTS-v2 synthesis locally."""
    print("=" * 60)
    print("XTTS-v2 Local Synthesis Test")
    print("=" * 60)
    print()
    
    # Test 1: Check TTS library
    print("📦 Checking TTS library installation...")
    try:
        from TTS.api import TTS
        print("✅ TTS library installed")
    except ImportError:
        print("❌ TTS library not found")
        print("Install with: pip install TTS==0.22.0")
        return False
    
    # Test 2: Initialize XTTS model
    print("\n📥 Loading XTTS-v2 model (first run downloads ~1.8GB)...")
    try:
        model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        print("✅ XTTS-v2 model loaded")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return False
    
    # Test 3: English synthesis
    print("\n🎵 Testing English synthesis...")
    try:
        output_file = "test_english.wav"
        model.tts_to_file(
            text="Hello! This is XTTS-v2 ultra-realistic voice synthesis.",
            language="en",
            file_path=output_file
        )
        
        file_size = os.path.getsize(output_file)
        print(f"✅ English synthesis successful: {output_file} ({file_size} bytes)")
    except Exception as e:
        print(f"❌ English synthesis failed: {e}")
        return False
    
    # Test 4: Hindi synthesis
    print("\n🎵 Testing Hindi synthesis...")
    try:
        output_file = "test_hindi.wav"
        model.tts_to_file(
            text="नमस्ते भारत! यह XTTS-v2 का परीक्षण है।",
            language="hi",
            file_path=output_file
        )
        
        file_size = os.path.getsize(output_file)
        print(f"✅ Hindi synthesis successful: {output_file} ({file_size} bytes)")
    except Exception as e:
        print(f"❌ Hindi synthesis failed: {e}")
        return False
    
    # Test 5: Integration test
    print("\n🔗 Testing platform integration...")
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
        
        from app.services.xtts_synthesis import XTTSSynthesisEngine
        
        engine = XTTSSynthesisEngine(use_sagemaker=False)
        
        audio_bytes = engine.synthesize(
            text="Integration test successful!",
            voice_id="default",
            language="en"
        )
        
        print(f"✅ Integration test passed: {len(audio_bytes)} bytes")
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Success!
    print()
    print("=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print()
    print("XTTS-v2 is ready to use!")
    print()
    print("To enable XTTS in your platform:")
    print("1. Update .env: USE_XTTS=True")
    print("2. Restart server: python start_server.py")
    print("3. Test endpoint: http://localhost:8000/v1/synthesize")
    print()
    print("Generated test files:")
    print("  - test_english.wav")
    print("  - test_hindi.wav")
    print()
    
    return True


if __name__ == "__main__":
    success = test_xtts_local()
    sys.exit(0 if success else 1)
