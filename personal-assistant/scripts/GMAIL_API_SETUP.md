# Gmail & Calendar API Direct Access Setup

This guide explains how to set up direct Gmail and Calendar API access to retrieve data without unnecessary content, avoiding the Zapier MCP token limits.

## Why This Approach?

The Zapier Gmail MCP tool always returns full email bodies, causing token limit issues with large inboxes. This direct API approach:
- **Gmail**: Fetches only metadata (subject, from, to, date, labels) without body content
- **Calendar**: Fetches only essential event data (title, time, attendees) with full control
- Dramatically reduced token usage
- Can handle hundreds of items within token limits
- Full control over filtering and pagination

## Setup Steps

### 1. Install Required Python Packages

```bash
pip3 install --upgrade google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 2. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing one)
3. Name it something like "Personal Assistant Gmail Access"

### 3. Enable Gmail API and Calendar API

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Gmail API" and click "Enable"
3. Search for "Google Calendar API" and click "Enable"

### 4. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: "Personal Assistant"
   - User support email: Your email
   - Developer contact: Your email
   - Add scopes:
     - `../auth/gmail.readonly`
     - `../auth/calendar.readonly`
   - Add your email as a test user
4. Create OAuth client ID:
   - Application type: "Desktop app"
   - Name: "Personal Assistant Gmail"
5. Download the JSON file
6. Save it as: `~/.claude/gmail_credentials.json`

### 5. First Run Authentication

The first time you run the script, it will:
1. Open your browser for OAuth authentication
2. Ask you to sign in to your Google account
3. Request permission to read your Gmail
4. Save the token to `~/.claude/gmail_token.json`

Subsequent runs will use the saved token.

## Usage

### Retrieve All Inbox Emails

```bash
/Users/paolo/.claude/skills/personal-assistant/scripts/gmail_fetch.py
```

### With Custom Query

```bash
# Unread emails only
/Users/paolo/.claude/skills/personal-assistant/scripts/gmail_fetch.py "in:inbox is:unread"

# Important emails
/Users/paolo/.claude/skills/personal-assistant/scripts/gmail_fetch.py "is:important"

# Starred emails
/Users/paolo/.claude/skills/personal-assistant/scripts/gmail_fetch.py "is:starred"

# Recent emails (last 7 days)
/Users/paolo/.claude/skills/personal-assistant/scripts/gmail_fetch.py "in:inbox after:2025/10/29"
```

### Limit Number of Results

```bash
# Get 50 emails
/Users/paolo/.claude/skills/personal-assistant/scripts/gmail_fetch.py "in:inbox" 50

# Get 200 emails (more than default 100)
/Users/paolo/.claude/skills/personal-assistant/scripts/gmail_fetch.py "in:inbox" 200
```

### Retrieve Calendar Events

```bash
# Get today's events
/Users/paolo/.claude/skills/personal-assistant/scripts/calendar_fetch.py "2025-11-05T00:00:00+01:00" "2025-11-05T23:59:59+01:00"

# Get tomorrow's events
/Users/paolo/.claude/skills/personal-assistant/scripts/calendar_fetch.py "2025-11-06T00:00:00+01:00" "2025-11-06T23:59:59+01:00"

# Get events from a specific calendar
/Users/paolo/.claude/skills/personal-assistant/scripts/calendar_fetch.py "2025-11-05T00:00:00+01:00" "2025-11-05T23:59:59+01:00" "paolo@a8c.com"

