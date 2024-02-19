"""
launch google API calls to get events and people's bithdays
pylint runme.py
-------------------------------------------------------------------
Your code has been rated at 10.00/10
"""
import datetime
from colorama import Fore, Style
from nextevents import Events
from nextbirthdays import Birthdays
from constants import MAXRESULTS, MAXBIRTHDAYS

def sort_events(data):
    """
    sort data by month and day criteria
    """
    def get_day(data):
        date_str = data['day']
        date_obj = datetime.datetime.strptime(date_str, '%a %d %b %Hh%M')
        return date_obj.day

    def get_month(data):
        date_str = data['day']
        date_obj = datetime.datetime.strptime(date_str, '%a %d %b %Hh%M')
        return date_obj.month

    # Define key functions for sorting
    key_functions = (get_month, get_day)
    # Sort the birthdays based on the month
    sorted_data = sorted(data, key=lambda x: tuple(func(x) for func in key_functions))

    return sorted_data

if __name__ == '__main__':
    events = Events()
    birthdays = Birthdays()
    merge = sort_events(events.get_events() + birthdays.get_birthdays()[:MAXBIRTHDAYS])

    if merge:
        COUNT = 0
        print(Fore.CYAN + Style.BRIGHT + '--- The upcoming events ---' +
              Style.RESET_ALL)
        for entry in merge:
            print(f'{entry["day"]} {entry["event"]}')
            COUNT += 1
            if COUNT == MAXRESULTS:
                break
    else:
        print('No upcoming events found.')
