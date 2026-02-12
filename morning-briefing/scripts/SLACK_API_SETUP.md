# Slack API Direct Access Setup

This guide explains how to set up direct Slack API access using the Slack Web API to retrieve messages, mentions, and activity data efficiently.

## Why This Approach?

Using the Slack API directly provides:
- **Full control**: Direct REST API calls with exactly the data you need
- **Efficiency**: Fetch only required data, reducing token usage
- **Flexibility**: Custom queries, time filtering, priority user handling
- **Reliability**: No dependency on MCP server availability
- **Performance**: Optimized queries for common use cases

## Implementation Details

### Search-Based Architecture (Avoiding Rate Limits)

This script uses Slack's `search.messages` API with time-based filtering to avoid rate limits in large workspaces:

**OLD approach (caused rate limits):**
1. Call `conversations.list` to fetch ALL conversations (1000+ in large workspaces)
2. Iterate through each conversation
3. Filter by time after fetching all data
4. ❌ Result: Immediate HTTP 429 rate limits

**NEW approach (no rate limits):**
1. Use `search.messages` with query syntax like `<@USER_ID> after:YYYY-MM-DD`
2. Slack filters at API level and returns only matching messages
3. ✅ Result: Single API call, no rate limits, much faster

**Query patterns used:**
- **Mentions**: `<@USER_ID> after:YYYY-MM-DD` - finds messages mentioning you
- **Activity**: `from:<@USER_ID> after:YYYY-MM-DD` - finds your sent messages
- **DMs**: `in:im after:YYYY-MM-DD` - finds all DM messages

### Form-Encoded Parameters

All Slack API methods (including `conversations.info`, `search.messages`, `users.list`) use form-encoded parameters (`application/x-www-form-urlencoded`), not JSON. The script automatically handles this for all API calls.

## Setup Steps

### 1. Install Required Python Package

```bash
pip3 install requests
```

### 2. Create a Slack App

