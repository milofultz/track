from datetime import date
from pathlib import Path
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
            long_journal += line[0:edge]
            line = line[edge:]
            long_journal += '\n'
        long_journal += line
        long_journal += '\n\n'

    # organize whole string
    entry = (delimiter + '\n' +
             top_line + '\n' +
             blank_line + '\n' +
             acc_lines + '\n' +
             blank_line + '\n' +
             mit_line + '\n' +
             blank_line + '\n' +
             long_journal)
    return entry

def record_entry(entry: str):
    """Record entry into file."""
    with open(FP, 'a') as f:
        f.write(entry)
    print('Entry recorded.')

# def init_journal():
#     """Create new journal file in root."""
#     if os.path.exists(FP) == False:
#         with open(FP, 'w') as f:
#             f.write('')
#         print('')
#         print(f'Journal created at:\n{FP}')
#     else:
#         print('')
#         print(f'A journal already exists at:\n{FP}')

def show_mit():
    # show mit set on previous day
    pass

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
        # go through options
        # elif option == 'init':
        #     init_journal()
        pass