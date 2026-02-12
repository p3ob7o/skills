---
name: calendar-briefing
description: Fetches today's calendar events from Google Calendar with times, titles, attendees, and meeting links.
---

# Calendar Briefing

## Overview

Fetch and present today's calendar events from Google Calendar. Provides a clear overview of the day's schedule. Can be used standalone or called by the morning-briefing orchestrator.

## When to Use This Skill

Use this skill to:
- See today's calendar events
- Get meeting times, titles, and links
- Review schedule for the day
- Get formatted calendar section ready for Obsidian daily note

## Workflow

### Step 1: Fetch Today's Events

Fetch events for today from Google Calendar:

```bash
cd /Users/paolo/.claude/skills/morning-briefing/scripts
python3 calendar_fetch.py today
```

**Decision Point:**
- If NO events found: Return empty or skip section
- If events found: Proceed to Step 2

> See [Calendar API details](references/calendar-api.md) for timeframes and output format.

### Step 2: Present Events

Display events in chronological order with key details:

**Format each event with:**
- Time range (e.g., "9:00 AM - 9:30 AM")
- Event title
- Meeting link (Google Meet, Zoom, or calendar link)
- Attendee count

> See [formatting rules](references/formatting-rules.md) for time formatting, link priority, and special cases.

**User Communication:**
"You have **N events** on your calendar today. Here's your schedule for the day."

**No Selection Needed:** Calendar is informational only - no user selection required.

### Step 3: Return Formatted Output

Format events as markdown ready for Obsidian:

```markdown
## Today's calendar

- **9:00 AM - 9:30 AM**: [Team Standup](https://meet.google.com/abc-defg-hij) (8 attendees)
- **10:00 AM - 11:00 AM**: [Product Review](https://zoom.us/j/123) (5 attendees)
- **2:00 PM - 3:00 PM**: [1:1 with Manager](https://calendar.google.com/...) (2 attendees)
```

**Return to caller:** If called by orchestrator, return formatted markdown. If standalone, confirm completion to user.

## Important Notes

- This skill is **read-only and informational** - no user interaction required
- Always show events in chronological order
- Include meeting links when available
- Show attendee count for context
- Handle timezone differences gracefully
- When called by orchestrator: return formatted markdown only
- When used standalone: display to user and optionally write to daily note
- Skip cancelled events by default

## Return Format (for orchestrator)

When called by the morning-briefing orchestrator, return:

```python
{
    "success": True,
    "section_name": "Today's calendar",
    "content": "- **9:00 AM - 9:30 AM**: [Title](link)\\n- **10:00 AM...",
    "metadata": {
        "event_count": 5,
        "has_conflicts": False,
        "first_event_time": "09:00",
        "last_event_time": "17:00"
    }
}
```
