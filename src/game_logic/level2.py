#!/usr/bin/env python


class Level2Logic:
    def __init__(self, game_state):
        self.state = game_state   #reference to shared game state
        
    def _get_inner_board_position(self, num):   #find position of number on inner 5x5 board
        for row in range(5):
            for col in range(5):
                if self.state.board[row][col] == num:
                    return (row, col)
        return None
    
    def _inner_to_outer_coords(self, inner_row, inner_col):   #convert inner board coords to outer 7x7 coords
        #inner board is offset by 1 in the 7x7 grid
        return (inner_row + 1, inner_col + 1)
    
    def _is_on_main_diagonal(self, row, col):   #check if position is on main diagonal (top-left to bottom-right)
        return row == col
    
    def _is_on_anti_diagonal(self, row, col):   #check if position is on anti-diagonal (top-right to bottom-left)
        return row + col == 4
    
    def get_valid_ring_cells(self, num):   #get valid outer ring cells for placing a number
        #find where this number is on the inner board
        inner_pos = self._get_inner_board_position(num)
        if inner_pos is None:
            return []
        
        inner_row, inner_col = inner_pos
        valid_cells = []
        
        #row ends - can place at left or right edge of this row
        #in 7x7 coords: row is inner_row + 1, cols are 0 and 6
        left_cell = (inner_row + 1, 0)
        right_cell = (inner_row + 1, 6)
        
        if self._is_ring_cell_empty(left_cell):
            valid_cells.append(left_cell)
        if self._is_ring_cell_empty(right_cell):
            valid_cells.append(right_cell)
            
        #column ends - can place at top or bottom edge of this column
        #in 7x7 coords: col is inner_col + 1, rows are 0 and 6
        top_cell = (0, inner_col + 1)
        bottom_cell = (6, inner_col + 1)
        
        if self._is_ring_cell_empty(top_cell):
            valid_cells.append(top_cell)
        if self._is_ring_cell_empty(bottom_cell):
            valid_cells.append(bottom_cell)
            
        #diagonal corners (if on main or anti diagonal)
        if self._is_on_main_diagonal(inner_row, inner_col):
            #main diagonal corners: (0,0) and (6,6)
            if self._is_ring_cell_empty((0, 0)):
                valid_cells.append((0, 0))
            if self._is_ring_cell_empty((6, 6)):
                valid_cells.append((6, 6))
                
        if self._is_on_anti_diagonal(inner_row, inner_col):
            #anti-diagonal corners: (0,6) and (6,0)
            if self._is_ring_cell_empty((0, 6)):
                valid_cells.append((0, 6))
            if self._is_ring_cell_empty((6, 0)):
                valid_cells.append((6, 0))
                
        return valid_cells
    
    def _is_ring_cell_empty(self, pos):   #check if a ring cell is empty
        return pos in self.state.outer_ring and self.state.outer_ring[pos] == 0
    
    def is_valid_move(self, ring_row, ring_col):   #check if placing current number at ring position is valid
        pos = (ring_row, ring_col)
        
        #check if it's a ring cell
        if pos not in self.state.outer_ring:
            return (False, "not_ring_cell")
        
        #check if cell is empty
        if self.state.outer_ring[pos] != 0:
            return (False, "cell_occupied")
        
        #check if this is a valid cell for the current number
        valid_cells = self.get_valid_ring_cells(self.state.current_num)
        if pos in valid_cells:
            return (True, None)
        
        return (False, "invalid_position")
    
    def place_number(self, ring_row, ring_col):   #place the current number in the outer ring
        valid, error = self.is_valid_move(ring_row, ring_col)
        if not valid:
            return (False, error)
        
        pos = (ring_row, ring_col)
        
        #place the number in the ring
        self.state.outer_ring[pos] = self.state.current_num
        
        #update state
        self.state.last_pos = pos
        self.state.move_history.record_outer_action(self.state.current_num - 1, pos)
        self.state.current_num += 1
        
        #check win condition (all 24 cells filled = numbers 2-25 placed)
        if self.state.current_num > 25:
            self.state.win = True
            
        return (True, None)
    
    def has_valid_moves(self):   #check if there are any valid moves for current number
        return len(self.get_valid_ring_cells(self.state.current_num)) > 0
    
    def get_ring_cell_positions(self):   #get all ring cell positions for rendering
        return list(self.state.outer_ring.keys())
