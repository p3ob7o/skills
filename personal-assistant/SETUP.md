# Personal Assistant System - Setup Guide

This guide will help you set up the automated scheduling for your personal assistant skills.

## Overview

The personal assistant system consists of four automated skills:

1. **Morning Briefing** - Runs daily at 9:00 local time
2. **Evening Reflection** - Runs daily at 19:00 local time
3. **Note Enricher** - Runs hourly (24/7)
4. **Weekly Review** - Runs Sunday at 19:15 local time

Each skill is triggered by a cron job that sends a notification reminder. You can then invoke the skill when you're ready (allowing you to snooze if needed).

## Prerequisites

- macOS with terminal access
- Claude Code CLI installed
- Obsidian vault set up at `/Users/paolo/Totoro`
- MCP servers configured (Google Calendar, Gmail, Slack, Linear, Obsidian)

## Installation Steps

### 1. Copy Notification Scripts

Copy the notification scripts from this directory to a convenient location:

```bash
mkdir -p ~/bin/personal-assistant
cp /Users/paolo/.claude/skills/personal-assistant/scripts/*.sh ~/bin/personal-assistant/
chmod +x ~/bin/personal-assistant/*.sh
```

### 2. Set Up Crontab

Open your crontab for editing:

```bash
crontab -e
```

Add the following entries (adjust paths as needed):

```cron
# Personal Assistant System Cron Jobs
# All times are in your computer's local timezone

# Morning Briefing - 9:00 daily (local time)
0 9 * * * ~/bin/personal-assistant/morning-reminder.sh

# Evening Reflection - 19:00 daily (local time)
0 19 * * * ~/bin/personal-assistant/evening-reminder.sh

# Weekly Review - Sunday 19:15 (local time)
15 19 * * 0 ~/bin/personal-assistant/weekly-reminder.sh

# Note Enricher - hourly (24/7)
0 * * * * ~/bin/personal-assistant/enricher-reminder.sh
```

**Note**: All times use your computer's local timezone, so the skills automatically adjust when you travel across time zones.

### 3. Grant Notification Permissions

The first time you run a notification script, macOS will ask for permission. Grant it to allow the notifications to appear.

## How It Works

### Notification Flow

1. **Cron triggers** at the scheduled time
2. **Notification appears** on your screen with the skill name
3. **You click the notification** when ready (or dismiss to snooze)
4. **Invoke the skill** manually in Claude Code when you're ready:
   - Morning: `/morning-briefing` or "Run my morning briefing"
   - Evening: `/evening-reflection` or "Run my evening reflection"
   - Weekly: `/weekly-review` or "Run my weekly review"

### Note Enricher

The note enricher runs automatically in the background every hour. It doesn't require your interaction unless it has questions for you (stored in the enrichment queue).

## Invoking Skills

### Via Command

You can invoke skills explicitly by name:
- `/morning-briefing`
- `/evening-reflection`
- `/weekly-review`

### Via Natural Language

Or simply tell Claude what you want:
- "Run my morning briefing"
- "Do my evening reflection"
- "Create my weekly review"
- "Help me process new notes" (for note enricher)

## Customization

### Adjusting Times

To change when skills run, edit your crontab:

```bash
crontab -e
```

Modify the time values. Cron format:
```
minute hour day month day_of_week command
```

Examples:
- `0 8 * * *` = 8:00 AM daily
- `30 18 * * *` = 6:30 PM daily
- `0 20 * * 0` = 8:00 PM Sundays only

### Disabling Skills

To temporarily disable a skill, comment out its cron line:

```cron
# 0 9 * * * TZ="Europe/Paris" ~/bin/personal-assistant/morning-reminder.sh
```

To permanently disable, remove the line from crontab.

## Troubleshooting

### Notifications Not Appearing

1. Check if the script is executable:
   ```bash
   ls -l ~/bin/personal-assistant/*.sh
   ```
   They should show `-rwxr-xr-x`.

2. Check notification permissions:
   - System Preferences → Notifications
   - Find "terminal-notifier" or "Script Editor"
   - Ensure notifications are allowed

3. Test the script manually:
   ```bash
   ~/bin/personal-assistant/morning-reminder.sh
   ```

### Cron Not Running

1. Check if cron is running:
   ```bash
   ps aux | grep cron
   ```

2. Check crontab syntax:
   ```bash
   crontab -l
   ```

3. View cron logs (if available):
   ```bash
   tail -f /var/log/system.log | grep cron
   ```

### Wrong Timezone

If times are off, verify your system timezone:
```bash
date
```

The cron jobs use your computer's local timezone, so they automatically adjust when you travel. To change your system timezone:
- System Preferences → Date & Time → Time Zone
- Or use: `sudo systemsetup -settimezone <timezone>`

## State Files

The system maintains state in `/Users/paolo/Totoro/meta/`:

- `briefing-history.json` - Morning briefing runs
- `daily-reflections.json` - Evening reflection runs
- `enrichment-queue.json` - Note enricher queue
- `assistant-state.json` - General system state
- `weekly-reviews/` - Weekly review states

These files track history and help skills maintain context across runs.

## Backup

Consider backing up your state files regularly:

```bash
# Create backup directory
mkdir -p ~/backups/personal-assistant

# Backup script (run weekly)
rsync -av /Users/paolo/Totoro/meta/ ~/backups/personal-assistant/meta-$(date +%Y%m%d)/
```

## Uninstallation

To remove the personal assistant system:

1. Remove cron entries:
   ```bash
   crontab -e
   # Delete the personal assistant lines
   ```

2. Remove scripts:
   ```bash
   rm -rf ~/bin/personal-assistant
   ```

3. (Optional) Remove state files:
   ```bash
   # Be careful - this deletes history
   rm -rf /Users/paolo/Totoro/meta
   ```

4. Remove skills:
   ```bash
   rm -rf /Users/paolo/.claude/skills/personal-assistant
   ```

## Support

For issues or questions:
- Check the individual skill SKILL.md files for details
- Review state files in `/meta/` for errors
- Check `assistant-state.json` for logged errors

## Updates

To update the skills:
1. Replace skill directories with new versions
2. State files are forward-compatible (version tracked)
3. Restart any running processes
4. No crontab changes needed unless scheduling changes
