"""Check and validate AWS credentials before running setup."""
import sys
import os

def check_credentials():
    """Check if AWS credentials are configured."""
    print("=" * 60)
    print("AWS Credentials Check")
    print("=" * 60)
    
    # Check environment variables
    print("\n1. Checking environment variables...")
    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    region = os.environ.get('AWS_DEFAULT_REGION')
    
    if access_key and secret_key:
        print(f"   ✓ AWS_ACCESS_KEY_ID: {access_key[:8]}...")
        print(f"   ✓ AWS_SECRET_ACCESS_KEY: {'*' * 20}")
        print(f"   ✓ AWS_DEFAULT_REGION: {region or 'Not set (will use default)'}")
    else:
        print("   ✗ Environment variables not set")
    
    # Check credentials file
    print("\n2. Checking credentials file...")
    creds_file = os.path.expanduser("~/.aws/credentials")
    config_file = os.path.expanduser("~/.aws/config")
    
    if os.path.exists(creds_file):
        print(f"   ✓ Credentials file exists: {creds_file}")
    else:
        print(f"   ✗ Credentials file not found: {creds_file}")
    
    if os.path.exists(config_file):
        print(f"   ✓ Config file exists: {config_file}")
    else:
        print(f"   ✗ Config file not found: {config_file}")
    
    # Try to import boto3 and test credentials
    print("\n3. Testing AWS connection...")
    try:
        import boto3
        from botocore.exceptions import NoCredentialsError, ClientError
        
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        
        print("   ✓ Successfully connected to AWS!")
        print(f"   - Account: {identity['Account']}")
        print(f"   - User ARN: {identity['Arn']}")
        print(f"   - User ID: {identity['UserId']}")
        
        # Get region
        session = boto3.session.Session()
        current_region = session.region_name
        print(f"   - Region: {current_region or 'Not set'}")
        
        return True
    
    except NoCredentialsError:
        print("   ✗ No credentials found!")
        print("\n" + "=" * 60)
        print("AWS CREDENTIALS NOT CONFIGURED")
        print("=" * 60)
        print("\nPlease configure AWS credentials using one of these methods:\n")
        print("Method 1: AWS CLI (Recommended)")
        print("  1. Install AWS CLI: pip install awscli")
        print("  2. Run: aws configure")
        print("  3. Enter your Access Key ID and Secret Access Key\n")
        print("Method 2: Environment Variables (PowerShell)")
        print('  $env:AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"')
        print('  $env:AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"')
        print('  $env:AWS_DEFAULT_REGION="ap-south-1"\n')
        print("Method 3: Credentials File")
        print(f"  Create file: {creds_file}")
        print("  Add:")
        print("    [default]")
        print("    aws_access_key_id = YOUR_ACCESS_KEY")
        print("    aws_secret_access_key = YOUR_SECRET_KEY\n")
        print("For detailed instructions, see: docs/AWS_SETUP_GUIDE.md")
        print("=" * 60)
        return False
    
    except ClientError as e:
        print(f"   ✗ AWS Error: {e}")
        print("\nCredentials may be invalid or expired.")
        return False
    
    except ImportError:
        print("   ✗ boto3 not installed!")
        print("\nPlease install boto3: pip install boto3")
        return False
    
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")
        return False


def main():
    """Main function."""
    success = check_credentials()
    
    if success:
        print("\n" + "=" * 60)
        print("✓ AWS credentials are configured correctly!")
        print("=" * 60)
        print("\nYou can now run:")
        print("  python scripts/setup_aws_infrastructure.py")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
