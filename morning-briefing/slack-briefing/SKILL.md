---
name: slack-briefing
description: Interactive Slack mentions triage. Fetches @mentions from past 24 hours and allows user selection for daily planning.
---

# Slack Briefing

## Overview

Fetch and present Slack @mentions from the past 24 hours. Organize by priority (DMs from leadership, then other mentions) and let user select which to handle today. Can be used standalone or called by the morning-briefing orchestrator.

## When to Use This Skill

Use this skill to:
- Review Slack @mentions from past 24 hours
- See priority DMs from leadership
- Select mentions to handle today
- Get formatted Slack section ready for Obsidian daily note

## Workflow

### Step 1: Fetch Recent Mentions

Fetch @mentions from past 24 hours using Slack search API:

```bash
cd /Users/paolo/.claude/skills/morning-briefing/scripts
python3 slack_fetch.py mentions 24
```

**Decision Point:**
- If NO mentions found: Return empty or skip section
- If mentions found: Proceed to Step 2

> See [Slack API details](references/slack-api.md) for modes and output format.

### Step 2: Organize and Present Mentions

Organize mentions by priority and present to user:

**Organization:**
1. **Priority DMs** (from Matt Mullenweg, Pedraum Pardehpoosh)
2. **Other Mentions** (all other @mentions in channels and DMs)

> See [filtering rules](references/filtering-rules.md) for priority criteria.

**Presentation Format:**

For each mention, show:
- Channel/sender name
- Message preview
- Timestamp (relative time)
- Direct link to message

Example:
```
## Priority DMs (1)

1. **Matt Mullenweg**: "Can you review the domains roadmap before tomorrow's meeting?"
   - Time: 2 hours ago
   - [View](https://a8c.slack.com/archives/...)

## Other Mentions (3)

2. **#domains**: Jane mentioned you: "Paolo what do you think about the pricing model?"
   - Time: 5 hours ago
   - [View](https://a8c.slack.com/archives/...)

3. **#product**: Bob mentioned you: "FYI deployment went well, Paolo"
   - Time: 8 hours ago
   - [View](https://a8c.slack.com/archives/...)
```

**User Communication:**
"You have **N Slack mentions** from the past 24 hours. I've organized them by priority above.

**Which mentions would you like to handle today?**

You can:
- Select by numbers (e.g., '1, 2, 3')
- Select a range (e.g., '1-3')
- Say 'all' for all mentions
- Say 'none' to skip"

**Wait for user selection.**

### Step 3: Return Formatted Output

Format selected mentions as markdown:

```markdown
- [ ] Slack mention from Matt Mullenweg: [Message preview](https://a8c.slack.com/archives/...)
- [ ] Slack mention in #domains: [Jane's question about pricing](https://a8c.slack.com/archives/...)
- [ ] Slack mention in #product: [Bob's deployment update](https://a8c.slack.com/archives/...)
```

**Return to caller:** If called by orchestrator, return formatted markdown. If standalone, confirm completion to user.

## Important Notes

- This skill is **interactive** - user selects which mentions to handle
- Uses Slack search API to find @mentions (efficient, avoids rate limits)
- Priority DMs shown first (configurable in slack_fetch.py)
- Message text is cleaned (user mentions resolved, markdown removed)
- When called by orchestrator: return formatted markdown only
- When used standalone: can optionally write directly to daily note

## Return Format (for orchestrator)

When called by the morning-briefing orchestrator, return:

```python
{
    "success": True,
    "section_name": "Slack mentions to handle today",
    "content": "- [ ] Slack mention from...\n- [ ] Slack mention in...",
    "metadata": {
        "total_mentions": 4,
        "priority_dm_count": 1,
        "other_mention_count": 3,
        "selected_count": 2
    }
}
```
