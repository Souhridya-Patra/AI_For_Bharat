"""Interactive script to set up AWS credentials."""
import os
import sys
from pathlib import Path
import getpass


def setup_credentials():
    """Set up AWS credentials interactively."""
    print("=" * 60)
    print("AWS Credentials Setup for AI Voice Platform")
    print("=" * 60)
    print()
    print("This script will help you configure AWS credentials.")
    print("You can find your credentials in:")
    print("  - AWS Console → IAM → Users → Security Credentials")
    print("  - Or your hackathon portal")
    print()
    
    # Get credentials from user
    access_key = input("Enter AWS Access Key ID: ").strip()
    secret_key = getpass.getpass("Enter AWS Secret Access Key: ").strip()
    region = input("Enter AWS Region (default: ap-south-1): ").strip() or "ap-south-1"
    
    if not access_key or not secret_key:
        print("\n✗ Error: Access Key and Secret Key are required!")
        sys.exit(1)
    
    print("\nSetting up credentials...")
    
    # Create .aws directory
    aws_dir = Path.home() / ".aws"
    aws_dir.mkdir(exist_ok=True)
    print(f"✓ Created directory: {aws_dir}")
    
    # Create credentials file
    credentials_file = aws_dir / "credentials"
    credentials_content = f"""[default]
aws_access_key_id = {access_key}
aws_secret_access_key = {secret_key}
"""
    
    credentials_file.write_text(credentials_content)
    print(f"✓ Created credentials file: {credentials_file}")
    
    # Create config file
    config_file = aws_dir / "config"
    config_content = f"""[default]
region = {region}
output = json
"""
    
    config_file.write_text(config_content)
    print(f"✓ Created config file: {config_file}")
    
    # Set environment variables
    os.environ['AWS_ACCESS_KEY_ID'] = access_key
    os.environ['AWS_SECRET_ACCESS_KEY'] = secret_key
    os.environ['AWS_DEFAULT_REGION'] = region
    print("✓ Set environment variables for current session")
    
    print("\n" + "=" * 60)
    print("✓ AWS Credentials configured successfully!")
    print("=" * 60)
    
    # Test credentials
    print("\nTesting AWS connection...")
    try:
        import boto3
        from botocore.exceptions import NoCredentialsError, ClientError
        
        sts = boto3.client('sts', region_name=region)
        identity = sts.get_caller_identity()
        
        print("✓ Successfully connected to AWS!")
        print(f"  - Account: {identity['Account']}")
        print(f"  - User ARN: {identity['Arn']}")
        print(f"  - Region: {region}")
        
        print("\n" + "=" * 60)
        print("Next steps:")
        print("  1. Run: python scripts/setup_aws_infrastructure.py")
        print("  2. Deploy model to SageMaker")
        print("  3. Start the API server")
        print("=" * 60)
        
    except NoCredentialsError:
        print("✗ Credentials not found. Please try again.")
        sys.exit(1)
    
    except ClientError as e:
        print(f"✗ AWS Error: {e}")
        print("\nCredentials may be invalid. Please check and try again.")
        sys.exit(1)
    
    except ImportError:
        print("✗ boto3 not installed. Installing...")
        os.system(f"{sys.executable} -m pip install boto3")
        print("\nPlease run this script again.")
        sys.exit(1)
    
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        sys.exit(1)


def main():
    """Main function."""
    try:
        setup_credentials()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
