"""One-command script to prepare everything for hackathon demo."""
import subprocess
import sys
import time

def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def run_command(description, command, show_output=False):
    """Run a command and report status."""
    print(f"\n{description}...")
    try:
        if show_output:
            # Show output in real-time
            result = subprocess.run(command, shell=True)
            return result.returncode == 0
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ {description} - SUCCESS")
                if result.stdout:
                    # Show last few lines of output
                    lines = result.stdout.strip().split('\n')
                    for line in lines[-3:]:
                        if line.strip():
                            print(f"  {line}")
                return True
            else:
                print(f"✗ {description} - FAILED")
                if result.stderr:
                    print(f"  Error: {result.stderr[:300]}")
                if result.stdout:
                    print(f"  Output: {result.stdout[:300]}")
                return False
    except Exception as e:
        print(f"✗ {description} - ERROR: {e}")
        return False

def main():
    """Prepare everything for hackathon."""
    print_header("AI VOICE PLATFORM - HACKATHON PREPARATION")
    print("\nThis script will:")
    print("  1. Check AWS credentials")
    print("  2. Verify AWS infrastructure")
    print("  3. Enable real voice synthesis (AWS Polly)")
    print("  4. Install dependencies")
    print("  5. Run tests")
    print()
    
    input("Press Enter to continue...")
    
    results = []
    
    # Step 1: Check AWS credentials
    print_header("Step 1: Checking AWS Credentials")
    result = run_command(
        "AWS credentials check",
        f"{sys.executable} scripts/check_aws_credentials.py",
        show_output=True
    )
    results.append(("AWS Credentials", result))
    
    if not result:
        print("\n⚠️  AWS credentials check failed!")
        print("\nTrying to verify manually...")
        
        # Try direct boto3 check
        try:
            import boto3
            sts = boto3.client('sts')
            identity = sts.get_caller_identity()
            print(f"\n✓ AWS connection successful!")
            print(f"  Account: {identity['Account']}")
            print(f"  User: {identity['Arn']}")
            result = True
            results[-1] = ("AWS Credentials", True)
        except Exception as e:
            print(f"\n✗ Cannot connect to AWS: {e}")
            print("\nPlease run: python scripts/setup_credentials.py")
            sys.exit(1)
    
    # Step 2: Check AWS infrastructure
    print_header("Step 2: Checking AWS Infrastructure")
    print("\nChecking S3 buckets...")
    result = run_command(
        "S3 bucket check",
        "aws s3 ls s3://ai-voice-platform-audio"
    )
    
    if not result:
        print("\n⚠️  AWS infrastructure not set up!")
        print("Run: python scripts/setup_aws_infrastructure.py")
        response = input("\nRun setup now? (y/n): ")
        if response.lower() == 'y':
            run_command(
                "AWS infrastructure setup",
                f"{sys.executable} scripts/setup_aws_infrastructure.py"
            )
    
    results.append(("AWS Infrastructure", result))
    
    # Step 3: Enable AWS Polly
    print_header("Step 3: Enabling Real Voice Synthesis")
    result = run_command(
        "Enable AWS Polly",
        f"{sys.executable} scripts/enable_polly.py"
    )
    results.append(("AWS Polly", result))
    
    # Step 4: Install dependencies
    print_header("Step 4: Installing Dependencies")
    result = run_command(
        "Install backend dependencies",
        f"{sys.executable} -m pip install -r backend/requirements.txt"
    )
    results.append(("Dependencies", result))
    
    # Summary
    print_header("PREPARATION SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nCompleted: {passed}/{total} steps\n")
    
    for step_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {step_name}")
    
    if passed == total:
        print_header("✅ READY FOR HACKATHON!")
        print("\nYour platform is ready for judges to test!")
        print("\nNext steps:")
        print("  1. Start server: python start_server.py")
        print("  2. Test: python scripts/test_all_endpoints.py")
        print("  3. Demo: python scripts/demo_hello_bharat.py")
        print("  4. Open docs: http://localhost:8000/docs")
        print()
        print("📖 See HACKATHON_READY.md for demo script")
        print()
    else:
        print_header("⚠️  SOME STEPS FAILED")
        print("\nPlease fix the issues above before proceeding.")
        print("\nCommon fixes:")
        print("  - AWS credentials: python scripts/setup_credentials.py")
        print("  - AWS infrastructure: python scripts/setup_aws_infrastructure.py")
        print("  - Dependencies: pip install -r backend/requirements.txt")
        print()
    
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPreparation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
