# Morning Briefing Assistant

A modular morning briefing system for Claude Code that orchestrates your daily preparation workflow across email, Linear, calendar, and Slack.

## Overview

This skill provides an automated morning briefing that helps you start your day prepared by:

1. **Gmail Triage** - Interactive inbox-zero email management with starred email selection
2. **Linear Triage** - Issue prioritization and selection for today's work
3. **Calendar Briefing** - Overview of today's scheduled events
4. **Slack Briefing** - Past 24 hours of Slack activity and @mentions

All results are compiled into your Obsidian daily note and committed to git.

## Architecture

### Orchestrator Pattern

The morning-briefing skill acts as an orchestrator that coordinates four specialized sub-skills. Each sub-skill:
- Handles its own API calls and data processing
- Provides interactive user selection when needed
- Returns formatted markdown content
- Can be used standalone or as part of the full briefing

### Data Flow

```
┌─────────────────┐
│  External Data  │
│  - Calendar     │
│  - Slack        │
│  - Gmail        │
│  - Linear       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│ Morning Briefing│◀────▶│  /meta/ State    │
│ (User-triggered)│      │  - briefing-     │
└────────┬────────┘      │    history.json  │
         │               │  - action-items  │
         ▼               └──────────────────┘
┌─────────────────┐
│ Obsidian Vault  │
│ - Daily notes   │
│ - Conversations │
│ - People        │
│ - Projects      │
└─────────────────┘
```

### Sub-Skills

1. **gmail-triage** - Interactive inbox-zero email triage
   - Categorizes emails into Reply Now/Star/Archive
   - User selects starred emails to handle today

2. **linear-triage** - Interactive Linear issues selection
   - Organizes by priority and status
   - User selects issues to handle today

3. **calendar-briefing** - Today's calendar overview (automated)
   - Shows all events with times, links, attendees

4. **slack-briefing** - Interactive Slack @mentions triage
   - Organizes by priority (DMs from leadership first)
   - User selects mentions to handle today

Each sub-skill can also be used standalone.

## Quick Start

### 1. Setup

Key steps:
- Copy notification scripts to `~/bin/personal-assistant/`
- Set up crontab entry for daily 9:00 AM reminder (optional)
- Grant notification permissions
- Ensure all required MCP servers are configured

### 2. Verify Installation

Check that all components are in place:

```bash
# Check main skill and sub-skills
ls /Users/paolo/.claude/skills/morning-briefing/SKILL.md
ls /Users/paolo/.claude/skills/morning-briefing/*/SKILL.md

# Check state directory
ls /Users/paolo/Totoro/meta/

# Check scripts
ls ~/bin/personal-assistant/
```

### 3. First Run

Manually trigger your first briefing:

```
"Run my morning briefing"
```

Or use the explicit command:
```
/morning-briefing
```

## Usage

### Invoking the Morning Briefing

**Via natural language:**
```
"Run my morning briefing"
"Prepare my day"
"Do my daily briefing"
```

**Via command:**
```
/morning-briefing
```

### Typical Daily Flow

**9:00 AM (local time)** - Optional notification appears
→ Click when ready
→ "Run my morning briefing"
→ Review and interact with each triage step
→ Daily note is automatically updated with your selections

**Throughout Day** - Work on priorities from briefing
→ Reference your daily note for selected tasks
→ Use sub-skills standalone for quick updates

### Using Sub-Skills Independently

Sub-skills can be invoked individually without running the full briefing:

```
"Run gmail-triage"           # Just handle email
"Show my Linear issues"      # Just review Linear
"What's on my calendar?"     # Just see today's events
"Show Slack activity"        # Just check Slack
```

When used standalone, sub-skills perform their function but don't automatically write to your daily note or commit to git.

## State Management

The morning-briefing skill maintains state in `/Users/paolo/Totoro/meta/`:

- `briefing-history.json` - Morning briefing runs and metrics
- `action-items.json` - Cross-skill action items
- `assistant-state.json` - Error logging and skill status

See `/meta/README.md` for detailed schema documentation.

## Integration Points

### Required MCP Servers

- **Google Calendar** - Event fetching and scheduling
- **Gmail** - Email triage and tracking
- **Slack** - Message searching and mention tracking
- **Linear** - Issue querying and updates
- **Obsidian** - Vault file operations

### Obsidian Vault Structure

Expected directories:
- `/YYYY/MM/` - Daily notes (YYYY-MM-DD.md)
- `/YYYY/W/` - Weekly notes (YYYY-Wnn.md)
- `/conversations/` - Meeting summaries
- `/people/` - People profiles
- `/highlights/` - Readwise highlights (read-only)
- `/draft notes/` - P2 post drafts
- `/meta/` - State files
- `/templates/` - Note templates

## Customization

### Adjusting Notification Times

