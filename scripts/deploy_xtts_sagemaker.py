"""Deploy XTTS-v2 model to AWS SageMaker for production-grade voice synthesis.

This script creates a SageMaker endpoint with XTTS-v2 for ultra-realistic
voice synthesis that rivals ElevenLabs quality.

Requirements:
- AWS credentials configured
- IAM role with SageMaker permissions
- XTTS model files uploaded to S3
"""
import boto3
import json
import time
from datetime import datetime

# Configuration
REGION = "us-east-1"
ROLE_NAME = "SageMakerExecutionRole"  # Update with your IAM role
MODEL_NAME = "xtts-v2-model"
ENDPOINT_CONFIG_NAME = "xtts-v2-config"
ENDPOINT_NAME = "xtts-v2-endpoint"
INSTANCE_TYPE = "ml.g4dn.xlarge"  # GPU instance for inference
INSTANCE_COUNT = 1

# S3 paths (update these)
S3_BUCKET = "ai-voice-platform-models"
S3_MODEL_PREFIX = "xtts-v2/"


def create_model_tar():
    """Create model.tar.gz with XTTS inference code."""
    print("📦 Creating model package...")
    
    # Create inference script
    inference_code = '''
import os
import json
import torch
from TTS.api import TTS

# Global model instance
model = None

def model_fn(model_dir):
    """Load XTTS model."""
    global model
    if model is None:
        print("Loading XTTS-v2 model...")
        model = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        print("Model loaded successfully")
    return model

def input_fn(request_body, request_content_type):
    """Parse input request."""
    if request_content_type == 'application/json':
        return json.loads(request_body)
    raise ValueError(f"Unsupported content type: {request_content_type}")

def predict_fn(input_data, model):
    """Generate speech using XTTS."""
    text = input_data.get('text', '')
    language = input_data.get('language', 'en')
    voice_id = input_data.get('voice_id', 'default')
    speed = input_data.get('speed', 1.0)
    
    # Generate audio
    output_path = "/tmp/output.wav"
    
    if voice_id == 'default':
        model.tts_to_file(
            text=text,
            language=language,
            file_path=output_path
        )
    else:
        # Voice cloning mode
        model.tts_to_file(
            text=text,
            language=language,
            speaker_wav=voice_id,
            file_path=output_path
        )
    
    # Read audio file
    import base64
    with open(output_path, 'rb') as f:
        audio_bytes = f.read()
    
    # Return base64 encoded audio
    return {
        'audio': base64.b64encode(audio_bytes).decode('utf-8'),
        'sample_rate': 24000,
        'format': 'wav'
    }

def output_fn(prediction, response_content_type):
    """Format output response."""
    return json.dumps(prediction)
'''
    
    # Save inference script
    with open('/tmp/inference.py', 'w') as f:
        f.write(inference_code)
    
    # Create requirements
    requirements = '''TTS==0.22.0
torch>=2.0.0
'''
    
    with open('/tmp/requirements.txt', 'w') as f:
        f.write(requirements)
    
    # Create model.tar.gz
    import tarfile
    with tarfile.open('/tmp/model.tar.gz', 'w:gz') as tar:
        tar.add('/tmp/inference.py', arcname='code/inference.py')
        tar.add('/tmp/requirements.txt', arcname='code/requirements.txt')
    
    print("✅ Model package created")
    return '/tmp/model.tar.gz'


def upload_to_s3(file_path):
    """Upload model package to S3."""
    print(f"📤 Uploading to S3: s3://{S3_BUCKET}/{S3_MODEL_PREFIX}...")
    
    s3 = boto3.client('s3', region_name=REGION)
    
    # Create bucket if not exists
    try:
        s3.create_bucket(Bucket=S3_BUCKET)
        print(f"✅ Created bucket: {S3_BUCKET}")
    except s3.exceptions.BucketAlreadyOwnedByYou:
        print(f"Bucket already exists: {S3_BUCKET}")
    except s3.exceptions.BucketAlreadyExists:
        print(f"Bucket already exists: {S3_BUCKET}")
    
    # Upload model
    s3.upload_file(
        file_path,
        S3_BUCKET,
        f"{S3_MODEL_PREFIX}model.tar.gz"
    )
    
    model_data_url = f"s3://{S3_BUCKET}/{S3_MODEL_PREFIX}model.tar.gz"
    print(f"✅ Uploaded to: {model_data_url}")
    return model_data_url


