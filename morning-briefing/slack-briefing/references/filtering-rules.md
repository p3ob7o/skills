# Conversation Filtering and Prioritization

## Priority Levels

### High Priority
Conversations requiring immediate attention:

**Criteria:**
- Direct messages
- @mentions from leadership (Matt, Pedraum, direct manager)
- Messages with urgent keywords
- Questions directly directed at user
- DMs with "?" (questions)

**Urgent Keywords:**
- "urgent", "asap", "blocker", "critical", "emergency"
- "broken", "down", "failing", "not working"
- "help", "stuck", "blocked"
- "need", "required", "must"

**Display:**
- Show at top of list
- Include preview of message
- Show unread indicator

### Medium Priority
Important work conversations:

**Criteria:**
- @mentions in work channels (#product, #engineering, etc.)
- Threads user is actively participating in
- Threads with > 10 messages (active discussion)
- Mentions in team-specific channels
- Follow-up to user's previous messages

**Display:**
- Group by channel/type
- Show channel context
- Show last message preview

### Low Priority
General channel activity:

**Criteria:**
- General channel activity without mentions
- Threads user hasn't responded to
- FYI messages
- Announcements
- Non-urgent updates

**Display:**
- Optionally exclude from briefing
- Or show at bottom with minimal detail

## Exclude Rules

Skip these conversations entirely:

### Automated Messages
- Bot messages (unless directed at user with @mention)
- CI/CD notifications (GitHub Actions, etc.)
- Automated reports and digests
- Scheduled reminders
- Integration notifications (Linear, Jira, etc.)

### System Messages
- Channel join/leave messages
- Channel rename/purpose changes
- Pin/unpin notifications
- File upload notifications (unless relevant)

### Already-Handled
- Threads user already responded to (optional)
- Read messages (if tracking read status)
- Archived channel messages

### Noise
- Emoji-only reactions without context
- "Thanks" / "Got it" acknowledgments
- Thread continuations after user left
- Off-topic social channels (configurable)

## Filtering by Conversation Type

### Direct Messages (Highest Priority)
**Always include:**
- All DMs from past 24 hours
- Even if user already replied
- Show full message preview

**Exceptions:**
- Automated DMs from bots
- "X has joined Slack" welcome messages

### Mentions in Channels
**Include if:**
- User was explicitly @mentioned
- Or user's name appears in message text
- And message is in subscribed/active channel

**Context:**
- Show channel name prominently
- Include who mentioned user
- Show surrounding context (1-2 messages before/after)

### Active Threads
**Include if:**
- User posted at least one message
- AND thread has new messages since user's last post
- AND thread is still active (< 7 days old)

**Exclude if:**
- User was only CC'd (@here, @channel)
- Thread has > 100 messages (too noisy)
- Thread marked as resolved/closed

### Channel Activity
**Include if:**
- In user's primary channels (defined list)
- Significant discussion (> 5 participants)
- Tagged with important topics

**Exclude:**
- Random/social channels by default
- Very high-traffic channels (> 100 messages/day)
- Channels user muted

## Time-Based Filtering

### Message Age
- Default: Past 24 hours
- Configurable: 12, 24, 48 hours
- Weekends: May extend to Friday if running on Monday

### Thread Freshness
- Include threads with activity in timeframe
- Even if thread started earlier
- Show only recent messages, not entire history

## Smart Deduplication

### Related Messages
If multiple messages reference same topic:
- Group them together
- Show as one conversation
- Indicate number of related messages

### Thread Branches
For complex threads with branches:
- Show main thread only
- Indicate if side discussions exist
- Link to full thread for context

## Response Indicators

### Awaiting User Response
Flag conversations where:
- User was asked a question
- No response from user yet
- Question is < 48 hours old

**Indicator:** "⚠️ Awaiting your response"

### User Already Responded
- Still show for context
- But lower priority
- Indicate: "✓ You responded"

## Formatting Examples

### High Priority Format
```markdown
### Direct Messages (3)

- **Sarah Johnson** (2h ago): "Can you review the PRD? Need feedback before tomorrow's meeting." [View](link)
- **Mike Chen** (5h ago): "Quick question about the API endpoint - which version should I use?" [View](link)
```

### Medium Priority Format
```markdown
### Mentions (5)

- **#product** - John Doe mentioned you: "Can you weigh in on the search redesign?" [View](link)
- **#engineering** - Alice Smith: "FYI @paolo - deployment completed successfully." [View](link)
```

### Active Threads Format
```markdown
### Active Threads (4)

- **#jetpack-product**: Q4 roadmap discussion (12 messages, last: 4h ago) [View](link)
- **#domains**: Pricing strategy (8 messages, awaiting your response) [View](link)
```
