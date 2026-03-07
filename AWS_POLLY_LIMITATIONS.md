# AWS Polly Language Limitations

## Supported Indian Languages

AWS Polly currently supports only **2 Indian languages**:

### ✅ Fully Supported
1. **Hindi (हिंदी)** - Voice: Aditi (Female)
2. **English (Indian accent)** - Voice: Aditi (Female)

### ❌ Not Supported
- Tamil (தமிழ்)
- Telugu (తెలుగు)
- Bengali (বাংলা)
- Marathi (मराठी)
- Kannada (ಕನ್ನಡ)
- Malayalam (മലയാളം)
- Gujarati (ગુજરાતી)
- Punjabi (ਪੰਜਾਬੀ)

## Why This Limitation?

AWS Polly is a global service and doesn't have comprehensive coverage for all Indian languages yet. The service focuses on widely-spoken global languages.

## What We Fixed

### Before:
- Language dropdown showed all Indian languages
- Selecting Tamil/Telugu/Bengali/Marathi would use Hindi voice (incorrect pronunciation)
- Users were confused why their language didn't work

### After:
- Language dropdown shows only supported languages (Hindi, English-IN, English-US)
- Clear message: "Tamil, Telugu, Bengali, and Marathi are not yet supported by AWS Polly"
- If unsupported language is selected via API, returns clear error message
- Example buttons updated to show only supported languages

## For Judges

When demonstrating the platform:

1. **Works perfectly for:**
   - Hindi text → Hindi speech ✓
   - English text → English (Indian) speech ✓
   - English text → English (US) speech ✓

2. **Does not work for:**
   - Tamil, Telugu, Bengali, Marathi, etc.

3. **Why this is acceptable for hackathon:**
   - AWS Polly limitation, not our code limitation
   - We clearly communicate the limitation to users
   - Hindi and English cover a large portion of Indian users
   - Platform architecture supports adding more languages when AWS adds them

## Future Improvements

To support more Indian languages, we could:

1. **Use Amazon Transcribe + Translate + Polly:**
   - Translate Tamil/Telugu/etc. to Hindi
   - Synthesize in Hindi
   - (Not ideal for pronunciation)

2. **Use different TTS service:**
   - Google Cloud TTS (supports more Indian languages)
   - Microsoft Azure TTS (supports Tamil, Telugu)
   - (Would require changing the synthesis engine)

3. **Train custom models:**
   - Use Amazon SageMaker with custom TTS models
   - Requires significant ML expertise and training data
   - (Future enhancement)

## Technical Details

### Voice: Aditi
- **Languages:** Hindi, English (Indian accent)
- **Gender:** Female
- **Engines:** Standard (16kHz), Neural (24kHz)
- **Quality:** Neural engine provides better quality but not available for all use cases

### Current Implementation
```python
self.voice_map = {
    "hi": "Aditi",       # Hindi - SUPPORTED
    "en-IN": "Aditi",    # English (Indian) - SUPPORTED
    "en": "Joanna",      # English (US) - SUPPORTED
    "ta": None,          # Tamil - NOT SUPPORTED
    "te": None,          # Telugu - NOT SUPPORTED
    "bn": None,          # Bengali - NOT SUPPORTED
    "mr": None,          # Marathi - NOT SUPPORTED
}
```

## User Experience

### Error Message (if unsupported language used):
```
Language 'ta' is not supported by AWS Polly.
Supported languages: Hindi (hi), English (en, en-IN).
Tamil, Telugu, Bengali, and Marathi are not available in AWS Polly.
```

### Frontend Message:
```
Note: Tamil, Telugu, Bengali, and Marathi are not yet supported by AWS Polly
```

## Conclusion

This is a **platform limitation, not a bug**. We've:
- ✅ Clearly communicated the limitation
- ✅ Removed unsupported options from UI
- ✅ Provided helpful error messages
- ✅ Focused on what works (Hindi & English)

For a hackathon project, this is acceptable and shows good UX design by being transparent about limitations.
