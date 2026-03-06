# Upload project to GitHub
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Upload to GitHub" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
$gitInstalled = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitInstalled) {
    Write-Host "Git is not installed!" -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Git is installed" -ForegroundColor Green
Write-Host ""

# Get GitHub username
$username = Read-Host "Enter your GitHub username"

# Get repository name (default: ai-voice-platform)
$repo = Read-Host "Enter repository name (default: ai-voice-platform)"
if ([string]::IsNullOrWhiteSpace($repo)) {
    $repo = "ai-voice-platform"
}

Write-Host ""
Write-Host "Repository will be created at:" -ForegroundColor Yellow
Write-Host "https://github.com/$username/$repo" -ForegroundColor White
Write-Host ""
Write-Host "Make sure you've created this repository on GitHub first!" -ForegroundColor Yellow
Write-Host "Go to: https://github.com/new" -ForegroundColor Cyan
Write-Host ""
$continue = Read-Host "Have you created the repository? (y/n)"

if ($continue -ne "y") {
    Write-Host "Please create the repository first, then run this script again." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Initializing git..." -ForegroundColor Yellow

# Initialize git if not already
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✓ Git initialized" -ForegroundColor Green
} else {
    Write-Host "✓ Git already initialized" -ForegroundColor Green
}

# Create .gitignore if it doesn't exist
if (-not (Test-Path ".gitignore")) {
    @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/

# Environment
.env
*.pem
*.key

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Host "✓ Created .gitignore" -ForegroundColor Green
}

Write-Host ""
Write-Host "Adding files..." -ForegroundColor Yellow
git add .

Write-Host "Committing..." -ForegroundColor Yellow
git commit -m "Initial commit - AI Voice Platform for Indian Languages"

Write-Host "Adding remote..." -ForegroundColor Yellow
$remoteUrl = "https://github.com/$username/$repo.git"
git remote remove origin 2>$null
git remote add origin $remoteUrl

Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
git branch -M main
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "✓ Successfully uploaded to GitHub!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your repository:" -ForegroundColor Cyan
    Write-Host "https://github.com/$username/$repo" -ForegroundColor White
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Verify code is on GitHub" -ForegroundColor White
    Write-Host "2. Follow EC2_DEPLOYMENT_STEPS.md to deploy" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "✗ Upload failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "1. Repository doesn't exist - create it at https://github.com/new" -ForegroundColor White
    Write-Host "2. Authentication failed - you may need to use a Personal Access Token" -ForegroundColor White
    Write-Host "   Generate one at: https://github.com/settings/tokens" -ForegroundColor Cyan
    Write-Host ""
}
