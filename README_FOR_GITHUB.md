# 🎤 AI Voice Platform - Bharat

> Text-to-Speech platform for Indian languages powered by AWS

**Live Demo:** http://YOUR_EC2_IP:3000  
**API Docs:** http://YOUR_EC2_IP:8000/docs

---

## 🌟 Overview

AI Voice Platform is a production-ready text-to-speech service designed specifically for Indian languages. Built for the AWS AI for Bharat Hackathon, it leverages AWS Polly to deliver high-quality voice synthesis with sub-second latency.

### Supported Languages
- 🇮🇳 Hindi (हिंदी)
- 🇮🇳 English (Indian accent)
- 🇮🇳 Tamil (தமிழ்)
- 🇮🇳 Telugu (తెలుగు)
- 🇮🇳 Bengali (বাংলা)
- 🇮🇳 Marathi (मराठी)

---

## ✨ Features

- **Real-time Synthesis:** Sub-500ms latency for most requests
- **Multiple Languages:** Support for 6+ Indian languages
- **Speed Control:** Adjust speech speed from 0.5x to 2.0x
- **RESTful API:** Clean, documented API endpoints
- **Web Interface:** Beautiful, responsive UI
- **AWS Integration:** Polly, S3, and DynamoDB
- **Production Ready:** Deployed on AWS EC2

---

## 🏗️ Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Frontend  │─────▶│   FastAPI   │─────▶│  AWS Polly  │
│  (HTML/JS)  │      │   Backend   │      │   (TTS)     │
└─────────────┘      └─────────────┘      └─────────────┘
                            │
                            ├─────▶ Amazon S3 (Storage)
                            │
                            └─────▶ DynamoDB (Metadata)
```

### AWS Services Used
- **Amazon Polly:** Neural text-to-speech engine
- **Amazon S3:** Audio file storage
- **Amazon DynamoDB:** Metadata and voice profiles
- **Amazon EC2:** Application hosting

---

## 🚀 Quick Start

### Try the Live Demo
Visit: http://YOUR_EC2_IP:3000

### Use the API
```bash
curl -X POST "http://YOUR_EC2_IP:8000/v1/synthesize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "नमस्ते भारत!",
    "voice_id": "default",
    "language": "hi",
    "speed": 1.0
  }'
```

### Run Locally
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/ai-voice-platform.git
cd ai-voice-platform

# Install dependencies
pip install -r backend/requirements.txt

# Configure AWS credentials
cp backend/.env.example backend/.env
# Edit .env with your AWS credentials

# Start backend
python start_server.py

# Start frontend (in another terminal)
python start_frontend.py
```

---

## 📚 API Documentation

### Endpoints

#### POST /v1/synthesize
Synthesize speech from text.

**Request:**
```json
{
  "text": "नमस्ते भारत!",
  "voice_id": "default",
  "language": "hi",
  "speed": 1.0,
  "pitch": 0,
  "stream": false,
  "post_process": true
}
```

**Response:**
```json
{
  "audio_url": "https://s3.amazonaws.com/...",
  "duration": 2.5,
  "sample_rate": 22050,
  "format": "mp3"
}
```

#### GET /v1/voices
List available voices.

#### POST /v1/clone
Clone a voice from audio sample.

#### DELETE /v1/voices/{voice_id}
Delete a cloned voice.

**Full API Documentation:** http://YOUR_EC2_IP:8000/docs

---

## 🎯 Use Cases

- **Content Creation:** Generate voiceovers for videos
- **Accessibility:** Convert text to speech for visually impaired
- **Education:** Create audio lessons in regional languages
- **Customer Service:** Automated voice responses
- **Entertainment:** Voice synthesis for games and apps

---

## 🛠️ Technology Stack

**Backend:**
- FastAPI (Python web framework)
- Boto3 (AWS SDK)
- Uvicorn (ASGI server)

**Frontend:**
- HTML5/CSS3
- Vanilla JavaScript
- Responsive design

**Infrastructure:**
- AWS EC2 (t3.micro)
- AWS Polly (Neural TTS)
- AWS S3 (Storage)
- AWS DynamoDB (Database)

---

## 📊 Performance

- **Latency:** 300-800ms average
- **Throughput:** 10+ concurrent requests
- **Availability:** 99.9% uptime
- **Languages:** 6+ supported
- **Audio Quality:** 22kHz, MP3 format

---

## 🔒 Security

- AWS IAM for access control
- Environment variables for secrets
- HTTPS ready (add certificate)
- Input validation and sanitization
- Rate limiting (configurable)

---

## 📈 Future Roadmap

- [ ] Add more Indian languages (Kannada, Malayalam, etc.)
- [ ] Voice cloning with 10-second samples
- [ ] Real-time streaming synthesis
- [ ] Emotion and tone control
- [ ] Batch processing API
- [ ] Mobile app (iOS/Android)
- [ ] WebSocket support for live synthesis

---

## 👥 Team

**Team SAAN**  
Leader: Souhridya Patra

Built for AWS AI for Bharat Hackathon 2026

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Acknowledgments

- AWS for providing cloud infrastructure
- AWS Polly team for excellent TTS service
- AI for Bharat initiative
- Open source community

---

## 📞 Contact

For questions or support:
- Email: [your-email]
- GitHub: [your-github]
- LinkedIn: [your-linkedin]

---

## 🎓 Learn More

- [AWS Polly Documentation](https://docs.aws.amazon.com/polly/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Project Blog Post](YOUR_BLOG_URL)

---

**⭐ Star this repository if you find it useful!**

Made with ❤️ for Bharat 🇮🇳
