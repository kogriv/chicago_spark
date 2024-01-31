import curses
import time

def main(stdscr):
    # Инициализация библиотеки curses
    curses.curs_set(0)
    stdscr.nodelay(1)

    # Портрет
    portrait = [
        "          ____",
        "        o8%8888,",
        "      o88%8888888.",
        "     8'-    -:8888b",
        "    8'         8888",
        "   d8.-=.  ==-.:888b",
        "   >8 '~'  '~'  d8888",
        "   88      \    ,88888",
        "   88b.  -~   ':88888",
        "   888b ~==~ .:88888",
        "   88888o--:':::8888",
        "   88888| :::' 8888b",
        "   8888^^'       8888b",
        "  d888           ,%888b.",
        " d88%            %%%8--'-.",
        "/88:.__ ,       _%-' ---  -",
        "    '''::===..-'   =  --."
    ]

    # Цикл анимации
    while True:
        stdscr.clear()  # Очистка экрана

        # Получение размеров окна терминала
        max_y, max_x = stdscr.getmaxyx()

        # Отображение портрета
        for y, line in enumerate(portrait):
            if y < max_y:
                stdscr.addstr(y, 0, line[:max_x])  # Выводим только то, что влазит по горизонтали

        # Моргание глаз
        portrait[6] = "   >8 '~'  '~'  d8888" \
            if time.time() % 2 > 1 else "   >8 \..  './  d8888"

        stdscr.refresh()  # Обновление экрана
        time.sleep(0.5)   # Задержка для анимации

        # Проверка нажатия клавиши для выхода
        if stdscr.getch() == ord('q'):
            return

if __name__ == "__main__":
    curses.wrapper(main)