from datetime import datetime
import os
import random
import re

from config import *
from utilities import (Colors, clear_screen, append_data,
                       set_mood, set_short_journal, set_accomplishments,
                       set_long_journal, get_completed_tasks_in_tod,
                       format_entry, paint, print_mood_graph,
                       get_start_and_end_dates, get_mood_data, get_average_mood,
                       show_help)


def track(yesterday: bool = False):
    """Run whole tracking sequence."""
    print(Colors.BLUE + '   TRACK  ' + Colors.NORMAL + '\n')
    if yesterday:
        print(Colors.YELLOW + 'Tracking for yesterday:\n' + Colors.NORMAL)
    try:
        tod_accomplishments = get_completed_tasks_in_tod()
        entry_dic = user_entry(tod_accomplishments)
    except FileNotFoundError:
        entry_dic = user_entry()
    entry = format_entry(entry_dic, yesterday)
    clear_screen()
    append_data(entry, os.getenv('TRACK_FP'))
    print('Entry recorded.')


def user_entry(imported_accomplishments: list = None):
    """Record entry data from user."""
    mood = set_mood()
    short_journal = set_short_journal()
    accomplishments = set_accomplishments(imported_accomplishments)
    long_journal = set_long_journal()

    entries = {
        "mood": mood,
        "accomplishments": accomplishments,
        "short_journal": short_journal,
        "long_journal": long_journal
    }

    return entries


def get_accs(data):
    """Return recent accomplishments."""
    pattern = re.compile(r'(?<=\n)\* .*')
    matches = re.findall(pattern, data)

    return matches


def print_average_mood(data: str):
    """Return mood averages over time."""
    start_date, end_date = get_start_and_end_dates(data)
    total_days = (datetime.now() - start_date).days

    formatted_start_date = start_date.strftime('%B %-d, %Y')
    formatted_end_date = end_date.strftime('%B %-d, %Y')

    dates_and_moods = get_mood_data(data)

    print(Colors.WHITE + 'Using the data from ' +
          f'{formatted_start_date} to {formatted_end_date}:\n' + Colors.NORMAL)

    week_avg = get_average_mood(dates_and_moods, 7)
    print('Your average mood over this week was ' +
          f'{Colors.WHITE}{week_avg}{Colors.NORMAL}.')

    if total_days >= 7:
        month_avg = get_average_mood(dates_and_moods, 28)
        print('Your average mood over this month was ' +
              f'{Colors.WHITE}{month_avg}{Colors.NORMAL}.')

    if total_days >= 28:
        year_avg = get_average_mood(dates_and_moods, 365)
        print('Your average mood over this month was ' +
              f'{Colors.WHITE}{year_avg}{Colors.NORMAL}.')

    total_avg = get_average_mood(dates_and_moods, None)
    print('Your average mood overall was ' +
          f'{Colors.WHITE}{total_avg}{Colors.NORMAL}.\n')

    print_mood_graph(dates_and_moods)


def get_overviews(data):
    """Return recent entry overviews."""
    pattern = re.compile(r'\d{8} \(\d\) .*')
    matches = re.findall(pattern, data)

    return matches


def print_random_entry(data):
    """Print random entry from .track file"""
    entries = data.split('---')[1:]
    entry = random.choice(entries).strip()
    entry_lst = [line for line in entry.split('\n')]
    formatted_entry = '\n'.join(paint(entry_lst))
    print('\n' + formatted_entry + '\n')


def print_recent_accomplishments(data):
    """Print recent accomplishments from .track file"""
    accomplishments = get_accs(data)[-TERMINAL_HEIGHT + 2:]
    formatted_accomplishments = '\n'.join(paint(accomplishments))
    print(f'\n{formatted_accomplishments}\n')


def print_recent_overviews(data):
    """Print recent overviews from .track file"""
    overviews = get_overviews(data)[-TERMINAL_HEIGHT+2:]
    formatted_overviews = '\n'.join(paint(overviews))
    print(f'\n{formatted_overviews}\n')


def print_unknown_options(options):
    """Print error message if invalid option used"""
    show_help()
    options = " ".join(arg for arg in options)
    print("Unknown option(s): " + options)
