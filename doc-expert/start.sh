#!/bin/bash

# Doc-Expert Application Start Script
# This script activates the virtual environment and starts the application

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Doc-Expert Application - Start"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo ""
    echo "💡 Run setup first:"
    echo "   ./setup.sh"
    exit 1
fi

# Check if virtual environment is already activated
if [ -n "$VIRTUAL_ENV" ]; then
    echo "ℹ️  Virtual environment is already activated: $VIRTUAL_ENV"
else
    echo "🔌 Activating virtual environment..."
    source venv/bin/activate
fi

# Verify activation
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Error: Failed to activate virtual environment."
    exit 1
fi

echo "✅ Virtual environment activated: $VIRTUAL_ENV"
echo ""

# Check Python and pip versions
echo "📊 Environment Information:"
echo "   Python: $(python --version)"
echo "   Pip: $(pip --version | cut -d' ' -f1,2)"
echo ""

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
if ! python -c "import pymilvus" 2>/dev/null; then
    echo "⚠️  Warning: pymilvus is not installed."
    echo "💡 Installing dependencies..."
    pip install -r requirements.txt
fi

echo "✅ All dependencies are installed."
echo ""
echo "🚀 Application environment is ready!"
echo ""
echo "📍 Virtual environment is now active in this shell session."
echo ""
echo "💡 You can now run application scripts:"
echo "   python step3_connect.py"
echo "   python step4_insert_data.py"
echo "   etc."
echo ""
echo "💡 To deactivate the environment, run:"
echo "   deactivate"
echo "   or"
echo "   ./stop.sh"
echo ""
echo "⚠️  Note: This script activates the venv in the current shell."
echo "   To use in a new terminal, run: source venv/bin/activate"
echo ""
