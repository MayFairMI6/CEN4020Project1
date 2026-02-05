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
        self.original_one_pos = None                        #original position of "1" for clear functionality
        self.game_over = False                              #game over flag
        self.win = False
        self.move_history = History()
    
    def reset_level1(self):   #reset for a new level 1 game (keeps "1" in original position per story 4)
        self.level = 1
        self.board = [[0 for _ in range(5)] for _ in range(5)]
        self.outer_ring = {}
        self.score = 0
        self.game_over = False
        self.win = False
        self.move_history.clear_history()
        
        #restore "1" to its original position (story 4 requirement)
        if self.original_one_pos:
            row, col = self.original_one_pos
            self.board[row][col] = 1
            self.last_pos = self.original_one_pos
            self.move_history.record_action_lv1(row, col, False)
            self.current_num = 2
        else:
            self.current_num = 1
            self.last_pos = None
        
    def start_level1_with_random_one(self):   #place number 1 randomly for level 1 start (story 1 requirement)
        self.level = 1
        self.board = [[0 for _ in range(5)] for _ in range(5)]
        self.outer_ring = {}
        self.score = 0
        self.game_over = False
        self.win = False
        self.move_history.clear_history()
        
        #place "1" randomly and save original position
        row = random.randint(0, 4)
        col = random.randint(0, 4)
        self.board[row][col] = 1
        self.last_pos = (row, col)
        self.original_one_pos = (row, col)   #save for clear functionality (story 4)
        self.move_history.record_action_lv1(row, col, False)
        self.current_num = 2
        
    def start_level2(self, completed_board):   #initialize level 2 with completed level 1 board
        self.level = 2
        self.board = [row[:] for row in completed_board]    #copy the completed board
        self.outer_ring = self._create_empty_ring()         #create empty outer ring
        self.current_num = 2                                #start placing from 2 in outer ring
        self.last_pos = self._find_number_position(1)       #find where 1 is on inner board
        self.game_over = False
        self.win = False
        
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
        self.move_history = state['board_history']
        self.game_over = False
        self.win = False
    
    def undo(self):
        #In lv 1 I can just pop from the array
        if self.level == 1:
            last_action = self.move_history.undo_history()
            penult_action = self.move_history.get_action(-1)
            
            self.board[last_action.inner_pos_x][last_action.inner_pos_y] = 0
            self.current_num -= 1
            self.last_pos = (penult_action.inner_pos_x, penult_action.inner_pos_y)
            
            if last_action.scored:
                self.score -= 1
            
        #In lv 2 I gotta pay attention to current num
        elif self.current_num > 2:
            #Current number is ahead of it's previous action by 1
            #Accounting for array starting at 0, previous action is current num - 2
            last_action = self.move_history.get_action(self.current_num - 2)
            penult_action = self.move_history.get_action(self.current_num - 3)
            
            self.outer_ring[last_action.outer_pos] = 0
            last_action.edit_outer_pos((-1, -1))
            self.current_num -= 1
            self.last_pos = (penult_action.inner_pos_x, penult_action.inner_pos_y)
    
    def reset_lv2(self):
        for i in range(self.current_num - 1):
            self.undo()
            
class History:
    def __init__(self):
        self.arr = []
    
    def record_action_lv1(self, x, y, scored):
        new_action = Action()
        new_action.record_lv1(x, y, scored)
        self.arr.append(new_action)
    
    def record_outer_action(self, index, outer):
        self.arr[index].edit_outer_pos(outer)

    def get_action(self, index):
        return self.arr[index]

    def undo_history(self):
        return self.arr.pop()

    def clear_history(self):
        self.arr = []
    
    def print_history(self):
        print("------------------------------")
        for i in range(len(self.arr)):
            print(i, ": ", self.get_action(i).action_log())
        print("------------------------------")

class Action:
    def __init__(self):
        self.inner_pos_x = -1
        self.inner_pos_y = -1
        self.outer_pos = (-1, -1)
        self.scored = False

    def record_lv1(self, x, y, scored = False):
        self.inner_pos_x = x
        self.inner_pos_y = y
        self.scored = scored

    def edit_outer_pos(self, outer_pos):
        self.outer_pos = outer_pos

    def action_log(self):
        text = "".join(str("Position (%d, %d)" % (self.inner_pos_x, self.inner_pos_y)))
        
        if self.scored:
            text += " Scored a point!"
        if self.outer_pos != (-1, -1):
            text += str(" Outer Ring Position: (%d, %d)" % (self.outer_pos))
        
        return text
