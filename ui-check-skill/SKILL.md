---
name: ui-check-skill
description: Visual UI inspection and quality assessment using Playwright. This skill should be used when the user wants to check, verify, or evaluate the visual quality of a specific UI element or page section on a website. It captures screenshots and provides analysis of the rendered output. Triggers on requests like "check the header", "verify the navigation looks correct", "inspect the footer styling", or "evaluate the dark mode toggle".
---

# UI Check Skill

This skill enables visual inspection of web page elements using Playwright browser automation. It captures screenshots of specified UI components and provides quality assessment feedback.

## Purpose

To visually inspect and evaluate specific parts of a webpage by:
1. Navigating to the specified URL using Playwright
2. Capturing a screenshot of the page or specific element
3. Analyzing the captured output for quality assessment
4. Providing feedback on visual appearance, layout, and potential issues

## Usage

When the user requests a UI check, gather the following information:

### Required Information
- **URL**: The webpage to inspect
- **Target**: What specific part to evaluate (e.g., "header", "navigation", "footer", "hero section")

### Optional Information (with defaults)
- **Browser**: chromium (default), firefox, or webkit
- **Device**: desktop (default), tablet, mobile, laptop, or 4k
- **Color scheme**: light or dark mode

## Workflow

### Step 1: Capture the Screenshot

Run the capture script with appropriate parameters:

```bash
python3 ~/.claude/skills/ui-check-skill/scripts/capture_ui.py --url URL [options]
```

**Common capture patterns:**

```bash
# Full page capture
python3 ~/.claude/skills/ui-check-skill/scripts/capture_ui.py --url http://localhost:8882/

# Specific element capture
python3 ~/.claude/skills/ui-check-skill/scripts/capture_ui.py --url http://localhost:8882/ --selector "header"

# Mobile viewport
python3 ~/.claude/skills/ui-check-skill/scripts/capture_ui.py --url http://localhost:8882/ --device mobile

# Dark mode
python3 ~/.claude/skills/ui-check-skill/scripts/capture_ui.py --url http://localhost:8882/ --color-scheme dark

# Multiple options combined
python3 ~/.claude/skills/ui-check-skill/scripts/capture_ui.py \
  --url http://localhost:8882/ \
  --selector ".wp-block-navigation" \
  --device tablet \
  --color-scheme dark \
  --json
```

### Step 2: View the Screenshot

After capture, use the Read tool to view the screenshot image file. The script outputs the path to the captured screenshot (typically in `/tmp/ui-captures/`).

### Step 3: Analyze and Provide Feedback

After viewing the screenshot, provide quality assessment covering:

1. **Visual Appearance**
   - Color scheme consistency
   - Typography and readability
   - Spacing and alignment
   - Visual hierarchy

2. **Layout Quality**
   - Element positioning
   - Responsive behavior
   - Overflow or clipping issues
   - Whitespace balance

3. **Functional Indicators**
   - Interactive elements visibility
   - Navigation clarity
   - Call-to-action prominence
   - Accessibility considerations

4. **Potential Issues**
   - Broken layouts
   - Missing elements
   - Contrast problems
   - Alignment inconsistencies

## Script Options Reference

| Option | Description | Default |
|--------|-------------|---------|
| `--url` | URL to capture (required) | - |
| `--output`, `-o` | Output path for screenshot | Auto-generated |
| `--browser` | Browser: chromium, firefox, webkit | chromium |
| `--device` | Preset: desktop, tablet, mobile, laptop, 4k | desktop |
| `--width` | Custom viewport width | - |
| `--height` | Custom viewport height | - |
| `--selector`, `-s` | CSS selector of element to capture | - |
| `--no-full-page` | Capture only visible viewport | false |
| `--color-scheme` | Color scheme: light, dark | - |
| `--wait-for` | Additional selector to wait for | - |
| `--timeout` | Navigation timeout in ms | 30000 |
| `--json` | Output results as JSON | false |

## Device Viewports

| Device | Width | Height |
|--------|-------|--------|
| desktop | 1280 | 720 |
| tablet | 768 | 1024 |
| mobile | 375 | 667 |
| laptop | 1440 | 900 |
| 4k | 3840 | 2160 |

## Common Selectors for WordPress Themes

- Header: `header`, `.wp-block-template-part[data-area="header"]`
- Footer: `footer`, `.wp-block-template-part[data-area="footer"]`
- Navigation: `nav`, `.wp-block-navigation`
- Site title: `.wp-block-site-title`
- Content area: `main`, `.entry-content`
- Hero section: `.wp-block-cover`, `.monochrome-hero`
- Dark mode toggle: `#dark-mode-toggle`

## Example Requests and Responses

**User**: "Check the header on my WordPress site"

**Response workflow**:
1. Capture header: `python3 ~/.claude/skills/ui-check-skill/scripts/capture_ui.py --url http://localhost:8882/ --selector "header"`
2. View the screenshot using Read tool
3. Provide analysis: "The header displays correctly with the site title on the left and navigation on the right. The dark mode toggle is visible and properly positioned. The spacing appears balanced, though the navigation items could benefit from slightly more padding between them for better touch targets on mobile."

**User**: "Verify the footer looks good on mobile"

**Response workflow**:
1. Capture footer on mobile: `python3 ~/.claude/skills/ui-check-skill/scripts/capture_ui.py --url http://localhost:8882/ --selector "footer" --device mobile`
2. View the screenshot
3. Provide analysis focusing on mobile-specific concerns
