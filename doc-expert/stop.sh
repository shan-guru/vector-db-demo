#!/bin/bash

# Doc-Expert Application Stop Script
# This script deactivates the virtual environment

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "Doc-Expert Application - Stop"
echo "=========================================="
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "ℹ️  Virtual environment is not currently activated."
    exit 0
fi

echo "🔌 Deactivating virtual environment..."
echo "   Previous environment: $VIRTUAL_ENV"
echo ""

# Deactivate the virtual environment
deactivate 2>/dev/null || true

echo "✅ Virtual environment deactivated."
echo ""
echo "💡 To reactivate, run:"
echo "   ./start.sh"
echo "   or"
echo "   source venv/bin/activate"
echo ""
