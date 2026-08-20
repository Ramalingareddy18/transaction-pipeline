# 🐳 Docker Complete Guide

## Docker & Container Deployment

**Read Time**: 15 minutes  
**Audience**: DevOps, Developers, Container Users

---

## 📚 What is Docker?

Docker is containerization technology that packages your entire application and its dependencies into a container that runs the same everywhere.

**Without Docker**
```
Developer Machine
├── Python 3.11
├── PostgreSQL 14
├── All libraries
└── Works perfectly

Production Machine
├── Python 3.10 (different!)
├── PostgreSQL 16 (different!)
├── Missing libraries
└── Breaks!
```

**With Docker**
```
Docker Image (Contains everything)
├── Python 3.11 ✓
├── PostgreSQL 14 ✓
├── All libraries ✓
└── Works everywhere! ✓
```

---

## 🚀 Quick Start with Docker

### Step 1: Install Docker

**Windows**
1. Download: https://docs.docker.com/desktop/install/windows-install/
2. Run installer
3. Restart computer

**macOS**
```bash
brew install docker-desktop
```

**Linux**
```bash
sudo apt-get install docker.io
sudo usermod -aG docker $USER
```

### Step 2: Verify Installation

```bash
docker --version
# Docker version 24.x.x

docker run hello-world
# Verifies Docker works
```

### Step 3: Navigate to Project

```bash
cd /path/to/transaction-pipeline
```

### Step 4: Start All Services

```bash
docker-compose up --build

# This will:
# 1. Build all images
# 2. Create containers
# 3. Start services
# 4. Show logs

# Wait for: "Application startup complete"
```

### Step 5: Access Services

```
API:       http://127.0.0.1:8000
Swagger:   http://127.0.0.1:8000/docs
Dashboard: http://127.0.0.1:8501
```

---

## 🐳 Understanding Docker Files

### Dockerfile

**Purpose**: Blueprint for building a container image

**File**: `Dockerfile`

```dockerfile
# Base image (official Python image)
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s \
    CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Explanation**
```
FROM        Base image to start with
WORKDIR     Directory inside container
COPY        Copy files from host to container
RUN         Execute command during build
EXPOSE      Expose port (documentation)
HEALTHCHECK Define health check
CMD         Command to run when container starts
```

---

### docker-compose.yml

**Purpose**: Define multiple services and how they connect

**File**: `docker-compose.yml`

```yaml
version: '3.9'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:16
    container_name: transaction-db
    environment:
      POSTGRES_DB: transaction_pipeline_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  # FastAPI Application
  api:
    build: .
    container_name: transaction-api
    ports:
      - "8000:8000"
    environment:
      DB_HOST: postgres
      DB_PORT: 5432
      DB_NAME: transaction_pipeline_db
      DB_USER: postgres
      DB_PASSWORD: ${DB_PASSWORD}
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - .:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # Streamlit Dashboard
  dashboard:
    build: .
    container_name: transaction-dash
    ports:
      - "8501:8501"
    environment:
      API_URL: http://api:8000
    depends_on:
      - api
    command: streamlit run dashboard.py --server.address 0.0.0.0

volumes:
  postgres_data:

networks:
  default:
    name: transaction_network
```

**Explanation**
```
services:        List of services (containers)
image:           Pre-built image to use
build:           Build from Dockerfile
ports:           Map host:container ports
environment:     Environment variables
volumes:         Persistent storage
healthcheck:     Check if service is healthy
depends_on:      Service dependencies
command:         Override default command
```

---

## 🔄 Docker Compose Commands

### Common Commands

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d

# Start and see logs
docker-compose up

# Stop services
docker-compose down

# View running containers
docker-compose ps

# View logs
docker-compose logs

# View API logs only
docker-compose logs api

# Follow logs (real-time)
docker-compose logs -f

# Execute command in container
docker-compose exec api python --version

# Stop all services
docker-compose stop

# Remove everything (containers and volumes)
docker-compose down -v
```

---

## 🏗️ Docker Architecture

### Container Isolation

```
Host Machine (Windows/macOS/Linux)
│
├─ Docker Engine
│  │
│  ├─ Container 1 (PostgreSQL)
│  │  ├─ Filesystem (isolated)
│  │  ├─ Processes (isolated)
│  │  ├─ Network (isolated)
│  │  └─ Ports: 5432→5432
│  │
│  ├─ Container 2 (FastAPI)
│  │  ├─ Filesystem (isolated)
│  │  ├─ Processes (isolated)
│  │  ├─ Network (isolated)
│  │  └─ Ports: 8000→8000
│  │
│  └─ Container 3 (Streamlit)
│     ├─ Filesystem (isolated)
│     ├─ Processes (isolated)
│     ├─ Network (isolated)
│     └─ Ports: 8501→8501
│
└─ Bridge Network (Container Communication)
   └─ postgres ↔ api ↔ dashboard
```

---

## 📊 Image vs Container

### Image (Blueprint)

```
Docker Image
├── Read-only template
├── Contains all code/dependencies
├── Built from Dockerfile
├── Stored locally/in registry
└── Can be shared
```

**Commands**
```bash
docker build -t transaction-api .
docker images
docker rmi image-name
```

### Container (Running Instance)

```
Docker Container
├── Running instance of image
├── Has read-write filesystem
├── Can be started/stopped
├── Isolated from other containers
└── Can be deleted
```

**Commands**
```bash
docker run -p 8000:8000 transaction-api
docker ps
docker rm container-name
```

---

## 🔒 Docker Security

