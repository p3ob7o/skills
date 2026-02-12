# Event Formatting Rules

## Time Formatting

### Standard Events
Convert ISO 8601 to human-readable format:
- Input: `"2025-11-08T09:00:00-08:00"` to `"2025-11-08T09:30:00-08:00"`
- Output: `"9:00 AM - 9:30 AM"`

### Time Parsing
- Extract hour and minute from ISO 8601
- Convert 24-hour to 12-hour format
- Add AM/PM suffix
- Show timezone only if different from user's default

### All-Day Events
- Show at top of list
- Format: `"All Day: Team Offsite"`
- No time range shown
- Check: `start.date` field present (not `start.dateTime`)

### Multi-Day Events
- Show date range: `"Nov 8-10: Conference"`
- Include start and end dates
- Mark as spanning multiple days

## Meeting Links Priority

When multiple link options exist, prioritize in this order:

1. **Google Meet** (`hangoutLink` field)
   - Most common for Google Calendar
   - Direct link to join

2. **Zoom links**
   - Check `description` for zoom.us URLs
   - Check `conferenceData.entryPoints[]` for Zoom

3. **Other conference platforms**
   - Microsoft Teams
   - Webex
   - Custom video links

4. **Calendar event link** (fallback)
   - Use `htmlLink` if no video link found
   - Links to view event in Google Calendar

## Attendee Display

### Count Only (default)
- Show total: `"8 attendees"`
- Exclude resources (rooms, equipment)
- Count based on `attendees` array length

### Names for Small Meetings (< 5 people)
- Show attendee names for 1-on-1s and small groups
- Format: `"With: Alice Smith, Bob Jones"`
- Useful for personal context

### Excluding Resources
- Check `attendee.resource` field
- Exclude conference rooms
- Exclude equipment (projectors, etc.)

## Event Status Indicators

### Confirmed (default)
- Show normally, no special indicator
- Most common status

### Tentative
- Add indicator: `"⚠️ Tentative"`
- Show after event title
- User hasn't confirmed attendance

### Cancelled
- Option 1: Skip entirely (recommended)
- Option 2: Show with strikethrough: `"~~Meeting Title~~ ❌ Cancelled"`

### Declined by User
- Skip by default
- User explicitly declined invitation
- No need to show in daily briefing

## Special Event Types

### Out of Office
- Indicator: `"🚫 Out of Office"`
- Show start/end time
- Usually all-day or multi-day

### Focus Time / Working Hours
- Indicator: `"🎯 Focus Time"`
- Personal time block
- Not a meeting with others

### Recurring Events
- Show each occurrence normally
- Optional note: `"(Recurring)"` after title
- Don't group, show individually

### Private Events
- Title may be hidden: `"Busy"`
- Respect privacy - don't try to fetch details
- Show time block only

## Output Format for Daily Note

Standard format:
```markdown
- **9:00 AM - 9:30 AM**: [Team Standup](https://meet.google.com/abc-defg-hij) (8 attendees)
- **10:00 AM - 11:00 AM**: [Product Review](https://zoom.us/j/123) (5 attendees)
- **2:00 PM - 3:00 PM**: [1:1 with Manager](https://calendar.google.com/...) (2 attendees)
```

With special indicators:
```markdown
- **All Day**: Conference in San Francisco
- **9:00 AM - 5:00 PM**: 🚫 Out of Office
- **2:00 PM - 3:00 PM**: [Meeting Title](link) ⚠️ Tentative
```

## Timezone Handling

### User's Default Timezone
- Assume all times in user's configured timezone
- Don't show timezone suffix by default
- Google Calendar API returns times in local timezone

### Different Timezone Events
- If event timezone != user timezone:
- Show timezone: `"9:00 AM PST - 10:00 AM PST"`
- Or convert and note: `"6:00 PM EST (3:00 PM PST)"`

### International Events
- Show original timezone for clarity
- Help user understand timing for different regions
