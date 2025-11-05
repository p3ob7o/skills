#!/usr/bin/env python3
"""
Gmail Inbox Fetcher
Retrieves inbox emails with minimal fields (no body) to avoid token limits.
"""

import json
import os
import sys
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Gmail API scopes - read-only access to Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Credentials file locations
TOKEN_FILE = Path.home() / '.claude' / 'gmail_token.json'
CREDENTIALS_FILE = Path.home() / '.claude' / 'gmail_credentials.json'


def get_gmail_service():
    """Authenticate and return Gmail API service."""
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

    return build('gmail', 'v1', credentials=creds)


def get_inbox_emails(service, query='in:inbox', max_results=100):
    """
    Fetch inbox emails with minimal fields.

    Args:
        service: Gmail API service
        query: Gmail search query (default: 'in:inbox')
        max_results: Maximum number of emails to retrieve

    Returns:
        List of email metadata dicts
    """
    try:
        # List messages matching query
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()

        messages = results.get('messages', [])

        if not messages:
            return []

        emails = []

        # Fetch each message with minimal fields
        for msg in messages:
            # Use format='metadata' and only fetch headers we need
            # This avoids fetching the body
            message = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['From', 'To', 'Subject', 'Date']
            ).execute()

            # Extract headers
            headers = {h['name']: h['value'] for h in message['payload']['headers']}

            emails.append({
                'id': message['id'],
                'thread_id': message['threadId'],
                'labels': message.get('labelIds', []),
                'snippet': message.get('snippet', ''),
                'from': headers.get('From', ''),
                'to': headers.get('To', ''),
                'subject': headers.get('Subject', ''),
                'date': headers.get('Date', ''),
                'message_url': f"https://mail.google.com/mail/u/0/#inbox/{message['id']}"
            })

        return emails

    except HttpError as error:
        print(json.dumps({
            'error': 'api_error',
            'message': str(error)
        }))
        sys.exit(1)


def main():
    """Main function."""
    # Parse command line arguments
    query = sys.argv[1] if len(sys.argv) > 1 else 'in:inbox'
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 100

    # Get Gmail service
    service = get_gmail_service()

    # Fetch emails
    emails = get_inbox_emails(service, query, max_results)

    # Output as JSON
    print(json.dumps({
        'count': len(emails),
        'emails': emails
    }, indent=2))


if __name__ == '__main__':
    main()
