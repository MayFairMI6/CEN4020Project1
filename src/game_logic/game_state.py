#!/usr/bin/env python

import random


class GameState:
    def __init__(self):
        self.level = 1                                      #current level (1 or 2)
        self.board = [[0 for _ in range(5)] for _ in range(5)]  #5x5 inner board
        self.outer_ring = {}                                #outer ring cells for level 2 (dict with (row, col) keys)
        self.current_num = 1                                #next number to place
        self.score = 0                                      #player score
        self.last_pos = None                                #position of last placed number
        self.game_over = False                              #game over flag
        self.win = False                                    #win flag for current level
        #NOTE: move_history is a placeholder for Story 5 (undo feature)
        self.move_history = []
        
    def reset_level1(self):   #reset for a new level 1 game
        self.level = 1
        self.board = [[0 for _ in range(5)] for _ in range(5)]
        self.outer_ring = {}
        self.current_num = 1
        self.score = 0
        self.last_pos = None
        self.game_over = False
        self.win = False
        self.move_history = []
        
    def start_level1_with_random_one(self):   #place number 1 randomly for level 1 start (story 1 requirement)
        self.reset_level1()
        row = random.randint(0, 4)
        col = random.randint(0, 4)
        self.board[row][col] = 1
        self.last_pos = (row, col)
        self.current_num = 2
        
    def start_level2(self, completed_board):   #initialize level 2 with completed level 1 board
        self.level = 2
        self.board = [row[:] for row in completed_board]    #copy the completed board
        self.outer_ring = self._create_empty_ring()         #create empty outer ring
        self.current_num = 2                                #start placing from 2 in outer ring
        self.last_pos = self._find_number_position(1)       #find where 1 is on inner board
        self.game_over = False
        self.win = False
        self.move_history = []                              #reset move history for level 2
        
    def _create_empty_ring(self):   #create empty outer ring dictionary
        ring = {}
        #top row (7 cells: col 0-6, row 0)
        for col in range(7):
            ring[(0, col)] = 0
        #bottom row (7 cells: col 0-6, row 6)
        for col in range(7):
            ring[(6, col)] = 0
        #left column excluding corners (rows 1-5, col 0)
        for row in range(1, 6):
            ring[(row, 0)] = 0
        #right column excluding corners (rows 1-5, col 6)
        for row in range(1, 6):
            ring[(row, 6)] = 0
        return ring
    
    def _find_number_position(self, num):   #find position of a number on the inner board
        for row in range(5):
            for col in range(5):
                if self.board[row][col] == num:
                    return (row, col)
        return None
    
    def get_state_dict(self):   #get state as dictionary for saving
        return {
            'level': self.level,
            'board': self.board,
            'outer_ring': self.outer_ring,
            'current_num': self.current_num,
            'score': self.score,
            'last_pos': self.last_pos,
            'move_history': self.move_history
        }
    
    def set_state_dict(self, state):   #restore state from dictionary
        self.level = state.get('level', 1)
        self.board = state['board']
        self.outer_ring = state.get('outer_ring', {})
        self.current_num = state['current_num']
        self.score = state['score']
        self.last_pos = state['last_pos']
        self.move_history = state.get('move_history', [])
        self.game_over = False
        self.win = False
