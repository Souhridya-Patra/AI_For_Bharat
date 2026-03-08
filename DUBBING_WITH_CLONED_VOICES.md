# 🎬 Dubbing with Cloned Voices Guide

## Overview
Now that you've cloned a voice, you can use it to **dub content** - converting any text to speech using your cloned voice!

## Quick Start

### Step 1: Verify Your Cloned Voice
1. Open frontend: `http://34.236.36.88:8000`
2. Go to **"🎭 Clone Voice"** tab
3. Check "Your Cloned Voices" section
4. You should see your voice with an ID like: `voice_abc123def456`

### Step 2: Go to Synthesis Tab
1. Click **"🎵 Text-to-Speech"** tab
2. Select your cloned voice from **"Voice Source"** dropdown
3. (If not visible, reload page - voices are saved in browser)

### Step 3: Input Your Text
1. Enter text you want to dub
2. Select language (Hindi, English, Tamil, etc.)
3. Adjust speech speed if needed (0.5x to 2.0x)

### Step 4: Synthesize
1. Click **"🎵 Synthesize Speech"**
2. Wait 2-5 seconds for synthesis
3. Audio plays automatically
4. Download or use the generated audio file

## Video Dubbing Workflow

### For Movie/Video Dubbing:

**Step 1: Extract Dialogue**
- Transcript all dialogue from your video
- Note timing for each line

**Step 2: Dub Each Line**
1. Copy one line of dialogue
2. Paste into text field
3. Select your cloned voice
4. Synthesize
5. Save audio file: `line_001.wav`

**Step 3: Adjust Timing**
- Use speech speed slider to match video timing
- Slower: 0.5x - 1.0x
- Faster: 1.2x - 2.0x

**Step 4: Assemble in Video Editor**
- Import all audio files into your video editor (DaVinci, Premiere, etc.)
- Sync with video footage
- Mix levels and add effects

## Examples

### Example 1: Hindi Movie Dubbing
```
Script:
"नमस्ते! मैं आपकी मदद के लिए यहाँ हूँ।"

Steps:
1. Synthesis tab → Select cloned voice "Actor Voice"
2. Paste text above
3. Language: Hindi
4. Speed: 1.0x (normal)
5. Click Synthesize
6. Download: actor_line_001.wav
```

### Example 2: English Documentary Narrator Dubbing
```
Script:
"Welcome to the ancient temples of India. These sacred structures have stood for thousands of years."

Steps:
1. Synthesis tab → Select cloned voice "Documentary Narrator"
2. Paste text above
3. Language: English
4. Speed: 0.9x (slower, more dramatic)
5. Click Synthesize
6. Download: narrator_002.wav
```

### Example 3: Character Dialogue Dubbing
```
Script:
Multiple characters:
- Character A: "Are you ready?"
- Character B: "Yes, let's go!"

Steps:
Option A: Clone separate voices for each character
- Clone voice for "Character A"
- Clone voice for "Character B"
- Synthesize each line with corresponding voice

Option B: Manually adjust pitch in video editor
- Use same voice, adjust pitch/EQ per character
```

## API Method (Advanced)

### Direct API Call for Dubbing

```bash
# Synthesize with cloned voice via API
curl -X POST http://34.236.36.88:8000/v1/synthesize \
  -H "Content-Type: application/json" \
  -d {
    "text": "Your dialogue text here",
    "voice_id": "voice_abc123def456",
    "language": "hi",
    "speed": 1.0,
    "pitch": 0,
    "stream": false,
    "post_process": true
  }
```

### Batch Dubbing Script (Python)

```python
import requests
import json

# Your cloned voice ID
VOICE_ID = "voice_abc123def456"
API_URL = "http://34.236.36.88:8000/v1/synthesize"

# Dialogue lines to dub
dialogue = [
    {"text": "नमस्ते भारत!", "language": "hi", "speed": 1.0},
    {"text": "यह एक AI प्लेटफॉर्म है।", "language": "hi", "speed": 1.0},
    {"text": "आप अपनी आवाज़ क्लोन कर सकते हैं।", "language": "hi", "speed": 0.9}
]

# Synthesize each line
for i, line in enumerate(dialogue):
    response = requests.post(API_URL, json={
        "text": line["text"],
        "voice_id": VOICE_ID,
        "language": line["language"],
        "speed": line["speed"],
        "pitch": 0,
        "stream": False,
        "post_process": True
    })
    
    if response.status_code == 200:
        result = response.json()
        # Save audio
        audio_url = result['audio_url']
        print(f"✅ Line {i+1} synthesized: {audio_url}")
    else:
        print(f"❌ Error: {response.text}")
```

## Quality Tips for Dubbing

### Audio Quality
- Clone with clear, professional-quality audio
- Minimal background noise
- Single speaker
- 6-10 seconds of natural speech

