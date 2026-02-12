#!/usr/bin/env python3
"""
UI Capture Script for visual inspection and quality assessment.

Captures screenshots of web pages with various options for browser, device,
viewport, and element highlighting.

Usage:
    python scripts/capture_ui.py --help
    python scripts/capture_ui.py --url URL [options]

Examples:
    # Basic capture
    python scripts/capture_ui.py --url http://localhost:8882/

    # Capture specific element
    python scripts/capture_ui.py --url http://localhost:8882/ --selector ".wp-block-navigation"

    # Mobile viewport
    python scripts/capture_ui.py --url http://localhost:8882/ --device mobile

    # Custom viewport
    python scripts/capture_ui.py --url http://localhost:8882/ --width 1920 --height 1080

    # Dark mode
    python scripts/capture_ui.py --url http://localhost:8882/ --color-scheme dark
"""
import argparse
import json
import os
import sys
from datetime import datetime
from playwright.sync_api import sync_playwright

# Predefined device configurations
DEVICES = {
    "desktop": {"width": 1280, "height": 720},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 375, "height": 667},
    "laptop": {"width": 1440, "height": 900},
    "4k": {"width": 3840, "height": 2160},
}

# Browser options
BROWSERS = ["chromium", "firefox", "webkit"]

def capture_ui(
    url: str,
    output_path: str = None,
    browser_name: str = "chromium",
    device: str = "desktop",
    width: int = None,
    height: int = None,
    selector: str = None,
    full_page: bool = True,
    color_scheme: str = None,
    wait_for: str = None,
    timeout: int = 30000,
):
    """
    Capture a screenshot of a web page.

    Args:
        url: The URL to capture
        output_path: Path to save the screenshot (auto-generated if not provided)
        browser_name: Browser to use (chromium, firefox, webkit)
        device: Device preset (desktop, tablet, mobile, laptop, 4k)
        width: Custom viewport width (overrides device)
        height: Custom viewport height (overrides device)
        selector: CSS selector of specific element to capture
        full_page: Whether to capture full page or just viewport
        color_scheme: Color scheme preference (light, dark)
        wait_for: Additional selector to wait for before capture
        timeout: Navigation timeout in milliseconds

    Returns:
        dict: Capture results including path, page info, and element details
    """
    # Determine viewport size
    if width and height:
        viewport = {"width": width, "height": height}
    else:
        viewport = DEVICES.get(device, DEVICES["desktop"])

    # Generate output path if not provided
    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs("/tmp/ui-captures", exist_ok=True)
        output_path = f"/tmp/ui-captures/capture_{timestamp}.png"

    results = {
        "url": url,
        "screenshot_path": output_path,
        "browser": browser_name,
        "viewport": viewport,
        "device": device,
        "selector": selector,
        "timestamp": datetime.now().isoformat(),
    }

    with sync_playwright() as p:
        # Launch browser
        if browser_name == "chromium":
            browser = p.chromium.launch(headless=True)
        elif browser_name == "firefox":
            browser = p.firefox.launch(headless=True)
        elif browser_name == "webkit":
            browser = p.webkit.launch(headless=True)
        else:
            browser = p.chromium.launch(headless=True)

        # Create context with options
        context_options = {"viewport": viewport}
        if color_scheme:
            context_options["color_scheme"] = color_scheme
            results["color_scheme"] = color_scheme

        context = browser.new_context(**context_options)
        page = context.new_page()

        # Set timeout
        page.set_default_timeout(timeout)

        # Capture console messages
        console_messages = []
        page.on("console", lambda msg: console_messages.append({
            "type": msg.type,
            "text": msg.text
        }))

        # Navigate
        print(f"📍 Navigating to: {url}")
        response = page.goto(url)
        page.wait_for_load_state("networkidle")

        # Wait for additional selector if specified
        if wait_for:
            print(f"⏳ Waiting for: {wait_for}")
            page.wait_for_selector(wait_for)

        # Get page info
        results["page_title"] = page.title()
        results["status_code"] = response.status if response else None

        # Get page dimensions
        results["page_dimensions"] = page.evaluate("""
            () => ({
                scrollWidth: document.documentElement.scrollWidth,
                scrollHeight: document.documentElement.scrollHeight,
                clientWidth: document.documentElement.clientWidth,
                clientHeight: document.documentElement.clientHeight
            })
        """)

        # Capture screenshot
        if selector:
            # Capture specific element
            element = page.locator(selector)
            if element.count() > 0:
                print(f"🎯 Capturing element: {selector}")

                # Get element info
                box = element.first.bounding_box()
                if box:
                    results["element_info"] = {
                        "selector": selector,
                        "count": element.count(),
                        "bounding_box": box,
                        "visible": element.first.is_visible(),
                    }

                    # Try to get computed styles
                    try:
                        styles = page.evaluate(f"""
                            (selector) => {{
                                const el = document.querySelector(selector);
                                if (!el) return null;
                                const computed = getComputedStyle(el);
                                return {{
                                    backgroundColor: computed.backgroundColor,
                                    color: computed.color,
                                    fontSize: computed.fontSize,
                                    fontFamily: computed.fontFamily,
                                    padding: computed.padding,
                                    margin: computed.margin
                                }};
                            }}
                        """, selector)
                        if styles:
                            results["element_info"]["computed_styles"] = styles
                    except Exception:
                        pass

                # Take element screenshot
                element.first.screenshot(path=output_path)
            else:
                print(f"⚠️  Element not found: {selector}")
                results["error"] = f"Element not found: {selector}"
                # Fall back to full page
                page.screenshot(path=output_path, full_page=full_page)
        else:
            # Capture full page or viewport
            print(f"📸 Capturing {'full page' if full_page else 'viewport'}")
            page.screenshot(path=output_path, full_page=full_page)

        # Get all visible text content for context
        results["visible_headings"] = page.locator("h1, h2, h3").all_text_contents()[:10]

        # Add console messages if any errors
        error_messages = [m for m in console_messages if m["type"] in ["error", "warning"]]
        if error_messages:
            results["console_errors"] = error_messages[:5]

        browser.close()

    print(f"✅ Screenshot saved: {output_path}")
    return results

