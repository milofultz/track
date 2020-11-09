from shutil import get_terminal_size


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
    BLACK_ON_WHITE = '\033[47m\033[30m'


TERMINAL_WIDTH, TERMINAL_HEIGHT = get_terminal_size()
