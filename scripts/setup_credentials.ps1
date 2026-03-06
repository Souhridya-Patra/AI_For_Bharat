# PowerShell script to set up AWS credentials
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host "AWS Credentials Setup for AI Voice Platform" -ForegroundColor Cyan
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 59) -ForegroundColor Cyan
Write-Host ""

# Prompt for credentials
Write-Host "Please enter your AWS credentials:" -ForegroundColor Yellow
Write-Host "(You can find these in your AWS Console or hackathon portal)" -ForegroundColor Gray
Write-Host ""

$accessKey = Read-Host "AWS Access Key ID"
$secretKey = Read-Host "AWS Secret Access Key" -AsSecureString
$secretKeyPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secretKey)
)
$region = Read-Host "AWS Region (default: ap-south-1)"

if ([string]::IsNullOrWhiteSpace($region)) {
    $region = "ap-south-1"
}

Write-Host ""
Write-Host "Setting up credentials..." -ForegroundColor Yellow

# Create .aws directory if it doesn't exist
$awsDir = "$env:USERPROFILE\.aws"
if (-not (Test-Path $awsDir)) {
    New-Item -ItemType Directory -Path $awsDir | Out-Null
    Write-Host "✓ Created .aws directory" -ForegroundColor Green
}

# Create credentials file
$credentialsFile = "$awsDir\credentials"
$credentialsContent = @"
[default]
aws_access_key_id = $accessKey
aws_secret_access_key = $secretKeyPlain
"@

Set-Content -Path $credentialsFile -Value $credentialsContent
Write-Host "✓ Created credentials file: $credentialsFile" -ForegroundColor Green

# Create config file
$configFile = "$awsDir\config"
$configContent = @"
[default]
region = $region
output = json
"@

Set-Content -Path $configFile -Value $configContent
Write-Host "✓ Created config file: $configFile" -ForegroundColor Green

# Set environment variables for current session
$env:AWS_ACCESS_KEY_ID = $accessKey
$env:AWS_SECRET_ACCESS_KEY = $secretKeyPlain
$env:AWS_DEFAULT_REGION = $region

Write-Host "✓ Set environment variables for current session" -ForegroundColor Green

Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Green
Write-Host ("=" * 59) -ForegroundColor Green
Write-Host "✓ AWS Credentials configured successfully!" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Green
Write-Host ("=" * 59) -ForegroundColor Green
Write-Host ""

# Test credentials
Write-Host "Testing AWS connection..." -ForegroundColor Yellow
try {
    python scripts/check_aws_credentials.py
} catch {
    Write-Host "Note: Run 'python scripts/check_aws_credentials.py' to verify" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Run: python scripts/check_aws_credentials.py" -ForegroundColor White
Write-Host "  2. Run: python scripts/setup_aws_infrastructure.py" -ForegroundColor White
Write-Host ""
