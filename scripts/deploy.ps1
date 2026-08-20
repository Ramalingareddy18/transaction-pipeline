# Deployment script for the Transaction Pipeline on Windows Docker
# Usage: .\scripts\deploy.ps1 -Environment development
# Usage: .\scripts\deploy.ps1 -Environment production

param(
    [string]$Environment = "development"
)

$ErrorActionPreference = "Stop"

Write-Host "================================================"
Write-Host "Transaction Pipeline Docker Deployment (Windows)"
Write-Host "================================================"

# Check Docker is installed
$dockerCheck = docker --version 2>$null
if (!$dockerCheck) {
    Write-Host "✗ Docker is not installed. Please install Docker Desktop for Windows."
    exit 1
}
Write-Host "✓ Docker is installed: $dockerCheck"

# Check Docker Compose is installed
$composeCheck = docker-compose --version 2>$null
if (!$composeCheck) {
    Write-Host "✗ Docker Compose is not installed."
    exit 1
}
Write-Host "✓ Docker Compose is installed: $composeCheck"

# Determine compose file
if ($Environment -eq "production") {
    $ComposeFile = "docker-compose.prod.yml"
    Write-Host "Deploying in PRODUCTION mode"
} else {
    $ComposeFile = "docker-compose.yml"
    Write-Host "Deploying in DEVELOPMENT mode"
}

# Check .env file
if (!(Test-Path ".env")) {
    Write-Host "✗ .env file not found. Creating from .env.example..."
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "⚠ .env created. Please update with your values."
        Write-Host "Press Enter after updating .env to continue..."
        Read-Host
    } else {
        Write-Host "✗ .env.example not found."
        exit 1
    }
}

Write-Host "Building Docker images..."
docker-compose -f $ComposeFile build
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Docker build failed"
    exit 1
}

Write-Host "Starting services..."
docker-compose -f $ComposeFile up -d
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to start services"
    exit 1
}

Write-Host "Waiting for services to be healthy..."
Start-Sleep -Seconds 10

# Check service health
Write-Host "Checking service health..."
$apiHealth = docker-compose -f $ComposeFile exec -T api curl -s http://localhost:8000/health
if ($apiHealth -match "ok") {
    Write-Host "✓ API is healthy"
} else {
    Write-Host "✗ API health check failed"
}

$dbHealth = docker-compose -f $ComposeFile exec -T postgres pg_isready -U postgres -d transaction_pipeline_db
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Database is healthy"
} else {
    Write-Host "✗ Database health check failed"
}

Write-Host ""
Write-Host "================================================"
Write-Host "Deployment Complete!"
Write-Host "================================================"
Write-Host "API: http://localhost:8000"
Write-Host "Dashboard: http://localhost:8501"
Write-Host "Database: localhost:5432"
Write-Host ""
Write-Host "View logs:"
Write-Host "  docker-compose -f $ComposeFile logs -f"
Write-Host ""
Write-Host "Stop services:"
Write-Host "  docker-compose -f $ComposeFile down"
Write-Host "================================================"
