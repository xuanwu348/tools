import random
import curses
from itertools import chain

class Action(object):
    UP = 'up'
    LEFT = 'left'
    DOWN = 'down'
    RIGHT = 'right'
    RESTART = 'restart'
    EXIT = 'exit'
  
    letter_codes = [ord[ch] for ch in 'WASDRQwasdrq']
    actions = [UP, LEFT, DOWN, RIGHT, RESTART, EXIT]
    actions_dict = dict(zip(letter_codes, actions * 2))
    
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def get(self):
        char = "N"
        while char not in self.actions_dict:
            char = stdscr.getch()
        return self.actions_dict[char]

class Grid(object):
    def __init__(self, size):
        

