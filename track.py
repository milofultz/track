from datetime import date, timedelta
from pathlib import Path
import re
import sys

# Constants
BREAKPOINTS = {
    ' ',
    '.',
    '!',
    '?'
}
FP = str(Path.home()) + '/.track'


# Utilities
def cls():
    """Clear screen with 40 blank lines."""
    print('\n'*40)


# Modules
def user_entry():
    """Record entries from user."""
    cls()

    # mood
    mood = input('#: ')

    # accomplishments
    accomplishments = []
    print('Write your accomplishments: ')
    while True:
        new_acc = input('-> ')
        # if blank entry, move on
        if new_acc != '': accomplishments.append(new_acc)
        else: break

    # MIT for tomorrow
    print("Tomorrow's most important task: ")
    mit = input('-> ')

    # short journal (50 chr)
    print('Summmarize your day in less than 50 characters:     |')
    while True:
        short_journal = input('-> ')
        if len(short_journal) > 50:
            print('Please write less than 50 characters. Try: ')
            print(short_journal[0:50])
        else: break
    cls()

    # long journal
    long_journal = []
    print('Write your long journal entry: ')
    while True:
        paragraph = input('-> ')
        # if blank entry, move on
        if paragraph != '': long_journal.append(paragraph)
        else: break

    entry_dic = {
        "mood": mood,
        "accomplishments": accomplishments,
        "mit": mit,
        "short_journal": short_journal,
        "long_journal": long_journal
    }
    return entry_dic

def make_entry(dic: dict):
    """Format entry for writing to file."""
    mood = dic.get('mood')
    accs = dic.get('accomplishments')
    mit = dic.get('mit')
    sj = dic.get('short_journal')
    lj = dic.get('long_journal')

    # format top lines
    delimiter = '---'
    blank_line = ''
    # get date as YYYYMMDD
    today = date.today()
    today = today.strftime("%Y%m%d")
    top_line = f"{today} ({mood}) {sj}"

    # format accomplishments
    acc_lines = ''
    for index, acc in enumerate(accs):
        acc_lines += f"* {acc}"
        if index + 1 != len(accs): acc_lines += '\n'
        else: pass
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
    entry = (delimiter + '\n' +
             top_line + '\n' +
             blank_line + '\n' +
             acc_lines + '\n' +
             blank_line + '\n' +
             mit_line + '\n' +
             blank_line + '\n' +
             long_journal + '\n')
    return entry

def record_entry(entry: str):
    """Record entry into file."""
    with open(FP, 'a') as f:
        f.write(entry)
    print('Entry recorded.')

def get_mit():
    """Show MIT from last tracked data."""
    # pull most recent data
    track_data = open(FP, 'r').read()
    pattern = re.compile('(---\n\d{8}.*> )(?!.*---\n\d{8}.*> )', re.DOTALL)
    last_data = re.search(pattern, track_data)

    # get MIT start and end
    mit_start = last_data.end()
    last_mit = track_file[mit_start:]
    last_mit = last_mit.split('\n')[0]

    # return MIT
    return last_mit

def avg_mood():
    # pull all mood data
    # using dates return
    #   1w avg
    #   1m avg
    #   1y avg
    #   all time avg
    pass

def get_accs():
    # pull all accs and return them on screen
    pass

def get_overviews():
    # pull all headers and return on screen
    pass

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # check for file
        entry_dic = user_entry()
        entry = make_entry(entry_dic)
        cls()
        record_entry(entry)
    else:
        option = sys.argv[1]
        # go through options
        if option == 'mit':
            last_mit = get_mit()
            print(f'\n> {last_mit}\n')
        pass