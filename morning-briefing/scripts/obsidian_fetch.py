#!/usr/bin/env python3
"""
Obsidian Local REST API Client

Interacts with Obsidian vault via Local REST API plugin.
Supports reading, appending, and creating notes with section-aware operations.

Usage:
    ./obsidian_fetch.py read "2025/11/2025-11-08.md"
    ./obsidian_fetch.py append "2025/11/2025-11-08.md" "New content here"
    ./obsidian_fetch.py append-section "2025/11/2025-11-08.md" "## Section Name" "Content to add"
    ./obsidian_fetch.py create "2025/11/2025-11-08.md" "# Title\n\nContent"
    ./obsidian_fetch.py exists "2025/11/2025-11-08.md"

Authentication:
    API key stored in macOS Keychain:
    - Service: obsidian-rest-api
    - Account: personal-assistant

    To store the key:
    security add-generic-password -s "obsidian-rest-api" -a "personal-assistant" -w "YOUR_API_KEY"
"""

import sys
import json
import subprocess
import urllib.request
import urllib.error
import urllib.parse
import ssl
import re
from datetime import datetime

# API Configuration
API_BASE_URL = "https://127.0.0.1:27124"
KEYCHAIN_SERVICE = "obsidian-rest-api"
KEYCHAIN_ACCOUNT = "personal-assistant"


def get_api_key():
    """Retrieve API key from macOS Keychain."""
    try:
        result = subprocess.run(
            ["security", "find-generic-password", "-s", KEYCHAIN_SERVICE, "-a", KEYCHAIN_ACCOUNT, "-w"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print(json.dumps({
            "error": "API key not found in Keychain",
            "help": f"Run: security add-generic-password -s '{KEYCHAIN_SERVICE}' -a '{KEYCHAIN_ACCOUNT}' -w 'YOUR_API_KEY'"
        }), file=sys.stderr)
        sys.exit(1)


def make_request(endpoint, method="GET", data=None, headers=None):
    """Make HTTP request to Obsidian REST API."""
    api_key = get_api_key()

    url = f"{API_BASE_URL}{endpoint}"

    # Prepare headers
    request_headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"  # Default content type
    }
    if headers:
        request_headers.update(headers)

    # Prepare request
    if data is not None:
        # Only JSON-encode dicts; strings are sent as-is
        if isinstance(data, dict):
            data = json.dumps(data).encode('utf-8')
        elif isinstance(data, str):
            data = data.encode('utf-8')

    req = urllib.request.Request(url, data=data, headers=request_headers, method=method)

    # Create SSL context that doesn't verify certificates (localhost self-signed)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
            response_data = response.read().decode('utf-8')
            if response_data:
                # Try to parse as JSON first
                try:
                    return json.loads(response_data)
                except json.JSONDecodeError:
                    # If not JSON, return as plain text (for read operations)
                    return {"content": response_data, "is_plain_text": True}
            return {}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ""
        try:
            error_json = json.loads(error_body) if error_body else {}
        except json.JSONDecodeError:
            error_json = {"error": error_body}

        return {
            "error": f"HTTP {e.code}: {e.reason}",
            "details": error_json,
            "url": url
        }
    except urllib.error.URLError as e:
        return {
            "error": f"Connection error: {str(e.reason)}",
            "url": url,
            "help": "Is Obsidian running with Local REST API plugin enabled?"
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}",
            "url": url
        }


def read_note(file_path):
    """Read a note from the vault."""
    # URL encode the path
    encoded_path = urllib.parse.quote(file_path)
    endpoint = f"/vault/{encoded_path}"

    result = make_request(endpoint, method="GET")

    if "error" in result:
        return result

    return {
        "success": True,
        "path": file_path,
        "content": result.get("content", ""),
        "exists": True
    }


def exists_note(file_path):
    """Check if a note exists in the vault."""
    result = read_note(file_path)

    if "error" in result:
        # Check if it's a 404 (not found)
        if "HTTP 404" in result.get("error", ""):
            return {
                "success": True,
                "path": file_path,
                "exists": False
            }
        return result

    return {
        "success": True,
        "path": file_path,
        "exists": True
    }


def create_note(file_path, content):
    """Create a new note in the vault."""
    encoded_path = urllib.parse.quote(file_path)
    endpoint = f"/vault/{encoded_path}"

    # Send content directly as plain text, not JSON wrapped
    result = make_request(endpoint, method="PUT", data=content, headers={"Content-Type": "text/markdown"})

    if "error" in result:
        return result

    return {
        "success": True,
        "path": file_path,
        "action": "created",
        "content": content
    }


def append_note(file_path, content):
    """Append content to the end of a note."""
    # First, read the existing content
    read_result = read_note(file_path)

    if "error" in read_result:
        # If note doesn't exist, create it
        if "HTTP 404" in read_result.get("error", ""):
            return create_note(file_path, content)
        return read_result

    existing_content = read_result.get("content", "")

    # Append new content
    new_content = existing_content + "\n" + content

    # Update the note
    encoded_path = urllib.parse.quote(file_path)
    endpoint = f"/vault/{encoded_path}"

    # Send content directly as plain text, not JSON wrapped
    result = make_request(endpoint, method="PUT", data=new_content, headers={"Content-Type": "text/markdown"})

    if "error" in result:
        return result

    return {
        "success": True,
        "path": file_path,
        "action": "appended",
        "appended_content": content
    }


