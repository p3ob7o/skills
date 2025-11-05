#!/bin/bash
# Morning Briefing Reminder
# Triggered daily at 9:00 CET

# Display notification
osascript -e 'display notification "Ready to prepare your day with calendar, emails, Slack mentions, and Linear issues" with title "☀️ Morning Briefing" sound name "Glass"'

# Log the reminder
echo "$(date '+%Y-%m-%d %H:%M:%S') - Morning briefing reminder sent" >> ~/Library/Logs/personal-assistant.log
