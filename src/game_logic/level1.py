#!/usr/bin/env python


class Level1Logic:
    def __init__(self, game_state):
        self.state = game_state   #reference to shared game state
        
    def is_valid_move(self, row, col):   #check if a move is valid
        #check bounds
        if row < 0 or row > 4 or col < 0 or col > 4:
            return (False, "out_of_bounds")
        #check if cell is empty
        if self.state.board[row][col] != 0:
            return (False, "cell_occupied")
        #first move can be anywhere (but in GUI, 1 is pre-placed)
        if self.state.current_num == 1:
            return (True, None)
        #check if one step away from last position
        last_row, last_col = self.state.last_pos
        row_diff = abs(row - last_row)
        col_diff = abs(col - last_col)
        if row_diff <= 1 and col_diff <= 1 and (row_diff + col_diff) > 0:
            return (True, None)
        return (False, "not_adjacent")
    
    def is_diagonal_move(self, row, col):   #check if move is diagonal from last position
        if self.state.last_pos is None:
            return False
        last_row, last_col = self.state.last_pos
        row_diff = abs(row - last_row)
        col_diff = abs(col - last_col)
        return row_diff == 1 and col_diff == 1
    
    def get_valid_cells(self):   #get list of all valid cells for current move
        valid = []
        for row in range(5):
            for col in range(5):
                is_valid, _ = self.is_valid_move(row, col)
                if is_valid:
                    valid.append((row, col))
        return valid
    
    def place_number(self, row, col):   #place the current number at the given position
        valid, error = self.is_valid_move(row, col)
        if not valid:
            return (False, error)
        
        scored = self.is_diagonal_move(row, col)
        #add score for diagonal moves
        if scored:
            self.state.score += 1
        
        #place the number
        self.state.board[row][col] = self.state.current_num
        
        #update state
        self.state.last_pos = (row, col)
        self.state.current_num += 1
        self.state.move_history.record_action_lv1(row, col, scored)
        
        #check win condition
        if self.state.current_num > 25:
            self.state.win = True
            
        return (True, None)
    
    def has_valid_moves(self):   #check if there are any valid moves left
        return len(self.get_valid_cells()) > 0