### Text Preparation
- Break long sentences into shorter phrases
- Use proper punctuation for correct pacing
- Mark emotional content (happy, sad, angry)
- Note speech speed variations

### Performance Tips
- Batch multiple syntheses for faster processing
- Use lower speeds (0.8x-1.0x) for clarity
- Use higher speeds (1.2x-1.5x) only for specific effect
- Test with one line before full batch

### Synchronization
- Use video editor timeline to align dubbed audio
- Watch with original for timing reference
- Adjust speed slider +/- 0.1x if needed
- Add silence gaps between dialogue

## Supported Languages for Dubbing

Your cloned voice can dub in multiple languages:
- **Hindi** (हिंदी) - Polly Neural
- **English (US)** - Polly Neural
- **English (India)** - Polly Neural
- **English (UK)** - Polly Neural
- **Tamil** (தமிழ்) - Google TTS
- **Telugu** (తెలుగు) - Google TTS
- **Bengali** (বাংলা) - Google TTS
- **Marathi** (मराठी) - Google TTS
- **Kannada** (ಕನ್ನಡ) - Google TTS
- **Malayalam** (മലയാളം) - Google TTS
- **Gujarati** (ગુજરાતી) - Google TTS
- **Punjabi** (ਪੰਜਾਬੀ) - Google TTS

## Common Issues

### Voice ID Not Showing
**Problem**: Cloned voice doesn't appear in dropdown
**Solution**: 
- Reload the page
- Check browser localStorage isn't disabled
- Voice IDs persist in browser only (not across devices)

### Audio Sync Issues
**Problem**: Dubbed audio doesn't match video timing
**Solution**:
- Use speech speed slider to adjust duration
- Break sentences differently if needed
- Add silence in video editor if audio is shorter

### Quality Issues
**Problem**: Dubbed voice sounds robotic or unnatural
**Solution**:
- Clone voice with more natural speech variety
- Use same tone of voice for all lines
- Add post-processing (EQ, compression) in video editor

### Performance Issues
**Problem**: Synthesis is slow or timing out
**Solution**:
- Use shorter text per synthesis
- Break into 1-2 sentence chunks
- Try again during off-peak hours
- Use streaming mode for very long texts

## Voice Cloning Best Practices for Dubbing

### Recording Tips
1. **Use good microphone**: Blue Yeti, Audio Technica, etc.
2. **Quiet room**: Minimize background noise
3. **Natural speech**: Don't sound robotic
4. **6-10 seconds**: Ideal length for training
5. **Variety**: Include different vowels and consonants

### Voice Sample Script
> "Hello, my name is [Character Name]. I'm an actor and voice performer. I love doing voice work for films and documentaries. The weather today is very pleasant."

This provides:
- ✅ 8-10 seconds duration
- ✅ Natural speech patterns
- ✅ Character introduction
- ✅ Variety of sounds
- ✅ Single speaker

## Workflow Example: Full Dubbing Project

### Project: Hindi Movie Trailer (30 seconds)

**Step 1: Clone Voice (5 min)**
- Record 8-second voice sample
- Clone as "Movie_Hero_Voice"

**Step 2: Transcribe Dialogue (10 min)**
```
Line 1: "मेरा नाम राज है। मैं एक एजेंट हूँ।" (2s)
Line 2: "मुझे एक मिशन दिया गया है।" (2.5s)
Line 3: "यह मिशन असंभव प्रतीत होता है।" (2.5s)
Line 4: "लेकिन मैं हर चुनौती स्वीकार करता हूँ।" (3s)
Line 5: "आओ, चलते हैं!" (1.5s)
```

**Step 3: Dub Each Line (15 min)**
- 5 lines × 3 min per line = 15 minutes
- For each line:
  - Paste text
  - Select cloned voice
  - Adjust speed for timing
  - Synthesize
  - Save with label

**Step 4: Edit & Mix (20 min)**
- Import all audio files into video editor
- Sync with video frame-by-frame
- Adjust levels and EQ
- Add background music/effects
- Export final version

**Total Time**: ~50 minutes for professional dubbing

## Advanced Features

### Coming Soon
- [ ] Pitch adjustment per voice
- [ ] Emotion selection (happy, sad, angry)
- [ ] Pause/silence control
- [ ] Voice blending (mix 2 cloned voices)
- [ ] Real-time dubbing preview
- [ ] Batch upload of transcripts
- [ ] Video timeline synchronization

## Support

### Issues?
Check VOICE_CLONING_GUIDE.md for troubleshooting

### Need Help?
- Email: team@aiforbharat.com
- GitHub: github.com/Souhridya-Patra/AI_For_Bharat
- Discord: [Join Community]

---

**Team SAAN** | AWS AI for Bharat Hackathon 2026

🎬 Happy Dubbing! 🎤
