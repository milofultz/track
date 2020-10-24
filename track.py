import sys

from config import *
from options import (track, complete_last_mit, print_random_entry,
                     print_recent_accomplishments, print_last_mit,
                     print_recent_mits, print_average_mood,
                     print_recent_overviews, print_unknown_options)
from utilities import clear_screen, load_data, show_help


if __name__ == "__main__":
    options = sys.argv[1:]
    clear_screen()

    if not options:
        track()

    else:
        option = options[0]
        try:
            data = load_data(Filepaths.TRACK)
        except FileNotFoundError:
            show_help()
            sys.exit()

        if option == '!':
            print_random_entry(data)
        elif option == 'accs':
            print_recent_accomplishments(data)
        elif option in 'help':
            show_help()
        elif option == 'mit':
            if 'done' in options:
                complete_last_mit(data)
            else:
                print_last_mit(data)
        elif option == 'mits':
            print_recent_mits(data)
        elif option == 'mood':
            print_average_mood(data)
        elif option == 'overviews':
            print_recent_overviews(data)
        elif option == 'y':
            track(yesterday=True)
        else:
            print_unknown_options(options)
