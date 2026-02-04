#!/bin/bash

# Doc-Expert Application Setup Script
# This script sets up the Python virtual environment and installs dependencies

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Doc-Expert Application Setup"
echo "=========================================="
echo ""

# Check Python version
echo "🔍 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Check if venv already exists
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists."
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing virtual environment..."
        rm -rf venv
    else
        echo "ℹ️  Using existing virtual environment."
        echo ""
        echo "✅ Setup complete!"
        echo ""
        echo "💡 To activate the environment, run:"
        echo "   source venv/bin/activate"
        echo ""
        echo "💡 Or use the start script:"
        echo "   ./start.sh"
        exit 0
    fi
fi

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null

# Install dependencies
echo "📥 Installing dependencies from requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️  requirements.txt not found. Installing basic dependencies..."
    pip install pymilvus numpy
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📍 Virtual environment created at: $SCRIPT_DIR/venv"
echo ""
echo "💡 To activate the environment manually, run:"
echo "   source venv/bin/activate"
echo ""
echo "💡 To start the application, run:"
echo "   ./start.sh"
echo ""
