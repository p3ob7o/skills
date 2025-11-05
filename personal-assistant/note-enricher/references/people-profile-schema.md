# People Profile Schema

This document defines the structure and field specifications for people profiles stored in `/people/`.

## File Naming Convention

`/people/Firstname Lastname.md`

Examples:
- `/people/Sarah Johnson.md`
- `/people/Matt Mullenweg.md`
- `/people/João Silva.md`

## Profile Structure

### Frontmatter

```yaml
---
updated: YYYY-MM-DD
---
```

The `updated` field tracks the last modification date.

### Field Order

Fields must appear in this exact order:

1. Role/Company/Title
2. Where They Live
3. Primary Language(s)
4. Relationship Context
5. Interaction History
6. Personal Notes
7. Collaboration Patterns
8. Action Items

## Field Specifications

### 1. Role/Company/Title

**Purpose**: Professional identity and organizational context

**Format**:
```markdown
## Role/Company/Title
[Job Title], [Company/Organization] - [Department/Team]
```

**Examples**:
- Senior Engineering Manager, Automattic - Domains Team
- Product Designer, External Partner
- CEO, Automattic
- Independent Consultant

**Notes**:
- Update when role changes
- Include team/department for internal colleagues
- Mark "External Partner" or "Consultant" for non-Automattic contacts

### 2. Where They Live

**Purpose**: Geographic context, timezone awareness, cultural context

**Format**:
```markdown
## Where They Live
[City], [Country] ([Timezone if known])
```

**Examples**:
- Portland, Oregon, USA (PST)
- London, UK (GMT)
- São Paulo, Brazil (BRT)
- Remote / Location Unknown

**Notes**:
- Include timezone in parentheses when known
- Update if person relocates
- Use "Remote / Location Unknown" if truly unknown

### 3. Primary Language(s)

**Purpose**: Communication context, language barriers, translation needs

**Format**:
```markdown
## Primary Language(s)
[Language 1], [Language 2]
```

**Examples**:
- English
- Portuguese, English
- Spanish (native), English (fluent)
- Mandarin

**Notes**:
- List primary language first
- Note proficiency level if relevant
- Can be inferred from location/name if unknown

### 4. Relationship Context

**Purpose**: Defines interaction patterns and communication norms

**Format**:
```markdown
## Relationship Context
[Type]: [colleague|report|stakeholder|external|friend]

[Additional context paragraph]
```

**Relationship Types**:
- **colleague**: Peer at same organization
- **report**: Direct or indirect report
- **stakeholder**: Internal stakeholder (different team)
- **external**: Partner, vendor, consultant, customer
- **friend**: Personal relationship

**Examples**:
```markdown
## Relationship Context
colleague

Sarah is a senior engineering manager on the Domains team. We work together closely on infrastructure and product decisions. She reports to me indirectly through the org structure.
```

```markdown
## Relationship Context
external

João is a consultant we hired for the Q4 domain pricing strategy project. He has deep industry expertise and provides strategic guidance.
```

**Notes**:
- Type should be lowercase, one of the five options
- Context paragraph provides nuance beyond the type
- Update as relationship evolves

### 5. Interaction History

**Purpose**: Track meetings, conversations, and relationship evolution

**Format**:
```markdown
## Interaction History

### Recent Meetings
- **YYYY-MM-DD**: [[Meeting Title or File]]
  - Topics: [Topic 1], [Topic 2]
  - Outcomes: [Key decisions or results]
  - [Notable contributions or insights]

- **YYYY-MM-DD**: [[Another Meeting]]
  - Topics: [Topics]
  - Outcomes: [Outcomes]

### Communication Patterns
- Preferred channels: [Slack|Email|Meetings|Mix]
- Response patterns: [Quick|Thoughtful|Async-first]
- Best times to reach: [Morning CET|Afternoon PST|Flexible]
```

**Examples**:
```markdown
## Interaction History

### Recent Meetings
- **2025-11-05**: [[Team Sync - Q4 Planning]]
  - Topics: Budget allocation, team structure, hiring
  - Outcomes: Approved 2 new hires, shifted focus to infrastructure
  - Sarah showed strong leadership on architecture decisions

- **2025-11-04**: [[1:1 - Career Development]]
  - Topics: Path to Director level, skill development
  - Outcomes: Aligned on roadmap for next 6 months

### Communication Patterns
- Preferred channels: Slack for quick questions, email for detailed proposals
- Response patterns: Quick on Slack during work hours, thoughtful on complex topics
- Best times to reach: Mornings PST (afternoons CET)
```

