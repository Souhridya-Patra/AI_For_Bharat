# Quick dependency installation for hackathon
# Avoids numpy compilation issues by using pre-built wheels

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "AI Voice Platform - Quick Dependency Installation" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if pip is available
Write-Host "Checking pip..." -ForegroundColor Yellow
python -m pip --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: pip not found. Please install Python first." -ForegroundColor Red
    exit 1
}

Write-Host "✓ pip found" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install minimal requirements (no compilation needed)
Write-Host ""
Write-Host "Installing core dependencies..." -ForegroundColor Yellow
python -m pip install -r backend/requirements-minimal.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✓ Dependencies installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Start server: python start_server.py" -ForegroundColor White
Write-Host "2. Test synthesis: python scripts/demo_hello_bharat.py" -ForegroundColor White
Write-Host "3. Open API docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
