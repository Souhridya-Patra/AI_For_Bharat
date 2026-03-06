"""Script to set up AWS infrastructure for AI Voice Platform."""
import boto3
import json
import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
REGION = "ap-south-1"  # Mumbai region for India
S3_AUDIO_BUCKET = "ai-voice-platform-audio"
S3_MODELS_BUCKET = "ai-voice-platform-models"
DYNAMODB_VOICES_TABLE = "voice_models"
DYNAMODB_PROJECTS_TABLE = "projects"
DYNAMODB_AUDIT_TABLE = "audit_logs"


def create_s3_buckets(s3_client):
    """Create S3 buckets for audio and models."""
    buckets = [S3_AUDIO_BUCKET, S3_MODELS_BUCKET]
    
    for bucket_name in buckets:
        try:
            logger.info(f"Creating S3 bucket: {bucket_name}")
            
            if REGION == "us-east-1":
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': REGION}
                )
            
            # Enable versioning
            s3_client.put_bucket_versioning(
                Bucket=bucket_name,
                VersioningConfiguration={'Status': 'Enabled'}
            )
            
            # Set lifecycle policy to delete old files
            lifecycle_policy = {
                'Rules': [
                    {
                        'ID': 'DeleteOldFiles',
                        'Status': 'Enabled',
                        'Prefix': '',
                        'Expiration': {'Days': 30}
                    }
                ]
            }
            s3_client.put_bucket_lifecycle_configuration(
                Bucket=bucket_name,
                LifecycleConfiguration=lifecycle_policy
            )
            
            logger.info(f"✓ Created bucket: {bucket_name}")
        
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                logger.info(f"Bucket already exists: {bucket_name}")
            else:
                logger.error(f"Failed to create bucket {bucket_name}: {e}")
                raise


def create_dynamodb_tables(dynamodb_client):
    """Create DynamoDB tables."""
    
    # Voice Models Table
    try:
        logger.info(f"Creating DynamoDB table: {DYNAMODB_VOICES_TABLE}")
        dynamodb_client.create_table(
            TableName=DYNAMODB_VOICES_TABLE,
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'},
                {'AttributeName': 'user_id', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'user_id-index',
                    'KeySchema': [
                        {'AttributeName': 'user_id', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        logger.info(f"✓ Created table: {DYNAMODB_VOICES_TABLE}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            logger.info(f"Table already exists: {DYNAMODB_VOICES_TABLE}")
        else:
            logger.error(f"Failed to create table: {e}")
            raise
    
    # Projects Table
    try:
        logger.info(f"Creating DynamoDB table: {DYNAMODB_PROJECTS_TABLE}")
        dynamodb_client.create_table(
            TableName=DYNAMODB_PROJECTS_TABLE,
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'},
                {'AttributeName': 'user_id', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'user_id-index',
                    'KeySchema': [
                        {'AttributeName': 'user_id', 'KeyType': 'HASH'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        logger.info(f"✓ Created table: {DYNAMODB_PROJECTS_TABLE}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            logger.info(f"Table already exists: {DYNAMODB_PROJECTS_TABLE}")
        else:
            logger.error(f"Failed to create table: {e}")
            raise
    
    # Audit Logs Table
    try:
        logger.info(f"Creating DynamoDB table: {DYNAMODB_AUDIT_TABLE}")
        dynamodb_client.create_table(
            TableName=DYNAMODB_AUDIT_TABLE,
            KeySchema=[
                {'AttributeName': 'id', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'id', 'AttributeType': 'S'},
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'timestamp', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'user_id-timestamp-index',
                    'KeySchema': [
                        {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                        {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'},
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        logger.info(f"✓ Created table: {DYNAMODB_AUDIT_TABLE}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            logger.info(f"Table already exists: {DYNAMODB_AUDIT_TABLE}")
        else:
            logger.error(f"Failed to create table: {e}")
            raise


def main():
    """Main setup function."""
    logger.info("=" * 60)
    logger.info("AI Voice Platform - AWS Infrastructure Setup")
    logger.info("=" * 60)
    
    # Initialize AWS clients
    s3_client = boto3.client('s3', region_name=REGION)
    dynamodb_client = boto3.client('dynamodb', region_name=REGION)
    
    # Create S3 buckets
    logger.info("\n1. Creating S3 Buckets...")
    create_s3_buckets(s3_client)
    
    # Create DynamoDB tables
    logger.info("\n2. Creating DynamoDB Tables...")
    create_dynamodb_tables(dynamodb_client)
    
    logger.info("\n" + "=" * 60)
    logger.info("✓ AWS Infrastructure setup completed successfully!")
    logger.info("=" * 60)
    logger.info("\nNext steps:")
    logger.info("1. Deploy XTTS-v2 model to SageMaker")
    logger.info("2. Update .env file with AWS resource names")
    logger.info("3. Start the FastAPI server")


if __name__ == "__main__":
    main()