### Security Best Practices

```dockerfile
# 1. Run as non-root user
RUN useradd -m appuser
USER appuser

# 2. Use specific versions (not latest)
FROM python:3.11-slim  # ✓ Specific version
FROM python:latest     # ✗ Avoid

# 3. Minimal base image
FROM python:3.11-slim  # ✓ Smaller, fewer vulnerabilities
FROM python:3.11       # ✗ Larger

# 4. Remove unnecessary files
RUN pip install --no-cache-dir -r requirements.txt

# 5. Use secrets for sensitive data
# Don't hardcode passwords in Dockerfile
```

### Environment Variables

```yaml
# Don't do this (visible in build)
RUN echo "PASSWORD=secret" > .env

# Do this instead (from external .env)
environment:
  DB_PASSWORD: ${DB_PASSWORD}
```

---

## 🔧 Development with Docker

### Hot Reload

```yaml
# docker-compose.yml
services:
  api:
    volumes:
      - .:/app  # Mount current directory
    command: uvicorn app.main:app --host 0.0.0.0 --reload
```

Changes to Python files automatically reload!

### Debugging

```bash
# Connect to running container
docker-compose exec api bash

# Inside container:
python
>>> import app
>>> app.main

# Exit
exit()
```

### Viewing Container Logs

```bash
# Real-time logs
docker-compose logs -f api

# Last 100 lines
docker-compose logs --tail 100 api

# With timestamps
docker-compose logs --timestamps api
```

---

## 🚀 Production Deployment

### Multi-Stage Build (Optimized)

```dockerfile
# Stage 1: Build
FROM python:3.11 as builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime (much smaller)
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
COPY . /app
WORKDIR /app
CMD ["python", "app/main.py"]
```

### Production Compose File

```yaml
version: '3.9'

services:
  api:
    image: myregistry/transaction-api:1.0.0
    restart: always
    environment:
      ENVIRONMENT: production
      DEBUG: "false"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

---

## 🐛 Docker Troubleshooting

### Container won't start

```bash
# View error logs
docker-compose logs api

# Check if port is already in use
netstat -tlnp | grep 8000

# Use different port
# In docker-compose.yml:
# ports:
#   - "8001:8000"  # Changed from 8000:8000
```

### Can't reach database from API

```bash
# Check network
docker network ls

# Check network connectivity
docker-compose exec api ping postgres

# Verify database is running
docker-compose ps

# Check environment variables
docker-compose exec api env | grep DB_
```

### Out of disk space

```bash
# Remove unused images
docker image prune

# Remove unused containers
docker container prune

# Remove all unused data
docker system prune

# With volumes (BE CAREFUL)
docker system prune --volumes
```

### Container keeps restarting

```bash
# Check logs
docker-compose logs --tail 50 api

# Increase logging
# Add to docker-compose.yml:
# logging:
#   driver: "json-file"
#   options:
#     max-size: "200k"
#     max-file: "10"
```

---

## 📊 Monitoring Containers

### Resource Usage

```bash
# View real-time stats
docker stats

# Output:
# CONTAINER          CPU %      MEM USAGE / LIMIT
# transaction-api    0.45%      150MiB / 2GiB
# transaction-db     1.23%      200MiB / 2GiB
```

### Health Checks

```bash
# Check health status
docker-compose ps

# Expected:
# NAME              STATUS
# transaction-db    Up (healthy)
# transaction-api   Up (healthy)

# If unhealthy:
docker-compose logs service-name
```

---

## 🔄 Docker Workflow

### Development Workflow

```
1. Make code changes
        ↓
2. Docker detects changes (hot reload)
        ↓
3. Container auto-reloads
        ↓
4. Test in browser
        ↓
5. If working, commit code
        ↓
6. Push to Git
```

### Production Workflow

```
1. Code merged to main
        ↓
2. GitHub Actions builds image
        ↓
3. Image pushed to Docker Hub
        ↓
4. Pull image on production server
        ↓
5. docker-compose pull
6. docker-compose up -d
        ↓
7. Running in production
```

---

## 📦 Docker Registry

### Docker Hub (Public Registry)

```bash
# Login
docker login

# Push image
docker tag transaction-api:latest myusername/transaction-api:1.0.0
docker push myusername/transaction-api:1.0.0

# Pull image
docker pull myusername/transaction-api:1.0.0
```

### Private Registry

```bash
# Configure in docker-compose.yml
services:
  api:
    image: myregistry.com/transaction-api:1.0.0
```

---

## 💡 Docker Best Practices

```
✓ Use specific base image versions
✓ Use .dockerignore to exclude files
✓ Minimize layer count
✓ Use multi-stage builds for production
✓ Keep images small
✓ Run as non-root user
✓ Set resource limits
✓ Enable restart policies
✓ Use health checks
✓ Log properly
✗ Don't hardcode secrets
✗ Don't run as root
✗ Don't use latest tag in production
✗ Don't mount entire filesystem
```

---

## 📚 Related Documentation

- **[DOCS_INDEX.md](DOCS_INDEX.md)** — All documentation
- **[7_DEPLOYMENT_GUIDE.md](7_DEPLOYMENT_GUIDE.md)** — Deployment
- **[1_QUICKSTART.md](1_QUICKSTART.md)** — Quick start
- **[12_MONITORING_HEALTH.md](12_MONITORING_HEALTH.md)** — Monitoring

---

**Docker is powerful, containerize everything!** 🐳✨

**Back to Documentation**: [← DOCS_INDEX.md](DOCS_INDEX.md)
