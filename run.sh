#!/bin/bash

# Exit on error
set -e

# Check if virtual environment exists, create if it doesn't
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install/update package in development mode
echo "Installing package in development mode..."
pip install -e .

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Please create one with your API keys:"
    echo "OPENAI_API_KEY=your_key_here"
    echo "GEMINI_API_KEY=your_key_here"
    exit 1
fi

# Run the main script
echo "Running main application..."
python src/agentic_order_routing/main.py 