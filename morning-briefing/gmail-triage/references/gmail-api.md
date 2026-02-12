# Gmail API Integration

## Script Location

```
/Users/paolo/.claude/skills/morning-briefing/scripts/gmail_fetch.py
```

## Usage

```bash
python3 gmail_fetch.py "<query>" <max_results>
```

## Common Queries

- Unread inbox: `"in:inbox is:unread"`
- Starred emails: `"is:starred"`
- Today's emails: `"newer_than:1d"`
- From specific person: `"from:john@example.com"`
- Combine filters: `"in:inbox is:unread from:john@example.com"`

## Query Operators

- `in:inbox` - Messages in inbox
- `is:unread` - Unread messages
- `is:starred` - Starred messages
- `is:important` - Important messages
- `from:email@domain.com` - From specific sender
- `to:email@domain.com` - To specific recipient
- `subject:keyword` - Subject contains keyword
- `newer_than:Xd` - Received in last X days
- `older_than:Xd` - Received more than X days ago

## Output Format

The script returns JSON with this structure:

```json
{
  "count": 25,
  "emails": [
    {
      "id": "msg_id_123",
      "thread_id": "thread_id_456",
      "from": "John Doe <john@example.com>",
      "to": "paolo@a8c.com",
      "subject": "Email subject here",
      "date": "2025-01-15T10:30:00Z",
      "labels": ["UNREAD", "INBOX"],
      "snippet": "First 200 characters of email body...",
      "message_url": "https://mail.google.com/mail/u/0/#inbox/msg_id_123"
    }
  ]
}
```

## Key Fields

- **id**: Unique message ID
- **thread_id**: Conversation thread ID
- **from**: Sender name and email (format: "Name <email>")
- **to**: Recipient email
- **subject**: Email subject line
- **date**: When email was received (ISO 8601 format)
- **labels**: Gmail labels array (UNREAD, IMPORTANT, STARRED, INBOX, etc.)
- **snippet**: Preview of email content (~200 chars)
- **message_url**: Direct link to email in Gmail web UI

## Performance

- Typical fetch time: 2-3 seconds for up to 150 emails
- OAuth token cached at `~/.claude/gmail_token.json`
- First run may require browser authentication
