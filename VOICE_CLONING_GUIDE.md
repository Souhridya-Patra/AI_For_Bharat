# 🎭 Voice Cloning Feature Guide

## Overview
Your AI Voice Platform now includes **Voice Cloning** functionality! Users can upload a 6-10 second audio sample and create a custom voice model for text-to-speech synthesis.

## Setup Instructions

### 1. Install Required Dependencies

On your Linux server, install librosa:

```bash
cd ~/AI_For_Bharat
source venv/bin/activate
pip install librosa==0.10.1
```

### 2. Pull Latest Code

```bash
git pull origin main
```

### 3. Restart the Server

```bash
python start_server.py
```

## How to Use Voice Cloning

### Step 1: Access the Clone Voice Tab
1. Open your frontend: `http://34.236.36.88:8000` (or your server IP)
2. Click on **"🎭 Clone Voice"** tab

### Step 2: Upload Audio Sample
- **Duration**: 6-10 seconds of clear speech
- **Format**: MP3, WAV, M4A, OGG
- **Quality**: Single speaker, minimal background noise
- **Content**: Any speech in any language

**Drag & drop** the audio file or **click to browse**

### Step 3: Name Your Voice
Enter a memorable name like:
- "My Voice"
- "Mom's Voice"
- "Professional Narrator"
- "Character Voice"

### Step 4: Clone
Click **"🎭 Clone This Voice"** button

The system will:
1. Validate audio duration (6-10 seconds)
2. Check for single speaker
3. Extract voice embedding
4. Store voice model in DynamoDB
5. Save reference audio to S3
6. Return voice ID

### Step 5: Use Cloned Voice
Your cloned voice ID will appear in the "Your Cloned Voices" section. You can use this ID in the synthesis API.

## API Endpoint

### Clone Voice
```bash
POST /v1/clone
Content-Type: multipart/form-data

Parameters:
- audio_file: Audio file (6-10 seconds)
- voice_name: Name for the cloned voice

Response:
{
  "voice_id": "voice_abc123def456",
  "status": "success",
  "message": "Voice 'My Voice' cloned successfully"
}
```

### Use Cloned Voice for Synthesis
```bash
POST /v1/synthesize
Content-Type: application/json

{
  "text": "Hello, this is my cloned voice!",
  "voice_id": "voice_abc123def456",  // Use your cloned voice ID
  "language": "en",
  "speed": 1.0
}
```

## Technical Details

### Voice Embedding
- Uses speaker encoder to extract 256-dimensional voice embedding
- Embeddings are stored in DynamoDB for fast retrieval
- Reference audio is saved to S3 for future use

### Quality Requirements
- **Minimum duration**: 6 seconds (shorter → poor quality)
- **Maximum duration**: 10 seconds (longer → slow processing)
- **Single speaker**: Multiple speakers will be rejected
- **Clear speech**: Background noise reduces quality

### Error Handling

#### Audio Too Short/Long
```json
{
  "error": {
    "code": "INVALID_AUDIO_DURATION",
    "message": "Audio sample must be between 6 and 10 seconds. Provided: 3.45 seconds"
  }
}
```

#### Multiple Speakers Detected
```json
{
  "error": {
    "code": "MULTIPLE_SPEAKERS",
    "message": "Multiple speakers detected (2). Please provide audio with a single speaker."
  }
}
```

#### File Too Large
```json
{
  "error": {
    "code": "FILE_TOO_LARGE",
    "message": "Audio file must be less than 10MB"
  }
}
```

## AWS Services Used

1. **S3**: Stores reference audio files
   - Bucket: Configured in `.env` (`S3_VOICE_MODELS_BUCKET`)
   - Path: `voices/{voice_id}/reference.{format}`

2. **DynamoDB**: Stores voice metadata and embeddings
   - Table: Configured in `.env` (`DYNAMODB_VOICES_TABLE`)
   - Schema:
     ```
     {
       "id": "voice_abc123def456",
       "user_id": "demo_user",
       "voice_name": "My Voice",
       "embedding": [0.123, 0.456, ...],  // 256-dim array
       "audio_url": "s3://bucket/voices/voice_abc123/reference.wav",
       "duration": 7.5,
       "created_at": "2026-03-08T06:30:00Z"
     }
     ```

## Frontend Features

### Tab Interface
- **🎵 Text-to-Speech**: Traditional TTS with predefined voices
- **🎭 Clone Voice**: Upload and clone custom voices

### Drag & Drop Upload
- Drag audio files directly to upload area
- Visual feedback during drag
- File size and format validation

### Cloned Voices List
- Shows all successfully cloned voices
- Displays voice name and ID
- Can be used for synthesis

## Best Practices

### Recording Quality Audio
1. **Use a good microphone** (not laptop mic)
2. **Quiet environment** (no background noise)
3. **6-10 seconds** of natural speech
4. **Single speaker** only
5. **Clear pronunciation** (not mumbling)

### Example Recording Script
> "Hello, my name is [Name]. I'm recording this sample to create a custom voice model. The weather today is beautiful and sunny."

This provides:
- ✅ ~8 seconds duration
- ✅ Natural speech patterns
- ✅ Variety of sounds (vowels, consonants)
- ✅ Single speaker

## Troubleshooting

### librosa ImportError
```bash
pip install librosa==0.10.1
```

### DynamoDB Table Not Found
Check `.env` file:
```bash
DYNAMODB_VOICES_TABLE=ai-voice-platform-voices
AWS_REGION=us-east-1
```

Create table if needed:
```python
import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.create_table(
    TableName='ai-voice-platform-voices',
    KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
    AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
    BillingMode='PAY_PER_REQUEST'
)
```

### S3 Bucket Not Found
Create bucket:
```python
import boto3
s3 = boto3.client('s3', region_name='us-east-1')
s3.create_bucket(Bucket='ai-voice-platform-models')
```

## Next Steps

1. **Test the feature**: Upload a sample and create your first cloned voice
2. **Integrate with synthesis**: Use cloned voice IDs in TTS requests
3. **Add voice management**: Implement list/delete voice endpoints
4. **Improve quality**: Add noise reduction and audio preprocessing

## Demo Video Script

> "Welcome to the voice cloning feature! Let me show you how easy it is to clone your voice. First, I'll click on the Clone Voice tab. Then, I'll drag and drop a 7-second audio sample of my voice. I'll name it 'My Professional Voice'. Click Clone, and in just a few seconds, my voice is cloned! Now I can use this custom voice for any text-to-speech synthesis."

---

**Team SAAN** | AWS AI for Bharat Hackathon 2026
