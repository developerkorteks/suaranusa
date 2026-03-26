#!/bin/bash
# Detik.com Scheduled Sync Runner - Production VPS Version

# Forced Absolute Configuration
SCRIPT_DIR="/root/suaranusa/detik-dynamic-scraper"
VENV_PATH="/root/suaranusa/venv_detik"
DB_PATH="/root/suaranusa/data/comprehensive_full_test.db"
ARTICLES_PER_DOMAIN=10
LOG_DIR="$SCRIPT_DIR/logs"
LOG_FILE="$LOG_DIR/scheduled_sync_$(date +%Y%m%d).log"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Change to script directory
cd "$SCRIPT_DIR"

echo "========================================" >> "$LOG_FILE"
echo "Scheduled Sync Started: $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Run sync using Absolute DB Path
python3 src/scheduler.py \
    --mode interval \
    --interval 24 \
    --articles-per-domain "$ARTICLES_PER_DOMAIN" \
    --db-path "$DB_PATH" \
    --run-now 2>&1 | tee -a "$LOG_FILE"

EXIT_CODE=$?

echo "========================================" >> "$LOG_FILE"
echo "Sync Completed: $(date)" >> "$LOG_FILE"
echo "Exit Code: $EXIT_CODE" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

exit $EXIT_CODE
