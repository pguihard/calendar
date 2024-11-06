"""
launch google API calls to get events and people's bithdays
pylint runme.py
-------------------------------------------------------------------
Your code has been rated at 10.00/10
"""
import datetime
from colorama import Fore, Style
from nextcollections import Collections
from nextevents import Events
from nextbirthdays import Birthdays
from constants import MAXRESULTS, MAXBIRTHDAYS, DATE_FORMAT, MAXCOLLECTIONS

def sort_events(data):
    """
    sort data by month and day criteria
    """
    def get_day(data):
        date_str = data['day']
        date_obj = datetime.datetime.strptime(date_str, DATE_FORMAT)
        return date_obj.day

    def get_month(data):
        date_str = data['day']
        date_obj = datetime.datetime.strptime(date_str, DATE_FORMAT)
        return date_obj.month

    def get_year(data):
        date_str = data['day']
        date_obj = datetime.datetime.strptime(date_str, DATE_FORMAT)
        return date_obj.year

    # Define key functions for sorting
    key_functions = (get_year, get_month, get_day)
    # Sort the birthdays based on the month
    sorted_data = sorted(data, key=lambda x: tuple(func(x) for func in key_functions))

    return sorted_data

if __name__ == '__main__':
    events = Events()
    birthdays = Birthdays()
    sorted_birthdays = sort_events(birthdays.get_birthdays())

    collections_obj = Collections()
    collects = collections_obj.get_collections()

    merge = sort_events(events.get_events() + sorted_birthdays[:MAXBIRTHDAYS] +
                         collects[:MAXCOLLECTIONS])

    if merge:
        COUNT = 0
        print(Fore.CYAN + Style.BRIGHT +
              f'--- The {min(len(merge), MAXRESULTS)} upcoming events ---' +
              Style.RESET_ALL)
        for entry in merge:
            if entry["type"] == "anniv":
                print(Fore.YELLOW + f'{entry["day"][5:]} {entry["event"]}' +
                Style.RESET_ALL)
            else:
                if entry["type"] == "trash":
                    print(Fore.GREEN + f'{entry["day"][5:]} {entry["event"]}' +
                    Style.RESET_ALL)
                else:
                    print(f'{entry["day"][5:]} {entry["event"]}')
            COUNT += 1
            if COUNT == MAXRESULTS:
                break
    else:
        print('No upcoming events found.')
