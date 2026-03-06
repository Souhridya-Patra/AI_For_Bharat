# PowerShell script to start the AI Voice Platform server

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "AI Voice Platform - Starting Server" -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""

# Check if in backend directory
if (Test-Path "backend") {
    Set-Location backend
}

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ Created .env file" -ForegroundColor Green
    Write-Host ""
    Write-Host "Note: Using MOCK synthesis mode for local development" -ForegroundColor Gray
    Write-Host "      Set USE_MOCK_SYNTHESIS=False in .env when SageMaker is ready" -ForegroundColor Gray
    Write-Host ""
}

# Check if dependencies are installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
$pipList = pip list 2>$null
if ($pipList -notmatch "fastapi") {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✓ Dependencies already installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting FastAPI server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Server will be available at:" -ForegroundColor Cyan
Write-Host "  - API: http://localhost:8000" -ForegroundColor White
Write-Host "  - Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "  - Health: http://localhost:8000/health" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Start server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
