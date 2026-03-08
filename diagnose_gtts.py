#!/usr/bin/env python3
"""Comprehensive gTTS diagnostic script."""
import sys
import io

print("=" * 70)
print("gTTS Diagnostic Script")
print("=" * 70)

# Step 1: Check if gTTS is installed
print("\n[1/5] Checking gTTS installation...")
try:
    import gtts
    print(f"✓ gTTS is installed: version {gtts.__version__}")
except ImportError as e:
    print(f"✗ gTTS is NOT installed: {e}")
    print("\nInstall with: pip install gTTS==2.5.0")
    sys.exit(1)

# Step 2: Check internet connectivity to Google
print("\n[2/5] Checking internet connectivity to Google...")
try:
    import urllib.request
    response = urllib.request.urlopen('https://translate.google.com', timeout=5)
    print(f"✓ Can reach Google Translate: HTTP {response.status}")
except Exception as e:
    print(f"✗ Cannot reach Google Translate: {e}")
    print("\nThis is likely the problem! gTTS needs internet access to Google.")
    sys.exit(1)

# Step 3: Test basic English synthesis
print("\n[3/5] Testing basic English synthesis...")
try:
    from gtts import gTTS
    
    tts = gTTS(text="Hello world", lang="en", lang_check=False)
    buffer = io.BytesIO()
    tts.write_to_fp(buffer)
    buffer.seek(0)
    audio_bytes = buffer.read()
    
    print(f"✓ English synthesis works: {len(audio_bytes)} bytes")
    
    if len(audio_bytes) < 1000:
        print(f"⚠ Warning: Audio is very small ({len(audio_bytes)} bytes)")
    
    # Save test file
    with open('test_english.mp3', 'wb') as f:
        f.write(audio_bytes)
    print("✓ Saved to test_english.mp3")
    
except Exception as e:
    print(f"✗ English synthesis failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 4: Test Indian language synthesis
print("\n[4/5] Testing Indian language synthesis...")

test_cases = [
    ("नमस्ते", "hi", "Hindi"),
    ("வணக்கம்", "ta", "Tamil"),
    ("హలో", "te", "Telugu"),
    ("হ্যালো", "bn", "Bengali"),
]

for text, lang, name in test_cases:
    try:
        tts = gTTS(text=text, lang=lang, lang_check=False)
        buffer = io.BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        audio_bytes = buffer.read()
        
        status = "✓" if len(audio_bytes) > 1000 else "⚠"
        print(f"{status} {name} ({lang}): {len(audio_bytes)} bytes")
        
        # Save test file
        filename = f'test_{lang}.mp3'
        with open(filename, 'wb') as f:
            f.write(audio_bytes)
        
    except Exception as e:
        print(f"✗ {name} ({lang}) failed: {e}")

# Step 5: Test with the actual problematic text
print("\n[5/5] Testing with actual example texts...")

examples = [
    ("வணக்கம் பாரதம்! இது ஒரு AI குரல் தளம்.", "ta", "Tamil full sentence"),
    ("నమస్కారం భారత్! ఇది ఒక AI వాయిస్ ప్లాట్‌ఫారమ్.", "te", "Telugu full sentence"),
    ("নমস্কার ভারত! এটি একটি AI ভয়েস প্ল্যাটফর্ম।", "bn", "Bengali full sentence"),
]

for text, lang, name in examples:
    try:
        print(f"\nTesting: {name}")
        print(f"Text: {text}")
        
        tts = gTTS(text=text, lang=lang, lang_check=False)
        buffer = io.BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        audio_bytes = buffer.read()
        
        print(f"Result: {len(audio_bytes)} bytes")
        
        if len(audio_bytes) < 1000:
            print(f"⚠ WARNING: Audio is suspiciously small!")
        else:
            print(f"✓ Audio looks good")
        
        # Check if it's valid MP3
        if audio_bytes[:3] == b'ID3' or audio_bytes[:2] in [b'\xff\xfb', b'\xff\xf3']:
            print(f"✓ Valid MP3 format detected")
        else:
            print(f"⚠ May not be valid MP3")
        
        # Save test file
        filename = f'test_full_{lang}.mp3'
        with open(filename, 'wb') as f:
            f.write(audio_bytes)
        print(f"✓ Saved to {filename}")
        
    except Exception as e:
        print(f"✗ Failed: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 70)
print("Diagnostic Complete!")
print("=" * 70)
print("\nGenerated test files:")
print("- test_english.mp3")
print("- test_hi.mp3, test_ta.mp3, test_te.mp3, test_bn.mp3")
print("- test_full_ta.mp3, test_full_te.mp3, test_full_bn.mp3")
print("\nYou can download these files and play them locally to verify:")
print("scp -i ai-voice-key.pem ubuntu@34.236.36.88:~/AI_For_Bharat/test_*.mp3 .")
print("\nIf all tests passed but your app still fails, check:")
print("1. Backend logs for detailed error messages")
print("2. Network connectivity from the app (security groups)")
print("3. Virtual environment activation")