1. Go to [Slack API Apps](https://api.slack.com/apps)
2. Click "Create New App"
3. Choose "From scratch"
4. Name it "Personal Assistant" or similar
5. Select your workspace

### 3. Configure OAuth Scopes

In your app settings, go to "OAuth & Permissions" and add these scopes:

**User Token Scopes** (recommended):
- `channels:history` - View messages in public channels
- `channels:read` - View basic channel info
- `groups:history` - View messages in private channels
- `groups:read` - View basic private channel info
- `im:history` - View messages in DMs
- `im:read` - View basic DM info
- `mpim:history` - View messages in group DMs
- `mpim:read` - View basic group DM info
- `users:read` - View users in workspace
- `search:read` - Search messages

**Why User Token**: User tokens act on behalf of you, so they see only what you have access to. This is more secure than Bot tokens which can access everything.

### 4. Install App to Workspace

1. Still in "OAuth & Permissions", click "Install to Workspace"
2. Review permissions and allow
3. Copy the "User OAuth Token" (starts with `xoxp-`)
4. **Important**: This is your personal access token - treat it like a password

### 5. Store Your Token Securely in macOS Keychain

Store your OAuth token in the encrypted macOS Keychain:

```bash
security add-generic-password -s slack-api -a personal-assistant -w "xoxp-YOUR-TOKEN-HERE"
```

**Benefits:**
- ✅ Encrypted storage using macOS security framework
- ✅ Protected by your macOS login password
- ✅ Can require Touch ID/password for access
- ✅ Standard practice for sensitive credentials
- ✅ Not stored in plain text anywhere
- ✅ Not visible in file system or backups

**To verify it was added:**
```bash
security find-generic-password -s slack-api -a personal-assistant -w
```

**To update the token:**
```bash
security delete-generic-password -s slack-api -a personal-assistant
security add-generic-password -s slack-api -a personal-assistant -w "NEW_TOKEN_HERE"
```

**To remove:**
```bash
security delete-generic-password -s slack-api -a personal-assistant
```

### 6. Verify Setup

Test the connection:

```bash
/Users/paolo/.claude/skills/morning-briefing/scripts/slack_fetch.py mentions 1
```

You should see your mentions from the last hour in JSON format.

## Usage

### Get Mentions

Fetch messages mentioning you, with priority DM separation:

```bash
# Default: last 24 hours
/Users/paolo/.claude/skills/morning-briefing/scripts/slack_fetch.py mentions

# Last 12 hours
/Users/paolo/.claude/skills/morning-briefing/scripts/slack_fetch.py mentions 12

# Since yesterday evening (19 hours ago)
/Users/paolo/.claude/skills/morning-briefing/scripts/slack_fetch.py mentions 19
```

**Output includes:**
- Priority DMs (Matt Mullenweg, Pedraum Pardehpoosh) shown first
- Other mentions from channels and DMs
- Message text, timestamp, channel/user name
- Permalinks to messages

### Get Your Activity

Fetch your own messages, grouped by channel:

```bash
# Default: last 24 hours
/Users/paolo/.claude/skills/morning-briefing/scripts/slack_fetch.py activity

# Last 12 hours
/Users/paolo/.claude/skills/morning-briefing/scripts/slack_fetch.py activity 12
```

**Output includes:**
- Priority DMs with message counts
- Channel activity (messages sent by you)
- Total message count
- Organized by priority users first

### Get All DMs

List all DM conversations with recent activity:

```bash
# All DMs with any messages
/Users/paolo/.claude/skills/morning-briefing/scripts/slack_fetch.py dms

# DMs with activity in last 24 hours
/Users/paolo/.claude/skills/morning-briefing/scripts/slack_fetch.py dms 24

# DMs with activity in last week
/Users/paolo/.claude/skills/morning-briefing/scripts/slack_fetch.py dms 168
```

**Output includes:**
- DM conversations sorted by priority, then by message count
- User names and message counts
- Latest message preview
- Priority user flag

## Output Format

### Mentions Mode

```json
{
  "mode": "mentions",
  "since_hours": 24,
  "user_id": "U12345",
  "priority_dm_count": 2,
  "other_mention_count": 5,
  "priority_dms": [
    {
      "channel_id": "D12345",
      "channel_name": "Matt Mullenweg",
      "timestamp": "2025-11-06T10:30:00+00:00",
      "user": "Matt Mullenweg",
      "text": "Hey @paolo can you look at this?",
      "thread_ts": null,
      "permalink": "slack://channel?id=D12345&message=1699267800"
    }
  ],
  "other_mentions": [
    {
      "channel_id": "C12345",
      "channel_name": "domains",
      "timestamp": "2025-11-06T14:20:00+00:00",
      "user": "Alice Smith",
      "text": "Thanks @paolo for the help!",
      "thread_ts": "1699253400",
      "permalink": "slack://channel?id=C12345&message=1699281600"
    }
  ]
}
```

### Activity Mode

```json
{
  "mode": "activity",
  "since_hours": 24,
  "user_id": "U12345",
  "total_messages": 45,
  "priority_dms": [
    {
      "user": "Matt Mullenweg",
      "message_count": 3,
      "channel_id": "D12345"
    }
  ],
  "channel_activity": {
    "#domains": 15,
    "#jetpack-backend": 8,
    "DM: Alice Smith": 4
  }
}
```

### DMs Mode

```json
{
  "mode": "dms",
  "since_hours": 24,
  "user_id": "U12345",
  "dm_count": 8,
  "dms": [
    {
      "user": "Matt Mullenweg",
      "user_id": "U67890",
      "channel_id": "D12345",
      "message_count": 5,
      "is_priority": true,
      "latest_message": {
        "timestamp": "2025-11-06T16:45:00+00:00",
        "text": "Sounds good, let's sync tomorrow"
      }
    }
  ]
}
```

## Integration Examples

### Morning Briefing Integration

```python
import subprocess
import json

# Fetch mentions since yesterday evening (19 hours ago)
result = subprocess.run(
    ['/Users/paolo/.claude/skills/morning-briefing/scripts/slack_fetch.py', 'mentions', '19'],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)

# Separate priority DMs
priority_dms = data['priority_dms']
other_mentions = data['other_mentions']

# Add to briefing sections...
```

### Evening Reflection Integration

```python
import subprocess
import json

# Fetch activity from last 24 hours
result = subprocess.run(
    ['/Users/paolo/.claude/skills/morning-briefing/scripts/slack_fetch.py', 'activity', '24'],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)

# Get totals
total_messages = data['total_messages']
priority_dms = data['priority_dms']
channel_activity = data['channel_activity']

# Format for evening reflection...
```

## Priority Users

The script has built-in priority handling for specific users. Priority DMs are:
- Always shown first in results
- Separated from other mentions
- Highlighted in activity summaries

**Currently configured priority users:**
- Matt Mullenweg
- Pedraum Pardehpoosh

To modify priority users, edit the `PRIORITY_USERS` dict in `slack_fetch.py`:

```python
PRIORITY_USERS = {
    'Matt Mullenweg': None,
    'Pedraum Pardehpoosh': None,
    'Your Boss Name': None  # Add more as needed
}
```

## Time Range Filtering

All modes support flexible time range filtering:

- `mentions 1` - Last hour
- `mentions 12` - Last 12 hours (half day)
- `mentions 19` - Since yesterday evening (for morning briefing)
- `mentions 24` - Last 24 hours (full day)
- `activity 24` - Last day of activity
- `dms 168` - Last week of DM activity
- `dms 0` or `dms` - All time

## Troubleshooting

### "token_missing" Error

You need to add your Slack OAuth token to Keychain:

```bash
security add-generic-password -s slack-api -a personal-assistant -w "xoxp-YOUR-TOKEN-HERE"
```

### Keychain Access Prompts

First time accessing the Keychain entry, macOS may prompt for your password or Touch ID. You can:
- **Allow Once**: Prompts every time (most secure)
- **Always Allow**: No future prompts for this script (convenient)

### "slack_api_error" - invalid_auth

Your token may be invalid or expired. Token issues to check:

1. **Token revoked**: Go to [Slack Apps](https://api.slack.com/apps) and reinstall your app
2. **Wrong token type**: Make sure you copied the "User OAuth Token" (xoxp-...), not the Bot token
3. **Workspace changed**: If you left/rejoined workspace, you'll need a new token
4. **Token expired**: Slack tokens can expire if unused for long periods

To get a new token:
1. Go to your app in [Slack Apps](https://api.slack.com/apps)
2. Navigate to "OAuth & Permissions"
3. Click "Reinstall to Workspace"
4. Copy the new "User OAuth Token"
5. Update Keychain:
   ```bash
   security delete-generic-password -s slack-api -a personal-assistant
   security add-generic-password -s slack-api -a personal-assistant -w "NEW_TOKEN_HERE"
   ```

### "slack_api_error" - missing_scope

Your app needs additional OAuth scopes. Go to your app settings:

1. Navigate to "OAuth & Permissions"
2. Add missing scopes (see Setup Step 3)
3. Reinstall app to workspace
4. Get new token and update Keychain:
   ```bash
   security delete-generic-password -s slack-api -a personal-assistant
   security add-generic-password -s slack-api -a personal-assistant -w "NEW_TOKEN_HERE"
   ```

### Empty Results

If you get 0 mentions/messages:

- Check that you have activity in Slack during the time range
- Try increasing the time range: `slack_fetch.py mentions 48`
- Verify your token works: Check [Slack Apps](https://api.slack.com/apps) shows your app installed
- Make sure you're searching the right workspace

### Rate Limits

Slack API has rate limits:
- Tier 3 methods: ~50 requests per minute
- Our usage is typically well within limits (< 20 requests per briefing)
- The script doesn't currently implement rate limit handling
- If you hit limits, wait 1 minute before retrying

## Security Notes

### Token Storage

**macOS Keychain:**
- ✅ Encrypted storage using macOS security framework
- ✅ Protected by your login password/Touch ID
- ✅ Not accessible to other users
- ✅ Can be backed up separately via iCloud Keychain
- ✅ Industry standard for credential storage

### Token Security

**Your Slack OAuth token**:
- Has full read access to your Slack workspace (everything you can see)
- Can read all messages, files, and user info you have access to
- Treat it like your Slack password
- Never share it or commit to git

**Best Practices:**
1. **Rotate tokens periodically** - Reinstall app every 3-6 months
2. **Revoke if compromised** - Delete and reinstall app immediately
3. **Use descriptive app name** - "Personal Assistant - MacBook Pro" to track usage
4. **Monitor app usage** - Check [Slack Apps](https://api.slack.com/apps) for unexpected activity

### Scope Minimization

The setup uses **User Token Scopes** which:
- ✅ Only access what you can already access
- ✅ Can't modify anything (read-only scopes)
- ✅ Can't post messages or take actions
- ✅ Respect your channel memberships and permissions

### Data Privacy

- Script only fetches data you already have access to
- No data is sent to external services (besides Slack API)
- All data stays local on your machine
- Results are printed to stdout in JSON format
- No caching or persistent storage (fetch fresh each time)

## Performance

- REST API calls are efficient (single request per channel/conversation)
- Typical response time: 500-2000ms depending on workspace size
- Fetching mentions from 10 channels: ~1-2 seconds
- Fetching 24h activity across workspace: ~2-3 seconds
- Much more efficient than MCP for bulk operations

## Limitations

### Current Limitations

1. **No threading detail**: Thread messages are mentioned but not fully expanded
2. **No reactions**: Emoji reactions are not fetched
3. **No file content**: File attachments are not downloaded
4. **Limited message history**: Fetches last 100 messages per channel (API limit)
5. **No real-time**: Must be polled; no webhook/websocket support

### Workarounds

- **Threading**: Use the `thread_ts` field to identify threaded conversations
- **More history**: Run multiple queries with different time ranges
- **Real-time**: Set up cron jobs to run every N minutes

### Future Enhancements

Possible improvements:
- macOS Keychain support (like Linear)
- Message threading expansion
- Reaction counts
- File attachment metadata
- Cursor-based pagination for large result sets
- Caching to reduce API calls
- Rate limit handling and retry logic

## API Documentation

Official Slack API documentation:
- [Web API Methods](https://api.slack.com/methods)
- [OAuth Scopes](https://api.slack.com/scopes)
- [Conversations API](https://api.slack.com/messaging/retrieving)
- [Search API](https://api.slack.com/methods/search.messages)
- [Rate Limits](https://api.slack.com/docs/rate-limits)

## Maintenance

### Token Rotation

To rotate your OAuth token:
1. Go to [Slack Apps](https://api.slack.com/apps)
2. Select your app
3. Navigate to "OAuth & Permissions"
4. Click "Reinstall to Workspace"
5. Copy new "User OAuth Token"
6. Update `~/.claude/slack_token.txt`

### Updating Priority Users

Edit the script if your priority contacts change:

```bash
# Edit the PRIORITY_USERS dictionary
vim /Users/paolo/.claude/skills/morning-briefing/scripts/slack_fetch.py

# Find and modify this section:
PRIORITY_USERS = {
    'Matt Mullenweg': None,
    'Pedraum Pardehpoosh': None,
    'New Priority Contact': None
}
```

### Extending Functionality

The script uses modular functions, making it easy to add new modes:

```python
def mode_my_new_feature(token, user_id, **kwargs):
    """
    Implement your custom feature.
    """
    # Your code here
    pass

# Add to main():
elif mode == 'my_new_feature':
    result = mode_my_new_feature(token, user_id)
    print(json.dumps(result, indent=2))
```
