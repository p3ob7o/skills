#!/usr/bin/env python3
"""
Slack Messages Fetcher
Retrieves Slack messages, conversations, and mentions using the Slack Web API.
"""

import json
import os
import sys
import subprocess
import time
import re
from pathlib import Path
from datetime import datetime, timezone, timedelta
import requests

# Slack API endpoint
SLACK_API_URL = 'https://slack.com/api'

# Keychain service and account names
KEYCHAIN_SERVICE = 'slack-api'
KEYCHAIN_ACCOUNT = 'personal-assistant'

# Priority users (show at top of DM list)
PRIORITY_USERS = {
    'Matt Mullenweg': None,  # Will be populated with user ID
    'Pedraum Pardehpoosh': None
}


def get_slack_token():
    """
    Read Slack OAuth token from macOS Keychain.

    Returns:
        str: Slack OAuth token
    """
    # Try Keychain (macOS only)
    try:
        result = subprocess.run(
            ['security', 'find-generic-password',
             '-s', KEYCHAIN_SERVICE,
             '-a', KEYCHAIN_ACCOUNT,
             '-w'],  # -w outputs password only
            capture_output=True,
            text=True,
            check=True
        )
        token = result.stdout.strip()
        if token:
            return token
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Keychain entry not found or security command not available
        pass

    # No token found
    print(json.dumps({
        'error': 'token_missing',
        'message': f'Slack OAuth token not found in Keychain.\n\n'
                   f'To add to Keychain:\n'
                   f'  security add-generic-password -s {KEYCHAIN_SERVICE} -a {KEYCHAIN_ACCOUNT} -w "YOUR_OAUTH_TOKEN"\n\n'
                   f'See SLACK_API_SETUP.md for OAuth setup instructions'
    }), file=sys.stderr)
    sys.exit(1)


def slack_api_call(method, token, **kwargs):
    """
    Make a Slack API call.

    Args:
        method: API method (e.g., 'conversations.list')
        token: OAuth token
        **kwargs: Additional parameters for the API call

    Returns:
        dict: API response
    """
    headers = {
        'Authorization': f'Bearer {token}'
    }

    # Most Slack API methods expect form-encoded parameters, not JSON
    # Use form-encoded data as default
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    response = requests.post(
        f'{SLACK_API_URL}/{method}',
        headers=headers,
        data=kwargs  # Use form data for all methods
    )

    try:
        data = response.json()

        if not data.get('ok'):
            error_msg = data.get('error', 'unknown_error')

            # For rate limits, raise a special exception that can be caught and retried
            if error_msg == 'ratelimited':
                retry_after = int(response.headers.get('Retry-After', 10))
                raise Exception(f"rate_limit:{retry_after}")

            # For other errors, exit immediately
            error_details = {
                'error': 'slack_api_error',
                'method': method,
                'message': f'Slack API error on {method}: {error_msg}',
                'http_status': response.status_code,
                'response_body': data
            }
            print(json.dumps(error_details, indent=2), file=sys.stderr)
            sys.exit(1)

        return data

    except Exception as e:
        # Re-raise rate_limit exceptions so they can be caught and retried
        if str(e).startswith('rate_limit:'):
            raise
        # For other exceptions, print error and exit
        print(json.dumps({
            'error': 'api_error',
            'message': str(e)
        }), file=sys.stderr)
        sys.exit(1)


def get_user_id(token):
    """Get the authenticated user's ID."""
    data = slack_api_call('auth.test', token)
    return data['user_id']


def get_users(token):
    """
    Get list of all users in workspace.

    Returns:
        dict: Map of user names to user IDs
    """
    data = slack_api_call('users.list', token)
    users = {}

    for user in data.get('members', []):
        if not user.get('deleted'):
            # Store by real name and display name
            real_name = user.get('real_name', '')
            display_name = user.get('profile', {}).get('display_name', '')
            user_id = user['id']

            if real_name:
                users[real_name] = user_id
            if display_name:
                users[display_name] = user_id

    return users


def get_conversations(token, user_id, types='public_channel,private_channel,mpim,im'):
    """
    Get list of conversations for the user.

    Args:
        token: OAuth token
        user_id: User ID
        types: Conversation types (comma-separated)

    Returns:
        list: List of conversation dicts
    """
    conversations = []
    cursor = None

    while True:
        params = {
            'types': types,
            'exclude_archived': True,
            'limit': 20  # Start with smaller limit to avoid rate limits
        }

        if cursor:
            params['cursor'] = cursor

        data = slack_api_call('conversations.list', token, **params)
        conversations.extend(data.get('channels', []))

        cursor = data.get('response_metadata', {}).get('next_cursor')
        if not cursor:
            break

    return conversations


def get_conversation_history(token, channel_id, oldest=None, latest=None, limit=100):
    """
    Get message history from a conversation.

    Args:
        token: OAuth token
        channel_id: Channel/conversation ID
        oldest: Oldest timestamp (Unix timestamp as string)
        latest: Latest timestamp (Unix timestamp as string)
        limit: Maximum messages to retrieve

    Returns:
        list: List of message dicts
    """
    params = {
        'channel': channel_id,
        'limit': limit
    }

    if oldest:
        params['oldest'] = oldest
    if latest:
        params['latest'] = latest

    data = slack_api_call('conversations.history', token, **params)
    return data.get('messages', [])


def search_messages(token, query, count=100):
    """
    Search for messages matching query.

    Args:
        token: OAuth token
        query: Search query
        count: Maximum results

    Returns:
        list: List of message dicts
    """
    data = slack_api_call('search.messages', token, query=query, count=count)
    return data.get('messages', {}).get('matches', [])


