"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # AWS Configuration
    aws_region: str = "us-east-1"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    
    # SageMaker
    sagemaker_endpoint_name: str = "xtts-v2-endpoint"
    
    # S3
    s3_bucket_name: str = "ai-voice-platform-audio"
    s3_models_bucket: str = "ai-voice-platform-models"
    
    # DynamoDB
    dynamodb_voices_table: str = "voice_models"
    dynamodb_projects_table: str = "projects"
    dynamodb_audit_table: str = "audit_logs"
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: Optional[str] = None
    
    # API Configuration
    api_secret_key: str = "your-secret-key-change-this"
    api_algorithm: str = "HS256"
    api_access_token_expire_minutes: int = 60
    
    # Rate Limiting
    rate_limit_per_hour: int = 1000
    
    # Application
    debug: bool = True
    log_level: str = "INFO"
    use_mock_synthesis: bool = False  # Set to False when using real synthesis
    use_aws_polly: bool = True  # Set to True to use AWS Polly (fastest real synthesis)
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
