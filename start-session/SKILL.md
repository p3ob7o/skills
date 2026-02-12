---
name: start-session
description: Load project context from APP_DOCUMENTATION.md and CLAUDE.md at the start of a development session.
---

# Start Session

Load project context at the beginning of a development session.

**When to use:** At the start of any coding session to understand the current state of the project.

**Workflow:**

1. Read `CLAUDE.md` (project instructions and development guidelines)
2. Read `APP_DOCUMENTATION.md` (comprehensive app documentation)
3. Check git status for any uncommitted changes
4. Check recent git log for recent work
5. Provide a concise summary to the user covering:
   - Project overview and current version
   - What features are implemented vs pending
   - Current branch and any uncommitted work
   - Recent commits (last 5-10)
   - Quick reference of key commands

**Output format:**

```
## Session Started

**Project:** A Game of Domains v{version}
**Branch:** {current_branch}
**Status:** {clean/uncommitted changes}

### Recent Activity
{list of recent commits}

### Current State
{summary of implemented features}

### Ready to Work
{any pending items or uncommitted work to address}
```

## Important Notes

- Always preserve the existing structure and formatting of documentation files
- When in doubt, ask the user before making changes
