---
name: gmail-triage
description: Interactive Gmail inbox triage using inbox-zero methodology. Categorizes emails and allows user selection for daily planning.
---

# Gmail Triage

## Overview

Handle Gmail inbox triage using the inbox-zero methodology. Can be used standalone or called by the morning-briefing orchestrator.

## When to Use This Skill

Use this skill to:
- Process Gmail inbox using inbox-zero methodology
- Categorize emails into Reply Now / Star for Later / Archive
- Select starred emails to handle today
- Get formatted email list ready for Obsidian daily note

## Workflow

### Step 1: Fetch Inbox Emails

Fetch unread inbox emails using `gmail_fetch.py`:

```bash
cd /Users/paolo/.claude/skills/morning-briefing/scripts
python3 gmail_fetch.py "in:inbox is:unread" 150
```

**Decision Point:**
- If NO emails: Skip to Step 3 (starred emails)
- If emails found: Proceed to Step 2

> See [Gmail API details](references/gmail-api.md) for query syntax and output format.

### Step 2: Recommend Three Lists

Analyze each email and categorize into three lists:
- **Reply Now**: Urgent emails requiring immediate attention
- **Star for Later**: Complex emails requiring significant time
- **Archive**: Low-value emails with no action needed

Present all three lists with reasoning for each categorization.

> See [categorization rules](references/categorization-rules.md) for detailed criteria.

**User Communication:**
"I've categorized your inbox emails into three groups above. Please handle them in your Gmail:
- Reply to the 'Reply Now' emails
- Star the 'Star for Later' emails
- Archive the suggested 'Archive' emails

**When you're done, let me know and I'll verify your inbox is empty.**"

**Wait for user response.**

### Step 3: Verify Inbox Empty (Loop)

Re-fetch inbox to verify it's empty:

```bash
python3 gmail_fetch.py "in:inbox is:unread" 150
```

**Decision Logic:**
- If emails remaining: Ask if user wants to analyze them (loop to Step 2)
- If inbox empty: Confirm "✓ Inbox is empty!" and proceed

### Step 4: Fetch and Select Starred Emails

Fetch all starred emails:

```bash
python3 gmail_fetch.py "is:starred" 100
```

Present as interactive checklist. Ask user which starred emails they want to handle TODAY.

**User Interaction:**
"Which emails would you like to handle today? You can:
- Select by numbers (e.g., '1, 3, 5')
- Select a range (e.g., '1-5')
- Say 'all' for all emails
- Say 'none' to skip"

**Wait for user selection.**

### Step 5: Return Formatted Output

Format selected emails as markdown:

```markdown
- [ ] Email from Jane Doe: [Q4 Planning Discussion](https://mail.google.com/mail/u/0/#inbox/msg-id)
- [ ] Email from Bob Smith: [Code review request](https://mail.google.com/mail/u/0/#inbox/msg-id)
```

**Return to caller:** If called by orchestrator, return formatted markdown. If standalone, confirm completion to user.

## Error Handling

If Gmail API fails, check credentials and offer alternatives (retry, skip, manual entry).

> See [error handling guide](references/error-handling.md) for troubleshooting steps.

## Important Notes

- This skill is **interactive and conversational** - user controls the pace
- Wait at each decision point for user input
- Use full `message_url` from API response for Gmail links
- Extract sender names from `from` field (format: "Name <email>")
- When called by orchestrator: return formatted markdown only
- When used standalone: can optionally write directly to daily note

## Return Format (for orchestrator)

When called by the morning-briefing orchestrator, return:

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
