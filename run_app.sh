#!/bin/bash
# Deep Learning & Chaotic Cryptography UI Launcher
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

if [ -f "$DIR/venv/bin/streamlit" ]; then
    "$DIR/venv/bin/streamlit" run app.py
else
    streamlit run app.py
fi
