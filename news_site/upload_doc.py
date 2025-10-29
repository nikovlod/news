import os
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import google.auth.exceptions

# If modifying the document, you need this scope
SCOPES = ['https://www.googleapis.com/auth/documents']

# Path to your credentials.json file
CREDENTIALS_PATH = 'credentials.json'

# The ID of your Google Docs document
DOCUMENT_ID = '1PlmItN-lSbSHdv5g1U-1ij60hDCrNcwGoNeEJvensgQ'

with open("news.txt", "r") as f:
    news = f.read()

def authenticate():
    """Authenticate the user and create the service."""
    creds = None
    
    # Load existing credentials from 'token.json', if they exist
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no valid credentials are available, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_console()  # Use run_console() instead of run_local_server()
        
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    # Build the Docs service
    service = build('docs', 'v1', credentials=creds)
    return service

def clear_google_doc(service, document_id):
    """Clear the contents of a Google Docs document."""
    # Get the document content
    document = service.documents().get(documentId=document_id).execute()
    end_index = document.get('body').get('content')[-1].get('endIndex')

    # Define the requests to clear the document
    requests = [
        {
            'deleteContentRange': {
                'range': {
                    'startIndex': 1,
                    'endIndex': end_index - 1
                }
            }
        }
    ]

    # Execute the request to clear the document
    result = service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    print(f"Document cleared: {result}")

def write_to_google_doc(service, document_id, news):
    """Write some plain text to a Google Docs document."""
    # Define the requests to insert new text
    requests = [
        {
            'insertText': {
                'location': {
                    'index': 1,  # Insert at the beginning of the document
                },
                'text': news,
            }
        }
    ]

    # Execute the request to write to the document
    result = service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    print(f"Text added: {result}")

if __name__ == '__main__':
    service = authenticate()
    clear_google_doc(service, DOCUMENT_ID)  # Clear the document first
    write_to_google_doc(service, DOCUMENT_ID, news)  # Write new content

