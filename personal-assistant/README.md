# Personal Assistant System

A comprehensive, modular personal assistant system for Claude Code that provides automated daily preparation, evening synthesis, continuous note enrichment, and weekly review capabilities.

## Overview

This system consists of four specialized skills that work together to manage your daily workflow, enhance your knowledge base, and provide intelligent summaries:

1. **Morning Briefing** - Prepare your day (9:00 local time daily)
2. **Evening Reflection** - Close your day (19:00 local time daily)
3. **Note Enricher** - Enhance notes continuously (hourly, 24/7)
4. **Weekly Review** - Synthesize your week (Sunday 19:15 local time)

## Architecture

### Modular Design

Each skill is self-contained with:
- Complete workflow documentation (SKILL.md)
- Clear integration patterns
- State management
- Error handling

Skills communicate through:
- Shared state files in `/meta/`
- Obsidian vault structure
- MCP integrations

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
│ (Daily 9:00)    │      │  - briefing-     │
└────────┬────────┘      │    history.json  │
         │               │  - action-items  │
         ▼               │  - enrichment-   │
┌─────────────────┐      │    queue.json    │
│ Daily Work      │      └──────────────────┘
│ - Meetings      │               ▲
│ - Tasks         │               │
│ - Communications│               │
└────────┬────────┘               │
         │                        │
         ▼                        │
┌─────────────────┐               │
│Evening Reflection│◀─────────────┘
│ (Daily 19:00)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────────┐
│ Obsidian Vault  │◀────▶│  Note Enricher   │
│ - Daily notes   │      │  (Hourly)        │
│ - Conversations │      └──────────────────┘
│ - People        │               ▲
│ - Projects      │               │
└────────┬────────┘               │
         │                        │
         ▼                        │
