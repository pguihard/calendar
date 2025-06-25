"""
Generate the calendar.txt file based on GPSEO rules
pylint generatedata.py
-------------------------------------------------------------------
Your code has been rated at 10.00
"""
import datetime

start_date = datetime.date(2025, 1, 1)
end_date = datetime.date(2025, 12, 31)

start_recycle = datetime.date(2025, 1, 8)

start_plant = datetime.date(2025, 3, 24)

start_glass = datetime.date(2025, 4, 21)

start_bulky = datetime.date(2025, 1, 27)

delta = datetime.timedelta(days=1)

with open("calendar.txt", "w", encoding="utf-8") as file:
    current_date = start_date
    while current_date <= end_date:
        #TRASHTYPES =
        #  ['Ordures ménagères', 'Verres','Emballages recyclables','Végétaux','Encombrants']
        #
        # Ordures ménagères Mercredi AM toutes les semaines (code 0)
        if current_date.weekday() == 2:
            file.write(f'{current_date.strftime("%Y%m%d")}06 0\n')
        #
        # Verres le Lundi AM tous les mois (code 1)
        if current_date.weekday() == 0 and (current_date - start_glass).days % 28 == 0:
            file.write(f'{current_date.strftime("%Y%m%d")}06 1\n')
        #
        # # Emballages recyclables le Mercredi PM tous les 15 jours (code 2)
        if current_date.weekday() == 2 and (current_date - start_recycle).days % 14 == 0:
            file.write(f'{current_date.strftime("%Y%m%d")}12 2\n')
        #
        # Végétaux le Lundi PM tous les 15 jours (code 3)
        # Arrêt le 18 Novembre 2024, reprise le 24 Mars 2025
        if current_date.weekday() == 0 and start_plant <= current_date \
            and (current_date - start_plant).days % 14 == 0:
            file.write(f'{current_date.strftime("%Y%m%d")}12 3\n')
        #
        # Encombrants Lundi AM tous les 3 mois (code 4)
        if current_date.weekday() == 0 and (current_date - start_bulky).days % 91 == 0:
            file.write(f'{current_date.strftime("%Y%m%d")}06 4\n')

        current_date += delta
