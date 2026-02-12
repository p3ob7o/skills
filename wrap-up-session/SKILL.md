---
name: wrap-up-session
description: Update APP_DOCUMENTATION.md and CLAUDE.md with changes made during the session before ending.
---

# Wrap Up Session

Update project documentation before ending a session.

**When to use:** Before ending a coding session, especially after making significant changes.

**Workflow:**

1. Run `git diff` and `git log` to identify changes made this session
2. Review what was modified (new files, changed files, deleted files)
3. Read current `APP_DOCUMENTATION.md` and `CLAUDE.md`
4. Determine what documentation updates are needed:
   - New components or features added
   - Changed architecture or file structure
   - New patterns or conventions established
   - Updated test counts or coverage
   - New environment variables or configuration
   - Changed commands or scripts
5. Ask the user to confirm the proposed updates
6. Apply updates to documentation files
7. Optionally commit the documentation updates

**Documentation update checklist:**

For `CLAUDE.md`:
- New development guidelines or patterns
- Updated project structure
- New commands or scripts
- Changed testing approach
- New environment variables

For `APP_DOCUMENTATION.md`:
- New features in "Current Status" section
- Updated component tables
- New files in project structure
- Changed test counts
- Updated "Next Steps" sections
- Architecture changes

**Output format:**

```
## Session Wrap-Up

### Changes This Session
{summary of git changes}

### Proposed Documentation Updates

**CLAUDE.md:**
- {list of updates, or "No updates needed"}

**APP_DOCUMENTATION.md:**
- {list of updates, or "No updates needed"}

Shall I apply these updates?
```

## Important Notes

- Always preserve the existing structure and formatting of documentation files
- Only update sections that are directly affected by changes
- Keep updates concise and factual
- Update the "Last updated" timestamp in APP_DOCUMENTATION.md
- When in doubt, ask the user before making changes
- Commit documentation changes with a descriptive message
