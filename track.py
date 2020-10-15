from datetime import datetime, timedelta
from pathlib import Path
import random
import re
from shutil import get_terminal_size
import sys


# Constants

GREEN = "\033[92m"
RED = "\033[91m"
NORMAL = '\033[0m'
BREAKPOINTS = {
    ' ',
    '.',
    '!',
    '?'
}
FP = str(Path.home()) + '/.track'
TERMINAL_HEIGHT = get_terminal_size()[1]


# Utilities

def cls():
    """Clear screen with 40 blank lines."""
    print('\n'*40)


def load_data():
    try:
        with open(FP, 'r') as f:
            data = f.read()
        return data
    except:
        print('No file found.')
        return None


# Main Functions
def user_entry():
    """Record entry data from user."""
    cls()

    # Mood
    mood = input('#: ')

    # Accomplishments
    accomplishments = []
    print('Write your accomplishments: ')
    while True:
        new_acc = input('-> ')
        # if blank entry, move on
        if new_acc != '':
            accomplishments.append(new_acc)
        else:
            break

    # MIT for Tomorrow
    print("Tomorrow's most important task: ")
    mit = input('-> ')

    # Short Journal (50 chr)
    print('Summarize your day in less than 50 characters:      |')
    while True:
        short_journal = input('-> ')
        if len(short_journal) > 50:
            print('Please write less than 50 characters. Try: ')
            print(short_journal[0:50])
        else:
            break
    cls()

    # Long Journal
    long_journal = []
    print('Write your long journal entry:')
    while True:
        paragraph = input('-> ')
        # if blank entry, move on
        if paragraph != '':
            long_journal.append(paragraph)
        else:
            break

    entries = {
        "mood": mood,
        "accomplishments": accomplishments,
        "mit": mit,
        "short_journal": short_journal,
        "long_journal": long_journal
    }
    return entries


def make_entry(dic: dict):
    """Return formatted entry."""
    mood = dic.get('mood')
    accs = dic.get('accomplishments')
    mit = dic.get('mit')
    sj = dic.get('short_journal')
    lj = dic.get('long_journal')

    delimiter = '---'
    blank_line = ''
    # if tracked between midnight and 3am, use prior day's date
    now = datetime.now()
    if int(now.strftime('%-H')) < 4:
    	now = now - timedelta(days=1)
    day = now.strftime("%Y%m%d")
    top_line = f"{day} ({mood}) {sj}"

    acc_lines = ''
    for index, acc in enumerate(accs):
        acc_lines += f"* {acc}"
        if index + 1 != len(accs):
            acc_lines += '\n'
        else:
            pass

    mit_line = f"> {mit}"

    long_journal = ''
    for index, paragraph in enumerate(lj):
        line = paragraph
        while len(line) > 76:
            edge = 75
            while line[edge] not in BREAKPOINTS:
                edge -= 1
            long_journal += line[0:edge].strip()
            line = line[edge:]
            long_journal += '\n'
        long_journal += line.strip()
        long_journal += '\n\n'

    formatted_entry = (delimiter + '\n' +
                       top_line + '\n' +
                       blank_line + '\n' +
                       acc_lines + '\n' +
                       blank_line + '\n' +
                       mit_line + '\n' +
                       blank_line + '\n' +
                       long_journal + '\n')

    return formatted_entry


def record_entry(new_data: str):
    """Append entry to tracking file."""
    with open(FP, 'a') as f:
        f.write(new_data)
    print('Entry recorded.')


# Options

def get_mit(entries: str):
    """Return MIT from last tracked data."""
    last_data = entries.rsplit('\n> ', 1)
    last_mit, endcap = last_data[1].split('\n', 1)

    return last_mit


def complete_mit(entries: str, mit: str):
    """Update entries with completed MIT."""    
    first_entries, last_entry = entries.rsplit('---', 1)
    split_entry = last_entry.split('\n')
    for line in split_entry:
        # check if already completed
        if '> ' in line and ' (Completed)' in line:
            print('MIT already completed.\n')
            return
    last_entry = last_entry.replace(mit, mit + ' (Completed)')
    updated_entries = first_entries + '---' + last_entry

    with open(FP, 'w') as f:
        f.write(updated_entries)
        print('Entry updated.\n')

