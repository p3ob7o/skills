# Email Categorization Rules

## Reply Now

Emails requiring immediate attention and quick response (< 5 minutes):

### Criteria
- Contains "urgent", "asap", "immediately", "blocker", "critical" in subject
- From leadership team (Matt Mullenweg, Pedraum, direct manager)
- Customer escalation or production issue
- Simple question that can be answered quickly
- Meeting request or calendar coordination requiring immediate response
- Reply expected within hours
- Time-sensitive requests with today's deadline
- Direct questions from team members blocking their work

### Examples
- "Urgent: Production issue on checkout flow"
- "Quick question about today's meeting"
- "Need your approval by EOD"
- "Customer escalation - site down"

## Star for Later

Emails requiring significant time or thoughtful response (> 10 minutes):

### Criteria
- Requires research, data analysis, or code review
- Strategic planning or architecture discussions
- Proposals, RFCs, or design documents
- Complex problem-solving requests
- Lengthy threads requiring context review
- Can wait 1-3 days for response
- Requires consultation with others before responding
- Needs careful consideration or decision-making

### Examples
- "Proposal: New architecture for search system"
- "RFC: Migration plan for database upgrade"
- "Feedback requested on Q4 roadmap"
- "Code review: Large refactoring PR"

## Archive

Emails with no action needed or low value:

### Criteria
- Automated notifications (CI/CD, monitoring, GitHub, Linear, etc.)
- Newsletter confirmations or unsubscribe notices
- Social media notifications
- Already-handled threads (forwarded, delegated, or completed)
- Low-value FYI messages with no action required
- Obvious spam or irrelevant content
- Auto-replies and out-of-office messages
- Marketing emails and promotional content

### Examples
- "[Repository] Build passed for PR #123"
- "You've been added to the #general channel"
- "Monthly newsletter from Company X"
- "Your LinkedIn connection request was accepted"

## Edge Cases

### Ambiguous Emails
- If unclear whether Reply Now or Star: Default to **Star for Later**
- Reason: Better to take time on important responses than rush

### Multiple Categories
- If email fits multiple categories, use highest priority:
  1. Reply Now (highest)
  2. Star for Later
  3. Archive (lowest)

### Personal Judgment
- User always has final say on categorization
- These are recommendations, not mandates
- Adjust based on user's specific context and priorities
