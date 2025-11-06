---
name: evening-reflection
description: This skill should be used every evening at 19:00 local time (7 days/week) to close the user's day through reflection, summarization, and profile updates. It conducts an interactive interview, synthesizes the day's events from calendar, notes, Slack, and email, then appends a comprehensive summary to the daily note while identifying people for profile enrichment.
---

# Evening Reflection

## Overview

This skill closes the user's day by conducting an interactive reflection interview, synthesizing activities from multiple sources (calendar, Slack, email, Linear, notes), and producing a comprehensive daily summary that captures accomplishments, challenges, interactions, and forward-looking priorities.

## When to Use This Skill

Trigger this skill:
- Daily at 19:00 local time via cron reminder (user initiates when ready)
- When the user explicitly requests an evening reflection or day summary
- When the user wants to capture end-of-day thoughts

## Workflow

### Phase 1: Data Collection

Collect data about what actually happened today:

1. **Google Calendar**
   - Fetch today's events using direct Calendar API script
   - Script location: `/Users/paolo/.claude/skills/personal-assistant/scripts/calendar_fetch.py`
   - Include event titles, times, attendees, conference links
   - Returns: summary, start, end, location, attendees, organizer

2. **Today's Daily Note**
   - Read the morning briefing section
   - Compare planned vs actual
   - Identify completed vs incomplete tasks
   - Use MCP Obsidian tools

3. **Slack Activity**
   - Fetch last 24 hours of messages
   - Focus on threads user participated in
   - **Priority DMs** (show at top):
     - Matt Mullenweg
     - Pedraum Pardehpoosh
   - Include channel participation counts
   - Use MCP Slack tools

4. **Gmail**
   - Count and categorize sent emails today
   - Identify key email threads
   - Track response patterns
   - Use MCP Gmail tools

5. **Linear**
   - Fetch issues updated today using direct Linear API script
   - Script location: `/Users/paolo/.claude/skills/personal-assistant/scripts/linear_fetch.py`
   - Identify completed vs in-progress items
   - Note blockers or status changes
   - Returns: id, identifier, title, state changes, labels, comments

6. **Conversations**
   - Check `/conversations/` for new meeting summaries added today
   - Extract attendees and topics
   - Use MCP Obsidian tools

7. **State**
   - Read `/meta/daily-reflections.json` for context
   - Check `/meta/enrichment-queue.json`
   - Use file system tools

### Phase 2: Interactive Interview

Conduct a structured reflection interview with the user:

**Question 1: "How did today go overall?"**
- Open-ended question to set the tone
- Capture overall sentiment and energy level

**Question 2: "What did you accomplish that wasn't on the morning list?"**
- Identify unplanned wins
- Capture opportunistic work
- Recognize adaptability

**Question 3: "Any blockers or challenges to note?"**
- Surface obstacles encountered
- Document dependencies
- Capture frustrations or learnings

**Question 4: "Who did you interact with significantly today?"**
- Identify key people for profile updates
- Note quality of interactions
- Capture relationship context

**Question 5: "What's top of mind for tomorrow?"**
- Forward-looking priorities
- Capture urgent items that emerged
- Note what needs to carry over

**Question 6: "Any action items to capture?"**
- Explicit todos for tomorrow
- Follow-ups needed
- Promises made

**Interview Style:**
- Ask one question at a time
- Allow space for reflection
- Follow up on interesting details
- Keep it conversational, not formulaic
- Total interview time: 5-10 minutes

### Phase 3: Synthesis

Process all collected data and interview responses:

1. **Narrative Summary**
   - Write 2-3 paragraphs synthesizing the day
   - Blend calendar events, accomplishments, interactions
   - Include user's reflections and sentiment
   - Connect themes and patterns

2. **Structured Extraction**
   - List concrete accomplishments
   - Document blockers and challenges
   - Identify key interactions
   - Summarize communication patterns

3. **Activity Metrics**
   - Slack: Message counts by channel, DM activity
   - Email: Sent count, key threads
   - Linear: Completed/updated issues
   - Meetings: Count and total time

4. **Forward Planning**
   - Capture tomorrow's priorities
   - Note carry-over items
   - Identify urgent issues that emerged

5. **People Queue**
   - Extract names mentioned in interview
   - Add to `/meta/enrichment-queue.json` for profile updates
   - Prioritize people with new information

### Phase 4: Output Generation

Append to today's daily note at `YYYY/MM/YYYY-MM-DD.md`:

```markdown
## Evening Reflection

### What Happened
[2-3 paragraph narrative synthesizing the day's activities, interactions, and user's reflections. Include sentiment, energy level, and key themes. Connect morning plan to actual execution.]

### Accomplishments
- ✅ [LIN-XXX] Completed issue title
- ✅ Productive meeting with [Person] - achieved [outcome]
- ✅ Sent proposal to [stakeholder]
- ✅ [Unplanned accomplishment from interview]

### Blockers & Challenges
- [Blocker description] - waiting on [dependency]
- [Challenge faced] - will address by [approach]
- [Learning or frustration] - noted for future

### Key Interactions
- [[Person Name]] - [Context: meeting/Slack/email], [Key topic or outcome]
- [[Person Name]] - [Context], [Key topic or outcome]
- [[Person Name]] - [Context], [Key topic or outcome]

### Slack Activity (24h)
**Priority DMs:**
- **Matt Mullenweg**: N messages ([brief topic summary])
- **Pedraum Pardehpoosh**: N messages ([brief topic summary])

**Channel Participation:**
- #channel-name: N messages ([topic or discussion])
- #channel-name: N messages ([topic or discussion])

### Email Activity
- **Sent**: N emails (N internal, N external)
- **Key threads**: [Brief list of important email conversations]

### Linear Updates
- **Completed**: [LIN-XXX] Issue title
- **In Progress**: [LIN-XXX] Issue title (status change or update)
- **Blocked**: [LIN-XXX] Issue title (reason for blocker)

### Tomorrow's Top Priorities
1. [Urgent item that emerged today]
2. [Carry-over from incomplete morning plan]
3. [Proactive item user wants to tackle]

---
```

