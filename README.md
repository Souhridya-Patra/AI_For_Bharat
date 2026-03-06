# AI Voice Platform - ElevenLabs Competitor for India

High-fidelity voice synthesis and cloning platform with focus on Indian regional languages, built for the AWS "AI for Bharat" Hackathon.

## Features

- **Voice Cloning**: Clone any voice with just 6-10 seconds of audio
- **Text-to-Speech**: Natural-sounding speech synthesis in 15+ languages
- **Indian Language Support**: Hindi, Tamil, Marathi, Bengali, Telugu, and more
- **Real-time Streaming**: Ultra-low latency (<200ms first chunk)
- **Studio Interface**: Web-based audio editing and project management
- **AWS Integration**: Fully deployed on AWS infrastructure

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
┌──────▼──────────────────────────────────────────┐
│           API Gateway (FastAPI)                  │
│  - Authentication (JWT)                          │
│  - Rate Limiting                                 │
│  - Request Validation                            │
└──────┬──────────────────────────────────────────┘
       │
┌──────▼──────────────────────────────────────────┐
│         Core Services                            │
│  ┌────────────────┐  ┌────────────────┐        │
│  │ Voice Synthesis│  │ Voice Cloning  │        │
│  │    Engine      │  │    Module      │        │
│  └────────┬───────┘  └────────┬───────┘        │
│           │                    │                 │
│  ┌────────▼────────────────────▼───────┐       │
│  │   SageMaker Inference (XTTS-v2)     │       │
│  │   - GPU-accelerated                  │       │
│  │   - Auto-scaling                     │       │
│  └──────────────────────────────────────┘       │
└──────┬──────────────────────────────────────────┘
       │
┌──────▼──────────────────────────────────────────┐
│         AWS Data Layer                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │    S3    │  │ DynamoDB │  │  Redis   │      │
│  │  Audio   │  │  Voices  │  │  Cache   │      │
│  └──────────┘  └──────────┘  └──────────┘      │
└──────────────────────────────────────────────────┘
```

## AWS Services Used

- **Amazon SageMaker**: Host XTTS-v2 model for inference
- **Amazon S3**: Store audio files and model artifacts
- **Amazon DynamoDB**: Store voice profiles and metadata
- **Amazon Bedrock**: Claude 3.5 Sonnet for text processing
- **Amazon Comprehend**: Content safety and toxicity detection
- **Amazon CloudWatch**: Monitoring and alerting
- **AWS Lambda**: Serverless API functions (optional)
- **Amazon CloudFront**: CDN for frontend delivery

## Quick Start

### Prerequisites

- Python 3.9+
- AWS Account with credits
- Node.js 18+ (for frontend)

### 1. Set Up AWS Infrastructure

```bash
# Install dependencies
pip install boto3

# Configure AWS credentials
aws configure

# Run infrastructure setup
python scripts/setup_aws_infrastructure.py
```

This creates:
- S3 buckets for audio and models
- DynamoDB tables for voices, projects, and audit logs
- CloudWatch log groups

### 2. Deploy XTTS-v2 Model to SageMaker

```bash
# See deployment guide in docs/sagemaker_deployment.md
python scripts/deploy_model_to_sagemaker.py
```

### 3. Start Backend API

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your AWS credentials and resource names
nano .env

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at `http://localhost:8000`

### 4. Run Demo

```bash
# Test the "Hello Bharat" demo
python scripts/demo_hello_bharat.py
```

This tests:
- Synthesis in Hindi, Tamil, Marathi, Bengali, English
- Latency measurement (<500ms target)
- Voice listing

## API Endpoints

### Synthesis

```bash
POST /v1/synthesize
Content-Type: application/json

{
  "text": "नमस्ते भारत!",
  "voice_id": "default",
  "speed": 1.0,
  "pitch": 0,
  "stream": false,
  "language": "hi"
}
```

### Voice Cloning

```bash
POST /v1/clone
Content-Type: multipart/form-data

audio_file: <audio file (6-10 seconds)>
voice_name: "My Voice"
```

### List Voices

```bash
GET /v1/voices
```

### Delete Voice

```bash
DELETE /v1/voices/{voice_id}
```

## 24-Hour Goal Achievement

Our immediate milestone for the hackathon:

✅ Deploy XTTS-v2 model as SageMaker Real-time Endpoint  
✅ Implement FastAPI backend with synthesis endpoint  
✅ Demonstrate "Hello Bharat" generation in Hindi  
✅ Achieve <500ms latency for synthesis  
✅ Support multiple Indian languages  

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── models/           # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── config.py         # Configuration
│   │   └── main.py           # FastAPI app
│   └── requirements.txt
├── frontend/                 # React + Next.js (TODO)
├── scripts/
│   ├── setup_aws_infrastructure.py
│   ├── deploy_model_to_sagemaker.py
│   └── demo_hello_bharat.py
├── .kiro/specs/             # Design specifications
└── README.md
```

## Development

### Running Tests

```bash
cd backend
pytest tests/ -v
```

### Property-Based Tests

```bash
# Run with Hypothesis
pytest tests/property/ -v --hypothesis-show-statistics
```

### Code Quality

```bash
# Format code
black backend/

# Lint
flake8 backend/

# Type checking
mypy backend/
```

## Deployment to Production

### Option 1: AWS Lambda + API Gateway

```bash
# Package application
cd backend
pip install -t package -r requirements.txt
cd package && zip -r ../deployment.zip .
cd .. && zip -g deployment.zip app/

# Deploy to Lambda
aws lambda create-function \
  --function-name ai-voice-platform \
  --runtime python3.9 \
  --handler app.main.handler \
  --zip-file fileb://deployment.zip
```

### Option 2: EC2 with Docker

```bash
# Build Docker image
docker build -t ai-voice-platform .

# Run container
docker run -p 8000:8000 \
  -e AWS_REGION=ap-south-1 \
  -e SAGEMAKER_ENDPOINT_NAME=xtts-v2-endpoint \
  ai-voice-platform
```

### Option 3: ECS/Fargate

See `docs/ecs_deployment.md` for details.

## Cost Optimization

- Use SageMaker auto-scaling to scale down during low traffic
- Set S3 lifecycle policies to delete old audio files
- Use DynamoDB on-demand pricing for variable workloads
- Enable CloudFront caching for static assets
- Use spot instances for non-critical workloads

## Monitoring

Access CloudWatch dashboards:
- Synthesis latency metrics
- Error rates
- GPU utilization
- API request throughput

Set up alarms for:
- Latency > 500ms
- Error rate > 5%
- GPU utilization > 80%

## Contributing

This is a hackathon project. Contributions welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file

## Team

**Team SAAN**
- Team Leader: Souhridya Patra
- Project: AI Voice Platform for Bharat

## Acknowledgments

- AWS for hackathon credits and infrastructure
- Coqui AI for XTTS-v2 model
- AI4Bharat for Indian language datasets
- ElevenLabs for inspiration

## Support

For issues or questions:
- Open a GitHub issue
- Contact: [your-email]

---

Built with ❤️ for India 🇮🇳
