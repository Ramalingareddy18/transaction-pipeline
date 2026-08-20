#!/bin/bash
# Deployment script for the Transaction Pipeline on Docker

set -e

echo "================================================"
echo "Transaction Pipeline Docker Deployment"
echo "================================================"

# Check Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "✗ Docker is not installed. Please install Docker."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "✗ Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi

echo "✓ Docker and Docker Compose are installed"

# Determine deployment environment
ENV=${1:-development}

if [ "$ENV" = "production" ]; then
    COMPOSE_FILE="docker-compose.prod.yml"
    echo "Deploying in PRODUCTION mode"
else
    COMPOSE_FILE="docker-compose.yml"
    echo "Deploying in DEVELOPMENT mode"
fi

# Check .env file
if [ ! -f ".env" ]; then
    echo "✗ .env file not found. Creating from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "⚠ .env created. Please update with your values."
        echo "Pausing for manual .env configuration..."
        read -p "Press Enter after updating .env"
    else
        echo "✗ .env.example not found either."
        exit 1
    fi
fi

echo "Building Docker images..."
docker-compose -f "$COMPOSE_FILE" build

echo "Starting services..."
docker-compose -f "$COMPOSE_FILE" up -d

echo "Waiting for services to be healthy..."
sleep 10

# Check service health
echo "Checking service health..."
api_health=$(docker-compose -f "$COMPOSE_FILE" exec -T api curl -s http://localhost:8000/health || echo '{}')
if echo "$api_health" | grep -q "ok"; then
    echo "✓ API is healthy"
else
    echo "✗ API health check failed"
fi

db_health=$(docker-compose -f "$COMPOSE_FILE" exec -T postgres pg_isready -U postgres -d transaction_pipeline_db > /dev/null 2>&1 && echo "ok" || echo "fail")
if [ "$db_health" = "ok" ]; then
    echo "✓ Database is healthy"
else
    echo "✗ Database health check failed"
fi

echo ""
echo "================================================"
echo "Deployment Complete!"
echo "================================================"
echo "API: http://localhost:8000"
echo "Dashboard: http://localhost:8501"
echo "Database: localhost:5432"
echo ""
echo "View logs:"
echo "  docker-compose -f $COMPOSE_FILE logs -f"
echo ""
echo "Stop services:"
echo "  docker-compose -f $COMPOSE_FILE down"
echo "================================================"
