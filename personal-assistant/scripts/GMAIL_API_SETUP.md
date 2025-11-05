# Gmail API Direct Access Setup

This guide explains how to set up direct Gmail API access to retrieve emails without body content, avoiding the Zapier MCP token limits.

## Why This Approach?

The Zapier Gmail MCP tool always returns full email bodies, causing token limit issues with large inboxes. This direct API approach:
- Fetches only metadata (subject, from, to, date, labels)
- No email body content = dramatically reduced token usage
- Can handle hundreds of emails within token limits
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

### 3. Enable Gmail API

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click "Enable"

### 4. Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - User Type: External
   - App name: "Personal Assistant"
   - User support email: Your email
   - Developer contact: Your email
   - Add scope: `../auth/gmail.readonly`
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

## Output Format

The script outputs JSON:

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

## Token Usage Comparison

**Zapier MCP (with body):**
- 123 emails = ~74,000 tokens ❌ (exceeds 25,000 limit)

**Direct API (metadata only):**
- 123 emails = ~3,000-5,000 tokens ✅ (well within limits)

## Integration with Morning Briefing

To use this in the morning briefing skill:

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

## Troubleshooting

### "credentials_missing" Error

You need to download OAuth credentials from Google Cloud Console and save to `~/.claude/gmail_credentials.json`.

### "invalid_grant" Error

Token has expired. Delete `~/.claude/gmail_token.json` and re-authenticate.

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
