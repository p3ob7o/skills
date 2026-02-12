---
name: morning-briefing
description: Orchestrates morning briefing workflow by coordinating gmail-triage, linear-triage, calendar-briefing, and slack-briefing sub-skills, then writing results to daily note.
---

# Morning Briefing (Orchestrator)

## Overview

Orchestrator for the morning briefing workflow. Coordinates four sub-skills and handles Obsidian I/O and git commits. User manually launches this skill to review their day's priorities across email, Linear, calendar, and Slack.

## Architecture

The morning-briefing orchestrator calls these sub-skills **sequentially**:
1. **gmail-triage** - Email inbox zero and starred email selection
2. **linear-triage** - Linear issues selection
3. **slack-briefing** - Past 24 hours Slack activity
4. **calendar-briefing** - Today's calendar events

> See [sub-skill coordination](references/sub-skill-coordination.md) for invocation details and return formats.

Each sub-skill:
- Handles its own API calls and user interaction
- Returns formatted markdown content
- Can be used standalone or by this orchestrator

The orchestrator:
- Invokes sub-skills using the Skill tool
- Collects formatted markdown from each
- Writes all sections to Obsidian daily note at once
- Commits changes to git

## When to Use This Skill

User will manually trigger this skill when ready for their morning briefing to:
- Process Gmail inbox using inbox-zero methodology
- Select Linear issues to handle today
- Review today's calendar
- Check Slack activity from past 24 hours
- Have everything organized in their daily note

**Important**: This is NOT automated. User explicitly invokes this skill when ready.

## The Orchestration Workflow

Use TodoWrite to track progress through these steps.

### Step 1: Initialize Daily Note

Get today's date and prepare daily note path:

```python
from datetime import datetime
today = datetime.now()
date_str = today.strftime("%Y-%m-%d")
year_month = today.strftime("%Y/%m")
daily_note_path = f"{year_month}/{date_str}.md"
```

Check if daily note exists, create if needed:

```bash
cd /Users/paolo/.claude/skills/morning-briefing/scripts
python3 obsidian_fetch.py exists "{daily_note_path}"
```

> See [Obsidian integration](references/obsidian-integration.md) for operations and date formatting.

### Step 2: Invoke Sub-Skills Sequentially

Call each sub-skill and collect their output:

```python
Skill(command="gmail-triage")    # Returns formatted markdown
Skill(command="linear-triage")   # Returns formatted markdown
Skill(command="calendar-briefing") # Returns formatted markdown
Skill(command="slack-briefing")  # Returns formatted markdown
```

Store the returned markdown content from each for later writing to Obsidian.

> See [sub-skill coordination](references/sub-skill-coordination.md) for error handling and return formats.

### Step 3: Write All Sections to Daily Note

Write all collected content to the daily note using `append-section`:

```bash
python3 obsidian_fetch.py append-section "{daily_note_path}" "## Emails to handle today" "{gmail_content}"
python3 obsidian_fetch.py append-section "{daily_note_path}" "## Linear issues to handle today" "{linear_content}"
python3 obsidian_fetch.py append-section "{daily_note_path}" "## Today's calendar" "{calendar_content}"
python3 obsidian_fetch.py append-section "{daily_note_path}" "## Slack activity (past 24 hours)" "{slack_content}"
```

The script automatically triggers "Reload app without saving" after each write.

### Step 4: Commit to Git

Commit the daily note changes to git and push:

```bash
cd /Users/paolo/Totoro
git add "{daily_note_path}"
git commit -m "Morning briefing: Complete daily planning

- Processed Gmail inbox (N emails)
- Selected M Linear issues
- Reviewed calendar (X events)
- Checked Slack activity

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push
```

### Step 5: Confirm Completion

Inform user that morning briefing is complete:

```
✓ **Morning briefing complete!**

Your daily note has been updated with:
- **Emails to handle today** (N selected)
- **Linear issues to handle today** (M selected)
- **Today's calendar** (X events)
- **Slack activity** (Y conversations)

Everything is in your daily note at `{daily_note_path}` and committed to git.
```

## Important Notes

- This skill is the **orchestrator only** - it delegates work to sub-skills
- Each sub-skill handles its own API calls and user interaction
- The orchestrator is responsible for Obsidian I/O and git commits
- Use TodoWrite to track progress through all steps
- Sub-skills can be used independently for standalone operations
- All write operations use `obsidian_fetch.py` with auto-reload
- Commit message includes summary statistics from all sub-skills
- Handle errors gracefully - allow skipping failed sections

## Standalone Sub-Skill Usage

Users can invoke sub-skills directly without the orchestrator:
- "Please run gmail-triage" - Just handle email, don't write to Obsidian
- "Check my Linear issues" - Invoke linear-triage standalone
- "What's on my calendar today?" - Invoke calendar-briefing standalone
- "Show me Slack activity" - Invoke slack-briefing standalone

When sub-skills are used standalone, they should:
- Perform their function normally
- Optionally offer to write to daily note
- Not automatically commit to git
