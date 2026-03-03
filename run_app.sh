#!/bin/bash
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

if ! command -v streamlit &> /dev/null; then
    echo "Installing requirements..."
    pip install streamlit pandas
fi

echo "Starting Superbowl Ad Rater..."
streamlit run app.py