def main():
    parser = argparse.ArgumentParser(
        description="Capture UI screenshots for visual inspection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --url http://localhost:8882/
  %(prog)s --url http://localhost:8882/ --selector "header"
  %(prog)s --url http://localhost:8882/ --device mobile
  %(prog)s --url http://localhost:8882/ --browser firefox
  %(prog)s --url http://localhost:8882/ --color-scheme dark
        """
    )

    parser.add_argument("--url", required=True, help="URL to capture")
    parser.add_argument("--output", "-o", help="Output path for screenshot")
    parser.add_argument("--browser", choices=BROWSERS, default="chromium",
                        help="Browser to use (default: chromium)")
    parser.add_argument("--device", choices=list(DEVICES.keys()), default="desktop",
                        help="Device preset (default: desktop)")
    parser.add_argument("--width", type=int, help="Custom viewport width")
    parser.add_argument("--height", type=int, help="Custom viewport height")
    parser.add_argument("--selector", "-s", help="CSS selector of element to capture")
    parser.add_argument("--no-full-page", action="store_true",
                        help="Capture only visible viewport")
    parser.add_argument("--color-scheme", choices=["light", "dark"],
                        help="Color scheme preference")
    parser.add_argument("--wait-for", help="Additional selector to wait for")
    parser.add_argument("--timeout", type=int, default=30000,
                        help="Navigation timeout in ms (default: 30000)")
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON")

    args = parser.parse_args()

    results = capture_ui(
        url=args.url,
        output_path=args.output,
        browser_name=args.browser,
        device=args.device,
        width=args.width,
        height=args.height,
        selector=args.selector,
        full_page=not args.no_full_page,
        color_scheme=args.color_scheme,
        wait_for=args.wait_for,
        timeout=args.timeout,
    )

    if args.json:
        print(json.dumps(results, indent=2, default=str))
    else:
        print(f"\n📊 Capture Results:")
        print(f"   URL: {results['url']}")
        print(f"   Title: {results.get('page_title', 'N/A')}")
        print(f"   Browser: {results['browser']}")
        print(f"   Viewport: {results['viewport']['width']}x{results['viewport']['height']}")
        if results.get('element_info'):
            info = results['element_info']
            print(f"   Element: {info['selector']} ({info['count']} found)")
            if info.get('bounding_box'):
                box = info['bounding_box']
                print(f"   Size: {box['width']:.0f}x{box['height']:.0f}px")
        print(f"   Screenshot: {results['screenshot_path']}")

if __name__ == "__main__":
    main()
