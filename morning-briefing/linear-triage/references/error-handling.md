# Error Handling

## Linear API Failures

### Symptoms
- Script returns error message
- Empty results when issues should exist
- Authentication errors
- Timeout errors

### Troubleshooting Steps

1. **Check script permissions**
   ```bash
   ls -la /Users/paolo/.claude/skills/morning-briefing/scripts/linear_fetch.py
   ```

2. **Verify API key exists in Keychain**
   ```bash
   security find-generic-password -s 'linear-api' -a 'personal-assistant' -w
   ```
   Should return the API key.

3. **Test API key manually**
   Try fetching user info:
   ```bash
   python3 linear_fetch.py me
   ```

4. **Check for error message**
   Look at script stderr output for specific errors.

5. **Common Issues**

   **Invalid API key:**
   - Regenerate key in Linear settings
   - Store in Keychain:
     ```bash
     security add-generic-password -s 'linear-api' -a 'personal-assistant' -w 'YOUR_KEY'
     ```

   **Rate limiting:**
   - Wait 60 seconds and retry
   - Reduce limit parameter
   - Linear typically allows 1000 requests/hour

   **Network issues:**
   - Check internet connection
   - Verify Linear API is accessible
   - Try again in a moment

   **GraphQL errors:**
   - Check Linear API version compatibility
   - Verify query syntax in script

6. **User Communication**
   ```
   ⚠️ Linear API unavailable. Please check your credentials.

   Would you like to:
   - Retry the request
   - Continue with manual issue entry
   - Skip Linear triage for now
   ```

## No Issues Found

### When active mode returns 0 issues

**Possible causes:**
- No issues assigned to user (normal)
- All issues are in backlog or completed
- API key doesn't have workspace access
- User not assigned to any issues

**Actions:**
1. Confirm: "No active Linear issues found."
2. Try alternate mode: `updated_today` or `completed_this_week`
3. Explain possible reasons
4. Offer to skip this section

### When updated_today returns 0 issues

**Normal scenario:**
- No issues were updated today
- This is expected on quiet days

**Actions:**
1. Inform: "No issues updated today."
2. Offer to fetch all active issues instead
3. Proceed with user preference

## Script Crashes

### Python errors or exceptions

**Actions:**
1. Log the full error message
2. Check Python version: `python3 --version` (need 3.8+)
3. Verify dependencies:
   ```bash
   python3 -c "import requests, json; print('OK')"
   ```
4. Inform user of technical issue
5. Offer to skip this section

**Common Python errors:**
- `ModuleNotFoundError`: Install requests: `pip3 install requests`
- `JSONDecodeError`: API response format changed
- `KeyError`: Expected field missing from API response

## Partial Results

### Script returns some issues but count seems low

**Actions:**
1. Check limit parameter (default 100)
2. Increase if needed: `python3 linear_fetch.py active 500`
3. Inform user if hitting limit
4. Offer to fetch in batches

## Selection Parsing Errors

### User provides invalid selection format

**Common mistakes:**
- Typos: "1,3 5" (missing comma)
- Out of range: "1-100" when only 20 issues shown
- Invalid team: "all INVALID" when team doesn't exist

**Actions:**
1. Show clear error: "I couldn't parse your selection: [reason]"
2. Show valid formats again
3. Ask user to try again
4. Offer simpler options: "Would you like to select all or none?"

## Timeout Issues

### API takes too long to respond

**Actions:**
1. Inform user: "Linear API is responding slowly..."
2. Wait up to 30 seconds
3. If timeout: Offer to retry or skip
4. Consider reducing limit parameter

## Error Message Template

```
⚠️ Linear API failed: [Brief description]

Possible causes:
- [Cause 1]
- [Cause 2]

Troubleshooting:
1. [Step 1]
2. [Step 2]

Would you like to:
1. Retry
2. Skip this section
3. Try with different parameters
```