def avg_mood(entries: str):
    """Return mood averages over time."""
    pattern = re.compile('\d{8} \(\d\)') # find all dates and mood numbers
    raw_data = pattern.findall(entries)
    mood_arr = []
    for item in raw_data:
        date, mood = item.split() # parse data into tuples
        mood_arr.append((date, mood[1]))
    
    start_date = mood_arr[0][0]
    end_date = mood_arr[-1][0]
    print(f'Using the data from {start_date} to {end_date}:\n')
    
    # 1w avg
    week_avg = 0
    day_count = 0
    for date, mood in mood_arr[:-7:-1]:
        week_avg += int(mood)
        day_count += 1
    week_avg = round(week_avg/day_count, 2)
    color = GREEN if week_avg > 2 else RED
    print('Your average mood over this week was ' + 
          f'{GREEN}{week_avg}{NORMAL}.')
    # 1m avg
    if len(mood_arr) > 7:
        month_avg = 0
        day_count = 0
        for date, mood in mood_arr[:-30:-1]:
            month_avg += int(mood)
            day_count += 1
        month_avg = round(month_avg/day_count, 2)
        color = GREEN if month_avg > 2 else RED
        print('Your average mood over this month was ' + 
              f'{GREEN}{month_avg}{NORMAL}.')
    # 1y avg
    if len(mood_arr) > 28:
        year_avg = 0
        day_count = 0
        for date, mood in mood_arr[:-365:-1]:
            month_avg += int(mood)
            day_count += 1
        year_avg = round(year_avg/day_count, 2)
        color = GREEN if year_avg > 2 else RED
        print('Your average mood over this month was ' +
              f'{color}{year_avg}{NORMAL}.')
    # all time avg
    total_avg = 0
    day_count = 0
    for date, mood in mood_arr[:-7:-1]:
        total_avg += int(mood)
        day_count += 1
    total_avg = round(total_avg/day_count, 2)
    color = GREEN if total_avg > 2 else RED
    print('Your average mood overall was ' + 
          f'{GREEN}{total_avg}{NORMAL}.\n')


def get_accs(data):
    """Return recent accomplishments."""
    pattern = re.compile('(?<=\n)\* .*')
    matches = re.findall(pattern, data)
    
    return matches[:TERMINAL_HEIGHT-2]


def get_overviews(data):
    """Return recent entry overviews."""
    pattern = re.compile('\d{8} \(\d\) .*')
    matches = re.findall(pattern, data)
    
    return matches[:TERMINAL_HEIGHT-2]


def get_mits(data):
    """Return recent MITs."""
    pattern = re.compile('(?<=\n)> .*')
    matches = re.findall(pattern, data)

    return matches[:TERMINAL_HEIGHT-2]


def show_help():
    print('\n' +
          'track: Input info for daily tracking:\n'
          '  * Mood\n' +
          '  * Accomplishments\n' +
          "  * Tomorrow's Most Important Task\n" +
          '  * Short Daily Summary\n' +
          '  * Long Journal Entry\n' +
          '\n' +
          'Usage: track.py [options]\n'
          '\n' +
          'Options:\n' +
          '  [none]      Input and record daily tracking\n' +
          '  accs        Print all recent accomplishments\n' +
          '  help        Print this help menu\n' +
          '  mit         Print last recorded MIT\n' +
          '  mit done    Record last MIT as completed\n' +
          '  mood        Print average mood over time\n' +
          '  overview    Print all recent daily summaries\n')


if __name__ == "__main__":
    if len(sys.argv) == 1 or re.match('\d{8}', option):
        entry_dic = user_entry()
        entry = make_entry(entry_dic)
        cls()
        record_entry(entry)
    else:
        option = sys.argv[1]
        data = load_data()
        if not data: 
            show_help()
            sys.exit()

        if option == '!':
            cls()
            entries = data.split('---')[1:]
            entry = random.choice(entries).strip()
            print('\n' + entry + '\n')

        elif option == 'accs':
            cls()
            accs_list = get_accs(data)
            print('\n'.join(line for line in accs_list),
                  '\n')

        elif option in ['help', 'info']:
            show_help()

        elif option == 'mit':
            cls()
            mit = get_mit(data)
            if len(sys.argv) == 3 and sys.argv[2] == 'done':
                complete_mit(data, mit)
            else: 
                if ' (Completed)' in mit:
                    mit = mit[:-12] + GREEN + mit[-12:] + NORMAL
                print(f'\n> {mit}\n')

        if option == 'mits':
            cls()
            mits = get_mits(data)
            for index, mit in enumerate(mits):
                if ' (Completed)' in mit:
                    mits[index] = mit[:-12] + GREEN + mit[-12:] + NORMAL
            print('\n'.join(line for line in mits),
                  '\n')

        elif option == 'mood':
            cls()
            avg_mood(data)

        elif option == 'overview':
            cls()
            overviews = get_overviews(data)
            print('\n'.join(line for line in overviews),
                  '\n')

        pass