### Phase 5: State Updates

Update state files in `/meta/`:

**Update `/meta/daily-reflections.json`:**
```json
{
  "history": [
    {
      "date": "YYYY-MM-DD",
      "timestamp": "ISO-8601 timestamp",
      "sentiment": "positive|neutral|challenging",
      "accomplishments_count": 5,
      "blockers_count": 2,
      "key_people": ["Person Name 1", "Person Name 2"],
      "slack_messages": 45,
      "emails_sent": 18,
      "linear_completed": 3,
      "meetings_count": 4,
      "summary": "Brief one-line summary of the day"
    }
  ]
}
```

**Update `/meta/enrichment-queue.json`:**
Add people mentioned for profile updates:
```json
{
  "pending": [
    {
      "id": "enrich-NNN",
      "type": "profile",
      "person": "Person Name",
      "added": "ISO-8601 timestamp",
      "priority": "high",
      "status": "pending",
      "context": "Met in [meeting], discussed [topic]",
      "questions": [
        "Update interaction history with meeting details",
        "Note collaboration pattern or communication style"
      ]
    }
  ]
}
```

**Update tomorrow's action items:**
Create or update `/meta/action-items.json` with items for tomorrow's briefing:
```json
{
  "pending": [
    {
      "date_added": "YYYY-MM-DD",
      "item": "Action item description",
      "priority": "high|medium|low",
      "source": "evening_reflection"
    }
  ]
}
```

## Integration Patterns

### Calendar Integration
```
Use direct Calendar API script:
- Script: /Users/paolo/.claude/skills/personal-assistant/scripts/calendar_fetch.py
- Fetch today's events that occurred: ./calendar_fetch.py "YYYY-MM-DDT00:00:00+TZ" "YYYY-MM-DDT23:59:59+TZ"
- Compare to morning briefing to see planned vs actual
- See morning-briefing/SKILL.md for full integration example
```

### Slack Integration
```
Use MCP Slack tools:
- Fetch messages from last 24 hours where user participated
- slack_find_message or slack_get_conversation for threads
- Prioritize DMs: Matt Mullenweg, Pedraum Pardehpoosh
- Count messages by channel
```

### Gmail Integration
```
Use MCP Gmail tools:
- gmail_find_email with query:"after:YYYY/MM/DD is:sent"
- Count total sent, categorize (internal vs external)
- Identify key threads or recipients
```

### Linear Integration
```
Use direct Linear API script:
- Script: /Users/paolo/.claude/skills/personal-assistant/scripts/linear_fetch.py
- Fetch issues updated today: ./linear_fetch.py updated_today 50

Example Python integration:
import subprocess
import json

result = subprocess.run(
    ['/Users/paolo/.claude/skills/personal-assistant/scripts/linear_fetch.py', 'updated_today', '50'],
    capture_output=True,
    text=True
)
data = json.loads(result.stdout)
issues = data['issues']

# Group by state for evening reflection
completed = [i for i in issues if i['state']['type'] == 'completed']
in_progress = [i for i in issues if i['state']['type'] == 'started']
blocked = [i for i in issues if 'blocked' in [label['name'].lower() for label in i['labels']]]

# Format for daily note
for issue in completed:
    # [LIN-XXX] Issue title
    pass
```

### Obsidian Integration
```
Use MCP Obsidian tools:
- obsidian_get_vault_file to read today's daily note (morning section)
- obsidian_append_to_vault_file to write evening reflection
- List files in /conversations/ modified today
- Update /meta/ state files
```

## Interview Best Practices

**Tone and Approach:**
- Conversational and supportive, not interrogative
- Allow silence and thinking time
- Follow up on interesting details: "Tell me more about that"
- Validate feelings and challenges
- Keep it human, not robotic

**Question Adaptations:**
- If user had a challenging day, adjust tone with empathy
- If user is brief, probe gently for details
- If user is exhausted, keep it shorter
- If user is excited, explore the wins

**Time Management:**
- Aim for 5-10 minutes total
- Don't rush, but keep momentum
- Can skip questions if user covers them naturally
- Always end with forward-looking priority

## Error Handling

If any integration fails:
- Continue with available data sources
- Note the failure: "⚠️ [Source] unavailable for today's summary"
- Rely more heavily on interview responses
- Log the error to `/meta/assistant-state.json`

## Performance Targets

- Data collection: < 15 seconds
- Interactive interview: 5-10 minutes (user-paced)
- Synthesis and writing: < 20 seconds
- Total: < 15 minutes including user interaction

## Important Notes

- This skill appends to (does not overwrite) the daily note
- The interview is conversational, not a form to fill out
- People mentioned are automatically queued for profile enrichment
- Forward-looking priorities feed into tomorrow's morning briefing
- Sentiment tracking helps identify patterns over time
- Times are in the user's local timezone (adjusts automatically when traveling)