# Get more events (default is 50)
/Users/paolo/.claude/skills/personal-assistant/scripts/calendar_fetch.py "2025-11-05T00:00:00+01:00" "2025-11-05T23:59:59+01:00" "primary" 100
```

## Output Formats

### Gmail Output

The gmail_fetch.py script outputs JSON:

```json
{
  "count": 123,
  "emails": [
    {
      "id": "19a5566cea1204e8",
      "thread_id": "19a5566cea1204e8",
      "labels": ["UNREAD", "CATEGORY_UPDATES", "INBOX"],
      "snippet": "Brief preview of email content...",
      "from": "Sender Name <sender@example.com>",
      "to": "paolo@a8c.com",
      "subject": "Email subject line",
      "date": "Wed, 05 Nov 2025 19:03:10 +0000 (UTC)",
      "message_url": "https://mail.google.com/mail/u/0/#inbox/19a5566cea1204e8"
    }
  ]
}
```

### Calendar Output

The calendar_fetch.py script outputs JSON:

```json
{
  "count": 5,
  "start_time": "2025-11-05T00:00:00+01:00",
  "end_time": "2025-11-05T23:59:59+01:00",
  "calendar_id": "primary",
  "events": [
    {
      "id": "event_id_here",
      "summary": "Team Standup",
      "description": "Daily team sync",
      "location": "Zoom",
      "start": "2025-11-05T09:00:00+01:00",
      "end": "2025-11-05T09:30:00+01:00",
      "all_day": false,
      "status": "confirmed",
      "attendees": [
        {
          "email": "colleague@example.com",
          "name": "Colleague Name",
          "response_status": "accepted",
          "organizer": false
        }
      ],
      "attendee_count": 5,
      "organizer": "paolo@a8c.com",
      "html_link": "https://calendar.google.com/calendar/event?eid=...",
      "hangout_link": "https://meet.google.com/...",
      "conference_data": {}
    }
  ]
}
```

## Token Usage Comparison

**Zapier MCP (with body):**
- 123 emails = ~74,000 tokens ❌ (exceeds 25,000 limit)

**Direct API (metadata only):**
- 123 emails = ~3,000-5,000 tokens ✅ (well within limits)

## Integration Examples

### Gmail Integration (Morning Briefing)

```python
import subprocess
import json

# Fetch inbox emails
result = subprocess.run(
    ['/Users/paolo/.claude/skills/personal-assistant/scripts/gmail_fetch.py', 'in:inbox', '150'],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)
emails = data['emails']

# Process emails for triage
for email in emails:
    # Classify based on subject, from, labels, etc.
    # No body content available, but that's fine for triage
    pass
```

### Calendar Integration (Morning Briefing)

```python
import subprocess
import json
from datetime import datetime, timedelta

# Get today's date range
today = datetime.now()
start_time = today.replace(hour=0, minute=0, second=0).isoformat()
end_time = today.replace(hour=23, minute=59, second=59).isoformat()

# Fetch today's calendar events
result = subprocess.run(
    ['/Users/paolo/.claude/skills/personal-assistant/scripts/calendar_fetch.py',
     start_time, end_time, 'paolo@a8c.com', '50'],
    capture_output=True,
    text=True
)

data = json.loads(result.stdout)
events = data['events']

# Process events for the briefing
for event in events:
    # Format event for display
    summary = event['summary']
    start = event['start']
    end = event['end']
    location = event['location']
    attendees = event['attendees']
    # Add to briefing...
```

## Troubleshooting

### "credentials_missing" Error

You need to download OAuth credentials from Google Cloud Console and save to `~/.claude/gmail_credentials.json`.

### "invalid_grant" Error or Missing Calendar Access

Token has expired or doesn't have calendar scope. This can happen if you set up Gmail first and then added Calendar API later.

**Solution**: Delete `~/.claude/gmail_token.json` and re-authenticate:
```bash
rm ~/.claude/gmail_token.json
# Run either script to re-authenticate with both scopes
/Users/paolo/.claude/skills/personal-assistant/scripts/gmail_fetch.py "in:inbox" 10
```

### Browser Doesn't Open for Auth

Try running the script from terminal directly to see authentication URL.

### Permission Denied Errors

Make sure script is executable: `chmod +x gmail_fetch.py`

## Security Notes

- `gmail_credentials.json` contains your OAuth client secret (keep private)
- `gmail_token.json` contains your access token (keep private, never commit to git)
- Both files are in `~/.claude/` which should be in your `.gitignore`
- The script only requests `gmail.readonly` scope (cannot modify or delete emails)

## Maintenance

### Token Refresh

Tokens automatically refresh when expired. If refresh fails, delete `gmail_token.json` and re-authenticate.

### Revoke Access

To revoke access:
1. Go to [Google Account Security](https://myaccount.google.com/permissions)
2. Find "Personal Assistant"
3. Click "Remove Access"
4. Delete `~/.claude/gmail_token.json`
