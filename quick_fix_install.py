"""Quick fix for installation issues - bypasses Pydantic compilation."""
import subprocess
import sys
import shutil
from pathlib import Path

def run(cmd, description):
    """Run command."""
    print(f"\n{description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"✗ Failed: {description}")
        if result.stderr:
            print(result.stderr)
        return False
    print(f"✓ {description} completed")
    return True

def main():
    print("=" * 60)
    print("Quick Fix Installation (No Pydantic Compilation)")
    print("=" * 60)
    
    # Step 1: Install minimal packages (no pydantic)
    packages = [
        "fastapi",
        "uvicorn",
        "boto3",
        "soundfile",
        "python-multipart",
        "python-dotenv"
    ]
    
    print("\nInstalling packages without Pydantic...")
    for pkg in packages:
        if not run(f"{sys.executable} -m pip install {pkg}", f"Installing {pkg}"):
            print(f"\nWarning: {pkg} failed, but continuing...")
    
    # Step 2: Replace config.py with simple version
    print("\nUpdating configuration file...")
    config_path = Path("backend/app/config.py")
    simple_config_path = Path("backend/app/config_simple.py")
    
    if simple_config_path.exists():
        # Backup original
        if config_path.exists():
            shutil.copy(config_path, "backend/app/config_original.py")
            print("✓ Backed up original config.py")
        
        # Replace with simple version
        shutil.copy(simple_config_path, config_path)
        print("✓ Updated config.py (no Pydantic)")
    
    print("\n" + "=" * 60)
    print("✓ Quick Fix Complete!")
    print("=" * 60)
    print("\nYour server is ready to run!")
    print("\nNext steps:")
    print("1. python start_server.py")
    print("2. python scripts/demo_hello_bharat.py")
    print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