┌─────────────────┐               │
│ Weekly Review   │───────────────┘
│ (Sun 19:15)     │
└─────────────────┘
```

## Quick Start

### 1. Setup

Follow the installation guide:

```bash
# View setup instructions
cat /Users/paolo/.claude/skills/personal-assistant/SETUP.md
```

Key steps:
- Copy notification scripts to `~/bin/personal-assistant/`
- Set up crontab entries
- Grant notification permissions

### 2. Verify Installation

Check that all components are in place:

```bash
# Check skills
ls /Users/paolo/.claude/skills/personal-assistant/*/SKILL.md

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

## Skills

### Morning Briefing
**When:** Daily 9:00 local time
**Duration:** ~2 minutes (automated)
**Purpose:** Prepare your day

Collects and prioritizes:
- Google Calendar events
- Linear issues (assigned/subscribed/mentioned)
- Gmail inbox (starred + triage)
- Slack mentions (overnight)
- Carry-over items from yesterday

Applies three-layer prioritization:
1. Eisenhower Matrix (Urgent/Important)
2. Temporal Buckets (Now/Next/Later)
3. Energy-Based (Deep/Shallow work)

**Output:** Daily note with structured briefing

### Evening Reflection
**When:** Daily 19:00 local time
**Duration:** ~10 minutes (interactive)
**Purpose:** Close your day

Interactive interview covering:
- Overall sentiment
- Accomplishments (planned + unplanned)
- Blockers and challenges
- Key interactions
- Tomorrow's priorities
- Action items

**Output:** Evening reflection appended to daily note, state updates

### Note Enricher
**When:** Hourly (24/7)
**Duration:** ~5 minutes per batch (automated)
**Purpose:** Continuously enhance knowledge base

Processes:
- New meeting summaries in `/conversations/`
- People profiles in `/people/`
- Adds structured sections
- Queues clarification questions
- Updates interaction history

**Output:** Enhanced notes, updated profiles, enrichment queue

### Weekly Review
**When:** Sunday 19:15 local time
**Duration:** ~20 minutes (interactive)
**Purpose:** Synthesize the week

Aggregates data from:
- 7 daily notes (Monday-Sunday)
- Highlights (domain industry news)
- Linear sprint metrics
- Calendar summary
- Conversations

Conducts GTD-style interview with 7 questions

**Outputs:**
1. Weekly note at `/YYYY/W/YYYY-Wnn.md`
2. P2 post draft at `/draft notes/P2 - Week NN.md`

## State Management

All skills maintain state in `/Users/paolo/Totoro/meta/`:

- `briefing-history.json` - Morning briefing runs and metrics
- `daily-reflections.json` - Evening reflection history
- `enrichment-queue.json` - Pending enrichments and clarifications
- `action-items.json` - Cross-skill action items
- `assistant-state.json` - Error logging and skill status
- `weekly-reviews/` - Per-week review states

See `/meta/README.md` for detailed schema documentation.

## Integration Points

### MCP Servers Required

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

## Usage

### Invoking Skills

**Via command:**
```
/morning-briefing
/evening-reflection
/weekly-review
```

**Via natural language:**
```
"Run my morning briefing"
"Do my evening reflection"
"Create my weekly review"
"Help me process new notes"
```

### Typical Daily Flow

**9:00 AM (local time)** - Notification appears
→ Click when ready
→ "Run my morning briefing"
→ Review and start your day

**Throughout Day** - Work on priorities from briefing
→ Note enricher runs hourly in background
→ Continue normal workflow

**7:00 PM (local time)** - Notification appears
→ Click when ready
→ "Do my evening reflection"
→ Answer interview questions
→ Review daily summary

**Sunday 7:15 PM (local time)** - Weekly review notification
→ Click when ready
→ "Create my weekly review"
→ Answer GTD interview questions
→ Review weekly note and P2 draft

## Customization

### Adjusting Schedules

Edit crontab to change times:
```bash
crontab -e
```

### Modifying Skills

Each skill has a SKILL.md file documenting its workflow. To modify:
1. Edit the SKILL.md in the skill directory
2. Test the changes
3. Update version if needed

### Adding Integrations

To add new data sources:
1. Update relevant SKILL.md files
2. Add MCP server configuration
3. Update state schemas if needed

## Troubleshooting

### Skills Not Running

1. Check crontab: `crontab -l`
2. View logs: `tail -f ~/Library/Logs/personal-assistant.log`
3. Check state: `cat /Users/paolo/Totoro/meta/assistant-state.json`

### Notifications Not Appearing

1. Test scripts manually: `~/bin/personal-assistant/morning-reminder.sh`
2. Check permissions: System Preferences → Notifications
3. Verify script is executable: `ls -l ~/bin/personal-assistant/`

### Data Collection Failures

If integrations fail:
- Skills gracefully degrade
- Missing data is noted in output
- Errors logged to `assistant-state.json`
- Skills continue with available data

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
mkdir -p ~/backups/personal-assistant
rsync -av /Users/paolo/Totoro/meta/ ~/backups/personal-assistant/meta-$(date +%Y%m%d)/
```

## Files Structure

```
/Users/paolo/.claude/skills/personal-assistant/
├── README.md                    # This file
├── SETUP.md                     # Installation guide
├── morning-briefing/
│   └── SKILL.md                 # Morning briefing workflow
├── evening-reflection/
│   └── SKILL.md                 # Evening reflection workflow
├── note-enricher/
│   ├── SKILL.md                 # Note enricher workflow
│   └── references/
│       └── people-profile-schema.md  # Profile structure spec
├── weekly-review/
│   └── SKILL.md                 # Weekly review workflow
└── scripts/
    ├── README.md                # Scripts documentation
    ├── morning-reminder.sh      # Morning notification
    ├── evening-reminder.sh      # Evening notification
    ├── weekly-reminder.sh       # Weekly notification
    └── enricher-reminder.sh     # Enricher notification

/Users/paolo/Totoro/meta/
├── README.md                    # State files documentation
├── briefing-history.json        # Morning briefing state
├── daily-reflections.json       # Evening reflection state
├── enrichment-queue.json        # Note enricher queue
├── action-items.json            # Cross-skill actions
├── assistant-state.json         # General state
└── weekly-reviews/              # Per-week states

/Users/paolo/Totoro/templates/
└── person template.md           # People profile template
```

## Version

**Current Version:** 1.0.0
**Created:** 2025-11-05
**Last Updated:** 2025-11-05

## License

This is a personal assistant system for private use.

## Support

For issues or questions:
- Review individual SKILL.md files for detailed workflows
- Check `/meta/README.md` for state file schemas
- Review `assistant-state.json` for logged errors
- Consult SETUP.md for installation troubleshooting