def append_to_section(file_path, section_header, content):
    """Append content within a specific section of a note."""
    # First, read the existing content
    read_result = read_note(file_path)

    if "error" in read_result:
        # If note doesn't exist, create it with the section
        if "HTTP 404" in read_result.get("error", ""):
            new_content = f"{section_header}\n\n{content}"
            return create_note(file_path, new_content)
        return read_result

    existing_content = read_result.get("content", "")

    # Find the section header
    lines = existing_content.split('\n')
    section_found = False
    insert_index = -1
    section_level = len(re.match(r'^#+', section_header).group()) if re.match(r'^#+', section_header) else 2

    for i, line in enumerate(lines):
        # Check if this line is the target section header
        if line.strip() == section_header.strip():
            section_found = True
            insert_index = i + 1

            # Find where this section ends (next header of same or higher level)
            for j in range(i + 1, len(lines)):
                header_match = re.match(r'^(#+)\s', lines[j])
                if header_match:
                    next_level = len(header_match.group(1))
                    if next_level <= section_level:
                        # Found next section, insert before it
                        insert_index = j
                        break
            else:
                # No next section found, append to end
                insert_index = len(lines)

            break

    if not section_found:
        # Section doesn't exist, append it to the end
        new_content = existing_content + f"\n\n{section_header}\n\n{content}"
    else:
        # Insert content in the section
        lines.insert(insert_index, content)
        new_content = '\n'.join(lines)

    # Update the note
    encoded_path = urllib.parse.quote(file_path)
    endpoint = f"/vault/{encoded_path}"

    # Send content directly as plain text, not JSON wrapped
    result = make_request(endpoint, method="PUT", data=new_content, headers={"Content-Type": "text/markdown"})

    if "error" in result:
        return result

    return {
        "success": True,
        "path": file_path,
        "action": "appended_to_section",
        "section": section_header,
        "section_found": section_found,
        "appended_content": content
    }


def list_commands():
    """List all available Obsidian commands."""
    endpoint = "/commands/"
    result = make_request(endpoint, method="GET")

    if "error" in result:
        return result

    return {
        "success": True,
        "commands": result
    }


def execute_command(command_id):
    """Execute an Obsidian command by ID."""
    encoded_id = urllib.parse.quote(command_id)
    endpoint = f"/commands/{encoded_id}/"

    try:
        result = make_request(endpoint, method="POST")
        return {
            "success": True,
            "command_id": command_id,
            "executed": True
        }
    except Exception as e:
        return {
            "error": f"Failed to execute command: {str(e)}",
            "command_id": command_id
        }


def reload_app():
    """Trigger 'Reload app without saving' command."""
    # Command ID for reload is typically "app:reload"
    return execute_command("app:reload")


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Missing operation",
            "usage": {
                "read": "./obsidian_fetch.py read <file_path>",
                "append": "./obsidian_fetch.py append <file_path> <content>",
                "append-section": "./obsidian_fetch.py append-section <file_path> <section_header> <content>",
                "create": "./obsidian_fetch.py create <file_path> <content>",
                "exists": "./obsidian_fetch.py exists <file_path>",
                "list-commands": "./obsidian_fetch.py list-commands",
                "execute-command": "./obsidian_fetch.py execute-command <command_id>",
                "reload": "./obsidian_fetch.py reload"
            }
        }))
        sys.exit(1)

    operation = sys.argv[1].lower()

    try:
        if operation == "read":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Missing file_path argument"}))
                sys.exit(1)
            file_path = sys.argv[2]
            result = read_note(file_path)

        elif operation == "exists":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Missing file_path argument"}))
                sys.exit(1)
            file_path = sys.argv[2]
            result = exists_note(file_path)

        elif operation == "append":
            if len(sys.argv) < 4:
                print(json.dumps({"error": "Missing file_path or content argument"}))
                sys.exit(1)
            file_path = sys.argv[2]
            content = sys.argv[3]
            result = append_note(file_path, content)
            # Auto-reload after write operation
            if result.get("success"):
                reload_app()

        elif operation == "append-section":
            if len(sys.argv) < 5:
                print(json.dumps({"error": "Missing file_path, section_header, or content argument"}))
                sys.exit(1)
            file_path = sys.argv[2]
            section_header = sys.argv[3]
            content = sys.argv[4]
            result = append_to_section(file_path, section_header, content)
            # Auto-reload after write operation
            if result.get("success"):
                reload_app()

        elif operation == "create":
            if len(sys.argv) < 4:
                print(json.dumps({"error": "Missing file_path or content argument"}))
                sys.exit(1)
            file_path = sys.argv[2]
            content = sys.argv[3]
            result = create_note(file_path, content)
            # Auto-reload after write operation
            if result.get("success"):
                reload_app()

        elif operation == "list-commands":
            result = list_commands()

        elif operation == "execute-command":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "Missing command_id argument"}))
                sys.exit(1)
            command_id = sys.argv[2]
            result = execute_command(command_id)

        elif operation == "reload":
            result = reload_app()

        else:
            result = {
                "error": f"Unknown operation: {operation}",
                "available_operations": ["read", "append", "append-section", "create", "exists", "list-commands", "execute-command", "reload"]
            }

        print(json.dumps(result, indent=2))

        # Exit with error code if operation failed
        if "error" in result:
            sys.exit(1)

    except Exception as e:
        print(json.dumps({
            "error": f"Unexpected error: {str(e)}",
            "operation": operation
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
