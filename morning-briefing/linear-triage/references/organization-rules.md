# Issue Organization Rules

## Presentation Order

Issues should be organized and presented in this priority order:

1. **High Priority Issues** (priority = 2)
2. **Urgent Issues** (priority = 1)
3. **In Progress Issues** (state type = started)
4. **Triage Issues** (state type = triage)
5. **Medium/Low Priority Todo Issues** (priority = 3 or 4, state = unstarted)
6. **Backlog Issues** (state type = backlog)

## Categorization by Priority

### Urgent (priority = 1)
- Critical issues requiring immediate attention
- Blockers preventing team progress
- Production incidents
- Customer escalations

### High (priority = 2)
- Important issues to prioritize this week
- Key features or improvements
- Significant bugs affecting users
- Strategic initiatives

### Medium (priority = 3)
- Standard priority work
- Regular feature development
- Non-critical bug fixes
- Routine improvements

### Low (priority = 4)
- Nice-to-have enhancements
- Minor improvements
- Can be deferred if needed
- Tech debt cleanup

### No Priority (priority = 0)
- Needs triage
- Priority not yet assigned
- Backlog items

## Categorization by State

### Triage
- Newly created issues needing review
- Requires priority assignment
- Needs clarification or scoping
- Should be processed first

### Todo (unstarted)
- Ready to start
- Properly scoped and prioritized
- Waiting for team capacity
- Clear acceptance criteria

### In Progress (started)
- Currently being worked on
- Active development
- Should be completed before starting new work
- Monitor for blockers

### Backlog (backlog)
- Not planned for immediate work
- Future considerations
- Good ideas but not current priority
- May be revisited later

### Completed / Canceled
- Excluded from active triage
- Only shown in completed_this_week mode

## Selection Helpers

### By Numbers
- "1, 3, 5" → issues 1, 3, 5
- "1-5" → issues 1 through 5
- "1-3, 7, 9-11" → issues 1, 2, 3, 7, 9, 10, 11

### By Team
- "all DOMAINS" → all issues from DOMAINS team
- "all TOTORO" → all issues from TOTORO team
- "all JPPROD" → all issues from Jetpack Product team

### Special Commands
- "all" → select all presented issues
- "none" → skip issue selection
- "high priority only" → select only priority 1 and 2
- "in progress" → select only started issues

## Presentation Format

For each issue category, show:
- Issue identifier (e.g., DOMAINS-1827)
- Title
- State (current status)
- Team name
- Last updated (relative time: "1 day ago", "15 days ago")
- Direct link to Linear

Example:
```
## High Priority Issues (2)

1. **DOMAINS-1827**: Domain Names Customer Conversations
   - State: Todo
   - Team: Domaison
   - Updated: 1 day ago
   - [View](https://linear.app/a8c/issue/DOMAINS-1827/...)
```

## Edge Cases

### Issues with no priority
- Group in "Triage Issues" section
- Suggest assigning priority

### Multiple teams
- Group by team if user works across many teams
- Show team name prominently

### Stale issues
- Flag issues not updated in > 30 days
- Suggest closing or updating
