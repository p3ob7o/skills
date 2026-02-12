# Linear API Integration

## Script Location

```
/Users/paolo/.claude/skills/morning-briefing/scripts/linear_fetch.py
```

## Usage

```bash
python3 linear_fetch.py <mode> [limit]
```

## Available Modes

- `me` - Get authenticated user info
- `active` - Get active issues assigned to me (excludes completed/canceled)
- `updated_today` - Get issues updated today assigned to me
- `completed_this_week` - Get issues completed this week
- `team <team_key>` - Get issues for specific team

## Output Format

The script returns JSON with this structure:

```json
{
  "viewer": {
    "id": "user-id",
    "name": "Paolo Belcastro",
    "email": "paolo@a8c.com"
  },
  "count": 37,
  "mode": "active",
  "issues": [
    {
      "id": "issue-id",
      "identifier": "DOMAINS-1827",
      "title": "Domain Names Customer Conversations",
      "description": "...",
      "priority": 2,
      "priority_label": "High",
      "url": "https://linear.app/a8c/issue/DOMAINS-1827/...",
      "created_at": "2025-11-07T16:06:25.019Z",
      "updated_at": "2025-11-07T16:06:33.820Z",
      "due_date": null,
      "state": {
        "id": "state-id",
        "name": "Todo",
        "type": "unstarted",
        "color": "#e2e2e2"
      },
      "team": {
        "id": "team-id",
        "key": "DOMAINS",
        "name": "Domaison"
      },
      "assignee": {...},
      "creator": {...},
      "project": {...},
      "labels": [...],
      "comment_count": 0,
      "latest_comment": null,
      "parent": null,
      "child_count": 0,
      "children": []
    }
  ]
}
```

## Key Fields

- **identifier**: Issue ID (e.g., "DOMAINS-1827")
- **title**: Issue title
- **description**: Issue description (can be empty)
- **priority**: 0-4 (0=none, 1=urgent, 2=high, 3=medium, 4=low)
- **priority_label**: Human-readable priority
- **url**: Direct link to Linear issue
- **state.type**: unstarted, started, completed, canceled, backlog, triage
- **state.name**: Human-readable state (Todo, In Progress, Done, etc.)
- **team**: Team information with key and name
- **updated_at**: Last update timestamp (ISO 8601)
- **created_at**: Creation timestamp
- **due_date**: Due date if set (ISO 8601 or null)

## State Types

- **triage**: Needs review and prioritization
- **unstarted**: Ready to start (Todo)
- **started**: Currently in progress
- **backlog**: Not immediate, future work
- **completed**: Finished
- **canceled**: Not doing

## Priority Levels

- **0**: No priority / Needs triage
- **1**: Urgent (highest priority)
- **2**: High
- **3**: Medium
- **4**: Low

## API Authentication

API key stored in macOS Keychain:
```bash
security find-generic-password -s 'linear-api' -a 'personal-assistant' -w
```

## Performance

- Typical fetch time: 2-3 seconds for up to 100 issues
- No rate limiting concerns for typical usage
