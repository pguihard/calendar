"""
pylint nextbirthdays.py
-------------------------------------------------------------------
Your code has been rated at 10.00/10
"""
import datetime
from googleapiclient.discovery import build
from authenticate import authenticate_google_api

class Birthdays():
    """
    Shows basic usage of the Google People API.
    """
    # pylint: disable=too-many-locals
    # pylint: disable=too-few-public-methods
    def get_birthdays(self):
        """
        Involve the API service
        """
        days = []
        creds = authenticate_google_api('people_token.json',
                ['https://www.googleapis.com/auth/contacts.readonly'])
        if not creds:
            return days
        # Build the People API service
        service = build('people', 'v1', credentials=creds)
        # The People API may return paginated results.
        # More connections can be returned in a single response,
        # so we need to handle pagination by making additional requests
        # using the nextPageToken provided in the response.
        connections = []
        # pylint: disable=no-member
        request = (
            service.people()
            .connections()
            .list(resourceName='people/me', personFields='names,birthdays')
        )
        while request is not None:
            connections_page = request.execute()
            connections.extend(connections_page.get('connections', []))
            request = service.people().connections().list_next(request, connections_page)
        #
        for person in connections:
            names = person.get('names', [])
            birthdays_info = person.get('birthdays', [])
            if birthdays_info:
                # Get the current date and time
                current_date = datetime.datetime.now()
                birthday_date = birthdays_info[0].get('date', {})
                if "year" in birthday_date:
                    age = str(current_date.year - birthday_date["year"])
                else:
                    age = "?"
                date_str = (
                    #current_date.year not used but fixes strptime failure when 29 Feb (leap year)
                    f'{current_date.year}-'
                    f'{birthday_date["month"]}-'
                    f'{birthday_date["day"]}'
                    )
                current_str = f'{current_date.year}-{current_date.month}-{current_date.day}'
                current_obj = datetime.datetime.strptime(current_str, "%Y-%m-%d")
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                # don't keep the date before the current day
                if date_obj < current_obj:
                    continue
                day_str = date_obj.strftime("%Y %a %d %b %Hh%M")
                if birthday_date:
                    for name in names:
                        days.append({'day': day_str, 'event': name['displayName'] +
                                     ' ' + age + 'ans', 'type': 'anniv'})
        return days

if __name__ == '__main__':
    birthdays = Birthdays()
    birthd = birthdays.get_birthdays()
    if birthd:
        print('Upcoming Birthdays:')
        for entry in birthd:
            print(f'{entry["day"]} {entry["event"]}')
    else:
        print('No upcoming birthdays found.')
