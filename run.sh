#!/bin/bash

# =====================================================================
# OpenModelica Two Connected Tanks Simulator - Run Script (Linux/macOS)
# =====================================================================
# This script sets up the Python virtual environment and launches
# the GUI application.
# =====================================================================

set -e

echo ""
echo "OpenModelica Model Simulator - Setup & Run"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or later"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "Python version: $PYTHON_VERSION"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo ""
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Check if dependencies are installed
if ! pip show PyQt6 > /dev/null 2>&1; then
    echo ""
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the application
echo ""
echo "Launching OpenModelica Model Simulator..."
echo ""
python src/app.py

echo ""
echo "Application closed"
