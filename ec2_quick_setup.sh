#!/bin/bash
# Quick setup script for EC2 deployment

echo "============================================================"
echo "AI Voice Platform - EC2 Quick Setup"
echo "============================================================"
echo ""

# Update system
echo "Updating system..."
sudo apt update && sudo apt upgrade -y
echo "✓ System updated"
echo ""

# Install dependencies
echo "Installing system dependencies..."
sudo apt install -y python3-pip python3-venv git libsndfile1
echo "✓ System dependencies installed"
echo ""

# Check if already in project directory
if [ ! -f "start_server.py" ]; then
    echo "✗ Error: start_server.py not found"
    echo "Please run this script from the ai-voice-platform directory"
    echo ""
    echo "If you haven't cloned the repo yet:"
    echo "  git clone YOUR_GITHUB_REPO"
    echo "  cd ai-voice-platform"
    echo "  bash ec2_quick_setup.sh"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install Python packages
echo "Installing Python packages..."
pip install fastapi uvicorn boto3 soundfile python-multipart python-dotenv
if [ $? -eq 0 ]; then
    echo "✓ Python packages installed"
else
    echo "✗ Error installing Python packages"
    exit 1
fi
echo ""

# Check if AWS credentials are configured
echo "Checking AWS credentials..."
if [ ! -f ~/.aws/credentials ]; then
    echo "⚠ AWS credentials not configured"
    echo ""
    echo "Please configure AWS credentials:"
    echo "  mkdir -p ~/.aws"
    echo "  nano ~/.aws/credentials"
    echo ""
    echo "Add:"
    echo "  [default]"
    echo "  aws_access_key_id = YOUR_KEY"
    echo "  aws_secret_access_key = YOUR_SECRET"
    echo ""
else
    echo "✓ AWS credentials found"
fi
echo ""

# Install screen if not installed
echo "Installing screen..."
sudo apt install -y screen
echo "✓ Screen installed"
echo ""

echo "============================================================"
echo "✓ Setup Complete!"
echo "============================================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Configure AWS credentials (if not done):"
echo "   mkdir -p ~/.aws"
echo "   nano ~/.aws/credentials"
echo ""
echo "2. Start backend:"
echo "   screen -S backend"
echo "   source venv/bin/activate"
echo "   python3 start_server.py"
echo "   # Press Ctrl+A then D to detach"
echo ""
echo "3. Start frontend:"
echo "   screen -S frontend"
echo "   source venv/bin/activate"
echo "   python3 start_frontend.py"
echo "   # Press Ctrl+A then D to detach"
echo ""
echo "4. Test:"
echo "   curl http://localhost:8000/health"
echo ""
echo "5. Access from browser:"
echo "   http://YOUR_EC2_IP:3000"
echo ""
