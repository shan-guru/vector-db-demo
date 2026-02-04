# Step 1: Run Milvus Using Docker

We use the **official Milvus standalone Docker setup** with Docker Compose.

## Prerequisites

* Docker and Docker Compose installed
* Docker daemon running

## Docker Compose Setup

The project includes Docker setup files in the `docker-setup/` directory:
- `docker-compose.yml` - Sets up:
  - **Milvus Standalone** - The vector database service
  - **etcd** - Metadata storage
  - **MinIO** - Object storage for Milvus data
- `start.sh` - Start/restart script
- `stop.sh` - Stop script

## Start Milvus

### Using the Start Script (Recommended)

```bash
cd docker-setup
./start.sh
```

Or from the project root:

```bash
./docker-setup/start.sh
```

This script will:
- Check if Docker is running
- Start or restart Milvus containers
- Display container status
- Show connection information

### Using Docker Compose Directly

```bash
cd docker-setup
docker compose up -d
```

Or from the project root:

```bash
cd docker-setup && docker compose up -d
```

## Stop Milvus

### Using the Stop Script (Recommended)

```bash
cd docker-setup
./stop.sh
```

Or from the project root:

```bash
./docker-setup/stop.sh
```

### Using Docker Compose Directly

```bash
cd docker-setup
docker compose down
```

## Restart Milvus

The `start.sh` script automatically handles restarting. If containers are already running, it will stop them first and then start fresh:

```bash
cd docker-setup
./start.sh
```

Or manually:

```bash
cd docker-setup
./stop.sh && ./start.sh
```

## Connection Information

Milvus will be available at:

* **Host:** `localhost`
* **Port:** `19530` (gRPC)
* **Health Check:** `http://localhost:9091/healthz`
* **MinIO Console:** `http://localhost:9001` (default credentials: minioadmin/minioadmin)

## Verify Installation

Check if containers are running:

```bash
cd docker-setup
docker compose ps
```

View logs:

```bash
cd docker-setup
docker compose logs -f
```

Check Milvus health:

```bash
curl http://localhost:9091/healthz
```

> This setup uses Milvus v2.3.3 (stable version) and avoids deprecated APIs.
