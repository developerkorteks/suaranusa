#!/bin/bash
# Run Streamlit Dashboard

cd "$(dirname "$0")"
source ../venv_detik/bin/activate

echo "🚀 Starting Detik Dynamic Scraper Dashboard..."
echo ""
echo "Dashboard will be available at:"
echo "  → http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo ""

streamlit run dashboard.py
