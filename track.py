import os
import sys

from options import (track, print_random_entry, print_recent_accomplishments,
                     print_average_mood, print_recent_overviews, print_unknown_options,
                     add_to_journal)
from utilities import clear_screen, load_data, show_help, set_env_variables


if __name__ == "__main__":
    set_env_variables()
    options = sys.argv[1:]
    clear_screen()
    try:
        data = load_data(os.getenv('TRACK_FP'))
    except FileNotFoundError:
        show_help()
        sys.exit()

    if not options:
        track()

    else:
        option = options[0]

        if option == '!':
            print_random_entry(data)
        elif option == 'accs':
            print_recent_accomplishments(data)
        elif option == 'add':
            add_to_journal()
        elif option in 'help':
            show_help()
        elif option == 'mood':
            print_average_mood(data)
        elif option == 'overviews':
            print_recent_overviews(data)
        elif option == 'y':
            track(yesterday=True)
        else:
            print_unknown_options(options)
