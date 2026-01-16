#!/bin/bash

# Linux/macOS Test Runner Script for fake-useragent
# This script installs dependencies and runs all tests

echo ""
echo "================================================"
echo "fake-useragent Test Runner"
echo "================================================"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check Python is available
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python is not installed or not in PATH"
        echo "Please install Python 3.6+ and ensure it's added to your PATH"
        exit 1
    fi
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

$PYTHON_CMD --version

# Check if pip is available
echo ""
echo "Checking pip installation..."
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "ERROR: pip is not available"
    echo "Please ensure pip is installed with Python"
    exit 1
fi

# Create requirements.txt
echo ""
echo "Creating requirements.txt if needed..."
cat > requirements.txt << 'EOF'
pytest
pytest-cov
EOF

# Install dependencies
echo ""
echo "Installing test dependencies..."
$PYTHON_CMD -m pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo "Dependencies installed successfully!"

# Run tests
echo ""
echo "================================================"
echo "Running Tests"
echo "================================================"
echo ""

$PYTHON_CMD -m pytest src/test_fake.py -v

# Capture exit code
if [ $? -ne 0 ]; then
    echo ""
    echo "================================================"
    echo "TEST EXECUTION FAILED"
    echo "================================================"
    exit 1
else
    echo ""
    echo "================================================"
    echo "ALL TESTS PASSED!"
    echo "================================================"
    exit 0
fi
