#!/bin/bash

# Milvus Docker Stop Script
# This script stops the Milvus standalone setup

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Milvus Vector DB - Stop Script"
echo "=========================================="
echo ""

# Check if containers are running
if ! docker ps --format '{{.Names}}' | grep -q "milvus-standalone\|milvus-etcd\|milvus-minio"; then
    echo "ℹ️  Milvus containers are not running."
    exit 0
fi

echo "🛑 Stopping Milvus containers..."
echo ""

# Stop the containers
docker compose down

echo ""
echo "✅ Milvus containers have been stopped."
echo ""
echo "💡 To start Milvus again, run: ./start.sh"
echo ""
