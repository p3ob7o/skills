---
name: linear-triage
description: Interactive Linear issues triage. Organizes issues by priority/status and allows user selection for daily planning.
---

# Linear Triage

## Overview

Handle Linear issues triage for the morning briefing. Fetch and categorize issues, then let user select which ones to handle today. Can be used standalone or called by the morning-briefing orchestrator.

## When to Use This Skill

Use this skill to:
- Review Linear issues assigned to user
- See issues updated in the past 24 hours
- Select issues to handle today
- Get formatted issue list ready for Obsidian daily note

## Workflow

### Step 1: Fetch Recent Issues

Try fetching issues updated today first, then fall back to all active issues:

```bash
cd /Users/paolo/.claude/skills/morning-briefing/scripts

# Try today's updates first
python3 linear_fetch.py updated_today 100

# If none found, get all active issues
python3 linear_fetch.py active 100
```

**Decision Point:**
- If issues updated today found: Show those
- If no issues updated today: Show all active issues

> See [Linear API details](references/linear-api.md) for modes and output format.

### Step 2: Organize and Present Issues

Organize issues by priority and status, then present to user:

**Organization:**
1. High Priority Issues (priority = 2)
2. In Progress Issues (state type = started)
3. Triage Issues (state type = triage)
4. Medium/Low Priority Todo Issues
5. Backlog Issues (state type = backlog)

> See [organization rules](references/organization-rules.md) for detailed categorization.

**User Communication:**
"You have **N active Linear issues** assigned to you. I've organized them by priority and status above.

**Which issues would you like to handle today?**

You can:
- Select by numbers (e.g., '1, 2, 6')
- Select a range (e.g., '1-5')
- Select by team (e.g., 'all DOMAINS issues')
- Say 'none' to skip"

**Wait for user selection.**

### Step 3: Return Formatted Output

Format selected issues as markdown:

```markdown
- [ ] Issue TOTORO-114: [P2 post about Dataprovider and webinar](https://linear.app/a8c/issue/TOTORO-114)
- [ ] Issue TOTORO-44: [Reboot follow up with Leanne](https://linear.app/a8c/issue/TOTORO-44)
- [ ] Issue DOMAINS-1338: [Sub $1 domain purchase flow](https://linear.app/a8c/issue/DOMAINS-1338/...)
```

**Return to caller:** If called by orchestrator, return formatted markdown. If standalone, confirm completion to user.

## Error Handling

If Linear API fails, check credentials and offer alternatives (retry, skip, manual entry).

> See [error handling guide](references/error-handling.md) for troubleshooting steps.

## Important Notes

- This skill is **interactive and conversational** - user controls which issues to select
- Use full `url` field from API response for issue links
- When called by orchestrator: return formatted markdown only
- When used standalone: can optionally write directly to daily note
- Always exclude completed and canceled issues by default
- Show most recently updated issues first

## Return Format (for orchestrator)

When called by the morning-briefing orchestrator, return:

```python
{
    "success": True,
    "section_name": "Linear issues to handle today",
    "content": "- [ ] Issue TOTORO-114: [Title](url)\n- [ ] Issue...",
    "metadata": {
        "total_active": 37,
        "selected_count": 3,
        "high_priority_count": 2,
        "in_progress_count": 3
    }
}
```
