#!/bin/bash
# Evening Reflection Reminder
# Triggered daily at 19:00 CET

# Display notification
osascript -e 'display notification "Time to reflect on your day and capture accomplishments, challenges, and tomorrow priorities" with title "🌙 Evening Reflection" sound name "Glass"'

# Log the reminder
echo "$(date '+%Y-%m-%d %H:%M:%S') - Evening reflection reminder sent" >> ~/Library/Logs/personal-assistant.log
