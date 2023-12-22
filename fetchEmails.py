import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=5000)  # Fixed port set to 5000
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)

    # List the user's Gmail messages
    results = service.users().messages().list(userId='me').execute()
    messages = results.get('messages', [])

    subjects = []  # List to store subjects

    if not messages:
        print('No messages found.')
    else:
        for message in messages[:5]:  # Get first 5 messages
            msg = service.users().messages().get(userId='me', id=message['id'], format='metadata').execute()
            headers = msg.get('payload', {}).get('headers', [])
            subject_line = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
            if subject_line:
                subjects.append(subject_line)

        # Save subjects to a JSON file
        with open('email_subjects.json', 'w') as file:
            json.dump(subjects, file)

        print('Saved subjects of emails to email_subjects.json')

if __name__ == '__main__':
    main()
