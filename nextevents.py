"""
pylint nextevents.py
-------------------------------------------------------------------
Your code has been rated at 10.00/10

https://console.cloud.google.com/apis/credentials?hl=fr&project=beaming-opus-401310
https://developers.google.com/calendar/api/quickstart/python?hl=fr

A Google Cloud Platform project with an OAuth consent screen configured for
an external user type and a publishing status of "Testing" is issued a refresh token
expiring in 7 days.

"""
import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from authenticate import authenticate_google_api
from constants import MAXRESULTS

# pylint: disable=too-few-public-methods
class Events():
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next events on the user's calendar.
    """
    def get_events(self):
        """
        API call to retrieve the events
        """
        result = []
        creds = authenticate_google_api('token.json',
                ['https://www.googleapis.com/auth/calendar.readonly'])
        if not creds:
            return result
        try:
            service = build('calendar', 'v3', credentials=creds)
            # Call the Calendar API
            now = datetime.datetime.now().isoformat() + 'Z'  # 'Z' indicates UTC time
            # pylint: disable=no-member
            # no need to manage any pagination in this API call as maxResults is coded
            events_result = service.events().list(maxResults=MAXRESULTS, calendarId='primary',
                                                timeMin=now,
                                                singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                print('No upcoming events found.')
                return None
            # Prints the start and name of the next NUMBER events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                date_obj = datetime.datetime.fromisoformat(start)
                # print(date_obj.strftime("%Y %a %d %b %Hh%M"))
                day_str = date_obj.strftime("%a %d %b %Hh%M")
                event_str = event['summary'][:16]
                result.append({'day': day_str, 'event': event_str, 'type': 'event'})

        except HttpError as error:
            print(f'An error occurred: {error}')
        return result

if __name__ == '__main__':
    events_obj = Events()
    evts = events_obj.get_events()
    if evts:
        print('Upcoming Events:')
        for entry in evts:
            print(f'{entry["day"]} {entry["event"]}')
    else:
        print('No upcoming Events found.')
