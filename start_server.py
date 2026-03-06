"""Python script to start the AI Voice Platform server."""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Start the server."""
    print("=" * 60)
    print("AI Voice Platform - Starting Server")
    print("=" * 60)
    print()
    
    # Change to backend directory if needed
    if Path("backend").exists():
        os.chdir("backend")
    
    # Check if .env exists
    if not Path(".env").exists():
        print("Creating .env file from template...")
        import shutil
        shutil.copy(".env.example", ".env")
        print("✓ Created .env file")
        print()
        print("Note: Using MOCK synthesis mode for local development")
        print("      Set USE_MOCK_SYNTHESIS=False in .env when SageMaker is ready")
        print()
    
    # Check dependencies
    print("Checking dependencies...")
    try:
        import fastapi
        import uvicorn
        print("✓ Dependencies already installed")
    except ImportError:
        print("Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed")
    
    print()
    print("Starting FastAPI server...")
    print()
    print("Server will be available at:")
    print("  - API: http://localhost:8000")
    print("  - Docs: http://localhost:8000/docs")
    print("  - Health: http://localhost:8000/health")
    print()
    print("Press Ctrl+C to stop the server")
    print()
    
    # Start server
    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
        sys.exit(0)
