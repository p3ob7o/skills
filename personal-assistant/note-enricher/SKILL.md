---
name: note-enricher
description: This skill runs hourly (24/7) to continuously enhance conversation notes and people profiles through contextual enrichment and targeted questioning. It scans for new conversation files in /conversations/, enriches them with structured sections, updates people profiles in /people/, and maintains a queue in /meta/enrichment-queue.json for pending clarifications from the user.
---

# Note Enricher

## Overview

This skill provides continuous, automated enhancement of the user's knowledge base by processing new meeting summaries, expanding conversation notes with structured sections, updating people profiles with recent interaction data, and intelligently queuing clarification questions when information is incomplete or ambiguous.

## When to Use This Skill

Trigger this skill:
- Hourly via cron (automated, runs 24/7)
- After new conversation files appear in `/conversations/`
- When `/meta/enrichment-queue.json` has pending items
- When user explicitly requests note or profile enrichment

## Workflow

### Phase 1: Queue Management

Check and prioritize work to be done:

1. **Scan for New Conversations**
   - List files in `/conversations/` directory
   - Identify files modified in last hour (or since last run)
   - Files follow naming: `YYYY-MM-DD Event Name.md`
   - Use MCP Obsidian tools

2. **Check Enrichment Queue**
   - Read `/meta/enrichment-queue.json`
   - Identify pending enrichment tasks
   - Prioritize: new conversations > profile updates > backfill

3. **Determine Batch Size**
   - Process up to 5 items per hourly run
   - Prioritize by timestamp (newest first)
   - Balance conversation vs profile work (3:2 ratio if both pending)

### Phase 2: Conversation Enrichment

For each new conversation file:

**Step 1: Read and Analyze**
- Read the conversation summary (from Granola via Zapier)
- Identify people mentioned (attendees and discussed parties)
- Extract key topics, decisions, action items
- Identify gaps or ambiguities in the summary

**Step 2: Structure Enhancement**
Add structured sections if not present:

```markdown
---
date: YYYY-MM-DD
type: meeting
attendees:
  - [[Person Name 1]]
  - [[Person Name 2]]
topics:
  - Topic 1
  - Topic 2
related_projects:
  - [[Project Name]]
---

# Meeting Title

## Summary
[Original summary from Granola/transcription service]

## Key Decisions
- Decision 1: [Description and rationale]
- Decision 2: [Description and rationale]

## Action Items
- [ ] Person: Task description with deadline
- [ ] Person: Task description with deadline

## Discussion Topics

### Topic 1
[Expanded notes based on summary and context]

### Topic 2
[Expanded notes based on summary and context]

## People Context
- **Person Name**: [Notable contribution, insight, or interaction pattern]

## Related
- [[Related Project]]
- [[Related Daily Note]]
- [[Related Document]]
```

**Step 3: Gap Identification**

If information is incomplete or ambiguous:
- Identify what's missing (decisions unclear, action items vague, outcomes unknown)
- Formulate specific questions
- Add to enrichment queue for user clarification

**Step 4: Write Enhanced Note**
- Update the conversation file with enhanced structure
- Preserve original content
- Add structured sections
- Link to people profiles using [[Person Name]] format
- Use MCP Obsidian tools

### Phase 3: Profile Enrichment

For each person mentioned in conversations or flagged in queue:

**Step 1: Locate or Create Profile**
- Check if `/people/Firstname Lastname.md` exists
- If not, create new profile with template structure
- Use MCP Obsidian tools

**Step 2: Extract New Information**
From the conversation or context:
- Role/company updates
- Location information
- Primary language(s)
- Relationship context
- Recent interaction details
- Collaboration patterns
- Action items or follow-ups

**Step 3: Update Profile**

Follow the field order (from architectural spec):
1. Role/Company/Title
2. Where they live
3. Primary language(s)
4. Relationship context (colleague, report, stakeholder, external, friend)
5. Interaction history (when last met, topics discussed)
6. Personal notes (interests, communication preferences, timezone)
7. Collaboration patterns
8. Action items or follow-ups

**Profile Template Structure:**
```markdown
---
updated: YYYY-MM-DD
---

# Person Name

## Role/Company/Title
[Current role and organization]

## Where They Live
[City, Country - include timezone if known]

## Primary Language(s)
[Languages they speak]

## Relationship Context
[colleague|report|stakeholder|external|friend]
[Additional context about the relationship]

## Interaction History

### Recent Meetings
- **YYYY-MM-DD**: [[Meeting Title]]
  - Topics: [List of discussion topics]
  - Outcomes: [Key decisions or results]
  - [Notable contributions or insights]

### Communication Patterns
- Preferred channels: [Slack/Email/Meetings]
- Response patterns: [Quick/Thoughtful/Async]
- Best times to reach: [Timezone-aware scheduling]

## Personal Notes
- Interests: [Hobbies, passions, professional interests]
- Communication style: [Direct/Diplomatic/Data-driven/etc]
- Works best with: [Async/Sync/Detailed context/etc]
- Timezone: [Their local timezone]

## Collaboration Patterns
- Strengths: [What they excel at]
- Working style: [How they approach work]
- Team interactions: [How they collaborate]

## Action Items
- [ ] [Follow-up item with deadline]
- [ ] [Promised deliverable or commitment]

---

## Notes Archive
[Historical notes from previous interactions...]
```

