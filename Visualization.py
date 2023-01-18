import curses

# Tworzymy listę z pozycjami wojowników
core = [(0, ['MOV', None, [[None, 0], [None, 1]], None]),
        (1, ['MOV', None, [[None, 0], [None, 1]], None]),
        (2, ['MOV', None, [[None, 0], [None, 1]], None]),
        (3, ['MOV', None, [[None, 0], [None, 1]], None]),
        (4, ['MOV', None, [[None, 0], [None, 1]], None]),
        (5, ['MOV', None, [[None, 0], [None, 1]], None]),
        (6, ['MOV', None, [[None, 0], [None, 1]], None]),
        (7, ['MOV', None, [[None, 0], [None, 1]], None]),
        (8, ['MOV', None, [[None, 0], [None, 1]], None]),
        (9, ['MOV', None, [[None, 0], [None, 1]], None]),
        (10, ['MOV', None, [[None, 0], [None, 1]], None]),
        (11, ['MOV', None, [[None, 0], [None, 1]], None]),
        (12, ['MOV', None, [[None, 0], [None, 1]], None]),
        (13, ['MOV', None, [[None, 0], [None, 1]], None]),
        (14, ['MOV', None, [[None, 0], [None, 1]], None]),
        (15, ['MOV', None, [[None, 0], [None, 1]], None])]

# Inicjalizujemy bibliotekę curses
stdscr = curses.initscr()

for i, c in enumerate(core):
    if c[0] is not None:
        stdscr.addch(0, i, c[0])
    if c[1] is not None:
        stdscr.addch(1, i, c[1])

stdscr.refresh()

stdscr.getkey()

curses.endwin()