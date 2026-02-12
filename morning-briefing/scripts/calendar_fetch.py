#!/usr/bin/env python3
"""
Google Calendar Event Fetcher
Retrieves calendar events with minimal fields to avoid token limits.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Calendar API scopes - read-only access
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar.readonly'
]

# Credentials file locations
TOKEN_FILE = Path.home() / '.claude' / 'gmail_token.json'
CREDENTIALS_FILE = Path.home() / '.claude' / 'gmail_credentials.json'


def get_calendar_service():
    """Authenticate and return Calendar API service."""
    creds = None

    # Load existing token
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(json.dumps({
                    'error': 'credentials_missing',
                    'message': f'Please download OAuth credentials from Google Cloud Console to {CREDENTIALS_FILE}'
                }))
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


def parse_datetime(date_str):
    """Parse datetime string or return None."""
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except:
        return None


def get_calendar_events(service, start_time, end_time, calendar_id='primary', max_results=50):
    """
    Fetch calendar events for a specific time range.

    Args:
        service: Calendar API service
        start_time: Start time as ISO 8601 string (e.g., "2025-11-05T00:00:00+01:00")
        end_time: End time as ISO 8601 string (e.g., "2025-11-05T23:59:59+01:00")
        calendar_id: Calendar ID (default: 'primary')
        max_results: Maximum number of events to retrieve

    Returns:
        List of event dicts
    """
    try:
        # Fetch events
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=start_time,
            timeMax=end_time,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])

        if not events:
            return []

        result_events = []

        for event in events:
            # Extract start and end times
            start = event.get('start', {})
            end = event.get('end', {})

            # Handle all-day events (date) vs timed events (dateTime)
            if 'date' in start:
                start_str = start['date']
                end_str = end.get('date', '')
                all_day = True
            else:
                start_str = start.get('dateTime', '')
                end_str = end.get('dateTime', '')
                all_day = False

            # Extract attendees
            attendees = []
            for attendee in event.get('attendees', []):
                attendees.append({
                    'email': attendee.get('email', ''),
                    'name': attendee.get('displayName', attendee.get('email', '')),
                    'response_status': attendee.get('responseStatus', 'needsAction'),
                    'organizer': attendee.get('organizer', False)
                })

            result_events.append({
                'id': event['id'],
                'summary': event.get('summary', '(No title)'),
                'description': event.get('description', ''),
                'location': event.get('location', ''),
                'start': start_str,
                'end': end_str,
                'all_day': all_day,
                'status': event.get('status', 'confirmed'),
                'attendees': attendees,
                'attendee_count': len(attendees),
                'organizer': event.get('organizer', {}).get('email', ''),
                'html_link': event.get('htmlLink', ''),
                'hangout_link': event.get('hangoutLink', ''),
                'conference_data': event.get('conferenceData', {})
            })

        return result_events

    except HttpError as error:
        print(json.dumps({
            'error': 'api_error',
            'message': str(error)
        }))
        sys.exit(1)


def main():
    """Main function."""
    # Parse command line arguments
    if len(sys.argv) < 3:
        print(json.dumps({
            'error': 'invalid_arguments',
            'message': 'Usage: calendar_fetch.py <start_time> <end_time> [calendar_id] [max_results]',
            'example': 'calendar_fetch.py "2025-11-05T00:00:00+01:00" "2025-11-05T23:59:59+01:00" primary 50'
        }))
        sys.exit(1)

    start_time = sys.argv[1]
    end_time = sys.argv[2]
    calendar_id = sys.argv[3] if len(sys.argv) > 3 else 'primary'
    max_results = int(sys.argv[4]) if len(sys.argv) > 4 else 50

    # Get Calendar service
    service = get_calendar_service()

    # Fetch events
    events = get_calendar_events(service, start_time, end_time, calendar_id, max_results)

    # Output as JSON
    print(json.dumps({
        'count': len(events),
        'start_time': start_time,
        'end_time': end_time,
        'calendar_id': calendar_id,
        'events': events
    }, indent=2))


if __name__ == '__main__':
    main()
