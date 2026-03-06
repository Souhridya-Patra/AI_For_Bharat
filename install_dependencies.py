"""Quick dependency installation for hackathon."""
import subprocess
import sys

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"✗ Error: {description} failed")
        print(result.stderr)
        return False
    
    print(f"✓ {description} completed")
    return True

def main():
    """Install dependencies."""
    print("=" * 60)
    print("AI Voice Platform - Quick Dependency Installation")
    print("=" * 60)
    
    # Check pip
    if not run_command(f"{sys.executable} -m pip --version", "Checking pip"):
        print("\nError: pip not found. Please install Python first.")
        sys.exit(1)
    
    # Upgrade pip
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")
    
    # Install minimal requirements
    if not run_command(
        f"{sys.executable} -m pip install -r backend/requirements-minimal.txt",
        "Installing core dependencies"
    ):
        print("\n✗ Failed to install dependencies")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓ Installation Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Start server: python start_server.py")
    print("2. Test synthesis: python scripts/demo_hello_bharat.py")
    print("3. Open API docs: http://localhost:8000/docs")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
