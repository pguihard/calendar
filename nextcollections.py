"""
retrieve the next trash collections from a text file into data folder
pylint nextcollections.py
-------------------------------------------------------------------
Your code has been rated at 10.00
"""
import datetime
from tools.constants import TRASHTYPES

class Collections:
    """
    the class
    """
    def __init__(self):
        """
        constructor
        """
        self.file_path = "tools/calendar.txt"
        self.collections = []

    def add_item(self, date, event):
        """
        add items into the area
        """
        self.collections.append({'day': date, 'event': TRASHTYPES[int(event)], 'type': 'trash'})

    def get_collections(self):
        """
        read the data file
        """
        # Get the current date and time
        current_date = datetime.datetime.now()

        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                date, value = line.strip().split()
                current_str = f'{current_date.year}{current_date.month:02d}{current_date.day:02d}'
                current_obj = datetime.datetime.strptime(current_str, "%Y%m%d")
                date_obj = datetime.datetime.strptime(date, "%Y%m%d%H")
                # don't keep the date before the current day
                if date_obj < current_obj:
                    continue
                day_str = date_obj.strftime("%Y %a %d %b %Hh%M")
                self.add_item(day_str, value)
            return self.collections

if __name__ == '__main__':
    collections_obj = Collections()
    collects = collections_obj.get_collections()
    if collects:
        print('Upcoming Collections:')
        for entry in collects:
            print(f'{entry}')
    else:
        print('No upcoming Collections found.')
