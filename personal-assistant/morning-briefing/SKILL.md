---
name: morning-briefing
description: This skill should be used every morning at 9:00 CET (7 days/week) to prepare the user's day through intelligent triage and prioritization of calendar events, Linear issues, emails, Slack mentions, and pending action items. The skill implements a three-layer prioritization framework (Eisenhower Matrix → Now/Next/Later → Deep/Shallow work) and produces a comprehensive briefing written to the daily note.
---

# Morning Briefing

## Overview

This skill prepares the user for their day by collecting data from multiple sources (Google Calendar, Linear, Gmail, Slack, Obsidian notes), triaging emails using inbox-zero methodology, and applying a sophisticated three-layer prioritization framework to present an actionable daily plan.

## When to Use This Skill

Trigger this skill:
- Daily at 9:00 CET via cron reminder (user initiates when ready)
- When the user explicitly requests a morning briefing or day preparation
- When the user needs to re-prioritize their day

## Workflow

### Phase 1: Data Collection

Collect data from all integrated sources:

1. **Google Calendar**
   - Fetch today's events (all day and time-specific)
   - Include event titles, times, locations, attendees
   - Use MCP Google Calendar tools
   - **IMPORTANT**: Zapier Google Calendar has counter-intuitive parameter naming:
     - `end_time` = earliest timestamp (start of search window)
     - `start_time` = latest timestamp (end of search window)
     - Example: To get events for Nov 5, use `end_time="2025-11-05T00:00:00+01:00"` and `start_time="2025-11-05T23:59:59+01:00"`
   - Use `calendarid="paolo@a8c.com"` (primary calendar)

2. **Linear**
   - Query for active issues with filters:
     - Assigned to user OR mentions user OR user is subscribed
     - State NOT IN ["Completed", "Canceled"]
   - Include issue title, priority, labels, due dates
   - Use MCP Linear tools

3. **Gmail**
   - Fetch starred emails
   - Fetch all untreated inbox emails
   - Prepare for inbox-zero triage
   - Use MCP Gmail tools

4. **Slack**
   - Query mentions from 19:00 yesterday to now
   - Prioritize DMs from: Matt Mullenweg, Pedraum Pardehpoosh
   - Include channel context and message previews
   - Use MCP Slack tools

5. **Obsidian**
   - Read yesterday's daily note for carry-over items
   - Check `/meta/briefing-history.json` for context
   - Check `/meta/enrichment-queue.json` for pending items
   - Use MCP Obsidian tools

### Phase 2: Email Triage (Inbox-Zero)

For each untreated inbox email, classify into three buckets:

**Respond Immediately:**
- Urgent emails requiring immediate attention
- Easy emails that can be answered in < 5 minutes
- Customer escalations or time-sensitive requests

**Star for Later:**
- Emails requiring significant time or thought
- Complex questions needing research
- Lengthy proposals requiring analysis
- Non-urgent but important communications

**Suggested to Trash:**
- Newsletter confirmations
- Low-value notifications
- Spam or irrelevant emails
- Already-handled threads

Present this as an actionable list in the briefing.

### Phase 3: Three-Layer Prioritization

Apply the user's prioritization framework to all items (Linear issues, calendar events, emails, action items):

**Layer 1 - Eisenhower Matrix:**

Classify each item into four quadrants:
- **Do now**: Urgent AND Important
- **Do later**: Important but NOT urgent
- **Delegate**: Urgent but NOT important
- **Delete**: Neither urgent nor important

Criteria:
- Urgent: Has a deadline today/tomorrow, blocking others, time-sensitive
- Important: Aligns with key goals, has significant impact, strategic value

**Layer 2 - Temporal Buckets:**

Transform Layer 1 classifications into temporal buckets:
- **Now** (Today): Items from "Do now" + urgent "Do later" items
- **Next** (This week): Remaining "Do later" items + "Delegate" items
- **Later** (Beyond this week): Non-urgent "Do later" items

**Layer 3 - Energy-Based Scheduling:**

For "Now" (Today) items, categorize by work type:

**Deep Work (before 13:00 CET):**
- Complex problem-solving
- Strategic planning
- Creative work
- Focused coding or writing
- Important decisions

**Shallow Work (after 14:00 CET):**
- Email responses
- Administrative tasks
- Routine updates
- Quick meetings
- Status checks

