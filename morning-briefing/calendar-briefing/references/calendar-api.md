# Google Calendar API Integration

## Script Location

```
/Users/paolo/.claude/skills/morning-briefing/scripts/calendar_fetch.py
```

## Usage

```bash
python3 calendar_fetch.py <timeframe> [days]
```

## Available Timeframes

- `today` - Events for today only
- `tomorrow` - Events for tomorrow
- `week` - Events for next 7 days
- `days <N>` - Events for next N days

## Output Format

The script returns JSON with this structure:

```json
{
  "timeframe": "today",
  "start_date": "2025-11-08",
  "end_date": "2025-11-08",
  "event_count": 5,
  "events": [
    {
      "id": "event_id_123",
      "summary": "Team Standup",
      "description": "Daily team sync...",
      "start": {
        "dateTime": "2025-11-08T09:00:00-08:00",
        "timeZone": "America/Los_Angeles"
      },
      "end": {
        "dateTime": "2025-11-08T09:30:00-08:00",
        "timeZone": "America/Los_Angeles"
      },
      "location": "Google Meet",
      "hangoutLink": "https://meet.google.com/abc-defg-hij",
      "conferenceData": {
        "entryPoints": [
          {
            "entryPointType": "video",
            "uri": "https://meet.google.com/abc-defg-hij"
          }
        ]
      },
      "attendees": [
        {
          "email": "person1@example.com",
          "displayName": "Person One",
          "responseStatus": "accepted"
        }
      ],
      "creator": {
        "email": "paolo@a8c.com",
        "displayName": "Paolo Belcastro"
      },
      "organizer": {
        "email": "paolo@a8c.com",
        "displayName": "Paolo Belcastro"
      },
      "htmlLink": "https://calendar.google.com/calendar/event?eid=...",
      "status": "confirmed"
    }
  ]
}
```

## Key Fields

- **id**: Unique event ID
- **summary**: Event title
- **description**: Event description/notes (optional)
- **start.dateTime**: Event start time (ISO 8601 format with timezone)
- **end.dateTime**: Event end time
- **location**: Physical or virtual location
- **hangoutLink**: Google Meet link (if available)
- **conferenceData.entryPoints[]**: All video/phone conference links
- **attendees[]**: List of attendees with response status
- **htmlLink**: Link to view event in Google Calendar
- **status**: confirmed, tentative, or cancelled

## Response Status Values

- **accepted**: Attendee accepted the invitation
- **declined**: Attendee declined
- **tentative**: Attendee marked as tentative/maybe
- **needsAction**: No response yet

## Event Status Values

- **confirmed**: Event is confirmed
- **tentative**: Event is tentative
- **cancelled**: Event was cancelled (usually excluded from results)

## API Authentication

OAuth token cached at `~/.claude/gmail_token.json` (shared with Gmail).

First run may require browser authentication to Google account.

## Performance

- Typical fetch time: 2-3 seconds for today's events
- Supports fetching up to 30 days ahead
- No rate limiting concerns for typical usage
