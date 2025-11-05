---
name: weekly-review
description: This skill should be used every Sunday at 19:15 local time (after the evening reflection at 19:00) to synthesize the week through guided reflection and draft a comprehensive team post for domainsmaison.wordpress.com. It aggregates all 7 daily notes (Monday-Sunday), highlights from /highlights, Linear sprint data, and conducts a GTD-style interview to produce both a weekly note and a casual, first-person P2 post draft.
---

# Weekly Review

## Overview

This skill provides comprehensive weekly synthesis by aggregating data from the entire week (Monday-Sunday), conducting a structured GTD-style reflection interview, and producing both a detailed weekly note and a draft team P2 post in a casual, first-person reflective tone.

## When to Use This Skill

Trigger this skill:
- Weekly on Sundays at 19:15 local time via cron reminder (user initiates when ready)
- After Sunday's evening reflection completes (19:00-19:15)
- When the user explicitly requests a weekly review or summary
- When preparing the weekly team update post

## Workflow

### Phase 1: Data Aggregation

Collect and synthesize data from the entire week:

1. **Daily Notes (7 days)**
   - Read Monday through Sunday daily notes
   - Extract accomplishments from each day
   - Collect blockers and challenges
   - Identify recurring themes
   - Use path format: `YYYY/MM/YYYY-MM-DD.md`
   - Use MCP Obsidian tools

2. **Highlights**
   - Scan `/highlights/` for items added this week
   - Filter for domain name industry news
   - Look for articles with domain-related keywords:
     - Domain registration, TLD, registrar, ICANN
     - DNS, domain pricing, domain industry
     - Competitors: GoDaddy, Namecheap, Google Domains
   - Include links and brief summaries
   - Note: /highlights is READ-ONLY

3. **Linear Sprint Data**
   - Query completed issues this week
   - Query in-progress issues
   - Query blocked issues
   - Calculate completion rate
   - Identify patterns (types of work, blockers)
   - Use MCP Linear tools

4. **Calendar Summary**
   - Aggregate week's meetings from daily notes (preferred - already collected)
   - Alternative: Can fetch directly using calendar_fetch.py for full week
   - Calculate total meeting hours
   - Categorize: 1:1s, team meetings, cross-functional, external
   - Identify heaviest meeting days
   - Note: Daily notes should already have this data from morning/evening reflections

5. **Conversations**
   - List week's meeting summaries from `/conversations/`
   - Identify key meetings for reference
   - Extract attendee patterns (who you met with most)
   - Use MCP Obsidian tools

6. **Email & Slack Metrics**
   - Aggregate from daily notes
   - Total emails sent (internal vs external)
   - Slack activity by channel
   - Communication patterns
   - Use data from daily notes

7. **State**
   - Read previous week's review from `/meta/weekly-reviews/`
   - Compare metrics week-over-week
   - Identify trends
   - Use file system tools

### Phase 2: Interactive Review Interview (GTD-Style)

Conduct a comprehensive weekly review interview:

**Question 1: "What did you accomplish this week?"**
- Pre-populate with extracted accomplishments from daily notes
- User adds, edits, or re-prioritizes
- Focus on outcomes, not just activities

**Question 2: "What blockers or challenges did you face?"**
- Pre-populate with blockers from daily notes
- User elaborates on impact
- Identify patterns across the week
- Note what's resolved vs still blocking

**Question 3: "What did you learn this week?"**
- Open-ended reflection
- Professional learnings
- Process improvements
- Team or organizational insights

**Question 4: "Who should be recognized for their contributions?"**
- Team shoutouts
- Note specific contributions
- Capture collaboration highlights
- Remember to be specific (what they did, why it mattered)

**Question 5: "What are your top priorities for next week?"**
- Forward-looking planning
- 3-5 main priorities
- Connect to ongoing projects and goals

**Question 6: "Any domain industry news worth sharing?"**
- Review pre-selected highlights
- User confirms relevance
- Add commentary or context
- Filter for what matters to team/audience

**Question 7: "Anything else to capture?"**
- Open space for additional thoughts
- Wins not yet mentioned
- Concerns for next week
- Team dynamics or organizational observations

**Interview Style:**
- More contemplative than daily reflection
- Allow time for synthesis and pattern recognition
- 15-20 minutes total
- Focus on "so what?" and "what's next?"
- Help user see the week's arc and narrative

### Phase 3: Synthesis

Process all data and interview responses:

1. **Week Narrative Arc**
   - Identify the week's story
   - What was the theme or focus?
   - How did the week evolve?
   - What shifted from plan to reality?

2. **Accomplishments Synthesis**
   - Categorize: features, bugs, planning, people, external
   - Note high-impact items
   - Connect to team/company goals

3. **Metrics Compilation**
   - Linear: completed, in progress, blocked counts
   - Meetings: hours, distribution, types
   - Communication: Slack messages, emails sent
   - Compare to previous week

