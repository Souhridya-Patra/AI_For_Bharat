# Install dependencies for Python 3.12+ (avoids Rust compilation)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "AI Voice Platform - Python 3.12+ Installation" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
$pythonVersion = python --version 2>&1
Write-Host "Python version: $pythonVersion" -ForegroundColor Yellow
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ pip upgraded" -ForegroundColor Green
} else {
    Write-Host "✗ pip upgrade failed (continuing anyway)" -ForegroundColor Yellow
}
Write-Host ""

# Install packages one by one
Write-Host "Installing packages..." -ForegroundColor Yellow
Write-Host ""

$packages = @(
    @{Name="fastapi==0.109.2"; Description="FastAPI"},
    @{Name="uvicorn==0.27.1"; Description="Uvicorn"},
    @{Name="boto3"; Description="AWS SDK"},
    @{Name="soundfile"; Description="Audio processing"},
    @{Name="python-multipart"; Description="File upload support"},
    @{Name="python-dotenv"; Description="Environment variables"}
)

$failed = @()

foreach ($pkg in $packages) {
    Write-Host "Installing $($pkg.Description)..." -ForegroundColor Cyan
    python -m pip install $pkg.Name
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ $($pkg.Description) installed" -ForegroundColor Green
    } else {
        Write-Host "✗ $($pkg.Description) failed" -ForegroundColor Red
        $failed += $pkg.Description
    }
    Write-Host ""
}

Write-Host "============================================================" -ForegroundColor Cyan
if ($failed.Count -eq 0) {
    Write-Host "✓ All dependencies installed successfully!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Configure AWS credentials in backend/.env" -ForegroundColor White
    Write-Host "2. Run: python start_server.py" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "✗ Some packages failed to install:" -ForegroundColor Red
    foreach ($pkg in $failed) {
        Write-Host "  - $pkg" -ForegroundColor Red
    }
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Try installing failed packages manually:" -ForegroundColor Yellow
    foreach ($pkg in $failed) {
        Write-Host "  pip install $pkg" -ForegroundColor White
    }
    Write-Host ""
}
