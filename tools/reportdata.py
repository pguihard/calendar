"""
Creating report.txt from calendar.txt
pylint tools/reportdata.py
Your code has been rated at 10.00/10
"""
import datetime
from constants import TRASHTYPES

def read_and_process_calendar(input_file, output_file):
    """
    creating a file that can be processed
    """
    with open(input_file, 'r',  encoding="utf-8") as infile, \
        open(output_file, 'w',  encoding="utf-8") as outfile:
        current_month = None
        for line in infile:
            parts = line.strip().split()
            if len(parts) == 2:
                date_str, value = parts
                date_obj = datetime.datetime.strptime(date_str, "%Y%m%d%H")
                day_str = date_obj.strftime("%A").ljust(9)
                formatted_date = date_obj.strftime(f"{day_str} %d %B %Y %H-00")
                month = date_obj.month
                if current_month is not None and current_month != month:
                    outfile.write("\n")  # Add a blank line when the month changes
                current_month = month
                output_line = f"{formatted_date}: {TRASHTYPES[int(value)]}\n"
                outfile.write(output_line)

read_and_process_calendar("calendar.txt", "report.txt")
