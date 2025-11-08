#!/usr/bin/env python3
"""
Slack Messages Fetcher
Retrieves Slack messages, conversations, and mentions using the Slack Web API.
"""

import json
import os
import sys
import subprocess
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
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(
        f'{SLACK_API_URL}/{method}',
        headers=headers,
        json=kwargs
    )

    try:
        data = response.json()

        if not data.get('ok'):
            error_msg = data.get('error', 'unknown_error')
            print(json.dumps({
                'error': 'slack_api_error',
                'message': f'Slack API error: {error_msg}'
            }), file=sys.stderr)
            sys.exit(1)

        return data

    except Exception as e:
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
            'limit': 200
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


def mode_mentions(token, user_id, since_hours=24):
    """
    Get messages mentioning the user in the last N hours.

    Args:
        token: OAuth token
        user_id: User ID
        since_hours: Hours to look back

    Returns:
        dict: Mentions grouped by priority and channel
    """
    # Calculate timestamp for N hours ago
    since = datetime.now(timezone.utc) - timedelta(hours=since_hours)
    since_ts = since.timestamp()

    # Get all conversations
    conversations = get_conversations(token, user_id)

    # Get user list for priority filtering
    users_map = get_users(token)

    # Populate priority user IDs
    for name in PRIORITY_USERS:
        PRIORITY_USERS[name] = users_map.get(name)

    priority_dms = []
    other_mentions = []

    # Check each conversation for mentions
    for conv in conversations:
        channel_id = conv['id']

        # Get recent messages
        messages = get_conversation_history(
            token,
            channel_id,
            oldest=str(since_ts),
            limit=100
        )

        # Filter for messages mentioning user
        mentions = [
            msg for msg in messages
            if f'<@{user_id}>' in msg.get('text', '')
        ]

        if mentions:
            # Check if this is a DM from priority user
            is_dm = conv.get('is_im', False)

            if is_dm:
                # Get the other user in the DM
                dm_user = conv.get('user')
                is_priority = dm_user in PRIORITY_USERS.values()

                dm_user_name = get_user_name(users_map, dm_user) if dm_user else 'Unknown'

                for msg in mentions:
                    mention_data = {
                        'channel_id': channel_id,
                        'channel_name': dm_user_name,
                        'timestamp': format_timestamp(msg.get('ts')),
                        'user': get_user_name(users_map, msg.get('user', '')),
                        'text': msg.get('text', ''),
                        'thread_ts': msg.get('thread_ts'),
                        'permalink': f"slack://channel?id={channel_id}&message={msg.get('ts', '').replace('.', '')}"
                    }

                    if is_priority:
                        priority_dms.append(mention_data)
                    else:
                        other_mentions.append(mention_data)
            else:
                # Regular channel mention
                channel_name = get_channel_name([conv], channel_id)

                for msg in mentions:
                    other_mentions.append({
                        'channel_id': channel_id,
                        'channel_name': channel_name,
                        'timestamp': format_timestamp(msg.get('ts')),
                        'user': get_user_name(users_map, msg.get('user', '')),
                        'text': msg.get('text', ''),
                        'thread_ts': msg.get('thread_ts'),
                        'permalink': f"slack://channel?id={channel_id}&message={msg.get('ts', '').replace('.', '')}"
                    })

    return {
        'priority_dms': priority_dms,
        'other_mentions': other_mentions
    }


