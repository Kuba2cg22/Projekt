import curses
import time

lista = [1,2,3,4,5,6,7]

screen = curses.initscr()
curses.start_color()
curses.use_default_colors()
curses.init_pair(1, curses.COLOR_RED, -1)
screen.clear()

for x in range(19):
    lista.append(x)
    screen.addstr(str(lista).encode('ascii', 'ignore') + '\n')
    screen.refresh()
    time.sleep(1)

curses.endwin()

