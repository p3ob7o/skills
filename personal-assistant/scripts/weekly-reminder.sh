#!/bin/bash
# Weekly Review Reminder
# Triggered Sunday at 19:15 CET

# Display notification
osascript -e 'display notification "Time for your weekly synthesis: review the week, conduct GTD interview, and draft your team post" with title "📊 Weekly Review" sound name "Sosumi"'

# Log the reminder
echo "$(date '+%Y-%m-%d %H:%M:%S') - Weekly review reminder sent" >> ~/Library/Logs/personal-assistant.log
