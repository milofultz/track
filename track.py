from datetime import datetime, timedelta
from pathlib import Path
import re
from shutil import get_terminal_size
import sys

# Constants
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
    return open(FP, 'r').read()


# Main Functions
def user_entry():
    """Record entry data from user."""
    cls()

    # mood
    mood = input('#: ')

    # accomplishments
    accomplishments = []
    print('Write your accomplishments: ')
    while True:
        new_acc = input('-> ')
        # if blank entry, move on
        if new_acc != '':
            accomplishments.append(new_acc)
        else:
            break

    # MIT for tomorrow
    print("Tomorrow's most important task: ")
    mit = input('-> ')

    # short journal (50 chr)
    print('Summarize your day in less than 50 characters:      |')
    while True:
        short_journal = input('-> ')
        if len(short_journal) > 50:
            print('Please write less than 50 characters. Try: ')
            print(short_journal[0:50])
        else:
            break
    cls()

    # long journal
    long_journal = []
    print('Write your long journal entry: ')
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

    # format top lines
    delimiter = '---'
    blank_line = ''
    # if tracked between midnight and 3am, use prior day's date
    now = datetime.now()
    if int(now.strftime('%-H')) < 4:
    	now = now - timedelta(days=1)
	# get date as YYYYMMDD
    day = now.strftime("%Y%m%d")
    top_line = f"{day} ({mood}) {sj}"

    # format accomplishments
    acc_lines = ''
    for index, acc in enumerate(accs):
        acc_lines += f"* {acc}"
        if index + 1 != len(accs):
            acc_lines += '\n'
        else:
            pass
    mit_line = f"> {mit}"

    # format long journal
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

    # organize whole string
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
    """Record entry into tracking file."""
    with open(FP, 'a') as f:
        f.write(new_data)
    print('Entry recorded.')


# Options
def get_mit(entries: str):
    """Return MIT from last tracked data."""
    # pull most recent data
    pattern = re.compile('(---\n\d{8}.*> )(?!.*---\n\d{8}.*> )', re.DOTALL)
    last_data = re.search(pattern, entries)

    # get MIT start and end
    mit_start = last_data.end()
    last_mit = entries[mit_start:]
    last_mit = last_mit.split('\n')[0]

    return last_mit


def avg_mood():
    # pull all mood data
    # using dates return
    #   1w avg
    #   1m avg
    #   1y avg
    #   all time avg
    pass


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


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # check for file
        entry_dic = user_entry()
        entry = make_entry(entry_dic)
        cls()
        record_entry(entry)
    else:
        option = sys.argv[1]
        data = load_data()
        # go through options
        if option == 'mit':
            cls()
            mit = get_mit(data)
            print(f'\n> {mit}\n')
        elif option == 'overview':
            cls()
            overview_list = get_overviews(data)
            print('\n'.join(line for line in overview_list),
                  '\n')
        elif option == 'accs':
            cls()
            accs_list = get_accs(data)
            print('\n'.join(line for line in accs_list),
                  '\n')
        pass
