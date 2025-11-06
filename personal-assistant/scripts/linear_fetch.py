#!/usr/bin/env python3
"""
Linear Issues Fetcher
Retrieves issues from Linear using GraphQL API with efficient queries.
"""

import json
import os
import sys
from pathlib import Path
import requests

# Linear API endpoint
LINEAR_API_URL = 'https://api.linear.app/graphql'

# API key location
API_KEY_FILE = Path.home() / '.claude' / 'linear_api_key.txt'


def get_api_key():
    """Read Linear API key from file."""
    if not API_KEY_FILE.exists():
        print(json.dumps({
            'error': 'api_key_missing',
            'message': f'Please save your Linear API key to {API_KEY_FILE}'
        }))
        sys.exit(1)

    with open(API_KEY_FILE, 'r') as f:
        return f.read().strip()


def query_linear(query, variables=None):
    """Execute a GraphQL query against Linear API."""
    api_key = get_api_key()

    headers = {
        'Authorization': api_key,
        'Content-Type': 'application/json'
    }

    payload = {
        'query': query,
        'variables': variables or {}
    }

    try:
        response = requests.post(LINEAR_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        if 'errors' in data:
            print(json.dumps({
                'error': 'graphql_error',
                'message': data['errors']
            }))
            sys.exit(1)

        return data['data']

    except requests.exceptions.RequestException as e:
        print(json.dumps({
            'error': 'api_error',
            'message': str(e)
        }))
        sys.exit(1)


def get_viewer_id():
    """Get the authenticated user's ID."""
    query = """
    query {
        viewer {
            id
            name
            email
        }
    }
    """

    data = query_linear(query)
    return data['viewer']


def get_issues(filters=None, include_completed=False, limit=50):
    """
    Fetch issues with optional filters.

    Args:
        filters: Dict with optional keys:
            - assignee_id: Filter by assignee
            - state_type: Filter by state type (started, unstarted, completed, canceled, backlog)
            - updated_after: ISO date string (e.g., "2025-11-05T00:00:00Z")
            - team_id: Filter by team
            - project_id: Filter by project
        include_completed: Include completed/canceled issues
        limit: Maximum number of issues to fetch

    Returns:
        List of issue dicts
    """
    filters = filters or {}

    # Build GraphQL filter
    gql_filters = []

    if 'assignee_id' in filters:
        gql_filters.append(f'assignee: {{ id: {{ eq: "{filters["assignee_id"]}" }} }}')

    if 'state_type' in filters:
        gql_filters.append(f'state: {{ type: {{ eq: "{filters["state_type"]}" }} }}')
    elif not include_completed:
        # Exclude completed and canceled by default
        gql_filters.append('state: { type: { nin: ["completed", "canceled"] } }')

    if 'updated_after' in filters:
        gql_filters.append(f'updatedAt: {{ gte: "{filters["updated_after"]}" }}')

    if 'team_id' in filters:
        gql_filters.append(f'team: {{ id: {{ eq: "{filters["team_id"]}" }} }}')

    if 'project_id' in filters:
        gql_filters.append(f'project: {{ id: {{ eq: "{filters["project_id"]}" }} }}')

    filter_str = ', '.join(gql_filters) if gql_filters else ''

    query = f"""
    query {{
        issues(
            first: {limit}
            {f'filter: {{ {filter_str} }}' if filter_str else ''}
            orderBy: updatedAt
        ) {{
            nodes {{
                id
                identifier
                title
                description
                priority
                priorityLabel
                url
                createdAt
                updatedAt
                dueDate
                state {{
                    id
                    name
                    type
                    color
                }}
                team {{
                    id
                    key
                    name
                }}
                assignee {{
                    id
                    name
                    email
                }}
                creator {{
                    id
                    name
                    email
                }}
                project {{
                    id
                    name
                    url
                }}
                labels {{
                    nodes {{
                        id
                        name
                        color
                    }}
                }}
                comments {{
                    nodes {{
                        id
                        createdAt
                        body
                        user {{
                            name
                        }}
                    }}
                }}
                parent {{
                    id
                    identifier
                    title
                }}
                children {{
                    nodes {{
                        id
                        identifier
                        title
                    }}
                }}
            }}
        }}
    }}
    """

    data = query_linear(query)
    issues = data['issues']['nodes']

    # Format issues for easier consumption
    formatted_issues = []
    for issue in issues:
        formatted_issues.append({
            'id': issue['id'],
            'identifier': issue['identifier'],
            'title': issue['title'],
            'description': issue.get('description', ''),
            'priority': issue['priority'],
            'priority_label': issue['priorityLabel'],
            'url': issue['url'],
            'created_at': issue['createdAt'],
            'updated_at': issue['updatedAt'],
            'due_date': issue.get('dueDate'),
            'state': {
                'id': issue['state']['id'],
                'name': issue['state']['name'],
                'type': issue['state']['type'],
                'color': issue['state']['color']
            },
            'team': {
                'id': issue['team']['id'],
                'key': issue['team']['key'],
                'name': issue['team']['name']
            },
            'assignee': {
                'id': issue['assignee']['id'],
                'name': issue['assignee']['name'],
                'email': issue['assignee']['email']
            } if issue.get('assignee') else None,
            'creator': {
                'id': issue['creator']['id'],
                'name': issue['creator']['name'],
                'email': issue['creator']['email']
            } if issue.get('creator') else None,
            'project': {
                'id': issue['project']['id'],
                'name': issue['project']['name'],
                'url': issue['project']['url']
            } if issue.get('project') else None,
            'labels': [
                {
                    'id': label['id'],
                    'name': label['name'],
                    'color': label['color']
                }
                for label in issue['labels']['nodes']
            ],
            'comment_count': len(issue['comments']['nodes']),
            'latest_comment': issue['comments']['nodes'][-1] if issue['comments']['nodes'] else None,
            'parent': {
                'id': issue['parent']['id'],
                'identifier': issue['parent']['identifier'],
                'title': issue['parent']['title']
            } if issue.get('parent') else None,
            'child_count': len(issue['children']['nodes']),
            'children': [
                {
                    'id': child['id'],
                    'identifier': child['identifier'],
                    'title': child['title']
                }
                for child in issue['children']['nodes']
            ]
        })

    return formatted_issues


def main():
    """Main function."""
    # Parse command line arguments
    mode = sys.argv[1] if len(sys.argv) > 1 else 'active'

    # Get viewer info
    viewer = get_viewer_id()

    if mode == 'me':
        # Get the authenticated user info
        print(json.dumps(viewer, indent=2))
        return

    elif mode == 'active':
        # Get active issues assigned to me
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        issues = get_issues(
            filters={'assignee_id': viewer['id']},
            include_completed=False,
            limit=limit
        )

    elif mode == 'updated_today':
        # Get issues updated today
        from datetime import datetime, timezone
        today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        issues = get_issues(
            filters={
                'assignee_id': viewer['id'],
                'updated_after': today.isoformat()
            },
            include_completed=True,
            limit=limit
        )

    elif mode == 'completed_this_week':
        # Get issues completed this week
        from datetime import datetime, timezone, timedelta

        # Get Monday of this week at 00:00:00 UTC
        today = datetime.now(timezone.utc)
        monday = today - timedelta(days=today.weekday())
        monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)

        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        issues = get_issues(
            filters={
                'assignee_id': viewer['id'],
                'state_type': 'completed',
                'updated_after': monday.isoformat()
            },
            include_completed=True,
            limit=limit
        )

    elif mode == 'team':
        # Get issues for a specific team
        team_key = sys.argv[2] if len(sys.argv) > 2 else None
        if not team_key:
            print(json.dumps({
                'error': 'missing_team_key',
                'message': 'Please provide team key as second argument'
            }))
            sys.exit(1)

        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 50

        # First get team ID from team key
        query = f"""
        query {{
            teams(filter: {{ key: {{ eq: "{team_key}" }} }}) {{
                nodes {{
                    id
                    key
                    name
                }}
            }}
        }}
        """
        data = query_linear(query)
        teams = data['teams']['nodes']

        if not teams:
            print(json.dumps({
                'error': 'team_not_found',
                'message': f'Team with key "{team_key}" not found'
            }))
            sys.exit(1)

        team = teams[0]
        issues = get_issues(
            filters={
                'assignee_id': viewer['id'],
                'team_id': team['id']
            },
            include_completed=False,
            limit=limit
        )

    else:
        print(json.dumps({
            'error': 'invalid_mode',
            'message': f'Unknown mode: {mode}. Use: active, updated_today, completed_this_week, team, me'
        }))
        sys.exit(1)

    # Output results
    print(json.dumps({
        'viewer': viewer,
        'count': len(issues),
        'mode': mode,
        'issues': issues
    }, indent=2))


if __name__ == '__main__':
    main()