def mode_activity(token, user_id, since_hours=24):
    """
    Get user's Slack activity in the last N hours.

    Args:
        token: OAuth token
        user_id: User ID
        since_hours: Hours to look back

    Returns:
        dict: Activity summary by channel
    """
    # Calculate timestamp for N hours ago
    since = datetime.now(timezone.utc) - timedelta(hours=since_hours)
    since_ts = since.timestamp()

    # Get all conversations
    conversations = get_conversations(token, user_id)

    # Get user list for DM name resolution
    users_map = get_users(token)

    # Populate priority user IDs
    for name in PRIORITY_USERS:
        PRIORITY_USERS[name] = users_map.get(name)

    priority_dms = []
    channel_activity = {}

    # Check each conversation for user's messages
    for conv in conversations:
        channel_id = conv['id']

        # Get recent messages
        messages = get_conversation_history(
            token,
            channel_id,
            oldest=str(since_ts),
            limit=100
        )

        # Filter for user's messages
        user_messages = [
            msg for msg in messages
            if msg.get('user') == user_id
        ]

        if user_messages:
            message_count = len(user_messages)

            # Check if this is a DM with priority user
            is_dm = conv.get('is_im', False)

            if is_dm:
                dm_user = conv.get('user')
                is_priority = dm_user in PRIORITY_USERS.values()
                dm_user_name = get_user_name(users_map, dm_user) if dm_user else 'Unknown'

                if is_priority:
                    priority_dms.append({
                        'user': dm_user_name,
                        'message_count': message_count,
                        'channel_id': channel_id
                    })
                else:
                    channel_activity[f'DM: {dm_user_name}'] = message_count
            else:
                channel_name = get_channel_name([conv], channel_id)
                channel_activity[f'#{channel_name}'] = message_count

    return {
        'priority_dms': priority_dms,
        'channel_activity': channel_activity,
        'total_messages': sum(channel_activity.values()) + sum(dm['message_count'] for dm in priority_dms)
    }


def mode_dms(token, user_id, since_hours=24):
    """
    Get all DM conversations with message counts.

    Args:
        token: OAuth token
        user_id: User ID
        since_hours: Hours to look back (0 = all time)

    Returns:
        list: List of DM conversation dicts
    """
    # Get DM conversations only
    conversations = get_conversations(token, user_id, types='im')

    # Get user list for name resolution
    users_map = get_users(token)

    # Populate priority user IDs
    for name in PRIORITY_USERS:
        PRIORITY_USERS[name] = users_map.get(name)

    dms = []

    # Calculate timestamp if filtering by time
    since_ts = None
    if since_hours > 0:
        since = datetime.now(timezone.utc) - timedelta(hours=since_hours)
        since_ts = str(since.timestamp())

    for conv in conversations:
        channel_id = conv['id']
        dm_user = conv.get('user')
        dm_user_name = get_user_name(users_map, dm_user) if dm_user else 'Unknown'
        is_priority = dm_user in PRIORITY_USERS.values()

        # Get message count
        messages = get_conversation_history(
            token,
            channel_id,
            oldest=since_ts,
            limit=100
        )

        if messages:
            dms.append({
                'user': dm_user_name,
                'user_id': dm_user,
                'channel_id': channel_id,
                'message_count': len(messages),
                'is_priority': is_priority,
                'latest_message': {
                    'timestamp': format_timestamp(messages[0].get('ts')),
                    'text': messages[0].get('text', '')[:100]
                } if messages else None
            })

    # Sort: priority first, then by message count
    dms.sort(key=lambda x: (not x['is_priority'], -x['message_count']))

    return dms


def main():
    """Main function."""
    # Parse command line arguments
    mode = sys.argv[1] if len(sys.argv) > 1 else 'mentions'

    # Get token
    token = get_slack_token()

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

    elif mode == 'activity':
        # Get user's activity from last N hours
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        result = mode_activity(token, user_id, since_hours=hours)

        print(json.dumps({
            'mode': 'activity',
            'since_hours': hours,
            'user_id': user_id,
            'total_messages': result['total_messages'],
            'priority_dms': result['priority_dms'],
            'channel_activity': result['channel_activity']
        }, indent=2))

    elif mode == 'dms':
        # Get all DMs with message counts
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        dms = mode_dms(token, user_id, since_hours=hours)

        print(json.dumps({
            'mode': 'dms',
            'since_hours': hours if hours > 0 else 'all',
            'user_id': user_id,
            'dm_count': len(dms),
            'dms': dms
        }, indent=2))

    else:
        print(json.dumps({
            'error': 'invalid_mode',
            'message': f'Unknown mode: {mode}. Use: mentions, activity, dms'
        }))
        sys.exit(1)


if __name__ == '__main__':
    main()
