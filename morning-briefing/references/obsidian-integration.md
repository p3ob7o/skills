# Obsidian Integration

## Script Location

```
/Users/paolo/.claude/skills/morning-briefing/scripts/obsidian_fetch.py
```

## Available Operations

```bash
python3 obsidian_fetch.py <operation> <args>
```

## Operations

### Check if Note Exists

```bash
python3 obsidian_fetch.py exists "2025/11/2025-11-08.md"
```

Returns: `{"exists": true}` or `{"exists": false}`

### Create New Note

```bash
python3 obsidian_fetch.py create "2025/11/2025-11-08.md" "---
created: 2025-11-08 08:00:00
updated: 2025-11-08 08:00:00
permalink: 2025/11/2025-11-08
---
"
```

Creates note with frontmatter.

### Append to Section

This is the primary operation for the morning briefing:

```bash
python3 obsidian_fetch.py append-section "2025/11/2025-11-08.md" "## Section Name" "Content here"
```

**Behavior:**
- If section exists: Appends content to that section
- If section doesn't exist: Creates section and adds content
- Automatically triggers "Reload app without saving" after write

**Use for each briefing section:**
- `## Emails to handle today`
- `## Linear issues to handle today`
- `## Today's calendar`
- `## Slack activity (past 24 hours)`

### Append to End

```bash
python3 obsidian_fetch.py append "2025/11/2025-11-08.md" "Content to append"
```

Adds content to the end of the file.

## Daily Note Path Convention

Daily notes follow this structure:
```
YYYY/MM/YYYY-MM-DD.md
```

Examples:
- `2025/11/2025-11-08.md`
- `2025/12/2025-12-25.md`
- `2026/01/2026-01-01.md`

## Python Date Formatting

```python
from datetime import datetime
today = datetime.now()
date_str = today.strftime("%Y-%m-%d")
year_month = today.strftime("%Y/%m")
daily_note_path = f"{year_month}/{date_str}.md"
timestamp = today.strftime("%Y-%m-%d %H:%M:%S")
```

## Frontmatter Template

```yaml
---
created: YYYY-MM-DD HH:MM:SS
updated: YYYY-MM-DD HH:MM:SS
permalink: YYYY/MM/YYYY-MM-DD
---
```

## Auto-Reload Feature

The `obsidian_fetch.py` script automatically triggers "Reload app without saving" after these operations:
- `append`
- `append-section`
- `create`

This ensures Obsidian displays updated content immediately.

## Error Handling

### File Not Found
If note doesn't exist, create it first with frontmatter.

### Section Not Found
`append-section` creates the section automatically.

### Obsidian Not Running
Script will fail if Obsidian app isn't running. Check with user.

### REST API Port
Default port: 27124. Configured in Obsidian Local REST API plugin.

## Vault Location

Vault path: `/Users/paolo/Totoro`

This is where all daily notes and content live.
