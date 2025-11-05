# Personal Assistant Notification Scripts

These scripts are triggered by cron to send notification reminders for each skill.

## Scripts

### `morning-reminder.sh`
**Trigger:** Daily at 9:00 CET
**Purpose:** Sends notification reminder for morning briefing
**Notification:** "☀️ Morning Briefing" with description about day preparation

### `evening-reminder.sh`
**Trigger:** Daily at 19:00 CET
**Purpose:** Sends notification reminder for evening reflection
**Notification:** "🌙 Evening Reflection" with description about daily recap

### `weekly-reminder.sh`
**Trigger:** Sunday at 19:15 CET
**Purpose:** Sends notification reminder for weekly review
**Notification:** "📊 Weekly Review" with description about weekly synthesis

### `enricher-reminder.sh`
**Trigger:** Hourly (24/7)
**Purpose:** Checks enrichment queue and sends notification if items pending
**Notification:** "🔄 Note Enricher" (only if pending items exist)

## Installation

1. Copy scripts to `~/bin/personal-assistant/`:
   ```bash
   mkdir -p ~/bin/personal-assistant
   cp /Users/paolo/.claude/skills/personal-assistant/scripts/*.sh ~/bin/personal-assistant/
   chmod +x ~/bin/personal-assistant/*.sh
   ```

2. Add to crontab (see SETUP.md for full instructions):
   ```bash
   crontab -e
   ```

## Logging

All scripts log to `~/Library/Logs/personal-assistant.log`:
- Timestamp of each reminder
- Which skill was triggered
- Queue status (for enricher)

View logs:
```bash
tail -f ~/Library/Logs/personal-assistant.log
```

## Testing

Test each script manually:
```bash
~/bin/personal-assistant/morning-reminder.sh
~/bin/personal-assistant/evening-reminder.sh
~/bin/personal-assistant/weekly-reminder.sh
~/bin/personal-assistant/enricher-reminder.sh
```

You should see a notification appear on your screen.

## Customization

### Change Notification Sound

Edit the script and modify the `sound name` parameter:
- "Glass" - gentle chime
- "Sosumi" - alert sound
- "Purr" - subtle notification
- "Ping" - quick ping
- "Hero" - triumphant sound

Available sounds: `/System/Library/Sounds/`

### Change Notification Text

Edit the notification text in the script:
```bash
osascript -e 'display notification "Your custom message" with title "Title" sound name "Sound"'
```

### Disable Notifications

To run skills without notifications, comment out the osascript line:
```bash
# osascript -e 'display notification...'
```

## Troubleshooting

### Notification Permissions

If notifications don't appear:
1. System Preferences → Notifications & Focus
2. Find "Script Editor" or "osascript"
3. Enable notifications

### Cron Issues

If cron doesn't trigger:
1. Verify crontab: `crontab -l`
2. Check cron is running: `ps aux | grep cron`
3. View system logs: `tail -f /var/log/system.log | grep cron`

### Script Errors

Check the log file for errors:
```bash
tail -100 ~/Library/Logs/personal-assistant.log
```

Test script manually to see error output:
```bash
bash -x ~/bin/personal-assistant/morning-reminder.sh
```

## macOS Specifics

These scripts use `osascript`, which is macOS-specific. For other platforms:
- Linux: Use `notify-send` or `zenity`
- Windows: Use PowerShell toast notifications or `msg`

## Security

These scripts:
- Only send notifications (read-only on system)
- Log to user's home directory
- Require no special permissions beyond notification access
- Don't access sensitive data directly
