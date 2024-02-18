"""
authentication for google API calls
pylint authenticate.py
-------------------------------------------------------------------
Your code has been rated at 10.00/10
"""
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow

def authenticate_google_api(token_file, scopes):
    """
    Load credentials from a file
    """
    creds = None
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError as err:
                print(f'Nextevents.py - RefreshError: {err.args[0]}')
                try:
                    os.remove(token_file)
                    print('The obsolete token file is removed, please retry !')
                except FileNotFoundError as fnf:
                    print(f'Nextevents.py - FileNotFoundError : {fnf}')
                return None
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'apps.googleusercontent.com.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'w', encoding='utf-8') as token:
            token.write(creds.to_json())
    return creds