**Step 4: Gap Identification**

If profile information is incomplete:
- Identify missing fields (location, language, role, etc.)
- Formulate specific questions
- Add to enrichment queue for user clarification
- Priority: high for role/relationship, medium for location/language, low for preferences

### Phase 4: Interactive Clarification

When user is available and queue has pending questions:

**Clarification Types:**

**For Conversations:**
- "In your meeting with [People], you discussed [Topic]. What was decided?"
- "The action items from [Meeting] are unclear. Can you clarify who is responsible for what?"
- "What was the outcome of the discussion about [Topic] in [Meeting]?"

**For People Profiles:**
- "Where is [Person Name] based? (City/Country)"
- "What language does [Person Name] primarily speak?"
- "What's your relationship with [Person Name]? (colleague/report/stakeholder/external/friend)"
- "What's [Person Name]'s current role and company?"
- "I noticed you met with [Person Name] on [Date]. Any notable insights to capture?"

**Clarification Style:**
- Ask 1-3 questions at a time (don't overwhelm)
- Provide context for why you're asking
- Make it easy to answer (suggest options when applicable)
- Allow "skip for now" option
- Track which questions were answered vs skipped

### Phase 5: State Updates

Update `/meta/enrichment-queue.json`:

```json
{
  "pending": [
    {
      "id": "enrich-001",
      "type": "conversation|profile",
      "file": "/conversations/2025-11-05 Team Sync.md",
      "person": "Person Name",
      "field": "location",
      "added": "ISO-8601 timestamp",
      "priority": "high|medium|low",
      "status": "pending|in_progress|blocked",
      "questions": [
        "Specific question text"
      ],
      "context": "Additional context for the enrichment"
    }
  ],
  "completed": [
    {
      "id": "enrich-000",
      "type": "profile",
      "person": "Person Name",
      "completed": "ISO-8601 timestamp"
    }
  ],
  "last_run": "ISO-8601 timestamp",
  "stats": {
    "conversations_processed": 45,
    "profiles_updated": 23,
    "questions_queued": 12,
    "questions_answered": 8
  }
}
```

## People Profile Field Priorities

When enriching profiles, prioritize fields:

**High Priority (essential context):**
1. Role/Company/Title - critical for professional context
2. Relationship context - defines how you interact
3. Where they live - important for timezone and context

**Medium Priority (helpful context):**
4. Primary language(s) - aids communication
5. Interaction history - tracks relationship evolution
6. Collaboration patterns - improves working relationship

**Low Priority (nice to have):**
7. Personal notes - enriches relationship over time
8. Action items - captures commitments

## Integration Patterns

### Obsidian Integration
```
Use MCP Obsidian tools:
- obsidian_list_vault_files(directory="/conversations") for scanning
- obsidian_get_vault_file to read conversations and profiles
- obsidian_create_vault_file or obsidian_patch_vault_file to update
- obsidian_search_vault to find related context
```

### Daily Notes Integration
```
When enriching conversations:
- Link to relevant daily note: [[YYYY-MM-DD]]
- Check daily note for additional context
- Cross-reference with morning/evening sections
```

### Highlights Integration
```
When enriching profiles or conversations:
- Search /highlights for related content
- Link relevant articles or research
- Note: /highlights is READ-ONLY (managed by Readwise)
```

## Processing Heuristics

**Conversation Priority:**
- Most recent conversations first
- Conversations with more attendees (>3 people) get higher priority
- Conversations mentioning key stakeholders (Matt, Pedraum) prioritized

**Profile Priority:**
- People mentioned in multiple recent conversations
- Profiles with missing high-priority fields
- People user interacts with frequently (check daily notes)

**Question Batching:**
- Group related questions (all about one person)
- Ask profile questions separately from conversation questions
- Provide "answer all for [Person]" option

## Error Handling

If file operations fail:
- Log error to `/meta/assistant-state.json`
- Move item to "blocked" status in queue
- Retry on next run (up to 3 attempts)
- After 3 failures, flag for manual review

If user is unavailable:
- Queue questions, don't block enrichment
- Continue with automated enhancements
- Retry clarifications next time user is available

## Performance Targets

- Scan /conversations/: < 2 seconds
- Process 1 conversation: < 10 seconds
- Update 1 profile: < 5 seconds
- Total run time: < 5 minutes (for 5-item batch)
- Run hourly without consuming excessive resources

## Important Notes

- This skill runs automatically (no user initiation required)
- Operates in background, doesn't interrupt user
- Gracefully handles when user is unavailable
- Preserves original content, only adds structure
- Uses Obsidian [[wikilinks]] for people cross-referencing
- Maintains queue persistence across runs
- Never deletes or removes information, only adds/enhances
- Times are in CET timezone for timestamp logging

## References

This skill includes a reference file for the people profile schema:

`references/people-profile-schema.md` - Detailed specification of profile fields and structure
