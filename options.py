from datetime import datetime, timedelta
import re

from utilities import Colors


# Options

def get_accs(data):
    """Return recent accomplishments."""
    pattern = re.compile('(?<=\n)\* .*')
    matches = re.findall(pattern, data)

    return matches


def get_mit(entries: str):
    """Return MIT from last tracked data."""
    if entries != '':
        last_data = entries.rsplit('\n> ', 1)
        last_mit, endcap = last_data[1].split('\n', 1)
        return last_mit
    else:
        return 'No recent MIT found.'


def get_mits(entries: str):
    """Return recent MITs."""
    pattern = re.compile('(?<=\n)> .*')
    matches = re.findall(pattern, entries)

    return matches


def complete_mit(entries: str, mit: str):
    """Return updated entries with completed MIT."""
    first_entries, last_entry = entries.rsplit('---', 1)
    split_entry = last_entry.split('\n')
    for line in split_entry:
        # check if already completed
        if '> ' in line and (' (Completed)' in line or
                             'No MIT recorded' in line):
            print('MIT already completed.')
            return
    last_entry = last_entry.replace(mit, mit + ' (Completed)')
    updated_entries = first_entries + '---' + last_entry

    return updated_entries


def avg_mood(entries: str):
    """Return mood averages over time."""
    pattern = re.compile('\d{8} \(\d\)')  # find all dates and mood numbers
    raw_data = pattern.findall(entries)
    mood_arr = []
    for item in raw_data:
        date, mood = item.split()  # parse data into tuples
        mood_arr.append((date, mood[1]))

    start_date = datetime.strptime(mood_arr[0][0], '%Y%m%d')
    start_date = start_date.strftime('%B %-d, %Y')
    end_date = datetime.strptime(mood_arr[-1][0], '%Y%m%d')
    end_date = end_date.strftime('%B %-d, %Y')
    print(f'Using the data from {start_date} to {end_date}:\n')

    # get total time from first entry
    now = datetime.now()
    total_days = (now - datetime.strptime(mood_arr[0][0], '%Y%m%d')).days

    # 1w avg
    week_avg = 0
    day_count = 0
    week_ago_date = now - timedelta(days=6)
    for date, mood in mood_arr[:-7:-1]:
        if datetime.strptime(date, '%Y%m%d') > week_ago_date:
            week_avg += int(mood)
            day_count += 1
    week_avg = round(week_avg/day_count, 2)
    color = Colors.GREEN if week_avg > 2 else Colors.RED
    print('Your average mood over this week was ' +
          f'{color}{week_avg}{Colors.NORMAL}.')

    # 1m avg
    if total_days >= 7:
        month_avg = 0
        day_count = 0
        month_ago_date = now - timedelta(days=27)
        for date, mood in mood_arr[:-28:-1]:
            if datetime.strptime(date, '%Y%m%d') > month_ago_date:
                month_avg += int(mood)
                day_count += 1
        month_avg = round(month_avg/day_count, 2)
        color = Colors.GREEN if month_avg > 2 else Colors.RED
        print('Your average mood over this month was ' +
              f'{color}{month_avg}{Colors.NORMAL}.')

    # 1y avg
    if total_days >= 28:
        year_avg = 0
        day_count = 0
        year_ago_date = now - timedelta(days=364)
        for date, mood in mood_arr[:-365:-1]:
            if datetime.strptime(date, '%Y%m%d') > year_ago_date:
                year_avg += int(mood)
                day_count += 1
        year_avg = round(year_avg/day_count, 2)
        color = Colors.GREEN if year_avg > 2 else Colors.RED
        print('Your average mood over this month was ' +
              f'{color}{year_avg}{Colors.NORMAL}.')

    # all time avg
    total_avg = 0
    day_count = 0
    for date, mood in mood_arr:
        total_avg += int(mood)
        day_count += 1
    total_avg = round(total_avg/day_count, 2)
    color = Colors.GREEN if total_avg > 2 else Colors.RED
    print('Your average mood overall was ' +
          f'{color}{total_avg}{Colors.NORMAL}.\n')


def get_overviews(data):
    """Return recent entry overviews."""
    pattern = re.compile('\d{8} \(\d\) .*')
    matches = re.findall(pattern, data)

    return matches
