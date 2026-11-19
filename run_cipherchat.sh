#!/bin/bash
# ==============================================================================
# CipherChat — Unified Launcher Script
# Starts both the FastAPI Cryptographic Backend (Port 8000)
# and the Vite/React Cybersecurity Frontend (Port 5173)
# ==============================================================================

DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

echo "=========================================================="
echo "🔐 Starting CipherChat Cryptography Platform"
echo "=========================================================="

# Trap to kill both processes on Ctrl+C
cleanup() {
    echo ""
    echo "Shutting down CipherChat services..."
    kill $(jobs -p) 2>/dev/null
    exit
}
trap cleanup SIGINT SIGTERM EXIT

# 1. Start Python FastAPI Backend on Port 8000
echo "🚀 [1/2] Starting FastAPI Backend on http://localhost:8000 ..."
"$DIR/venv/bin/python" "$DIR/cipherchat/backend/main.py" &
BACKEND_PID=$!

# Wait a moment for backend to initialize
sleep 2

# 2. Start Vite React Frontend on Port 5173
echo "✨ [2/2] Starting React/Vite Frontend on http://localhost:5173 ..."
cd "$DIR/cipherchat/frontend"
npm run dev -- --host 0.0.0.0 --port 5173 &
FRONTEND_PID=$!

echo ""
echo "=========================================================="
echo "✅ CipherChat is LIVE!"
echo "👉 Open Web Application: http://localhost:5173"
echo "👉 Backend API Docs:     http://localhost:8000/docs"
echo "=========================================================="
echo "Press Ctrl+C to stop all servers."
echo ""

# Keep running
wait
