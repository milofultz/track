from pathlib import Path
import random
import sys

from options import (get_accs, get_mit, get_mits, get_overviews,
                     paint, complete_mit, avg_mood)
from utilities import (cls, show_help,
                       Colors, TERMINAL_HEIGHT,
                       load_data, append_data, save_data,
                       import_completed_tasks,
                       format_entry)


# Constants

TOD_FP = str(Path.home()) + '/.tod'
TRACK_FP = str(Path.home()) + '/.track'


# Main Functions

def user_entry(imported_accs: list = None):
    """Record entry data from user."""
    # Mood
    while True:
        mood = input(Colors.RED + '#' + Colors.NORMAL + ': ')
        if len(mood) > 1 or not mood.isdigit():
            cls()
            print(Colors.RED + 'Please enter a single digit number.' + Colors.NORMAL)
        else:
            print()
            break

    # Short Journal (50 chr)
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
            break

    # Accomplishments
    print('Write your accomplishments:\n')

    if imported_accs is not None:
        accomplishments = paint(imported_accs)
    else:
        accomplishments = []
    if len(accomplishments) > 0:
        print(Colors.BLUE + "Accomplishments from Tod:" + Colors.NORMAL)
        for acc in imported_accs:
            print(acc)

    while True:
        new_acc = input(Colors.CYAN + '* ' + Colors.NORMAL)
        # if blank entry, move on
        if new_acc != '':
            accomplishments.append(new_acc)
        else:
            break

    # Long Journal
    long_journal = []
    print('Write your long journal entry:\n')
    while True:
        paragraph = input('  ')
        # if blank entry, move on
        if paragraph != '':
            long_journal.append(paragraph)
        else:
            break

    # MIT for Tomorrow
    print("Tomorrow's most important task: ")
    mit = input(Colors.WHITE + '> ' + Colors.NORMAL)
    if not mit or not mit.strip():
        mit = 'No MIT recorded'

    entries = {
        "mood": mood,
        "accomplishments": accomplishments,
        "mit": mit,
        "short_journal": short_journal,
        "long_journal": long_journal
    }
    return entries


def track(yesterday: bool = False):
    """Run whole tracking sequence."""
    cls()
    if yesterday:
        print(Colors.YELLOW + 'Tracking for yesterday:\n' + Colors.NORMAL)
    try:
        tod_data = load_data(TOD_FP)
        tod_accs = import_completed_tasks(tod_data)
        entry_dic = user_entry(tod_accs)
    except FileNotFoundError:
        entry_dic = user_entry()
    entry = format_entry(entry_dic, yesterday)
    cls()
    append_data(entry, TRACK_FP)
    print('Entry recorded.')


if __name__ == "__main__":
    if len(sys.argv) == 1:
        track()

    else:
        option = sys.argv[1]
        try:
            data = load_data(TRACK_FP)
        except FileNotFoundError:
            show_help()
            sys.exit()

        # Return random entry
        if option == '!':
            cls()
            entries = data.split('---')[1:]
            entry = random.choice(entries).strip()
            entry_lst = [line for line in entry.split('\n')]
            entry_lst = paint(entry_lst)
            entry = '\n'.join(line for line in entry_lst)
            print('\n' + entry + '\n')

        elif option == 'accs':
            cls()
            accs_list = get_accs(data)[-TERMINAL_HEIGHT+2:]
            accs_list = paint(accs_list)
            print('\n'.join(line for line in accs_list),
                  '\n')

        elif option in 'help':
            show_help()

        elif option == 'mit':
            cls()
            mit = get_mit(data)
            if 'done' in sys.argv:
                updated_entries = complete_mit(data, mit)
                save_data(updated_entries, TRACK_FP)
                mit = mit + ' (Completed)'
                print('Entry updated.')
            if ' (Completed)' in mit or 'done' in sys.argv:
                mit = paint(mit)
            print(f'\n> {mit}\n')

        elif option == 'mits':
            cls()
            mits = get_mits(data)[-TERMINAL_HEIGHT+2:]
            for index, mit in enumerate(mits):
                if ' (Completed)' in mit:
                    mits = paint(mits)
            print('\n'.join(line for line in mits),
                  '\n')

        elif option == 'mood':
            cls()
            avg_mood(data)

        elif option == 'overviews':
            cls()
            overviews = get_overviews(data)[-TERMINAL_HEIGHT+2:]
            print('\n'.join(line for line in overviews),
                  '\n')

        elif option == 'y':
            track(yesterday=True)

        else:
            options = " ".join(arg for arg in sys.argv[1:])
            print("Unknown option(s): " + options)
            print("Try `track help` for more information.")
