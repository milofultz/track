from datetime import datetime, timedelta
import os
import re

from terminalplot import plot

from config import *


def clear_screen():
    """Clear screen with 40 blank lines"""
    print('\n' * TERMINAL_HEIGHT)


def show_help():
    """Print help to screen"""
    print('\n' + Colors.BLACK_ON_WHITE +
          'track: Input info for daily tracking' + Colors.NORMAL + '\n'
          '  * Mood\n' +
          '  * Short Daily Summary\n' +
          '  * Accomplishments\n' +
          '  * Long Journal Entry\n' +
          "  * Tomorrow's Most Important Task\n" +
          '\n' +
          'Usage: track.py [options]\n'
          '\n' +
          'Options:\n' +
          '  [none]      Input and record daily tracking\n' +
          '  y           Input and record tracking for previous day\n' +
          '  !           Print random daily entry\n' +
          '  accs        Print all recent accomplishments\n' +
          '  help        Print this help menu\n' +
          '  mit         Print last recorded MIT\n' +
          '  mit done    Record last MIT as completed\n' +
          '  mits        Print MITs of most recent entries\n' +
          '  mood        Print average mood using past entries\n' +
          '  overviews   Print headers of all recent entries.\n')


def load_data(filepath):
    """Return data as a string"""
    with open(filepath, 'r') as f:
        data = f.read()
    return data


def save_data(data, filepath):
    """Write data to file"""
    if data:
        with open(filepath, 'w') as f:
            f.write(data)
    else:
        print('No data provided.')


def append_data(new_data, filepath):
    """Append entry to file"""
    with open(filepath, 'a') as f:
        f.write(new_data)


def set_env_variables():
    env_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '.env')
    env_data = load_data(env_path)
    for line in env_data.split('\n'):
        k, v = line.split('=', 1)
        os.environ[k] = v


def get_completed_tasks_in_tod():
    """Import completed tasks from .tod file"""
    completed_tasks = []
    tod_file_data = load_data(os.getenv('TOD_FP'))
    tod_file_data = tod_file_data.split('\n')

    for line in tod_file_data:
        if line == '' or line[0] != '[' or line[1] != 'X':
            continue
        completed_task = (f"{line[4:-7]} {line[-6:]}"
                          if line[-6:] != '(0:00)'
                          else line[4:-7])
        completed_tasks.append(completed_task)

    return completed_tasks


def get_start_and_end_dates(data):
    """Return start and end date range of entries"""
    dates = re.findall('\d{8}', data)

    start_date = datetime.strptime(dates[0], '%Y%m%d')
    end_date = datetime.strptime(dates[-1], '%Y%m%d')

    return start_date, end_date


def get_mood_data(data):
    """Return mood data from .track file"""
    matches = re.findall('\d{8} \([1-5]\)', data)
    dates_and_moods = []

    for match in matches:
        date, mood = match.split()
        date = datetime.strptime(date, '%Y%m%d')
        mood = mood[1]
        dates_and_moods.append((date, mood))

    return dates_and_moods


def get_average_mood(mood_data, past_days=None):
    """Return average mood from data in range"""
    mood_sum = 0
    total_days = 0
    if past_days is None:
        past_days = (datetime.now() - datetime(1970, 1, 1)).days
    start_date = datetime.now() - timedelta(days=past_days-1)
    for date, mood in mood_data[:-past_days:-1]:
        if date > start_date:
            mood_sum += int(mood)
            total_days += 1
    return round(mood_sum/total_days, 2)


def set_mood():
    """Return mood from user input"""
    while True:
        mood = input(Colors.RED + '#' + Colors.NORMAL + ': ')
        if len(mood) > 1 or not mood.isdigit():
            clear_screen()
            print(Colors.RED + 'Please enter a single digit number.' + Colors.NORMAL)
        else:
            print()
            break

    return mood


def set_short_journal():
    """Return short journal from user input"""
    print('Summarize your day in less than 50 characters:     ' +
          Colors.WHITE + '▼' + Colors.NORMAL)
    while True:
        short_journal = input(Colors.WHITE + '► ' + Colors.NORMAL)
        if len(short_journal) > 50:
            print(Colors.RED +
                  'Please write less than 50 characters. Try:' +
                  Colors.NORMAL)
            print(Colors.WHITE + short_journal[0:50] + Colors.NORMAL)
        else:
            print()
            return short_journal


