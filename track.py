from pathlib import Path
import random
import sys

from options import (get_accs, get_mit, get_mits, get_overviews,
                     complete_mit, avg_mood)
from utilities import (cls, show_help,
                       Colors, TERMINAL_HEIGHT,
                       load_data, append_data,
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
        mood = input('#: ')
        if len(mood) > 1 or not mood.isdigit():
            print('Please enter a single digit number.')
        else:
            break

    # Short Journal (50 chr)
    print('Summarize your day in less than 50 characters:      |')
    while True:
        short_journal = input('-> ')
        if len(short_journal) > 50:
            print('Please write less than 50 characters. Try: ')
            print(short_journal[0:50])
        else:
            break

    # Accomplishments
    if imported_accs is not None:
        accomplishments = imported_accs
    else:
        accomplishments = []
    if len(accomplishments) > 0:
        print('')
        print("Accomplishments from Tod:")
        for acc in imported_accs:
            print(f"* {acc}")
        print('')
    print('Write your accomplishments: ')
    while True:
        new_acc = input('-> ')
        # if blank entry, move on
        if new_acc != '':
            accomplishments.append(new_acc)
        else:
            break

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

    # MIT for Tomorrow
    print("Tomorrow's most important task: ")
    mit = input('-> ')
    if not mit:
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
        print('Tracking for yesterday:\n')
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
            print('\n' + entry + '\n')

        elif option == 'accs':
            cls()
            accs_list = get_accs(data)[-TERMINAL_HEIGHT+2:]
            print('\n'.join(line for line in accs_list),
                  '\n')

        elif option in 'help':
            show_help()

        elif option == 'mit':
            cls()
            mit = get_mit(data)
            if 'done' in sys.argv:
                updated_entries = complete_mit(data, mit)
                append_data(updated_entries, TRACK_FP)
                print('Entry updated.')
            if ' (Completed)' in mit:
                mit = mit[:-12] + Colors.GREEN + mit[-12:] + Colors.NORMAL
            print(f'\n> {mit}\n')

        elif option == 'mits':
            cls()
            mits = get_mits(data)[-TERMINAL_HEIGHT+2:]
            for index, mit in enumerate(mits):
                if ' (Completed)' in mit:
                    mits[index] = mit[:-12] + Colors.GREEN + mit[-12:] + Colors.NORMAL
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