Edit crontab to change reminder times:
```bash
crontab -e
```

### Modifying Sub-Skills

Each sub-skill has a SKILL.md file documenting its workflow. To modify:
1. Edit the SKILL.md in the sub-skill directory
2. Test the changes
3. Update version if needed

### Adding Data Sources

To add new data sources to the briefing:
1. Create a new sub-skill directory with SKILL.md
2. Update the orchestrator to invoke the new sub-skill
3. Add MCP server configuration if needed
4. Update state schemas as required

## Troubleshooting

### Briefing Not Working

1. Check that all MCP servers are running and authenticated
2. View logs: `tail -f ~/Library/Logs/personal-assistant.log`
3. Check state: `cat /Users/paolo/Totoro/meta/assistant-state.json`
4. Try sub-skills individually to isolate issues

### Notifications Not Appearing

1. Test scripts manually: `~/bin/personal-assistant/morning-reminder.sh`
2. Check permissions: System Preferences → Notifications
3. Verify script is executable: `ls -l ~/bin/personal-assistant/`
4. Check crontab: `crontab -l`

### Data Collection Failures

If integrations fail:
- Sub-skills gracefully degrade
- Missing data is noted in output
- Errors logged to `assistant-state.json`
- Briefing continues with available data

### State File Issues

If state files are corrupted:
1. Backup current state
2. Reset to initial state (see `/meta/README.md`)
3. Skills will rebuild from that point

## Maintenance

### Regular Tasks

**Weekly:**
- Review `assistant-state.json` for errors
- Check enrichment queue for pending items
- Archive old completed action items

**Monthly:**
- Review state file sizes
- Archive old history entries if needed
- Verify MCP integrations are working

**Quarterly:**
- Backup state files
- Review and update skill configurations
- Prune old notes archives

### Backups

Create regular backups of state files:
```bash
mkdir -p ~/backups/morning-briefing
rsync -av /Users/paolo/Totoro/meta/ ~/backups/morning-briefing/meta-$(date +%Y%m%d)/
```

## Files Structure

```
/Users/paolo/.claude/skills/morning-briefing/
├── README.md                    # This file
├── SKILL.md                     # Morning briefing orchestrator
├── references/
│   ├── obsidian-integration.md          # Obsidian operations
│   └── sub-skill-coordination.md        # Orchestrator patterns
├── gmail-triage/
│   ├── SKILL.md                 # Email triage workflow
│   └── references/
│       ├── gmail-api.md         # Gmail API details
│       ├── categorization-rules.md      # Email categorization
│       └── error-handling.md    # Troubleshooting
├── linear-triage/
│   ├── SKILL.md                 # Linear issues workflow
│   └── references/
│       ├── linear-api.md        # Linear API details
│       ├── organization-rules.md        # Issue organization
│       └── error-handling.md    # Troubleshooting
├── calendar-briefing/
│   ├── SKILL.md                 # Calendar overview workflow
│   └── references/
│       ├── calendar-api.md      # Google Calendar API
│       └── formatting-rules.md  # Event formatting
├── slack-briefing/
│   ├── SKILL.md                 # Slack activity workflow
│   └── references/
│       ├── slack-api.md         # Slack API details
│       └── filtering-rules.md   # Conversation filtering
└── scripts/
    ├── README.md                # Scripts documentation
    └── morning-reminder.sh      # Morning notification

/Users/paolo/Totoro/meta/
├── README.md                    # State files documentation
├── briefing-history.json        # Morning briefing state
├── action-items.json            # Cross-skill actions
└── assistant-state.json         # General state

/Users/paolo/Totoro/templates/
└── person template.md           # People profile template
```

## Version

**Current Version:** 1.3.0
**Created:** 2025-11-05
**Last Updated:** 2025-11-09

**v1.3.0 Changes:**
- Restructured to make morning-briefing the primary skill
- Moved morning-briefing/SKILL.md to top level
- Moved morning-briefing/references/ to top level
- Removed parent SKILL.md and SETUP.md files
- Updated README.md to reflect Morning Briefing Assistant purpose

**v1.2.0 Changes:**
- Removed evening-reflection, note-enricher, and weekly-review skills
- Simplified system to focus on morning-briefing only
- Removed associated notification scripts and state files
- Updated documentation to reflect current architecture

**v1.1.0 Changes:**
- Refactored morning-briefing into modular orchestrator pattern
- Added 4 sub-skills: gmail-triage, linear-triage, calendar-briefing, slack-briefing
- Implemented progressive disclosure with references/ directories
- Reduced main SKILL.md files by 61% through better organization

## License

This is a personal morning briefing system for private use.

## Support

For issues or questions:
- Review individual SKILL.md files for detailed workflows
- Check `/meta/README.md` for state file schemas
- Review `assistant-state.json` for logged errors