def get_execution_role():
    """Get SageMaker execution role ARN."""
    iam = boto3.client('iam')
    
    try:
        role = iam.get_role(RoleName=ROLE_NAME)
        role_arn = role['Role']['Arn']
        print(f"✅ Using IAM role: {role_arn}")
        return role_arn
    except iam.exceptions.NoSuchEntityException:
        print(f"❌ Role {ROLE_NAME} not found. Creating...")
        
        # Create role
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"Service": "sagemaker.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }]
        }
        
        role = iam.create_role(
            RoleName=ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        
        # Attach policies
        iam.attach_role_policy(
            RoleName=ROLE_NAME,
            PolicyArn='arn:aws:iam::aws:policy/AmazonSageMakerFullAccess'
        )
        
        role_arn = role['Role']['Arn']
        print(f"✅ Created role: {role_arn}")
        time.sleep(10)  # Wait for role to propagate
        return role_arn


def create_sagemaker_model(model_data_url, role_arn):
    """Create SageMaker model."""
    print(f"📦 Creating SageMaker model: {MODEL_NAME}")
    
    sagemaker = boto3.client('sagemaker', region_name=REGION)
    
    # Delete existing model if exists
    try:
        sagemaker.delete_model(ModelName=MODEL_NAME)
        print(f"Deleted existing model: {MODEL_NAME}")
        time.sleep(5)
    except:
        pass
    
    # Get PyTorch inference container
    # XTTS requires PyTorch
    container = f"763104351884.dkr.ecr.{REGION}.amazonaws.com/pytorch-inference:2.0.0-gpu-py310"
    
    model_params = {
        'ModelName': MODEL_NAME,
        'PrimaryContainer': {
            'Image': container,
            'ModelDataUrl': model_data_url,
            'Environment': {
                'SAGEMAKER_PROGRAM': 'inference.py',
                'SAGEMAKER_SUBMIT_DIRECTORY': model_data_url,
                'MMS_DEFAULT_RESPONSE_TIMEOUT': '900',
            }
        },
        'ExecutionRoleArn': role_arn,
    }
    
    response = sagemaker.create_model(**model_params)
    print(f"✅ Created model: {response['ModelArn']}")


def create_endpoint_config():
    """Create SageMaker endpoint configuration."""
    print(f"⚙️ Creating endpoint config: {ENDPOINT_CONFIG_NAME}")
    
    sagemaker = boto3.client('sagemaker', region_name=REGION)
    
    # Delete existing config if exists
    try:
        sagemaker.delete_endpoint_config(EndpointConfigName=ENDPOINT_CONFIG_NAME)
        print(f"Deleted existing config: {ENDPOINT_CONFIG_NAME}")
        time.sleep(5)
    except:
        pass
    
    config_params = {
        'EndpointConfigName': ENDPOINT_CONFIG_NAME,
        'ProductionVariants': [{
            'VariantName': 'AllTraffic',
            'ModelName': MODEL_NAME,
            'InstanceType': INSTANCE_TYPE,
            'InitialInstanceCount': INSTANCE_COUNT,
            'InitialVariantWeight': 1.0,
        }]
    }
    
    response = sagemaker.create_endpoint_config(**config_params)
    print(f"✅ Created config: {response['EndpointConfigArn']}")


def create_endpoint():
    """Create SageMaker endpoint."""
    print(f"🚀 Creating endpoint: {ENDPOINT_NAME}")
    
    sagemaker = boto3.client('sagemaker', region_name=REGION)
    
    # Check if endpoint exists
    try:
        sagemaker.describe_endpoint(EndpointName=ENDPOINT_NAME)
        print(f"Endpoint {ENDPOINT_NAME} already exists. Updating...")
        
        response = sagemaker.update_endpoint(
            EndpointName=ENDPOINT_NAME,
            EndpointConfigName=ENDPOINT_CONFIG_NAME
        )
    except:
        response = sagemaker.create_endpoint(
            EndpointName=ENDPOINT_NAME,
            EndpointConfigName=ENDPOINT_CONFIG_NAME
        )
    
    print(f"✅ Endpoint creation started: {response['EndpointArn']}")
    print(f"⏳ Waiting for endpoint to be in service (this may take 5-10 minutes)...")
    
    # Wait for endpoint
    waiter = sagemaker.get_waiter('endpoint_in_service')
    waiter.wait(EndpointName=ENDPOINT_NAME)
    
    print(f"✅ Endpoint is ready: {ENDPOINT_NAME}")


def test_endpoint():
    """Test the deployed endpoint."""
    print(f"🧪 Testing endpoint: {ENDPOINT_NAME}")
    
    runtime = boto3.client('sagemaker-runtime', region_name=REGION)
    
    test_payload = {
        'text': 'नमस्ते! यह XTTS-v2 का परीक्षण है।',
        'language': 'hi',
        'voice_id': 'default',
        'speed': 1.0
    }
    
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType='application/json',
        Body=json.dumps(test_payload)
    )
    
    result = json.loads(response['Body'].read())
    print(f"✅ Test successful! Audio size: {len(result.get('audio', ''))} bytes (base64)")


def main():
    """Main deployment flow."""
    print("=" * 60)
    print("XTTS-v2 SageMaker Deployment")
    print("=" * 60)
    print()
    
    try:
        # Step 1: Create model package
        model_tar_path = create_model_tar()
        
        # Step 2: Upload to S3
        model_data_url = upload_to_s3(model_tar_path)
        
        # Step 3: Get IAM role
        role_arn = get_execution_role()
        
        # Step 4: Create SageMaker model
        create_sagemaker_model(model_data_url, role_arn)
        
        # Step 5: Create endpoint config
        create_endpoint_config()
        
        # Step 6: Create endpoint
        create_endpoint()
        
        # Step 7: Test endpoint
        test_endpoint()
        
        print()
        print("=" * 60)
        print("✅ DEPLOYMENT COMPLETE!")
        print("=" * 60)
        print()
        print(f"Endpoint Name: {ENDPOINT_NAME}")
        print(f"Region: {REGION}")
        print(f"Instance Type: {INSTANCE_TYPE}")
        print()
        print("Update your .env file:")
        print(f"  SAGEMAKER_ENDPOINT_NAME={ENDPOINT_NAME}")
        print(f"  USE_XTTS=True")
        print(f"  USE_XTTS_SAGEMAKER=True")
        print()
        print("Estimated Cost: ~$0.60/hour (when active)")
        print()
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
