"""

Forked and modified from https://github.com/kressi/terminalplot
Original Author: Michael Kressibucher (username: kressi)

"""

from config import Colors, TERMINAL_HEIGHT, TERMINAL_WIDTH


def plot(x, y, rows=None, columns=None):
    """
    x, y list of values on x- and y-axis
    plot those values within canvas size (rows and columns)
    """
    if not rows or not columns:
        rows, columns = TERMINAL_HEIGHT, TERMINAL_WIDTH

    # Scale points such that they fit on canvas
    x_scaled = scale_x(x, columns)
    y_scaled = scale_y(y, rows)

    # Create empty canvas
    canvas = [[' ' for _ in range(columns)] for _ in range(rows)]

    # Add scaled points to canvas
    for ix, iy in zip(x_scaled, y_scaled):
        canvas[rows - iy - 1][ix] = Colors.BLUE + 'o'

    # Print rows of canvas
    for row in [''.join(row) for row in canvas]:
        print('│ ' + Colors.YELLOW + row + ' ' + Colors.NORMAL)
    print('└' + '─' * (columns+2) + Colors.NORMAL)


def scale_x(x, length):
    """
    Scale points in 'x', such that distance between
    max(x) and min(x) equals to 'length'. min(x)
    will be moved to 0.
    """
    s = float(length - 1) / \
        (max(x) - min(x)) if x and max(x) - min(x) != 0 else length
    return [int((i - min(x)) * s) for i in x]


def scale_y(y, length):
    """
    Scale points in 'y', such that distance between
    max(x) and 0 equals to 'length'.
    """
    s = float(length - 1) / \
        max(y) if y and max(y) != 0 else length
    return [int(i * s) for i in y]