Note: 13:00-14:00 is lunch break

### Phase 4: Output Generation

Write the briefing to today's daily note at `YYYY/MM/YYYY-MM-DD.md`:

```markdown
# YYYY-MM-DD

## Morning Briefing

### Today's Calendar
- HH:MM-HH:MM: Event Title (Location/Context)
- [List all events chronologically]

### Priority Matrix

#### Now (Today)
**Deep Work (before 13:00)**
- [ ] [LIN-XXX] Issue title
- [ ] Task description
- [ ] Action item from yesterday

**Shallow Work (after 14:00)**
- [ ] [LIN-XXX] Issue title
- [ ] Task description
- [ ] Quick email responses

#### Next (This Week)
- [ ] [LIN-XXX] Issue title
- [ ] Task description
- [ ] Follow-up items

#### Later (Beyond This Week)
- [ ] [LIN-XXX] Long-term planning
- [ ] Strategic initiatives
- [ ] Research projects

#### Delegate
- [ ] Task to delegate to [Person]
- [ ] Ask [Person] to handle [Task]

### Slack Overnight
**Priority DMs:**
- **Matt Mullenweg**: [Message preview]
- **Pedraum Pardehpoosh**: [Message preview]

**Other Mentions:**
- #channel-name: [Context of mention]
- #another-channel: [Context of mention]

### Email Triage

**Respond Immediately (N):**
1. ☆ [Subject line] - [Brief context]
2. [Subject line] - [Brief context]
...

**Star for Later (N):**
1. [Subject line] - [Brief context]
2. [Subject line] - [Brief context]
...

**Suggested to Trash (N):**
1. [Subject line] - [Brief context]
2. [Subject line] - [Brief context]
...

### Carry-Over from Yesterday
- [ ] [Unfinished item from yesterday]
- [ ] [Action item still pending]
- [ ] [Follow-up needed]

---
```

### Phase 5: State Updates

Update state files in `/meta/`:

**Update `/meta/briefing-history.json`:**
```json
{
  "history": [
    {
      "date": "YYYY-MM-DD",
      "timestamp": "ISO-8601 timestamp",
      "calendar_events": 5,
      "linear_issues": 12,
      "inbox_emails": 23,
      "slack_mentions": 8,
      "priority_items_deep": 3,
      "priority_items_shallow": 6,
      "summary": "Brief one-line summary of the day's focus"
    }
  ]
}
```

**Mark processed items in `/meta/enrichment-queue.json`:**
- Items addressed in the briefing can be marked as acknowledged

## Integration Patterns

### Calendar Integration
```
Use MCP Google Calendar tools:
- google_calendar_find_events with start_time=today_00:00 and end_time=today_23:59
- Filter for events where user is attendee or organizer
```

### Linear Integration
```
Use MCP Linear tools:
- Query issues with filters:
  assignee.id = user.id OR
  subscribers.id contains user.id OR
  mentions contains user.id
- Exclude states: Completed, Canceled
- Include: title, description, priority, labels, due_date
```

### Gmail Integration
```
Use MCP Gmail tools:
- gmail_find_email with query:"is:starred"
- gmail_find_email with query:"in:inbox is:unread"
- Classify each email for triage
```

### Slack Integration
```
Use MCP Slack tools:
- slack_find_message with time range: yesterday 19:00 to now
- Filter for messages mentioning user
- Prioritize DMs from: Matt Mullenweg, Pedraum Pardehpoosh
```

### Obsidian Integration
```
Use MCP Obsidian tools:
- obsidian_get_vault_file for yesterday's daily note
- obsidian_create_vault_file or obsidian_append_to_vault_file for today's note
- Read from /meta/ directory for state
```

## Error Handling

If any integration fails:
- Continue with available data sources
- Note the failure in the briefing: "⚠️ [Source] unavailable"
- Gracefully degrade (e.g., if Linear is down, focus on email/calendar)
- Log the error to `/meta/assistant-state.json`

## Performance Targets

- Complete data collection in < 20 seconds
- Generate briefing in < 30 seconds total
- Minimize API calls through caching when appropriate

## Important Notes

- This skill writes to the user's Obsidian vault
- All file paths use YYYY/MM/YYYY-MM-DD.md format
- Times are in CET timezone
- The skill is read-heavy (fetches data) and write-light (one daily note)
- State files in `/meta/` provide continuity across days
