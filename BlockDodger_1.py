#Used AI to help me fix bugs and learn ways to make code compatible with Windows and Mac/Linux/Unix. Most of the code and idea for this game was made by me.

import numpy as np
import os
import sys
import time
import random
import threading

current_move = None

def native_mac_keyboard_listener():
    global current_move
    import tty
    import termios
    fd = sys.stdin.fileno()
    while True:
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            key = sys.stdin.read(1).lower()
            if key in ['a', 'd', 'y', 'n']:
                current_move = key
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

if sys.platform != "win32":
    listener_thread = threading.Thread(target = native_mac_keyboard_listener, daemon = True)
    listener_thread.start()

def check_windows_input():
    global current_move
    if sys.platform == "win32":
        import msvcrt
        if msvcrt.kbhit():
            current_move = msvcrt.getch().decode('utf-8').lower()

grid_size = 10
board_x = 5
board_y = 9

fall_obj_x = random.randint(0, 9)
fall_obj_y = 0

grid = np.zeros((grid_size, grid_size))

start_time = time.time()
last_fall_time = time.time()
fall_delay = 0.25

while True:
    elapsed_time = time.time() - start_time
    if elapsed_time > 60:
        print("You won!")
        break
    elif elapsed_time > 40:
        fall_delay = 0.05
    elif elapsed_time > 20:
        fall_delay = 0.15
    else:
        fall_delay = 0.25

    grid[board_y, board_x] = 1
    grid[fall_obj_y, fall_obj_x] = 2
    os.system('clear' if os.name != 'nt' else 'cls')

    for row in grid:
        row_string = ""
        for cell in row:
            if cell == 2:
                row_string += "\033[41m  \033[0m"
            elif cell == 1:
                row_string += "\033[44m  \033[0m"
            elif cell == 0:
                row_string += "・"
        print(row_string)

    grid[board_y, board_x] = 0
    grid[fall_obj_y, fall_obj_x] = 0

    if time.time() - last_fall_time > fall_delay:
        fall_obj_y += 1
        last_fall_time = time.time()

        if fall_obj_y >= grid_size:
            fall_obj_y = 0
            fall_obj_x = random.randint(0, 9)

    if board_y == fall_obj_y and board_x == fall_obj_x:
        grid[board_y, board_x] = 0
        fall_obj_x, fall_obj_y = board_x, board_y
        grid[fall_obj_y, fall_obj_x] = 2

        os.system('clear' if os.name != 'nt' else 'cls')
        for row in grid:
            row_string = ""
            for cell in row:
                if cell == 2:
                    row_string += "\033[41m  \033[0m"
                elif cell == 1:
                    row_string += "\033[44m  \033[0m"
                elif cell == 0:
                    row_string += "・"
            print(row_string)

        print("\nGame Over")
        print("\nContinue? (Y/N): ")

        current_move = None

        while True:
            if sys.platform == "win32":
                check_windows_input()

            if current_move == 'y':
                break
            elif current_move == 'n':
                print("Bye")
                sys.exit()

            time.sleep(0.05)

        grid.fill(0)

        board_x = 5
        board_y = 9
        fall_obj_x = random.randint(0, 9)
        fall_obj_y = 0
        start_time = time.time()
        last_fall_time = time.time()
        current_move = None
        continue

    if sys.platform == "win32":
        check_windows_input()

    if current_move == 'a':
        board_x -= 1
    elif current_move == 'd':
        board_x += 1

    current_move = None

    if board_x > 9:
        board_x = 9
    elif board_x < 0:
        board_x = 0
    
    time.sleep(0.05)
