#!/usr/bin/env python3
from __future__ import division
import copy
import os
import random
import time
from asciimatics.effects import Cycle, Stars, Print
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen


# print welcome screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    text = r"""
______  ___ _____ _____ _      _____ _____ _   _ ___________ 
| ___ \/ _ \_   _|_   _| |    |  ___/  ___| | | |_   _| ___ \
| |_/ / /_\ \| |   | | | |    | |__ \ `--.| |_| | | | | |_/ /
| ___ \  _  || |   | | | |    |  __| `--. \  _  | | | |  __/ 
| |_/ / | | || |   | | | |____| |___/\__/ / | | |_| |_| |    
\____/\_| |_/\_/   \_/ \_____/\____/\____/\_| |_/\___/\_|    
                                                             

"""
    print(text)


# initialize 10*10 board with all False
def init_board(initial_value):
    board = []
    for i in range(10):
        row = []
        for j in range(10):
            row.append(initial_value)
        board.append(row)
    return board


# make a visual representation of board
def print_board(board):
    print('    0  1  2  3  4  5  6  7  8  9')
    print(33*'-')
    # type of board. True=ships, False=hit/miss
    board_type = isinstance(board[0][0], bool)
    for i in range(10):
        print(i, end=' | ')
        for j in range(10):
            # ships board
            if board_type:
                if board[i][j]:
                    print('X', end='  ')
                else:
                    print(' ', end='  ')
            # hit/miss board
            else:
                print(board[i][j], end='  ')
        print()


# count number of 'item' in 2d array
def count_occurances(board, item):
    count = 0
    for row in board:
        for pos in row:
            if pos == item:
                count += 1
    return count


# place a ship on board.
# params: row, col, length, direction (h or v)
def place_ship(board, row, col, length, direction):
    # copy original board
    new_board = copy.deepcopy(board)
    # number of ships expected
    expected = 0
    for c in range(length, 6):
        expected += c
    for i in range(length):
        # put ship on board
        if direction == 'h':
            new_board[col][row+i] = True
        elif direction == 'v':
            new_board[col+i][row] = True
    if expected == count_occurances(new_board, True):
        return new_board
    else:
        return None


def gen_computer_board():
    board = init_board(False)
    # start with ship w/ length 5
    length = 5
    while length > 1:
        # determine largest possible starting coordinate
        end_row = len(board[0]) - length
        end_col = len(board) - length
        # random starting position and direction
        r = random.randint(0, end_row)
        c = random.randint(0, end_col)
        d = random.choice(['h', 'v'])
        # place ship
        temp_board = place_ship(board, r, c, length, d)
        # save and move onto smaller ships if legal
        if temp_board:
            board = temp_board
            length -= 1
    return board


def make_player_board():
    # return (r,c,d) if legal, None otherwise
    def process_input(row, col, max_row, max_col, direction):
        # check if direction is correct
        if direction not in ['h', 'v']:
            return None
        # check if row and col are integers and within range
        try:
            row = int(row)
            col = int(col)
            if 0 <= row <= max_row and 0 <= col <= max_col:
                return (row, col, direction)
        except ValueError:
            return None

    board = init_board(False)
    length = 5
    while length > 1:
        clear_screen()
        print_board(board)
        print('\nPlacing a ship with length', length, '\n')
        # determine largest possible starting coordinate
        end_row = len(board[0]) - length
        end_col = len(board) - length
        # random starting position and direction
        r = input(f'Enter X coordinate (0-{end_row}): ')
        c = input(f'Enter Y coordinate (0-{end_col}): ')
        d = input(f'Enter direction (h or v): ')
        # check input
        try:
            r, c, d = process_input(r, c, end_row, end_col, d)
        except TypeError:
            print('Input invalid! Try again')
            time.sleep(1)
            continue
        # place ship
        temp_board = place_ship(board, r, c, length, d)
        # save and move onto smaller ships if legal
        if temp_board:
            board = temp_board
            length -= 1
        else:
            print('Overlap detected! Try again')
            time.sleep(1)
            continue
    return board


def hit(row, col, ships, board):
    # if there's a ship at [row][col], write 'H'
    if ships[col][row]:
        board[col][row] = 'H'
    # write 'M' otherwise
    else:
        board[col][row] = 'M'
    return board


# returns (bool:computer win, bool:player win)
def check_win():
    # count hits
    player_hits = 0
    computer_hits = 0
    for row in player_board:
        player_hits += row.count('H')
    for row in computer_board:
        computer_hits += row.count('H')
    # win when hits = 14
    player_win = player_hits == 14
    computer_win = computer_hits == 14
    return (player_win, computer_win)


# win/lose animation
def win_animation(screen):
    effects = [
        Cycle(
            screen,
            FigletText("YOU", font='big'),
            int(screen.height / 2 - 8)),
        Cycle(
            screen,
            FigletText("WON", font='big'),
            int(screen.height / 2 + 3)),
        Stars(screen, 200)
    ]
    screen.play([Scene(effects, 500)])


def lose_animation(screen):
    effects = [
        Print(screen, FigletText("YOU", font='big'),
              y=screen.height // 2 - 8),
        Print(screen, FigletText("LOST", font='big'),
              y=screen.height // 2 + 3),
    ]
    screen.play([Scene(effects, -1)], stop_on_resize=True)


if __name__ == '__main__':
    # ask player to place ships
    player_ships = make_player_board()
    # place ships for computer player
    computer_ships = gen_computer_board()

    # generate boards
    player_board = init_board(' ')
    computer_board = init_board(' ')

    player_win, computer_win = False, False

    # actual game logic
    while not player_win and not computer_win:
        clear_screen()
        print('Your ships:')
        print_board(player_ships)
        print('\n Computer:')
        print_board(computer_board)
        print('\n You:')
        print_board(player_board)
        # ask for where to hit
        hit_r = input('Enter X coordinate to hit (0-9): ')
        hit_c = input('Enter Y coordinate to hit (0-9): ')    
        try:
            if hit_r == 'I\'m so proud of this community.':
                clear_screen()
                print_board(computer_ships)
                time.sleep(1)
                continue
            elif hit_c == '4x Duke All-American':
                clear_screen()
                print('\nAre you winning at social?')
                time.sleep(2)
                continue
            hit_r = int(hit_r)
            hit_c = int(hit_c)
            assert(0 <= hit_r <= 10 and 0 <= hit_c <= 10)
        except (AssertionError, ValueError):
            clear_screen()
            print_board(player_board)
            continue
        # make hit
        if player_board[hit_c][hit_r] == ' ':
            hit(hit_r, hit_c, computer_ships, player_board)
        else:
            clear_screen()
            print_board(player_board)
            continue
        # computer randomly hit
        computer_r = random.randint(0,9)
        computer_c = random.randint(0,9)
        hit(computer_r, computer_c, player_ships, computer_board)
        # check for winning
        player_win, computer_win = check_win()

    # show win/lose message, end game
    if player_win:
        Screen.wrapper(win_animation)
    elif computer_win:
        Screen.wrapper(lose_animation)
