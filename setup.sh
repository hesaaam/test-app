#!/bin/bash

# User Profile REST API Setup Script
echo "🚀 Setting up User Profile REST API"
echo "====================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.12 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "📦 Installing pip3..."
    apt update && apt install -y python3-pip
fi

echo "✅ pip3 found"

# Create virtual environment
echo "📁 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment and install dependencies
echo "📦 Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt
pip install requests  # For testing

echo "✅ Dependencies installed successfully"

# Make scripts executable
chmod +x curl_demo.sh
echo "✅ Scripts made executable"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To start the API server:"
echo "source venv/bin/activate && python app.py"
echo ""
echo "To run tests:"
echo "source venv/bin/activate && python test_api.py"
echo ""
echo "To run demo:"
echo "source venv/bin/activate && python demo_api.py"
echo ""
echo "To run curl demo:"
echo "./curl_demo.sh"