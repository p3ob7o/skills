---
name: webpage-to-pdf
description: |
  Capture full-page screenshots of webpages and save them as multi-page PDF documents.
  Use this skill when the user wants to: capture a webpage as PDF, screenshot a URL to PDF,
  save a website page as PDF, create a PDF from a web page, or archive a webpage.
  Triggers: "capture this page as PDF", "screenshot URL to PDF", "save webpage as PDF",
  "convert webpage to PDF", "full page screenshot to PDF", "archive this page".
---

# Webpage to PDF Capture

Capture full-page screenshots of any webpage and save as a multi-page PDF.

## Workflow

### Step 1: Navigate to URL

Use Claude in Chrome browser tools to navigate to the target URL:

```
navigate(tabId, url)
```

Wait for page to fully load. Take an initial screenshot to verify.

### Step 2: Prepare the Page

Hide distracting elements (chat widgets, popups) using JavaScript:

```javascript
// Hide common chat widgets and floating elements
document.querySelectorAll('[class*="chat"], [class*="Chat"], [class*="widget"]')
  .forEach(el => el.style.display = 'none');
```

Scroll to top of page:

```javascript
window.scrollTo(0, 0);
```

### Step 3: Start Recording

Start GIF recording to capture frames as you scroll:

```
gif_creator(action="start_recording", tabId)
```

### Step 4: Capture Full Page

Take initial screenshot, then scroll through entire page capturing each viewport:

```
screenshot(tabId)  // Capture current view

scroll(tabId, coordinate=[center_x, center_y], direction="down", amount=8)
// Repeat until reaching page bottom (footer visible)
```

Scroll in increments of 8 ticks (~800px) to ensure overlap between frames.

### Step 5: Stop Recording and Export

Stop recording and export as GIF with download:

```
gif_creator(action="stop_recording", tabId)
gif_creator(action="export", tabId, download=true, filename="page_capture.gif")
```

### Step 6: Convert to PDF

The GIF downloads to user's Downloads folder. Access via filesystem MCP:

```python
# Read GIF from Downloads
read_media_file("/Users/<user>/Downloads/<filename>.gif")

# Process the saved JSON result with capture_webpage.py script
python scripts/capture_webpage.py <json_path> <output.pdf>
```

Or use the script directly if GIF path is known:

```bash
python scripts/capture_webpage.py /path/to/capture.gif /output/folder/filename.pdf
```

## Output

- Multi-page PDF where each page is a viewport screenshot
- Pages flow top-to-bottom matching the webpage scroll order
- Typical file size: 500KB - 2MB depending on page length

## Dependencies

- PIL/Pillow (for image processing)
- Claude in Chrome browser tools (navigate, screenshot, scroll, gif_creator)
- Filesystem MCP (to access downloaded GIF)

## Example

User: "Capture https://example.com/pricing as a PDF"

1. Navigate to https://example.com/pricing
2. Hide chat widgets, scroll to top
3. Start GIF recording
4. Screenshot → scroll down → repeat until footer
5. Stop recording, export GIF
6. Convert GIF to PDF using script
7. Save to requested location
