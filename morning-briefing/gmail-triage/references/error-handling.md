# Error Handling

## Gmail API Failures

### Symptoms
- Script returns error message
- Empty results when inbox should have emails
- Authentication errors

### Troubleshooting Steps

1. **Check script permissions**
   ```bash
   ls -la /Users/paolo/.claude/skills/morning-briefing/scripts/gmail_fetch.py
   ```
   Should be readable and executable.

2. **Verify OAuth token exists**
   ```bash
   ls -la ~/.claude/gmail_token.json
   ```
   Token file should exist and be readable.

3. **Check for error messages**
   Look at script stderr output for specific error messages.

4. **Common Issues**

   **Authentication expired:**
   - Delete `~/.claude/gmail_token.json`
   - Re-run script (will prompt for browser auth)

   **Rate limiting:**
   - Wait 60 seconds and retry
   - Reduce max_results parameter

   **Network issues:**
   - Check internet connection
   - Try again in a moment

   **Permission issues:**
   - Ensure Gmail API is enabled in Google Cloud Console
   - Check OAuth scopes include Gmail read access

5. **User Communication**
   ```
   ⚠️ Gmail API unavailable. Please check your credentials.

   Would you like to:
   - Retry the request
   - Continue with manual email entry
   - Skip email triage for now
   ```

6. **Offer alternatives**
   - Provide option to continue with manual input
   - Skip email section entirely
   - Retry after fixing credentials

## Empty Results

### When inbox returns 0 emails

**Possible causes:**
- Inbox actually is empty (success!)
- Query syntax incorrect
- Token doesn't have access to inbox

**Actions:**
1. Confirm with user: "Your inbox appears empty. Is this correct?"
2. If unexpected, check query syntax
3. Try alternate query: `"is:unread"` without inbox filter

### When starred returns 0 emails

**Possible causes:**
- No emails are starred (normal)
- Token doesn't have access

**Actions:**
1. Inform user: "No starred emails found."
2. Offer to skip starred email selection
3. Proceed to next step in workflow

## Script Crashes

### Python errors or exceptions

**Actions:**
1. Log the full error message
2. Check Python version: `python3 --version` (need 3.8+)
3. Verify dependencies installed
4. Inform user of technical issue
5. Offer to skip this section

## Partial Results

### Script returns some but not all emails

**Symptoms:**
- Count seems low
- Missing recent emails

**Actions:**
1. Check max_results parameter (default 150)
2. Increase if needed: `python3 gmail_fetch.py "query" 500`
3. Inform user of limitation
4. Offer to fetch in batches

## Handling Errors Gracefully

### Principles
- Always provide clear error messages
- Offer actionable alternatives
- Don't block entire workflow for one failure
- Log errors for debugging
- Keep user informed

### Error Message Template
```
⚠️ [Component] failed: [Brief description]

Possible causes:
- [Cause 1]
- [Cause 2]

Would you like to:
1. Retry
2. Skip this section
3. Try alternative approach
```
