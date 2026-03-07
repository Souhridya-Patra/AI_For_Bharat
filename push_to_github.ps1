# Push AI Voice Platform to GitHub

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Push AI Voice Platform to GitHub" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (-not (Test-Path ".git")) {
    Write-Host "Initializing git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✓ Git initialized" -ForegroundColor Green
    Write-Host ""
}

# Check if remote exists
$remotes = git remote
if ($remotes -notcontains "origin") {
    Write-Host "Please enter your GitHub repository URL:" -ForegroundColor Yellow
    Write-Host "Example: https://github.com/yourusername/ai-voice-platform.git" -ForegroundColor Gray
    $repoUrl = Read-Host "Repository URL"
    
    git remote add origin $repoUrl
    Write-Host "✓ Remote added" -ForegroundColor Green
    Write-Host ""
}

# Create .gitignore if it doesn't exist
if (-not (Test-Path ".gitignore")) {
    Write-Host "Creating .gitignore..." -ForegroundColor Yellow
    
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
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# AWS
.aws/

# Logs
*.log
"@ | Out-File -FilePath ".gitignore" -Encoding utf8
    
    Write-Host "✓ .gitignore created" -ForegroundColor Green
    Write-Host ""
}

# Add all files
Write-Host "Adding files to git..." -ForegroundColor Yellow
git add .
Write-Host "✓ Files added" -ForegroundColor Green
Write-Host ""

# Commit
Write-Host "Enter commit message (or press Enter for default):" -ForegroundColor Yellow
$commitMsg = Read-Host "Commit message"
if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $commitMsg = "Deploy AI Voice Platform for AWS Hackathon"
}

git commit -m $commitMsg
Write-Host "✓ Changes committed" -ForegroundColor Green
Write-Host ""

# Push
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
Write-Host ""

$branch = git branch --show-current
if ([string]::IsNullOrWhiteSpace($branch)) {
    $branch = "main"
    git branch -M main
}

git push -u origin $branch

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "✓ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Go to your EC2 instance" -ForegroundColor White
    Write-Host "2. Clone the repository:" -ForegroundColor White
    Write-Host "   git clone YOUR_REPO_URL" -ForegroundColor Gray
    Write-Host "3. Follow DEPLOY_TO_EC2_NOW.md" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "✗ Push failed. Please check your credentials and try again." -ForegroundColor Red
    Write-Host ""
    Write-Host "If this is your first push, you may need to:" -ForegroundColor Yellow
    Write-Host "1. Create a repository on GitHub" -ForegroundColor White
    Write-Host "2. Set up authentication (Personal Access Token or SSH)" -ForegroundColor White
    Write-Host ""
}
