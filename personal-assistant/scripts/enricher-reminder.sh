#!/bin/bash
# Note Enricher Background Process
# Triggered hourly (24/7)

# Check if there are pending items in the queue
QUEUE_FILE="/Users/paolo/Totoro/meta/enrichment-queue.json"

if [ -f "$QUEUE_FILE" ]; then
  # Count pending items
  PENDING_COUNT=$(grep -o '"pending":' "$QUEUE_FILE" | wc -l | tr -d ' ')

  if [ "$PENDING_COUNT" -gt 0 ]; then
    # Display subtle notification only if there are pending items
    osascript -e 'display notification "Background enrichment running - check for pending clarifications" with title "🔄 Note Enricher" sound name "Purr"'
  fi
fi

# Log the run
echo "$(date '+%Y-%m-%d %H:%M:%S') - Note enricher check completed" >> ~/Library/Logs/personal-assistant.log
