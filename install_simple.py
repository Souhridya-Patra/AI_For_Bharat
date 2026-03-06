"""Ultra-simple dependency installation - binary wheels only."""
import subprocess
import sys

def run(cmd):
    """Run command and show output."""
    print(f"\n> {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0

def main():
    print("=" * 60)
    print("AI Voice Platform - Simple Installation")
    print("=" * 60)
    
    # Install packages one by one with binary-only flag
    packages = [
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "pydantic==2.4.2",
        "pydantic-settings==2.0.3",
        "boto3==1.34.34",
        "soundfile==0.12.1",
        "python-multipart==0.0.6",
        "python-dotenv==1.0.0",
    ]
    
    print("\nInstalling packages (binary wheels only)...")
    
    for package in packages:
        print(f"\n[{packages.index(package)+1}/{len(packages)}] Installing {package}...")
        if not run(f"{sys.executable} -m pip install {package} --only-binary :all:"):
            print(f"Warning: {package} failed, trying without binary restriction...")
            if not run(f"{sys.executable} -m pip install {package}"):
                print(f"ERROR: Failed to install {package}")
                return False
    
    print("\n" + "=" * 60)
    print("✓ Installation Complete!")
    print("=" * 60)
    print("\nNext: python start_server.py")
    return True

if __name__ == "__main__":
    try:
        if main():
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nCancelled.")
        sys.exit(1)