def set_accomplishments(tod_accomplishments):
    """Return accomplishments from user input"""
    print('Write your accomplishments:\n')

    if tod_accomplishments is not None and tod_accomplishments != []:
        accomplishments = [accomplishment for accomplishment in tod_accomplishments]
        print_tod_accomplishments(accomplishments)
    else:
        accomplishments = []

    while True:
        accomplishment = input(Colors.CYAN + '* ' + Colors.NORMAL)
        if len(accomplishment) > 70:
            print(Colors.RED + 'Please write less than 70 characters. Try:')
            print(Colors.WHITE + '* ' + accomplishment[0:70] + Colors.NORMAL)
        elif accomplishment != '':
            accomplishments.append(accomplishment)
        else:
            return accomplishments


def set_long_journal():
    """Return long journal from user input"""
    long_journal = []

    print('Write your long journal entry:\n')
    while True:
        paragraph = input('  ')
        if paragraph != '':
            long_journal.append(paragraph)
        else:
            return long_journal


def set_mit():
    """Return MIT from user input"""
    print("Tomorrow's most important task: ")
    while True:
        mit = input(Colors.WHITE + '> ' + Colors.NORMAL)
        if not mit or not mit.strip():
            print("Please enter tomorrow's most important task")
        else:
            return mit


def format_entry(entry, yesterday: bool = False):
    """Return formatted entry"""
    overview_line = create_formatted_overview_line(entry['mood'],
                                                   entry['short_journal'],
                                                   yesterday)
    accomplishment_lines = create_formatted_accomplishments(
        entry['accomplishments']
    )
    mit_line = f"> {entry['mit']}"
    long_journal = create_formatted_long_journal(entry['long_journal'])

    return ('---' + '\n' +
            overview_line + '\n\n' +
            accomplishment_lines + '\n\n' +
            mit_line + '\n\n' +
            long_journal + '\n')


def create_formatted_overview_line(mood, short_journal, yesterday):
    """Return formatted overview line"""
    now = datetime.now()
    if yesterday or int(now.strftime('%-H')) < 4:
        now = now - timedelta(days=1)
    date = now.strftime("%Y%m%d")
    return f"{date} ({mood}) {short_journal}"


def create_formatted_accomplishments(accomplishments):
    """Return formatted string of accomplishment list"""
    output = ''

    for index, accomplishment in enumerate(accomplishments):
        output += f"* {accomplishment}"
        if index + 1 != len(accomplishments):
            output += '\n'

    return output


def create_formatted_long_journal(long_journal):
    """Return formatted long journal entry"""
    output = ''

    for index, line in enumerate(long_journal):
        while len(line) > 76:
            edge = 75
            while line[edge] != ' ':
                edge -= 1
            output += line[0:edge].strip()
            line = line[edge:]
            output += '\n'
        output += line.strip() + '\n\n'

    return output


def print_tod_accomplishments(accomplishments):
    """Print accomplishments from tod file"""
    print(Colors.BLUE + "Accomplishments from Tod:" + Colors.NORMAL)
    for accomplishment in accomplishments:
        print(Colors.CYAN + '* ' + Colors.NORMAL + accomplishment)


def paint(lines: list):
    """Return colored list of items"""
    for i, line in enumerate(lines):
        if line == '':
            continue
        if re.match('\d{8}', line[:8]):
            lines[i] = paint_date(line)
        elif line[0] == '*':
            lines[i] = paint_accomplishment(line)
        elif line[0] == '>':
            lines[i] = paint_mit(line)
    return lines


def paint_date(line):
    """Return colored date"""
    return (Colors.GREY + line[:8] +
            Colors.RED + line[8:13] +
            Colors.WHITE + line[13:] + Colors.NORMAL)


def paint_accomplishment(line):
    """Return colored accomplishment"""
    return Colors.CYAN + line[0] + Colors.NORMAL + line[1:]


def paint_mit(line):
    """Return colored MIT"""
    if ' (Completed)' in line:
        end = line[1:-12] + Colors.GREEN + line[-12:] + Colors.NORMAL
    else:
        end = line[1:]
    return Colors.WHITE + line[0] + Colors.NORMAL + end


def print_mood_graph(dates_and_moods):
    """Print line graph of mood in terminal"""
    x = range(len(dates_and_moods))
    y = [int(i[1]) for i in dates_and_moods]
    display_rows = 10
    display_columns = (TERMINAL_WIDTH
                       if TERMINAL_WIDTH < len(dates_and_moods)
                       else len(dates_and_moods) * 2)
    plot(x, y, rows=display_rows, columns=display_columns)
    print()


def is_last_mit_complete_in_tod(last_mit):
    tod_completed_tasks = get_completed_tasks_in_tod()
    for task in tod_completed_tasks:
        if last_mit in task:
            return True
    return False