4. **Team Shoutouts**
   - Specific people and contributions
   - Why it mattered
   - Connect to team values

5. **Industry Intelligence**
   - Select 2-4 domain news items
   - Add brief context or analysis
   - Connect to team's work when relevant

6. **Next Week Planning**
   - Top 3-5 priorities
   - Connect to quarterly goals
   - Note dependencies or concerns

### Phase 4: Output Generation

Generate two documents:

#### Document 1: Weekly Note

Save to `/YYYY/W/YYYY-Wnn.md`:

```markdown
---
week: YYYY-Wnn
dates: YYYY-MM-DD to YYYY-MM-DD
---

# Week NN - Month DD-DD, YYYY

## Overview
[2-3 paragraph narrative of the week's arc. What was the theme? How did things evolve? What was the primary focus?]

## Accomplishments
- ✅ [Major accomplishment with context]
- ✅ [Feature or project completed]
- ✅ [Team milestone]
- ✅ Completed NN Linear issues (N features, N bugs, N planning)

## Blockers & Challenges
- [Challenge 1] - [Current status and plan]
- [Challenge 2] - [Impact and mitigation]
- [Pattern observed] - [Systemic issue noted]

## Key Learnings
- [Learning 1]: [What you discovered and why it matters]
- [Learning 2]: [Insight from the week]
- [Process improvement]: [What you'll change]

## Team Shoutouts
- **Person Name**: [Specific contribution] - [Why it mattered]
- **Person Name**: [Specific contribution] - [Why it mattered]

## Key Meetings & Interactions
- Team Sync (Nx): [Main topics]
- 1:1s (N): [Key conversations]
- Cross-team (N): [Collaborations]
- External (N): [Partner/customer meetings]

## Priorities for Next Week
1. [Priority 1 with context]
2. [Priority 2 with context]
3. [Priority 3 with context]
4. [Priority 4 if needed]
5. [Priority 5 if needed]

## Domain Industry News
- **[Headline]**: [Brief summary and link]
  - [Your commentary or relevance to team]
- **[Headline]**: [Brief summary and link]
  - [Your commentary or relevance to team]

## Metrics
- **Linear**: NN completed, NN in progress, N blocked
- **Meetings**: NN hours (down/up from NN last week)
  - 1:1s: N, Team: N, Cross-team: N, External: N
- **Emails**: NN sent (NN% internal)
- **Slack**: NN messages across N channels

## Reflections
[Personal reflections from interview - what's on your mind, patterns you're seeing, how you're feeling about the work and the team]

---

## Daily Summaries

### Monday YYYY-MM-DD
[[YYYY-MM-DD]] - [One-line summary]

### Tuesday YYYY-MM-DD
[[YYYY-MM-DD]] - [One-line summary]

### Wednesday YYYY-MM-DD
[[YYYY-MM-DD]] - [One-line summary]

### Thursday YYYY-MM-DD
[[YYYY-MM-DD]] - [One-line summary]

### Friday YYYY-MM-DD
[[YYYY-MM-DD]] - [One-line summary]

### Saturday YYYY-MM-DD
[[YYYY-MM-DD]] - [One-line summary]

### Sunday YYYY-MM-DD
[[YYYY-MM-DD]] - [One-line summary]

---
```

#### Document 2: P2 Post Draft

Save to `/draft notes/P2 - Week NN.md`:

```markdown
---
title: Week NN Update - [Catchy Title Based on Theme]
destination: domainsmaison.wordpress.com
status: draft
audience: Domains team + broader Automattic community
---

# Week NN Update

[Opening paragraph: Set the scene, establish the week's theme or main narrative. Casual tone, first person.]

## Accomplishments

[2-3 paragraphs covering the week's main accomplishments. Connect to team goals. Call out specific wins. Name people and their contributions. Be specific about outcomes, not just activities.]

[Mention the Linear stats naturally: "We closed NN issues this week (N features, N bugs)..." ]

## Challenges & Learnings

[1-2 paragraphs on challenges faced and what you learned. Be honest about friction points while maintaining constructive tone. Explain what you're doing about blockers. Share insights that might help others.]

## Team Recognition

[Paragraph with specific shoutouts. Don't just list names - tell mini-stories about what people did and why it mattered. Be generous with credit.]

Shoutouts to:
- **Person** for [specific contribution and impact]
- **Person** for [specific contribution and impact]

## Domain Industry Tidbits

[Paragraph introducing the news/highlights section]

A few interesting things from the wider domain world this week:

- **[Headline]**: [Brief summary] - [Your take or relevance]
- **[Headline]**: [Brief summary] - [Your take or relevance]
- **[Headline]**: [Brief summary] - [Your take or relevance]

## Looking Ahead

[Closing paragraph: Top priorities for next week, what you're focused on, any asks or heads-ups for the team.]

[Warm sign-off]

—Paolo

---

*Generated with assistance from my personal assistant system*
```

