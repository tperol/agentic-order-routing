#!/bin/bash

# This script starts the Flask API server and the frontend HTTP server
# for the Fabric Intelligence application.

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# Frontend server details
FRONTEND_PORT=8000
FRONTEND_URL="http://localhost:${FRONTEND_PORT}"

# Backend server details (from api_server.py)
BACKEND_PORT=5001 # Ensure this matches api_server.py

# --- Start Frontend Server (in the background) ---
echo "Starting Frontend HTTP server on port ${FRONTEND_PORT}..."
# Run from the project root, as index.html is there.
cd "${SCRIPT_DIR}" || exit
python -m http.server ${FRONTEND_PORT} & # Run in background
FRONTEND_PID=$!
echo "Frontend HTTP server started with PID: ${FRONTEND_PID}"

# Give it a moment to start (optional, but can be helpful)
sleep 1 

# --- Start Backend API Server (in the foreground) ---
# Set PYTHONPATH to include the src directory, relative to the script's location
export PYTHONPATH="${SCRIPT_DIR}/src"

echo ""
echo "Starting Backend Flask API server on port ${BACKEND_PORT}..."
echo "PYTHONPATH set to: ${PYTHONPATH}"

echo ""
echo "-----------------------------------------------------"
echo "UI will be accessible at: ${FRONTEND_URL}"
echo "-----------------------------------------------------"
echo ""

# Ensure your virtual environment is activated if you use one, 
# or that Flask and other dependencies are globally available.
python "${SCRIPT_DIR}/src/api_server.py"

# --- Cleanup (optional, when Flask server is stopped) ---
# This part will run if the Flask server (foreground process) is stopped (e.g., Ctrl+C)
echo ""
echo "Flask API server stopped."
if kill -0 ${FRONTEND_PID} 2>/dev/null; then
    echo "Stopping Frontend HTTP server (PID: ${FRONTEND_PID})..."
    kill ${FRONTEND_PID}
else
    echo "Frontend HTTP server (PID: ${FRONTEND_PID}) already stopped."
fi

echo "Application shutdown complete."

# To make this script executable: chmod +x run.sh
# Then run it with: ./run.sh 