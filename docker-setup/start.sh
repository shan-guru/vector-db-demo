#!/bin/bash

# Milvus Docker Start/Restart Script
# This script starts or restarts the Milvus standalone setup

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Milvus Vector DB - Start/Restart Script"
echo "=========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Check if containers are already running
if docker ps --format '{{.Names}}' | grep -q "milvus-standalone\|milvus-etcd\|milvus-minio"; then
    echo "🔄 Milvus containers are already running. Restarting..."
    docker compose down
    sleep 2
fi

echo "🚀 Starting Milvus standalone setup..."
echo ""

# Start the containers
docker compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check container status
echo ""
echo "📊 Container Status:"
docker compose ps

echo ""
echo "✅ Milvus is starting up!"
echo ""
echo "📍 Milvus will be available at:"
echo "   - Host: localhost"
echo "   - Port: 19530"
echo "   - Health Check: http://localhost:9091/healthz"
echo ""
echo "💡 To view logs, run: docker compose logs -f"
echo "💡 To stop Milvus, run: ./stop.sh"
echo ""
