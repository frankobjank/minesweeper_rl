import random
import time
from pyray import *
from collections import deque
from datetime import date
from enum import Enum

# path to Python interpreter for pylance to recognize raylib/pyray
# /Users/jacobfrank/sources/minesweeper_rl/.venv/bin/python3

# Ideas from Google game:
    # make it so that you start on an empty square:
        # first selection is made
            # should not be able to flag until first move is made
        # create mines where each mine is at least 2 squares away from first selection
    
    # animate mines appearing when you die
        # could be annoying without the first fix though since it would happen too often




# game board constants
def initialize_board(difficulty):
    # width, height, num_mines
    if difficulty == "easy":
        w, h, num_mines = 10, 10, 10
    if difficulty == "medium":
        w, h, num_mines = 16, 16, 40
    if difficulty == "hard":
        w, h, num_mines = 30, 16, 99

    block = 30
    header_height=block*2
    screen_width=block*w
    screen_height=block*h+header_height

    board = {(x, y): Rectangle(x, y, block, block) for y in range(header_height, screen_height, block) for x in range(0, screen_width, block)}

    return screen_width, screen_height



set_target_fps(60)
display_menu = True

def menu_window(window_pointer):
    screen_width = 300
    screen_height = 360
    init_window(screen_width, screen_height, "Menu")
    while not window_should_close():
        # set constants
        selection = None
        mouse = get_mouse_position()
        button_len = 100
        easy = {"Easy": Rectangle((screen_width-button_len)//2, 90, button_len, 50)}
        medium = {"Medium": Rectangle((screen_width-button_len)//2, 150, button_len, 50)}
        hard = {"Hard": Rectangle((screen_width-button_len)//2, 220, button_len, 50)}
        exit = {"Exit": Rectangle((screen_width-button_len)//2, 300, button_len, 50)}
        buttons = [easy, medium, hard, exit]
        # get user input
        if is_mouse_button_released(MouseButton.MOUSE_BUTTON_LEFT):
            for button in buttons:
                for name, rec in button.items():
                    if check_collision_point_rec(mouse, rec):
                        window_pointer = name
                        break
        
        # render
        begin_drawing()
        clear_background(LIME)
        
        draw_text("Minesweeper", 0, 10, 50, BLACK)
        for button in buttons:
            for name, rec in button.items():
                draw_rectangle_rec(rec, GRAY)
                draw_text(name, int(rec.x), int(rec.y), 30, BLACK)

        # draw_rectangle_rec(easy_button, GRAY)
        # draw_text("Easy", int(easy_button.x), int(easy_button.y), 30, BLACK)
        # draw_rectangle_rec(medium_button, GRAY)
        # draw_text("Medium", int(medium_button.x), int(medium_button.y), 30, BLACK)
        # draw_rectangle_rec(hard_button, GRAY)
        # draw_text("Hard", int(hard_button.x), int(hard_button.y), 30, BLACK)
        # draw_rectangle_rec(exit_button, GRAY)
        # draw_text("Exit", int(exit_button.x), int(exit_button.y), 30, BLACK)

        end_drawing()
    print("closing window")
    close_window()

    return window_pointer


def color_window(window_pointer, color1, color2):
    init_window(300, 300, "color") # f"Minesweeper {difficulty}")

    while not window_should_close():
        mouse = get_mouse_position()
        button_top = Rectangle(0, 0, 300, 100)
        begin_drawing()
        clear_background(color2)
        draw_rectangle_rec(button_top, color1)

        if check_collision_point_rec(mouse, button_top):
            draw_rectangle_rec(button_top, GRAY)
            if is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT):
                window_pointer = "display_menu"
                break
        end_drawing()
    print("returning to menu")
    close_window()
    return window_pointer


def window_test(window_pointer):
    window_pointer = menu_window(window_pointer)
    if window_pointer == "green":
        window_pointer = color_window(window_pointer, GREEN, BLUE)
    elif window_pointer == "red":
        window_pointer = color_window(window_pointer, RED, BLACK)
    elif window_pointer == "exit":
        return
    

    if window_pointer == "display_menu":
        window_pointer = window_test(window_pointer)
    else:
        return


window_pointer = "display_menu"
# window_test(window_pointer)
# menu_window(window_pointer)

# I believe the issue of checking box twice has been resolved
# def code_test(x, y):
#     already_checked = set()
#     i = 1
#     already_checked.add((x, y))
#     to_reveal = []
#     while len(already_checked) < (screen_width//block*(screen_height-header_height)//block-1):
#         print(already_checked)
#         r = range(-i*block, i*block+1, block)
#         wholesquare = set((x+dx, y+dy) for dy in r for dx in r if (x+dx, y+dy) not in already_checked and 0<=x+dx<screen_width and header_height<=y+dy<screen_height)

#         outline = wholesquare.difference(already_checked)
#         already_checked = already_checked.union(outline)
#         for sq in outline:
#             to_reveal.append(sq)
#         i += 1



# Old non-recursive reveal
# def get_adjacent_not_recursive(self, state):
#     # could create sets for adj_to_mines and empty_squares
#     # so it's easier to know which squares should be revealed
#     # do pathfinder to get all empty squares connected to the self
#     # reveal all adjecents to empty_squares to get the adj_to_mines visible as well
#     state.to_reveal.appendleft(self)
#     i = 1
#     already_checked = set()
#     already_checked.add((self.x, self.y))
#     while len(already_checked) < (screen_width//block*(screen_height-header_height)//block-1):
#         r = range(-i*block, i*block+1, block)
#         whole_square = set(state.board[(self.x+dx, self.y+dy)] for dy in r for dx in r if (self.x+dx, self.y+dy) not in already_checked and 0<=self.x+dx<screen_width and header_height<=self.y+dy<screen_height)

#         outline = set(whole_square).difference(already_checked)
#         empty_squares = set()
#         for sq in outline:
#             if sq.adj > 0:
#                 continue
#             else:
#                 empty_squares.add(sq)
#         already_checked = already_checked.union(outline)
#         for sq in empty_squares:
#             state.to_reveal.appendleft(sq)
#         i += 1
