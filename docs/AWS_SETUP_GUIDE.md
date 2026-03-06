# AWS Setup Guide for AI Voice Platform

## Step 1: Get AWS Credentials

### For Hackathon Participants:
1. Log in to the AWS Hackathon portal
2. Navigate to your team's AWS account
3. Copy your Access Key ID and Secret Access Key
4. Note your assigned region (likely `ap-south-1` for Mumbai)

### For Personal AWS Account:
1. Log in to AWS Console: https://console.aws.amazon.com
2. Go to IAM (Identity and Access Management)
3. Click "Users" → Select your user (or create one)
4. Go to "Security credentials" tab
5. Click "Create access key"
6. Download the credentials CSV file

## Step 2: Configure AWS Credentials

### Method 1: Using AWS CLI (Recommended)

1. **Install AWS CLI** (if not already installed):
   ```powershell
   # Windows (using pip)
   pip install awscli
   
   # Or download installer from:
   # https://aws.amazon.com/cli/
   ```

2. **Configure credentials**:
   ```powershell
   aws configure
   ```
   
   Enter the following when prompted:
   ```
   AWS Access Key ID: YOUR_ACCESS_KEY_ID
   AWS Secret Access Key: YOUR_SECRET_ACCESS_KEY
   Default region name: ap-south-1
   Default output format: json
   ```

3. **Verify configuration**:
   ```powershell
   aws sts get-caller-identity
   ```
   
   You should see your account details.

### Method 2: Using Environment Variables

Set environment variables in PowerShell:

```powershell
# Set for current session
$env:AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
$env:AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
$env:AWS_DEFAULT_REGION="ap-south-1"

# Verify
echo $env:AWS_ACCESS_KEY_ID
```

To make it permanent, add to your PowerShell profile:
```powershell
# Open profile
notepad $PROFILE

# Add these lines:
$env:AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
$env:AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
$env:AWS_DEFAULT_REGION="ap-south-1"
```

### Method 3: Using Credentials File

Create/edit the AWS credentials file:

**Location**: `C:\Users\YOUR_USERNAME\.aws\credentials`

```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
```

Create/edit the AWS config file:

**Location**: `C:\Users\YOUR_USERNAME\.aws\config`

```ini
[default]
region = ap-south-1
output = json
```

## Step 3: Verify AWS Access

Run this test script:

```powershell
python -c "import boto3; print(boto3.client('sts').get_caller_identity())"
```

You should see output like:
```json
{
  "UserId": "AIDAI...",
  "Account": "123456789012",
  "Arn": "arn:aws:iam::123456789012:user/your-username"
}
```

## Step 4: Run Infrastructure Setup

Once credentials are configured:

```powershell
python scripts/setup_aws_infrastructure.py
```

## Troubleshooting

### Error: "Unable to locate credentials"
- Check that credentials are set correctly
- Verify the credentials file exists at `C:\Users\YOUR_USERNAME\.aws\credentials`
- Try running `aws configure` again

### Error: "Access Denied"
- Verify your IAM user has the necessary permissions:
  - AmazonS3FullAccess
  - AmazonDynamoDBFullAccess
  - AmazonSageMakerFullAccess
  - CloudWatchFullAccess

### Error: "Invalid region"
- Ensure region is set to a valid AWS region (e.g., `ap-south-1`)
- Check the config file or environment variable

## Required IAM Permissions

Your AWS user needs these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:CreateBucket",
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:PutBucketVersioning",
        "s3:PutLifecycleConfiguration",
        "dynamodb:CreateTable",
        "dynamodb:DescribeTable",
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:Query",
        "dynamodb:Scan",
        "dynamodb:DeleteItem",
        "sagemaker:CreateEndpoint",
        "sagemaker:CreateEndpointConfig",
        "sagemaker:CreateModel",
        "sagemaker:InvokeEndpoint",
        "cloudwatch:PutMetricData",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
```

## Next Steps

After successful setup:
1. Deploy XTTS-v2 model to SageMaker
2. Configure backend `.env` file
3. Start the API server
4. Run the demo

## Support

If you encounter issues:
1. Check AWS Console for error messages
2. Review CloudWatch logs
3. Verify IAM permissions
4. Contact hackathon support for credential issues