**P2 Post Tone Guidelines:**
- Casual but comprehensive
- First-person reflective
- Conversational (like an email to the team)
- Honest about challenges
- Generous with recognition
- Specific (names, numbers, examples)
- Connect to broader context (company goals, industry trends)
- End with forward-looking optimism

### Phase 5: State Updates

Save review data to `/meta/weekly-reviews/YYYY-Wnn.json`:

```json
{
  "week": "YYYY-Wnn",
  "dates": {
    "start": "YYYY-MM-DD",
    "end": "YYYY-MM-DD"
  },
  "timestamp": "ISO-8601 timestamp",
  "metrics": {
    "linear": {
      "completed": 12,
      "in_progress": 8,
      "blocked": 3,
      "breakdown": {
        "features": 8,
        "bugs": 4,
        "planning": 0
      }
    },
    "meetings": {
      "total_hours": 18,
      "count": {
        "one_on_ones": 4,
        "team": 2,
        "cross_team": 3,
        "external": 2
      }
    },
    "communication": {
      "emails_sent": 127,
      "internal_emails": 89,
      "external_emails": 38,
      "slack_messages": 156,
      "slack_channels": 8
    }
  },
  "themes": [
    "Q4 planning",
    "Team structure",
    "Infrastructure focus"
  ],
  "top_accomplishments": [
    "Finalized Q4 domain pricing strategy",
    "Hired two new engineers",
    "Shipped API v2.1"
  ],
  "top_challenges": [
    "Legal review delays",
    "Technical debt",
    "Budget approval process"
  ],
  "team_shoutouts": [
    {
      "person": "Sarah Johnson",
      "contribution": "Led architecture review"
    },
    {
      "person": "Jake Martinez",
      "contribution": "Shipped infrastructure fix early"
    }
  ],
  "industry_news_count": 3,
  "interview_duration_minutes": 18,
  "p2_draft_created": true,
  "weekly_note_created": true
}
```

## Integration Patterns

### Obsidian Integration
```
Use MCP Obsidian tools:
- obsidian_get_vault_file for each daily note (7 files)
- obsidian_list_vault_files(directory="/highlights") with date filter
- obsidian_list_vault_files(directory="/conversations") for week
- obsidian_create_vault_file for weekly note and P2 draft
- Read previous week's review from /meta/weekly-reviews/
```

### Linear Integration
```
Use MCP Linear tools:
- Query issues completed this week (updated_at in week range)
- Query current in-progress issues
- Query blocked issues
- Calculate sprint metrics
- Include user as assignee, subscriber, or mentioned
```

### Daily Notes Integration
```
Read all 7 daily notes to extract:
- Morning briefing priorities (what was planned)
- Evening reflection accomplishments (what actually happened)
- Blockers and challenges noted
- Key people interactions
- Linear updates mentioned
- Slack/email metrics
```

### Highlights Integration
```
Scan /highlights for domain industry news:
- Filter by date added (this week)
- Search for domain-related keywords
- Limit to 3-4 most relevant items
- Extract title, URL, and brief summary
- Note: /highlights is READ-ONLY
```

## Interview Best Practices

**Week-Level Thinking:**
- Help user zoom out from daily details
- Identify patterns across the week
- Connect activities to outcomes
- Think about what story the week tells

**Synthesis Over Lists:**
- Don't just list accomplishments
- Help user see themes and connections
- Identify what was most impactful
- Recognize pattern changes

**Forward-Looking:**
- Use review to inform next week
- Identify what needs to carry forward
- Spot early warning signs
- Plan for known challenges

**Team Context:**
- Keep broader audience in mind for P2 post
- Balance transparency with discretion
- Celebrate team, not just individual
- Connect team work to company goals

## Error Handling

If daily notes are missing:
- Note which days are missing in the review
- Work with available data
- Ask user about missing days
- Don't block the review

If integrations fail:
- Gracefully degrade (use available data)
- Note what's missing: "⚠️ Linear data unavailable"
- Rely more on interview and daily notes
- Log error to `/meta/assistant-state.json`

## Performance Targets

- Data aggregation: < 45 seconds (reading 7+ files)
- Interview: 15-20 minutes (user-paced)
- Synthesis and writing: < 30 seconds
- Total: < 25 minutes including user interaction

## Important Notes

- Runs after Sunday evening reflection (assumes it completes by 19:15 local time)
- Includes all 7 days (Monday-Sunday)
- P2 post is a DRAFT - user reviews before publishing
- Weekly note is internal documentation
- Times are in the user's local timezone (adjusts automatically when traveling)
- State files provide week-over-week comparison
- First-person, conversational tone for P2 post
- Be specific: names, numbers, examples
- Balance honesty with constructive tone
