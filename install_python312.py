"""Install dependencies for Python 3.12+ (avoids Rust compilation issues)."""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error: {description} failed")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    """Main installation function."""
    print("=" * 60)
    print("AI Voice Platform - Python 3.12+ Installation")
    print("=" * 60)
    print()
    print(f"Python version: {sys.version}")
    print()
    
    # Check if we're in the right directory
    if not Path("backend").exists():
        print("✗ Error: backend directory not found")
        print("Please run this script from the project root directory")
        return
    
    # Upgrade pip
    if not run_command(
        f"{sys.executable} -m pip install --upgrade pip",
        "Upgrading pip"
    ):
        print("\nWarning: Could not upgrade pip, continuing anyway...")
    
    print()
    print("Installing packages one by one to avoid conflicts...")
    print()
    
    # Install packages one by one
    packages = [
        ("fastapi==0.109.2", "FastAPI"),
        ("uvicorn==0.27.1", "Uvicorn"),
        ("boto3", "AWS SDK (boto3)"),
        ("soundfile", "Audio processing (soundfile)"),
        ("python-multipart", "File upload support"),
        ("python-dotenv", "Environment variables"),
    ]
    
    failed = []
    for package, description in packages:
        print(f"Installing {description}...")
        result = subprocess.run(
            f"{sys.executable} -m pip install {package}",
            shell=True,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✓ {description} installed")
        else:
            print(f"✗ {description} failed")
            failed.append(description)
        print()
    
    print("=" * 60)
    if not failed:
        print("✓ All dependencies installed successfully!")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Configure AWS credentials in backend/.env")
        print("2. Run: python start_server.py")
        print()
    else:
        print("✗ Some packages failed to install:")
        for pkg in failed:
            print(f"  - {pkg}")
        print("=" * 60)
        print()
        print("Try installing failed packages manually:")
        for pkg in failed:
            print(f"  pip install {pkg}")
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)
