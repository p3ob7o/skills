# Linear API Direct Access Setup

This guide explains how to set up direct Linear API access using GraphQL to retrieve issues and project data efficiently.

## Why This Approach?

Using the Linear API directly provides:
- **Full control**: Direct GraphQL queries with exactly the data you need
- **Efficiency**: Fetch only required fields, reducing token usage
- **Flexibility**: Complex filters, custom queries, pagination
- **Reliability**: No dependency on MCP server availability
- **Performance**: Single API call can fetch all needed data

## Setup Steps

### 1. Install Required Python Package

```bash
pip3 install requests
```

### 2. Get Your Linear API Key

1. Go to [Linear Settings → API](https://linear.app/settings/api)
2. Click "Create new key"
3. Name it "Personal Assistant" or similar
4. Copy the API key (starts with `lin_api_...`)
5. Store it securely using one of these methods:

#### Option A: macOS Keychain (Recommended - Most Secure)

Store your API key in the encrypted macOS Keychain:

```bash
security add-generic-password -s linear-api -a personal-assistant -w "lin_api_YOUR_KEY_HERE"
```

**Benefits:**
- Encrypted storage
- Protected by your macOS login password
- Can require Touch ID/password for access
- Standard practice for sensitive credentials
- Not stored in plain text anywhere

**To verify it was added:**
```bash
security find-generic-password -s linear-api -a personal-assistant -w
```

**To update the key:**
```bash
security delete-generic-password -s linear-api -a personal-assistant
security add-generic-password -s linear-api -a personal-assistant -w "NEW_KEY_HERE"
```

**To remove:**
```bash
security delete-generic-password -s linear-api -a personal-assistant
```

#### Option B: File with Restricted Permissions (Fallback)

If you prefer a file-based approach:

```bash
echo "lin_api_YOUR_KEY_HERE" > ~/.claude/linear_api_key.txt
chmod 600 ~/.claude/linear_api_key.txt
```

**Important:** The script will warn you if file permissions are too open (not 600).

**Security considerations:**
- ✅ File is readable only by you (chmod 600)
- ❌ Still stored as plain text on disk
- ❌ Visible in file system backups
- ❌ Can be read by any process running as your user

### 3. Verify Setup

Test the connection:

```bash
/Users/paolo/.claude/skills/personal-assistant/scripts/linear_fetch.py me
```

You should see your user info:

```json
{
  "id": "your-user-id",
  "name": "Your Name",
  "email": "your@email.com"
}
```

## Usage

### Get Active Issues Assigned to You

```bash
# Default: 50 active issues
/Users/paolo/.claude/skills/personal-assistant/scripts/linear_fetch.py active

# Get 100 active issues
/Users/paolo/.claude/skills/personal-assistant/scripts/linear_fetch.py active 100
```

### Get Issues Updated Today

```bash
# All issues you're assigned to that were updated today
/Users/paolo/.claude/skills/personal-assistant/scripts/linear_fetch.py updated_today

# Limit to 25 issues
/Users/paolo/.claude/skills/personal-assistant/scripts/linear_fetch.py updated_today 25
```

### Get Issues Completed This Week

```bash
# All issues completed since Monday 00:00 UTC
/Users/paolo/.claude/skills/personal-assistant/scripts/linear_fetch.py completed_this_week

# Limit to 30 issues
/Users/paolo/.claude/skills/personal-assistant/scripts/linear_fetch.py completed_this_week 30
```

### Get Issues for a Specific Team

```bash
# Get active issues for team with key "JET" (Jetpack)
/Users/paolo/.claude/skills/personal-assistant/scripts/linear_fetch.py team JET

# Get 75 issues from team "TOT" (Totoro)
/Users/paolo/.claude/skills/personal-assistant/scripts/linear_fetch.py team TOT 75
```

### Get Your User Info

```bash
/Users/paolo/.claude/skills/personal-assistant/scripts/linear_fetch.py me
```

## Output Format

The script outputs JSON with comprehensive issue data:

```json
{
  "viewer": {
    "id": "user-id",
    "name": "Your Name",
    "email": "your@email.com"
  },
  "count": 23,
  "mode": "active",
  "issues": [
    {
      "id": "issue-id",
      "identifier": "JET-123",
      "title": "Issue title",
      "description": "Issue description in markdown",
      "priority": 2,
      "priority_label": "High",
      "url": "https://linear.app/team/issue/JET-123",
      "created_at": "2025-11-01T10:00:00.000Z",
      "updated_at": "2025-11-05T14:30:00.000Z",
      "due_date": "2025-11-10",
      "state": {
        "id": "state-id",
        "name": "In Progress",
        "type": "started",
        "color": "#f2c94c"
      },
      "team": {
        "id": "team-id",
        "key": "JET",
        "name": "Jetpack"
      },
      "assignee": {
        "id": "user-id",
        "name": "Your Name",
        "email": "your@email.com"
      },
      "creator": {
        "id": "creator-id",
        "name": "Creator Name",
        "email": "creator@email.com"
      },
      "project": {
        "id": "project-id",
        "name": "Q4 Initiatives",
        "url": "https://linear.app/team/project/q4-initiatives"
      },
      "labels": [
        {
          "id": "label-id",
          "name": "bug",
          "color": "#eb5757"
        }
      ],
      "comment_count": 5,
      "latest_comment": {
        "id": "comment-id",
        "createdAt": "2025-11-05T12:00:00.000Z",
        "body": "Comment text",
        "user": {
          "name": "Commenter Name"
        }
      },
      "parent": {
        "id": "parent-id",
        "identifier": "JET-100",
        "title": "Parent issue title"
      },
      "child_count": 2,
      "children": [
        {
          "id": "child-id",
          "identifier": "JET-124",
          "title": "Child issue title"
        }
      ]
    }
  ]
}
```

## Integration Examples

### Morning Briefing Integration

```python
import subprocess
import json

# Fetch active issues
result = subprocess.run(
    ['/Users/paolo/.claude/skills/personal-assistant/scripts/linear_fetch.py', 'active', '50'],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)
issues = data['issues']

# Process issues for briefing
deep_work = []
shallow_work = []

for issue in issues:
    # Categorize by priority and state
    if issue['priority'] <= 2 and issue['state']['type'] == 'started':
        deep_work.append(issue)
    else:
        shallow_work.append(issue)

# Add to briefing sections...
```

### Evening Reflection Integration

```python
import subprocess
import json
from datetime import datetime, timezone

# Get today's date at 00:00 UTC
today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

# Fetch issues updated today
result = subprocess.run(
    ['/Users/paolo/.claude/skills/personal-assistant/scripts/linear_fetch.py', 'updated_today', '50'],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)
issues = data['issues']

# Group by state change
completed = [i for i in issues if i['state']['type'] == 'completed']
in_progress = [i for i in issues if i['state']['type'] == 'started']
blocked = [i for i in issues if 'blocked' in [label['name'].lower() for label in i['labels']]]

# Add to evening reflection...
```

### Weekly Review Integration

```python
import subprocess
import json

# Fetch issues completed this week
result = subprocess.run(
    ['/Users/paolo/.claude/skills/personal-assistant/scripts/linear_fetch.py', 'completed_this_week', '100'],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)
completed_issues = data['issues']

# Fetch all active issues for context
result = subprocess.run(
    ['/Users/paolo/.claude/skills/personal-assistant/scripts/linear_fetch.py', 'active', '100'],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)
active_issues = data['issues']

# Calculate metrics
completed_count = len(completed_issues)
in_progress_count = len([i for i in active_issues if i['state']['type'] == 'started'])
blocked_count = len([i for i in active_issues if 'blocked' in [label['name'].lower() for label in i['labels']]])

# Break down by type
features = len([i for i in completed_issues if 'feature' in [label['name'].lower() for label in i['labels']]])
bugs = len([i for i in completed_issues if 'bug' in [label['name'].lower() for label in i['labels']]])

# Add to weekly review...
```

## Filtering and Querying

The script supports several built-in modes, but you can also modify it to add custom filters:

### Available State Types
- `started` - Issues in progress
- `unstarted` - Not yet started
- `completed` - Finished issues
- `canceled` - Canceled issues
- `backlog` - Backlog items

### Priority Levels
- `0` - No priority
- `1` - Urgent
- `2` - High
- `3` - Normal
- `4` - Low

### Common Team Keys
- `JET` - Jetpack
- `TOT` - Totoro
- `SOC` - Social
- `REG` - Registry
- `P2` - P2

## Troubleshooting

### "api_key_missing" Error

You need to save your Linear API key using one of these methods:

**Keychain (recommended):**
```bash
security add-generic-password -s linear-api -a personal-assistant -w "lin_api_YOUR_KEY_HERE"
```

**File (fallback):**
```bash
echo "lin_api_YOUR_KEY_HERE" > ~/.claude/linear_api_key.txt
chmod 600 ~/.claude/linear_api_key.txt
```

### "insecure_permissions" Warning

If using the file method, the script detected insecure file permissions:

```bash
chmod 600 ~/.claude/linear_api_key.txt
```

### Keychain Access Prompts

First time accessing the Keychain entry, macOS may prompt for your password or Touch ID. You can:
- **Allow Once**: Prompts every time (most secure)
- **Always Allow**: No future prompts for this script (convenient)

If you get too many prompts, consider using the file method instead.

### "api_error" or 401 Unauthorized

Your API key may be invalid or expired. Generate a new one:
1. Go to [Linear Settings → API](https://linear.app/settings/api)
2. Revoke the old key
3. Create a new key
4. Update `~/.claude/linear_api_key.txt`

### "team_not_found" Error

The team key you provided doesn't exist. Common keys:
- Check your Linear workspace for exact team keys
- Team keys are usually 2-4 uppercase letters
- Case sensitive

### Empty Results

If you get 0 issues:
- Check that you have issues assigned to you in Linear
- Try `active` mode first to see all assigned issues
- Verify the date range for `updated_today` or `completed_this_week`

## Security Notes

### Storage Security

**Keychain (Recommended):**
- ✅ Encrypted storage using macOS security framework
- ✅ Protected by your login password/Touch ID
- ✅ Not accessible to other users
- ✅ Can be backed up separately via iCloud Keychain
- ✅ Industry standard for credential storage

**File Method:**
- ⚠️ Stored as plain text on disk (even with chmod 600)
- ⚠️ Readable by any process running as your user
- ⚠️ Included in Time Machine and other backups
- ⚠️ Visible in file system
- ✅ Never commit `~/.claude/linear_api_key.txt` to git
- ✅ Should be in your `.gitignore`

### API Key Permissions

- The API key has full read/write access to your Linear workspace
- Can create, read, update, and delete issues, comments, and projects
- Treat it like a password
- Revoke old keys when generating new ones
- Consider creating separate keys for different purposes

### Best Practices

1. **Use Keychain when possible** - It's the most secure option on macOS
2. **Rotate keys periodically** - Generate new keys every 3-6 months
3. **Revoke compromised keys immediately** - If you accidentally expose a key
4. **Use descriptive key names in Linear** - "Personal Assistant - MacBook Pro" to track usage
5. **Monitor API usage** - Check Linear settings for unexpected activity

## Performance

- GraphQL queries are efficient (single round-trip)
- Typical response time: 200-500ms
- Fetching 50 issues: ~2,000-3,000 tokens
- Much more efficient than MCP for large issue lists

## Rate Limits

Linear API has rate limits:
- Standard tier: 1000 requests per hour
- Our usage is well within limits (typically <10 requests per briefing)
- The script doesn't implement caching, but could be added if needed

## Maintenance

### API Key Rotation

To rotate your API key:
1. Generate new key in Linear
2. Update `~/.claude/linear_api_key.txt`
3. Revoke old key in Linear

### Extending the Script

The script uses GraphQL, so you can add custom queries:
- Modify the `get_issues()` function to add more filters
- Add new modes to the `main()` function
- Extend the GraphQL query to fetch additional fields
- See [Linear API docs](https://developers.linear.app/docs/graphql/working-with-the-graphql-api) for more options
