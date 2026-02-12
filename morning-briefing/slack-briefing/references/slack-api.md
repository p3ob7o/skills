# Slack API Integration

## Script Location

```
/Users/paolo/.claude/skills/morning-briefing/scripts/slack_fetch.py
```

## Usage

```bash
python3 slack_fetch.py <mode> <hours>
```

## Available Modes

- `conversations <hours>` - Fetch conversations from past N hours
- `mentions <hours>` - Fetch only @mentions
- `dms <hours>` - Fetch only direct messages
- `threads <hours>` - Fetch threads user participated in

## Output Format

The script returns JSON with this structure:

```json
{
  "timeframe_hours": 24,
  "timestamp_from": "2025-11-07T10:00:00Z",
  "timestamp_to": "2025-11-08T10:00:00Z",
  "conversation_count": 12,
  "conversations": [
    {
      "channel_id": "C12345",
      "channel_name": "product",
      "is_dm": false,
      "is_private": false,
      "thread_ts": "1699123456.123456",
      "permalink": "https://automattic.slack.com/archives/C12345/p1699123456",
      "messages": [
        {
          "user": "U67890",
          "user_name": "John Doe",
          "text": "@paolo Can you weigh in on the search redesign?",
          "ts": "1699123456.123456",
          "timestamp": "2025-11-08T09:30:00Z",
          "thread_ts": "1699123456.123456",
          "reply_count": 5,
          "mentions_user": true
        }
      ],
      "participant_count": 3,
      "message_count": 5,
      "last_message_time": "2025-11-08T09:45:00Z",
      "user_mentioned": true,
      "user_participated": true
    }
  ],
  "dm_count": 3,
  "mention_count": 5,
  "thread_count": 4
}
```

## Key Fields

### Conversation Level
- **channel_id**: Unique channel identifier
- **channel_name**: Human-readable channel or DM partner name
- **is_dm**: Boolean indicating if this is a direct message
- **is_private**: Boolean for private channels
- **permalink**: Direct link to message/thread in Slack
- **user_mentioned**: Boolean if user was @mentioned in this conversation
- **user_participated**: Boolean if user posted in this thread
- **message_count**: Total messages in thread
- **participant_count**: Unique participants
- **last_message_time**: Most recent message timestamp

### Message Level
- **user**: User ID
- **user_name**: Display name of message author
- **text**: Message content
- **ts**: Slack timestamp (unique message ID)
- **timestamp**: ISO 8601 formatted time
- **thread_ts**: Parent thread timestamp (same as ts if root message)
- **reply_count**: Number of replies in thread
- **mentions_user**: Boolean if user was @mentioned in this specific message

## Workspace Configuration

### Required OAuth Scopes
- `channels:history` - Read public channel messages
- `groups:history` - Read private channel messages
- `im:history` - Read direct messages
- `mpim:history` - Read group direct messages
- `users:read` - Read user information
- `channels:read` - List channels
- `groups:read` - List private channels

### Authentication
Slack API token must be configured in environment or stored securely.

## Performance

- Typical fetch time: 5-10 seconds for 24 hours
- May be slower with many active channels
- Respects Slack API rate limits