**Notes**:
- Keep 5-10 most recent meetings
- Archive older meetings to "Notes Archive" section at bottom
- Link to meeting files using [[wikilinks]]
- Communication patterns evolve - update regularly

### 6. Personal Notes

**Purpose**: Humanize the relationship, remember interests, improve communication

**Format**:
```markdown
## Personal Notes
- Interests: [Hobbies, passions, professional interests]
- Communication style: [Adjectives describing their style]
- Works best with: [Context preferences]
- Timezone: [Their timezone with offset from CET]
- [Other personal observations]
```

**Examples**:
```markdown
## Personal Notes
- Interests: Rock climbing, functional programming, architecture patterns
- Communication style: Data-driven, thorough, values direct feedback
- Works best with: Detailed written context before meetings, async with sync checkpoints
- Timezone: PST (CET -9 hours)
- Prefers morning meetings (her time)
- Has two young children - flexible about schedule
```

**Notes**:
- Balance professional and personal (err on professional side)
- Capture communication preferences to improve interactions
- Timezone offset helps with scheduling
- Update as you learn more

### 7. Collaboration Patterns

**Purpose**: Understand working style, optimize collaboration

**Format**:
```markdown
## Collaboration Patterns
- Strengths: [What they excel at]
- Working style: [How they approach work]
- Team interactions: [How they work with others]
- Decision-making: [How they make decisions]
```

**Examples**:
```markdown
## Collaboration Patterns
- Strengths: Technical architecture, mentoring engineers, cross-team coordination
- Working style: Methodical, detail-oriented, values documentation
- Team interactions: Collaborative, leads by influence, strong mentor to senior engineers
- Decision-making: Data-driven with room for intuition, seeks input before deciding
```

**Notes**:
- Focus on observable patterns
- Helps predict how they'll approach problems
- Useful for delegating or collaborating on projects

### 8. Action Items

**Purpose**: Track commitments, follow-ups, and pending items

**Format**:
```markdown
## Action Items
- [ ] [Description] - [Deadline or context]
- [ ] [Description] - [Deadline or context]
- [✓] [Completed item for reference]
```

**Examples**:
```markdown
## Action Items
- [ ] Provide feedback on Director role competencies by 2025-11-15
- [ ] Review her RFC on API redesign
- [ ] Schedule career development check-in (monthly recurring)
- [✓] Share Q4 planning doc - Completed 2025-11-03
```

**Notes**:
- Use checkbox format for active items
- Include deadlines or timeframes
- Mark completed items with [✓] and date
- Archive completed items periodically

## Notes Archive Section

**Purpose**: Long-term memory beyond recent interactions

**Format**:
```markdown
---

## Notes Archive

### 2025 Q3
[Historical notes from that period]

### 2025 Q2
[Historical notes from that period]
```

**Usage**:
- Move older interaction history here
- Organize by quarter or month
- Preserve important historical context
- Keep profile main sections focused on recent/current

## Profile Creation Workflow

When creating a new profile:

1. Create file: `/people/Firstname Lastname.md`
2. Add frontmatter with `updated: YYYY-MM-DD`
3. Add `# Firstname Lastname` heading
4. Add all 8 sections in order
5. Fill in known information
6. Use placeholders for unknown: "Unknown" or "To be updated"
7. Add to enrichment queue for missing information

## Profile Update Workflow

When updating an existing profile:

1. Read current profile
2. Update `updated` date in frontmatter
3. Add new interaction to Interaction History
4. Update any changed fields (role, location, etc.)
5. Add new action items if any
6. Preserve all existing information (never delete)
7. If interaction history is long (>10 items), archive older entries

## Linking Conventions

Use Obsidian [[wikilinks]] for:
- Meeting references: [[YYYY-MM-DD Meeting Title]]
- Daily note references: [[YYYY-MM-DD]]
- Project references: [[Project Name]]
- Other people: [[Person Name]]

## Examples

See complete examples in:
- `/people/Sarah Johnson.md` (internal colleague example)
- `/people/Matt Mullenweg.md` (executive example)
- `/people/External Consultant.md` (external relationship example)

## Maintenance

- Profiles should be updated after significant interactions
- Minimum update frequency: monthly for frequent contacts
- Archive old interaction history quarterly
- Prune completed action items quarterly
- Update role/location immediately when changes occur
