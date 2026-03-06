"""Quick AWS connection test."""
import sys

try:
    import boto3
    print("Testing AWS connection...")
    
    sts = boto3.client('sts')
    identity = sts.get_caller_identity()
    
    print("\n✓ AWS Connection Successful!")
    print(f"  Account: {identity['Account']}")
    print(f"  User: {identity['Arn']}")
    
    session = boto3.session.Session()
    print(f"  Region: {session.region_name}")
    
    sys.exit(0)
    
except ImportError:
    print("\n✗ boto3 not installed")
    print("Run: pip install boto3")
    sys.exit(1)
    
except Exception as e:
    print(f"\n✗ AWS connection failed: {e}")
    print("\nPlease check your credentials:")
    print("  python scripts/setup_credentials.py")
    sys.exit(1)
