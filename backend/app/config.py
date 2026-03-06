"""Application configuration - No Pydantic version."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings."""
    
    def __init__(self):
        # AWS Configuration
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        
        # SageMaker
        self.sagemaker_endpoint_name = os.getenv("SAGEMAKER_ENDPOINT_NAME", "xtts-v2-endpoint")
        
        # S3
        self.s3_bucket_name = os.getenv("S3_BUCKET_NAME", "ai-voice-platform-audio")
        self.s3_models_bucket = os.getenv("S3_MODELS_BUCKET", "ai-voice-platform-models")
        
        # DynamoDB
        self.dynamodb_voices_table = os.getenv("DYNAMODB_VOICES_TABLE", "voice_models")
        self.dynamodb_projects_table = os.getenv("DYNAMODB_PROJECTS_TABLE", "projects")
        self.dynamodb_audit_table = os.getenv("DYNAMODB_AUDIT_TABLE", "audit_logs")
        
        # Redis
        self.redis_host = os.getenv("REDIS_HOST", "localhost")
        self.redis_port = int(os.getenv("REDIS_PORT", "6379"))
        self.redis_password = os.getenv("REDIS_PASSWORD")
        
        # API Configuration
        self.api_secret_key = os.getenv("API_SECRET_KEY", "your-secret-key-change-this")
        self.api_algorithm = os.getenv("API_ALGORITHM", "HS256")
        self.api_access_token_expire_minutes = int(os.getenv("API_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
        
        # Rate Limiting
        self.rate_limit_per_hour = int(os.getenv("RATE_LIMIT_PER_HOUR", "1000"))
        
        # Application
        self.debug = os.getenv("DEBUG", "True").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.use_mock_synthesis = os.getenv("USE_MOCK_SYNTHESIS", "False").lower() == "true"
        self.use_aws_polly = os.getenv("USE_AWS_POLLY", "True").lower() == "true"


settings = Settings()
