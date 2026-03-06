#!/bin/bash
# Automated deployment script for EC2
# Run this on your EC2 instance after connecting via SSH

echo "=========================================="
echo "AI Voice Platform - EC2 Deployment"
echo "=========================================="
echo ""

# Update system
echo "Updating system..."
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
echo "Installing Python..."
sudo apt install -y python3.11 python3.11-venv python3-pip git

# Install system dependencies
echo "Installing system dependencies..."
sudo apt install -y build-essential libsndfile1

# Clone repository (update with your GitHub URL)
echo "Cloning repository..."
cd ~
if [ -d "ai-voice-platform" ]; then
    cd ai-voice-platform
    git pull
else
    git clone https://github.com/yourusername/ai-voice-platform.git
    cd ai-voice-platform
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install fastapi uvicorn boto3 soundfile python-multipart python-dotenv

# Configure AWS credentials
echo ""
echo "=========================================="
echo "AWS Credentials Setup"
echo "=========================================="
echo "Please enter your AWS credentials:"
read -p "AWS Access Key ID: " aws_key
read -sp "AWS Secret Access Key: " aws_secret
echo ""
read -p "AWS Region (default: us-east-1): " aws_region
aws_region=${aws_region:-us-east-1}

# Setup AWS credentials
mkdir -p ~/.aws
cat > ~/.aws/credentials << EOF
[default]
aws_access_key_id = $aws_key
aws_secret_access_key = $aws_secret
EOF

cat > ~/.aws/config << EOF
[default]
region = $aws_region
output = json
EOF

echo "✓ AWS credentials configured"

# Create systemd service for backend
echo "Creating backend service..."
sudo tee /etc/systemd/system/ai-voice-backend.service > /dev/null << EOF
[Unit]
Description=AI Voice Platform Backend
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/ai-voice-platform
ExecStart=/usr/bin/python3 start_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create systemd service for frontend
echo "Creating frontend service..."
sudo tee /etc/systemd/system/ai-voice-frontend.service > /dev/null << EOF
[Unit]
Description=AI Voice Platform Frontend
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/ai-voice-platform
ExecStart=/usr/bin/python3 start_frontend.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start services
echo "Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable ai-voice-backend
sudo systemctl enable ai-voice-frontend
sudo systemctl start ai-voice-backend
sudo systemctl start ai-voice-frontend

# Check status
echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Service Status:"
sudo systemctl status ai-voice-backend --no-pager | head -n 10
sudo systemctl status ai-voice-frontend --no-pager | head -n 10

# Get public IP
PUBLIC_IP=$(curl -s http://checkip.amazonaws.com)

echo ""
echo "=========================================="
echo "Access Your Application:"
echo "=========================================="
echo "Frontend: http://$PUBLIC_IP:3000"
echo "Backend API: http://$PUBLIC_IP:8000"
echo "API Docs: http://$PUBLIC_IP:8000/docs"
echo ""
echo "Share the Frontend URL with judges!"
echo "=========================================="
