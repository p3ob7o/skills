# Obsidian Local REST API Setup

This guide explains how to set up the Obsidian Local REST API plugin and configure the `obsidian_fetch.py` script.

## Prerequisites

- Obsidian installed
- Local REST API plugin installed in Obsidian
- Python 3.6+ (already installed on macOS)

## Step 1: Install Local REST API Plugin

1. Open Obsidian
2. Go to Settings → Community plugins
3. Browse community plugins
4. Search for "Local REST API"
5. Install and Enable the plugin

## Step 2: Configure Local REST API Plugin

1. In Obsidian Settings → Local REST API
2. Note your API key (you'll need this in the next step)
3. Verify the server is running at `https://127.0.0.1:27124`
4. Ensure HTTPS is enabled (default)

## Step 3: Store API Key in Keychain

Store your Obsidian REST API key in macOS Keychain:

```bash
security add-generic-password \
  -s "obsidian-rest-api" \
  -a "personal-assistant" \
  -w "YOUR_API_KEY_HERE"
```

Replace `YOUR_API_KEY_HERE` with your actual API key from the plugin settings.

### Verify Keychain Storage

```bash
security find-generic-password -s "obsidian-rest-api" -a "personal-assistant" -w
```

This should output your API key.

## Step 4: Test the Script

### Test: Check if a note exists

```bash
cd /Users/paolo/.claude/skills/morning-briefing/scripts
./obsidian_fetch.py exists "2025/11/2025-11-08.md"
```

Expected output:
```json
{
  "success": true,
  "path": "2025/11/2025-11-08.md",
  "exists": true
}
```

### Test: Read a note

```bash
./obsidian_fetch.py read "2025/11/2025-11-08.md"
```

Expected output:
```json
{
  "success": true,
  "path": "2025/11/2025-11-08.md",
  "content": "---\ncreated: ...\n...",
  "exists": true
}
```

### Test: Append content to end of note

```bash
./obsidian_fetch.py append "2025/11/2025-11-08.md" "Test content appended"
```

### Test: Append content to a specific section

```bash
./obsidian_fetch.py append-section "2025/11/2025-11-08.md" "## Test Section" "Content within section"
```

### Test: Create a new note

```bash
./obsidian_fetch.py create "test-note.md" "# Test Note\n\nThis is a test."
```

## Troubleshooting

### Error: "Connection error"

- **Check**: Is Obsidian running?
- **Check**: Is the Local REST API plugin enabled in Obsidian settings?
- **Check**: Is the server running at `https://127.0.0.1:27124`?

### Error: "API key not found in Keychain"

Run the security command from Step 3 to store your API key.

### Error: "HTTP 401: Unauthorized"

Your API key may be incorrect. Verify it in Obsidian Settings → Local REST API, then update Keychain:

```bash
# Delete old key
security delete-generic-password -s "obsidian-rest-api" -a "personal-assistant"

# Add new key
security add-generic-password -s "obsidian-rest-api" -a "personal-assistant" -w "NEW_API_KEY"
```

### Error: "HTTP 404: Not Found"

The file path doesn't exist in your vault. Check the path is correct relative to your vault root.

## Script Usage

### Operations

1. **read** - Read note content
   ```bash
   ./obsidian_fetch.py read "<file_path>"
   ```

2. **exists** - Check if note exists
   ```bash
   ./obsidian_fetch.py exists "<file_path>"
   ```

3. **append** - Append to end of note
   ```bash
   ./obsidian_fetch.py append "<file_path>" "<content>"
   ```

4. **append-section** - Append within a specific section
   ```bash
   ./obsidian_fetch.py append-section "<file_path>" "<section_header>" "<content>"
   ```

5. **create** - Create a new note
   ```bash
   ./obsidian_fetch.py create "<file_path>" "<content>"
   ```

### File Paths

File paths are relative to your Obsidian vault root:
- Daily notes: `2025/11/2025-11-08.md`
- Regular notes: `my-note.md`
- Folders: `folder/subfolder/note.md`

### Content with Newlines

Use `\n` for newlines in content:

```bash
./obsidian_fetch.py create "test.md" "# Title\n\nParagraph 1\n\nParagraph 2"
```

Or use shell's `$'...'` syntax:

```bash
./obsidian_fetch.py create "test.md" $'# Title\n\nParagraph 1\n\nParagraph 2'
```

## Security Notes

- API key is stored in macOS Keychain (encrypted)
- Script uses HTTPS to connect to local Obsidian instance
- SSL certificate verification is disabled for localhost (self-signed cert)
- API key is only accessible to your user account

## Integration with Morning Briefing

The morning briefing workflow uses `obsidian_fetch.py` to:
- Read today's daily note
- Append "## Emails to Handle" section
- Add email tasks with checkboxes and Gmail links
- Create daily note if it doesn't exist

Example from workflow:
```bash
./obsidian_fetch.py append-section "2025/11/2025-11-08.md" "## Emails to Handle" \
  "- [ ] Email from John: [Subject](gmail_url)"
```