def format_timestamp(ts):
    """Convert Slack timestamp to readable format."""
    try:
        dt = datetime.fromtimestamp(float(ts), tz=timezone.utc)
        return dt.isoformat()
    except:
        return ts


def get_channel_name(conversations, channel_id):
    """Get channel name from ID."""
    for conv in conversations:
        if conv['id'] == channel_id:
            if conv.get('is_im'):
                return 'DM'
            elif conv.get('is_mpim'):
                return conv.get('name', 'Group DM')
            else:
                return conv.get('name', channel_id)
    return channel_id


def get_user_name(users_map, user_id):
    """Get user name from ID."""
    for name, uid in users_map.items():
        if uid == user_id:
            return name
    return user_id


def clean_slack_text(text, users_map):
    """
    Clean Slack markdown formatting and resolve user mentions to names.

    Args:
        text: Raw Slack message text with markdown
        users_map: Dictionary mapping user names to IDs

    Returns:
        str: Cleaned text with user mentions resolved
    """
    if not text:
        return text

    # Replace user mentions <@USER_ID> or <@USER_ID|display_name> with actual names
    def replace_user_mention(match):
        user_id = match.group(1)
        user_name = get_user_name(users_map, user_id)
        return f"@{user_name}"

    text = re.sub(r'<@([A-Z0-9]+)(?:\|[^>]+)?>', replace_user_mention, text)

    # Replace channel mentions <#CHANNEL_ID|channel-name> with #channel-name
    text = re.sub(r'<#[A-Z0-9]+\|([^>]+)>', r'#\1', text)

    # Replace links <url|text> with just the text (for labeled links)
    text = re.sub(r'<https?://[^|>]+\|([^>]+)>', r'\1', text)

    # Replace bare links <url> with just the url
    text = re.sub(r'<(https?://[^>]+)>', r'\1', text)

    # Replace bold *text* with just text (optional - keep if you want to preserve emphasis)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)

    # Replace code `text` - keep the backticks for code formatting
    # (no change needed)

    return text


def mode_mentions(token, user_id, since_hours=24):
    """
    Get messages mentioning the user in the last N hours using search API.

    This approach uses search.messages with time-based filtering to avoid
    rate limits from listing all conversations in large workspaces.

    Args:
        token: OAuth token
        user_id: User ID
        since_hours: Hours to look back

    Returns:
        dict: Mentions grouped by priority and channel
    """
    # Calculate timestamp for N hours ago
    since = datetime.now(timezone.utc) - timedelta(hours=since_hours)

    # Format date for Slack search query (YYYY-MM-DD format)
    date_str = since.strftime('%Y-%m-%d')

    # Build search query: mentions of user after date
    query = f'<@{user_id}> after:{date_str}'

    # Get user list for priority filtering and name resolution
    users_map = get_users(token)

    # Populate priority user IDs
    for name in PRIORITY_USERS:
        PRIORITY_USERS[name] = users_map.get(name)

    # Search for mentions (returns up to 100 results)
    messages = search_messages(token, query, count=100)

    priority_dms = []
    other_mentions = []

    # Process search results
    for msg in messages:
        # Search API returns channel info as object
        channel_info = msg.get('channel', {})
        channel_id = channel_info.get('id')

        # Skip if no channel ID
        if not channel_id:
            continue

        channel_name = channel_info.get('name', channel_id)

        # Determine channel type (im = DM, channel = public, group = private)
        is_dm = channel_info.get('is_im', False)

        # Get message sender
        sender_id = msg.get('user')
        sender_name = get_user_name(users_map, sender_id) if sender_id else 'Unknown'

        # Get permalink (search API includes this)
        permalink = msg.get('permalink', f"slack://channel?id={channel_id}&message={msg.get('ts', '').replace('.', '')}")

        mention_data = {
            'channel_id': channel_id,
            'channel_name': sender_name if is_dm else f'#{channel_name}',
            'timestamp': format_timestamp(msg.get('ts')),
            'user': sender_name,
            'text': clean_slack_text(msg.get('text', ''), users_map),
            'thread_ts': msg.get('thread_ts'),
            'permalink': permalink
        }

        # Categorize by priority
        if is_dm:
            is_priority = sender_id in PRIORITY_USERS.values()
            if is_priority:
                priority_dms.append(mention_data)
            else:
                other_mentions.append(mention_data)
        else:
            # All channel mentions go to other_mentions
            other_mentions.append(mention_data)

    return {
        'priority_dms': priority_dms,
        'other_mentions': other_mentions
    }


def main():
    """Main function."""
    # Parse command line arguments
    mode = sys.argv[1] if len(sys.argv) > 1 else 'mentions'

    # Get token
    token = get_slack_token()

    # Test mode: just verify auth works
    if mode == 'test':
        data = slack_api_call('auth.test', token)
        print(json.dumps(data, indent=2))
        return

    # Get user ID
    user_id = get_user_id(token)

    if mode == 'mentions':
        # Get mentions from last N hours
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        result = mode_mentions(token, user_id, since_hours=hours)

        print(json.dumps({
            'mode': 'mentions',
            'since_hours': hours,
            'user_id': user_id,
            'priority_dm_count': len(result['priority_dms']),
            'other_mention_count': len(result['other_mentions']),
            'priority_dms': result['priority_dms'],
            'other_mentions': result['other_mentions']
        }, indent=2))

    else:
        print(json.dumps({
            'error': 'invalid_mode',
            'message': f'Unknown mode: {mode}. Use: mentions'
        }))
        sys.exit(1)


if __name__ == '__main__':
    main()
