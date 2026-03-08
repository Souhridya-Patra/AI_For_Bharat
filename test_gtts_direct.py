"""Direct test of gTTS to diagnose the audio generation issue."""
import io
from gtts import gTTS

# Test cases
test_cases = [
    ("Hello, this is a test", "en"),
    ("வணக்கம், இது ஒரு சோதனை", "ta"),  # Tamil
    ("హలో, ఇది ఒక పరీక్ష", "te"),  # Telugu
    ("হ্যালো, এটি একটি পরীক্ষা", "bn"),  # Bengali
    ("नमस्ते, यह एक परीक्षण है", "hi"),  # Hindi
]

print("Testing gTTS directly...")
print("=" * 60)

for text, lang in test_cases:
    print(f"\nTest: {lang}")
    print(f"Text: {text}")
    
    try:
        # Create gTTS object
        tts = gTTS(text=text, lang=lang, lang_check=False)
        
        # Save to buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Read bytes
        audio_bytes = audio_buffer.read()
        
        print(f"✓ Success: Generated {len(audio_bytes)} bytes")
        
        # Check if it's valid MP3
        if audio_bytes[:3] == b'ID3' or audio_bytes[:2] in [b'\xff\xfb', b'\xff\xf3', b'\xff\xf2']:
            print(f"✓ Valid MP3 format detected")
        else:
            print(f"⚠ Warning: May not be valid MP3 (first bytes: {audio_bytes[:10].hex()})")
        
        # Save to file for manual testing
        filename = f"test_{lang}.mp3"
        with open(filename, 'wb') as f:
            f.write(audio_bytes)
        print(f"✓ Saved to {filename}")
        
    except Exception as e:
        print(f"✗ Error: {e}")

print("\n" + "=" * 60)
print("Test complete. Check the generated MP3 files.")
