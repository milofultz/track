from datetime import datetime, timedelta
import re
from shutil import get_terminal_size


# Constants

class Colors:
    WHITE = "\033[97m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    GREY = '\x1b[90m'
    NORMAL = '\033[0m'


TERMINAL_HEIGHT = get_terminal_size()[1]


# Utilities

def cls():
    """Clear screen with 40 blank lines."""
    print('\n'*40)


def show_help():
    """Print help to screen."""
    print('\n' +
          'track: Input info for daily tracking\n'
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
          '  !           Print random daily entry\n' +
          '  accs        Print all recent accomplishments\n' +
          '  help        Print this help menu\n' +
          '  mit         Print last recorded MIT\n' +
          '  mit done    Record last MIT as completed\n' +
          '  mits        Print MITs of most recent entries\n' +
          '  mood        Print average mood using past entries\n' +
          '  overviews   Print headers of all recent entries.\n' +
          '  y           Record tracking for previous day (if you forget the night before)\n')


def load_data(fp):
    """Return data as a string."""
    with open(fp, 'r') as f:
        data = f.read()
    return data


def append_data(new_data, fp):
    """Append entry to tracking file."""
    with open(fp, 'a') as f:
        f.write(new_data)


def save_data(data, fp):
    if data:
        with open(fp, 'w') as f:
            f.write(data)
    else:
        print('No data provided.')


def import_completed_tasks(data: str):
    """Import completed tasks from .tod file"""
    completed_tasks = []
    data = data.split('\n')

    for task in data:
        if task == '' or task[0] != '[' or task[1] != 'X':
            continue
        completed_tasks.append(f"{task[4:-7]} {task[-6:]}")

    return completed_tasks


def format_entry(dic, yesterday: bool = False):
    """Return formatted entry."""
    mood = dic.get('mood')
    accs = dic.get('accomplishments')
    mit = dic.get('mit')
    sj = dic.get('short_journal')
    lj = dic.get('long_journal')

    delimiter = '---'
    blank_line = ''
    # if between midnight and 3am or 'y' option used, use prior day's date
    now = datetime.now()
    if yesterday or int(now.strftime('%-H')) < 4:
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
            while line[edge] != ' ':
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


def paint(lst):
    for i, line in enumerate(lst):
        if not line:
            continue
        elif re.match('\d{8}', line[:8]):
            lst[i] = (Colors.GREY + line[:8] +
                      Colors.RED + line[8:13] +
                      Colors.WHITE + line[13:]) + Colors.NORMAL
        elif line[0] == '*':
            lst[i] = Colors.CYAN + line[0] + Colors.NORMAL + line[1:]
        elif line[0] == '>':
            if ' (Completed)' in line:
                end = line[1:-12] + Colors.GREEN + line[-12:] + Colors.NORMAL
            else:
                end = line[1:]
            lst[i] = Colors.WHITE + line[0] + Colors.NORMAL + end
    return '\n'.join(item for item in lst)
