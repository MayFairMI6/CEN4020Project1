#!/usr/bin/env python

import pygame
from .colors import *


class BoardRenderer:
    def __init__(self, screen, cell_size=70, board_offset_y=120):
        self.screen = screen
        self.cell_size = cell_size
        self.board_offset_x = 50      #will be recalculated for centering
        self.board_offset_y = board_offset_y
        self.font = None
        self.small_font = None
        self.title_font = None
        
    def init_fonts(self):   #initialize fonts (must be called after pygame.init)
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 32)
        
    def center_board(self, level):
        #calculate board offsets to center the board
        #level 1 board is positioned where the inner board will be in level 2
        window_width = self.screen.get_width()
        window_height = self.screen.get_height()
        board_width_7x7 = 7 * self.cell_size
        board_height_7x7 = 7 * self.cell_size
        
        #vertical centering: between header (60px) and buttons (620px)
        header_end = 60
        buttons_start = 620
        available_height = buttons_start - header_end
        base_offset_y = header_end + (available_height - board_height_7x7) // 2
        
        #horizontal centering
        base_offset_x = (window_width - board_width_7x7) // 2
        
        if level == 1:
            #position level 1 board where inner board will be in level 2
            self.board_offset_x = base_offset_x + self.cell_size
            self.board_offset_y = base_offset_y + self.cell_size
        else:
            #level 2: position the full 7x7 grid centered
            self.board_offset_x = base_offset_x
            self.board_offset_y = base_offset_y
        
    def draw_header_bar(self, score, current_num, level, width):
        #draw header bar with score, next number, and level
        header_height = 60
        
        #draw header background
        header_rect = pygame.Rect(0, 0, width, header_height)
        pygame.draw.rect(self.screen, HEADER_BG, header_rect)
        
        #draw bottom border
        pygame.draw.line(self.screen, GRID_LINE, (0, header_height), (width, header_height), 2)
        
        #score section (left)
        score_label = self.small_font.render("SCORE", True, HEADER_LABEL)
        score_value = self.title_font.render(str(score), True, SCORE_COLOR)
        self.screen.blit(score_label, (30, 12))
        self.screen.blit(score_value, (30, 32))
        
        #next number section (center)
        next_label = self.small_font.render("NEXT NUMBER", True, HEADER_LABEL)
        next_value = self.title_font.render(str(current_num), True, TEXT_DARK)
        self.screen.blit(next_label, (width // 2 - 65, 12))
        self.screen.blit(next_value, (width // 2 - 15, 32))
        
        #level section (right)
        level_label = self.small_font.render("LEVEL", True, HEADER_LABEL)
        level_value = self.title_font.render(str(level), True, LEVEL_COLOR)
        self.screen.blit(level_label, (width - 80, 12))
        self.screen.blit(level_value, (width - 62, 32))
        
    def draw_level1_board(self, board, last_pos=None, hover_cell=None):
        #draw 5x5 board for level 1
        for row in range(5):
            for col in range(5):
                self._draw_cell(row, col, board[row][col], 
                               is_last=(last_pos == (row, col)),
                               is_hover=(hover_cell == (row, col)))
                               
    def draw_level2_board(self, inner_board, outer_ring, hover_cell=None):
        #draw 7x7 board for level 2 (inner board + outer ring)
        
        #draw outer ring cells first
        for pos, value in outer_ring.items():
            ring_row, ring_col = pos
            is_hover = hover_cell == pos
            is_corner = self._is_corner_cell(ring_row, ring_col)
            self._draw_ring_cell(ring_row, ring_col, value, is_hover, is_corner)
            
        #draw inner 5x5 board (offset by 1 in the 7x7 grid)
        for row in range(5):
            for col in range(5):
                self._draw_inner_cell_level2(row, col, inner_board[row][col])
                
    def _draw_cell(self, row, col, value, is_last=False, is_hover=False):
        #calculate cell position
        x = self.board_offset_x + col * self.cell_size
        y = self.board_offset_y + row * self.cell_size
        rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        
        #determine cell color
        if is_hover and value == 0:
            color = CELL_HOVER
        elif is_last:
            color = CELL_LAST
        elif value != 0:
            color = CELL_FILLED
        else:
            color = CELL_EMPTY
            
        #draw cell background
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, GRID_LINE, rect, 2)
        
        #draw number if cell is filled (blue text for inner board)
        if value != 0:
            text = self.font.render(str(value), True, TEXT_BLUE)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
            
    def _is_corner_cell(self, ring_row, ring_col):
        #check if cell is a corner of the 7x7 grid
        corners = [(0, 0), (0, 6), (6, 0), (6, 6)]
        return (ring_row, ring_col) in corners
        
    def _draw_ring_cell(self, ring_row, ring_col, value, is_hover=False, is_corner=False):
        #calculate position in 7x7 grid
        x = self.board_offset_x + ring_col * self.cell_size
        y = self.board_offset_y + ring_row * self.cell_size
        rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        
        #determine cell color
        if is_hover and value == 0:
            color = CELL_HOVER
        elif is_corner:
            color = RING_CORNER   #yellow corners
        elif value != 0:
            color = RING_CELL_FILLED
        else:
            color = RING_CELL_EMPTY
            
        #draw cell background
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, GRID_LINE, rect, 2)
        
        #draw number if cell is filled
        if value != 0:
            text = self.font.render(str(value), True, TEXT_DARK)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
            
    def _draw_inner_cell_level2(self, inner_row, inner_col, value):
        #inner board is offset by 1 in 7x7 grid
        grid_row = inner_row + 1
        grid_col = inner_col + 1
        
        x = self.board_offset_x + grid_col * self.cell_size
        y = self.board_offset_y + grid_row * self.cell_size
        rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        
        #inner board cells are locked in level 2
        pygame.draw.rect(self.screen, INNER_BOARD_LOCKED, rect)
        pygame.draw.rect(self.screen, GRID_LINE, rect, 2)
        
        #draw number (blue text for inner board)
        if value != 0:
            text = self.font.render(str(value), True, TEXT_BLUE)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
            
    def get_cell_at_pos(self, mouse_x, mouse_y, level=1):
        #convert mouse position to board cell coordinates
        if level == 1:
            grid_size = 5
        else:
            grid_size = 7
            
        col = (mouse_x - self.board_offset_x) // self.cell_size
        row = (mouse_y - self.board_offset_y) // self.cell_size
        
        if 0 <= row < grid_size and 0 <= col < grid_size:
            return (int(row), int(col))
        return None
        
    def draw_score(self, score, x=50, y=50):
        #draw score display
        text = self.font.render("Score: %d" % score, True, TEXT_DARK)
        self.screen.blit(text, (x, y))
        
    def draw_next_number(self, num, x=250, y=50):
        #draw next number indicator
        text = self.font.render("Next: %d" % num, True, TEXT_DARK)
        self.screen.blit(text, (x, y))
        
    def draw_level_indicator(self, level, x=400, y=50):
        #draw current level
        text = self.font.render("Level %d" % level, True, TEXT_DARK)
        self.screen.blit(text, (x, y))
        
    def draw_message(self, msg, y=None):
        #draw message between board and buttons
        if y is None:
            y = self.screen.get_height() - 115   #position above buttons
        text = self.font.render(msg, True, TEXT_DARK)
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, y))
        self.screen.blit(text, text_rect)
