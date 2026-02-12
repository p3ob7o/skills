# Sub-Skill Coordination

## Available Sub-Skills

The morning-briefing orchestrator coordinates these four sub-skills:

1. **gmail-triage** - Email inbox zero and starred email selection
2. **linear-triage** - Linear issues selection
3. **slack-briefing** - Past 24 hours Slack activity
4. **calendar-briefing** - Today's calendar events

## Invocation Method

Use the Skill tool to invoke each sub-skill:

```python
Skill(command="gmail-triage")
Skill(command="linear-triage")
Skill(command="calendar-briefing")
Skill(command="slack-briefing")
```

## Expected Return Format

Each sub-skill returns formatted markdown content ready for Obsidian:

```python
{
    "success": True,
    "section_name": "Section Header",
    "content": "Markdown content here...",
    "metadata": {
        # Sub-skill specific metadata
    }
}
```

### Gmail-Triage Returns

```python
{
    "success": True,
    "section_name": "Emails to handle today",
    "content": "- [ ] Email from...\n- [ ] Email from...",
    "metadata": {
        "inbox_count": 47,
        "starred_count": 34,
        "selected_count": 4
    }
}
```

### Linear-Triage Returns

```python
{
    "success": True,
    "section_name": "Linear issues to handle today",
    "content": "- [ ] Issue TOTORO-114: [Title](url)\n...",
    "metadata": {
        "total_active": 37,
        "selected_count": 3,
        "high_priority_count": 2,
        "in_progress_count": 3
    }
}
```

### Calendar-Briefing Returns

```python
{
    "success": True,
    "section_name": "Today's calendar",
    "content": "- **9:00 AM - 9:30 AM**: [Title](link)\n...",
    "metadata": {
        "event_count": 5,
        "has_conflicts": False,
        "first_event_time": "09:00",
        "last_event_time": "17:00"
    }
}
```

### Slack-Briefing Returns

```python
{
    "success": True,
    "section_name": "Slack activity (past 24 hours)",
    "content": "### Direct Messages\n- **Sarah**: message...",
    "metadata": {
        "conversation_count": 12,
        "dm_count": 3,
        "mention_count": 5,
        "thread_count": 4,
        "requires_response": 2
    }
}
```

## Execution Order

Sub-skills should be invoked **sequentially**, not in parallel:

1. Gmail-triage (interactive, takes 5-30 minutes)
2. Linear-triage (interactive, takes 1-5 minutes)
3. Calendar-briefing (automatic, takes <10 seconds)
4. Slack-briefing (automatic, takes <15 seconds)

**Reason:** Gmail and Linear require user interaction. Running in parallel would confuse the user.

## Collecting Output

After each sub-skill completes:

1. Wait for sub-skill to finish
2. Extract the returned markdown content
3. Store in a variable for later writing to Obsidian
4. Optionally extract metadata for commit message

Example workflow:
```python
# Invoke gmail-triage
gmail_result = Skill(command="gmail-triage")
gmail_content = gmail_result["content"]
gmail_metadata = gmail_result["metadata"]

# Invoke linear-triage
linear_result = Skill(command="linear-triage")
linear_content = linear_result["content"]
linear_metadata = linear_result["metadata"]

# ... continue for calendar and slack

# Then write all to Obsidian at once
```

## Error Handling

If a sub-skill fails:

1. Log the error
2. Inform user: `"⚠️ {sub-skill-name} failed: {error_message}"`
3. Ask user if they want to:
   - Skip this section and continue
   - Retry the sub-skill
   - Abort entire briefing
4. Continue with remaining sub-skills if user chooses to skip

Example:
```
⚠️ Slack-briefing failed: Slack API unavailable

Would you like to:
1. Skip Slack and continue with remaining sections
2. Retry slack-briefing
3. Abort morning briefing

Your choice: _
```

## Writing to Obsidian

After collecting all content, write each section using `append-section`:

```bash
cd /Users/paolo/.claude/skills/morning-briefing/scripts

python3 obsidian_fetch.py append-section "{daily_note_path}" "## Emails to handle today" "{gmail_content}"

python3 obsidian_fetch.py append-section "{daily_note_path}" "## Linear issues to handle today" "{linear_content}"

python3 obsidian_fetch.py append-section "{daily_note_path}" "## Today's calendar" "{calendar_content}"

python3 obsidian_fetch.py append-section "{daily_note_path}" "## Slack activity (past 24 hours)" "{slack_content}"
```

## Commit Message Format

Use metadata from all sub-skills to create informative commit message:

```
Morning briefing: Complete daily planning

- Processed Gmail inbox ({N} emails selected from {X} inbox, {Y} starred)
- Selected {M} Linear issues (from {Z} active issues)
- Reviewed calendar ({X} events today)
- Checked Slack activity ({Y} conversations past 24h)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Customization Options

Users can customize by:
- Skipping specific sub-skills: "Skip Slack today"
- Changing order: "Do Linear before email"
- Adding custom sections: "Also add a notes section"
- Changing time ranges: "Check Slack for past 48 hours"

The orchestrator should be flexible and adapt to user preferences.
