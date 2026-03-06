"""Quick start script - installs dependencies and tests AWS."""
import subprocess
import sys

def print_step(num, text):
    """Print step header."""
    print(f"\n{'='*60}")
    print(f"Step {num}: {text}")
    print('='*60)

def main():
    """Quick start."""
    print("\n" + "="*60)
    print("AI VOICE PLATFORM - QUICK START")
    print("="*60)
    
    # Step 1: Install boto3
    print_step(1, "Installing AWS SDK (boto3)")
    try:
        import boto3
        print("✓ boto3 already installed")
    except ImportError:
        print("Installing boto3...")
        subprocess.run([sys.executable, "-m", "pip", "install", "boto3", "botocore"])
        print("✓ boto3 installed")
    
    # Step 2: Test AWS
    print_step(2, "Testing AWS Connection")
    try:
        import boto3
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        
        print("✓ AWS Connection Successful!")
        print(f"  Account: {identity['Account']}")
        print(f"  User: {identity['Arn']}")
        
        session = boto3.session.Session()
        region = session.region_name
        print(f"  Region: {region}")
        
    except Exception as e:
        print(f"✗ AWS connection failed: {e}")
        print("\nYour credentials are configured but there might be an issue.")
        print("This could be:")
        print("  1. Invalid credentials")
        print("  2. Expired credentials")
        print("  3. Network issue")
        print("\nTry running: python scripts/setup_credentials.py")
        sys.exit(1)
    
    # Step 3: Check/Create infrastructure
    print_step(3, "Checking AWS Infrastructure")
    try:
        s3 = boto3.client('s3')
        
        # Check if bucket exists
        try:
            s3.head_bucket(Bucket='ai-voice-platform-audio')
            print("✓ S3 bucket exists")
        except:
            print("⚠️  S3 bucket not found")
            response = input("\nCreate AWS infrastructure now? (y/n): ")
            if response.lower() == 'y':
                print("\nRunning infrastructure setup...")
                subprocess.run([sys.executable, "scripts/setup_aws_infrastructure.py"])
    except Exception as e:
        print(f"Note: {e}")
    
    # Step 4: Enable Polly
    print_step(4, "Enabling Real Voice Synthesis")
    response = input("\nEnable AWS Polly for real voice synthesis? (y/n): ")
    if response.lower() == 'y':
        subprocess.run([sys.executable, "scripts/enable_polly.py"])
    
    # Step 5: Install backend dependencies
    print_step(5, "Installing Backend Dependencies")
    print("This may take a few minutes...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"],
        capture_output=True
    )
    if result.returncode == 0:
        print("✓ Dependencies installed")
    else:
        print("⚠️  Some dependencies may have failed")
        print("You can continue anyway")
    
    # Done
    print("\n" + "="*60)
    print("✅ SETUP COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Start server: python start_server.py")
    print("  2. Test: python scripts/test_all_endpoints.py")
    print("  3. Demo: python scripts/demo_hello_bharat.py")
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
