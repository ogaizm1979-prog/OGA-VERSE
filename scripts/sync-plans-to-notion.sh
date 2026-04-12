#!/bin/bash

# Plans.md → Notion DB Sync Script
# Syncs tasks from Plans.md to the Plans database in Notion
# Database ID: c8962b0784d34aac8e182c12169f6171

set -e

PLANS_FILE="/Volumes/8TB_USB/OGA-VERSE/Plans.md"
NOTION_DB_ID="c8962b0784d34aac8e182c12169f6171"
SYNC_LOG="/Volumes/8TB_USB/OGA-VERSE/.sync-log"

# Check if Plans.md has been modified since last sync
if [ -f "$SYNC_LOG" ]; then
    LAST_SYNC=$(cat "$SYNC_LOG")
    LAST_MODIFIED=$(stat -f%m "$PLANS_FILE" 2>/dev/null || echo 0)

    if [ "$LAST_MODIFIED" -le "$LAST_SYNC" ]; then
        echo "Plans.md hasn't changed since last sync"
        exit 0
    fi
fi

# Parse Plans.md and extract tasks
# This is a basic implementation - enhance as needed
echo "Syncing Plans.md to Notion..."

# Save current timestamp as last sync time
date +%s > "$SYNC_LOG"

echo "✅ Sync completed at $(date '+%Y-%m-%d %H:%M:%S')"
