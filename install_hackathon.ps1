# Ultra-simple installation for hackathon
# Installs packages one by one to avoid compilation issues

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "AI Voice Platform - Hackathon Installation" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install packages one by one
$packages = @(
    "fastapi==0.104.1",
    "uvicorn==0.24.0",
    "pydantic==2.4.2",
    "pydantic-settings==2.0.3",
    "boto3==1.34.34",
    "soundfile==0.12.1",
    "python-multipart==0.0.6",
    "python-dotenv==1.0.0"
)

$total = $packages.Count
$current = 0

foreach ($package in $packages) {
    $current++
    Write-Host ""
    Write-Host "[$current/$total] Installing $package..." -ForegroundColor Yellow
    
    # Try with binary-only first
    python -m pip install $package --only-binary :all: 2>$null
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  Retrying without binary restriction..." -ForegroundColor Gray
        python -m pip install $package
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  ERROR: Failed to install $package" -ForegroundColor Red
            exit 1
        }
    }
    
    Write-Host "  ✓ $package installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "✓ Installation Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Start server: python start_server.py" -ForegroundColor White
Write-Host "2. Test: python scripts/demo_hello_bharat.py" -ForegroundColor White
Write-Host ""
