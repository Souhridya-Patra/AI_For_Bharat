"""Script to enable AWS Polly for real voice synthesis."""
import os
import sys
from pathlib import Path

def main():
    """Enable AWS Polly synthesis."""
    print("=" * 60)
    print("Enable AWS Polly for Real Voice Synthesis")
    print("=" * 60)
    print()
    
    # Check if backend/.env exists
    env_file = Path("backend/.env")
    
    if not env_file.exists():
        print("Creating .env file from template...")
        import shutil
        shutil.copy("backend/.env.example", "backend/.env")
        print("✓ Created .env file")
    
    # Read current .env
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Update settings
    new_lines = []
    for line in lines:
        if line.startswith('USE_MOCK_SYNTHESIS='):
            new_lines.append('USE_MOCK_SYNTHESIS=False\n')
        elif line.startswith('USE_AWS_POLLY='):
            new_lines.append('USE_AWS_POLLY=True\n')
        else:
            new_lines.append(line)
    
    # Write updated .env
    with open(env_file, 'w') as f:
        f.writelines(new_lines)
    
    print("\n✓ AWS Polly enabled!")
    print()
    print("Configuration updated:")
    print("  - USE_MOCK_SYNTHESIS=False")
    print("  - USE_AWS_POLLY=True")
    print()
    print("=" * 60)
    print("AWS Polly Features:")
    print("=" * 60)
    print("✓ Real voice synthesis (not mock)")
    print("✓ High quality neural voices")
    print("✓ Supports Hindi (Aditi voice)")
    print("✓ Supports English (multiple voices)")
    print("✓ Speed control (0.5x to 2.0x)")
    print("✓ No deployment needed")
    print("✓ Pay per use (~$0.004 per request)")
    print()
    print("=" * 60)
    print("Supported Languages:")
    print("=" * 60)
    print("  - English (en, en-US, en-GB, en-IN)")
    print("  - Hindi (hi, hi-IN)")
    print("  - Tamil (ta) - uses Hindi voice")
    print("  - Telugu (te) - uses Hindi voice")
    print("  - Bengali (bn) - uses Hindi voice")
    print("  - Marathi (mr) - uses Hindi voice")
    print()
    print("=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print("1. Restart your server:")
    print("   python start_server.py")
    print()
    print("2. Test synthesis:")
    print("   python scripts/demo_hello_bharat.py")
    print()
    print("3. Try the API:")
    print("   http://localhost:8000/docs")
    print()
    print("=" * 60)
    print()
    print("Note: AWS Polly requires valid AWS credentials.")
    print("      Run 'python scripts/check_aws_credentials.py' to verify.")
    print()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
