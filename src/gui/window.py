#!/usr/bin/env python

import pygame
import sys
from .board_renderer import BoardRenderer
from .colors import *

#sound effects for User Story 2 and 6
pygame.mixer.init(44100, -16, 2, 2048)

valid_sound = pygame.mixer.Sound("Sprint1Story2.wav")
invalid_sound = pygame.mixer.Sound("Sprint1Story6.wav")


class Button:
    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.is_hovered = False
        
    def draw(self, screen):
        #determine button color
        if self.is_hovered:
            color = BUTTON_HOVER
        else:
            color = BUTTON_NORMAL
            
        #draw button
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 2, border_radius=5)
        
        #draw text
        text_surface = self.font.render(self.text, True, BUTTON_TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
        
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class GameWindow:
    def __init__(self, width=600, height=700):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Matrix Game - Level 1")
        self.clock = pygame.time.Clock()
        self.running = True
        
        #initialize renderer
        self.renderer = BoardRenderer(self.screen)
        self.renderer.init_fonts()
        
        #fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        
        #game state references (set by main.py)
        self.game_state = None
        self.level1_logic = None
        self.level2_logic = None
        
        #UI state
        self.hover_cell = None
        self.message = ""
        self.message_timer = 0
        
        #create buttons
        self._create_buttons()
        
    def _create_buttons(self):
        #buttons at bottom of screen
        btn_y = 600
        btn_width = 80
        btn_height = 35
        
        self.btn_quit = Button(50, btn_y, btn_width, btn_height, "Quit", self.small_font)
        self.btn_undo = Button(160, btn_y, btn_width, btn_height, "Undo", self.small_font)
        self.btn_clear = Button(270, btn_y, btn_width, btn_height, "Clear", self.small_font)
        
        self.buttons = [self.btn_quit, self.btn_undo, self.btn_clear]
        
    def set_game_components(self, game_state, level1_logic, level2_logic):
        #set game components from main
        self.game_state = game_state
        self.level1_logic = level1_logic
        self.level2_logic = level2_logic
        
    def show_message(self, msg, duration=2000):
        #display a temporary message
        self.message = msg
        self.message_timer = pygame.time.get_ticks() + duration
        
    def run(self):
        #main game loop
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(60)
            
        pygame.quit()
        sys.exit()
        
    def _handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        #update hover state for buttons
        for btn in self.buttons:
            btn.check_hover(mouse_pos)
            
        #update hover cell
        if self.game_state.level == 1:
            self.hover_cell = self.renderer.get_cell_at_pos(mouse_pos[0], mouse_pos[1], level=1)
        else:
            self.hover_cell = self.renderer.get_cell_at_pos(mouse_pos[0], mouse_pos[1], level=2)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:   #left click
                    self._handle_click(mouse_pos)
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
    def _handle_click(self, mouse_pos):
        #check button clicks
        if self.btn_quit.is_clicked(mouse_pos):
            self.running = False
            return
        
        #Should add undo functionality for lv1 by Sunday
        if self.btn_undo.is_clicked(mouse_pos) and self.game_state.current_num != 1:
            self.game_state.undo()
        
        #Will add clear functionality here later
        if self.btn_clear.is_clicked(mouse_pos):
            pass
        
        #check board click
        if self.game_state.win:
            return   #don't accept clicks if level is won (transition happens automatically)
            
        if self.game_state.level == 1:
            cell = self.renderer.get_cell_at_pos(mouse_pos[0], mouse_pos[1], level=1)
            if cell:
                self._handle_level1_click(cell)
        else:
            cell = self.renderer.get_cell_at_pos(mouse_pos[0], mouse_pos[1], level=2)
            if cell:
                self._handle_level2_click(cell)
                
    def _handle_level1_click(self, cell):
        row, col = cell
        success, error = self.level1_logic.place_number(row, col)
        
        if success:
            #placeholder for sound (story 2)
            valid_sound.play()
        else:
            #placeholder for error sound (story 6)
            if error == "out_of_bounds":
                self.show_message("Cell is out of bounds!")
                invalid_sound.play()
            elif error == "cell_occupied":
                self.show_message("Cell is already occupied!")
                invalid_sound.play()
            elif error == "not_adjacent":
                self.show_message("Must be adjacent to previous number!")
                invalid_sound.play()
                
    def _handle_level2_click(self, cell):
        ring_row, ring_col = cell
        
        #check if clicking on inner board (not allowed in level 2)
        if 1 <= ring_row <= 5 and 1 <= ring_col <= 5:
            self.show_message("Inner board is locked in Level 2!")
            return
            
        success, error = self.level2_logic.place_number(ring_row, ring_col)
        
        if success:
            #placeholder for sound (story 2)
            valid_sound.play()
        else:
            #placeholder for error sound (story 6)
            if error == "not_ring_cell":
                self.show_message("Click on the outer ring!")
                invalid_sound.play()
            elif error == "cell_occupied":
                self.show_message("Cell is already occupied!")
                invalid_sound.play()
            elif error == "invalid_position":
                self.show_message("Invalid position for this number!")
                invalid_sound.play()
                
    def _update(self):
        #update game state
        
        #clear message if timer expired
        if self.message and pygame.time.get_ticks() > self.message_timer:
            self.message = ""
            
        #check for level transition
        if self.game_state.level == 1 and self.game_state.win:
            self._transition_to_level2()
        
        #self.btn_undo.readonly = self.game_state.current_num == 1
        
            
    def _transition_to_level2(self):
        #save completed level 1 board
        completed_board = [row[:] for row in self.game_state.board]
        
        #start level 2
        self.game_state.start_level2(completed_board)
        self._update_window_title()
        self.show_message("Level 1 Complete! Starting Level 2...")
        
        #adjust renderer offset for 7x7 board
        self.renderer.board_offset_x = 30
        
    def _update_window_title(self):
        pygame.display.set_caption("Matrix Game - Level %d" % self.game_state.level)
        
    def _draw(self):
        #clear screen
        self.screen.fill(WHITE)
        
        #draw UI elements
        self.renderer.draw_score(self.game_state.score)
        self.renderer.draw_next_number(self.game_state.current_num)
        self.renderer.draw_level_indicator(self.game_state.level)
        
        #draw board based on current level
        if self.game_state.level == 1:
            self.renderer.draw_level1_board(
                self.game_state.board,
                last_pos=self.game_state.last_pos,
                hover_cell=self.hover_cell
            )
        else:
            self.renderer.draw_level2_board(
                self.game_state.board,
                self.game_state.outer_ring,
                hover_cell=self.hover_cell
            )
            
        #draw buttons
        for btn in self.buttons:
            btn.draw(self.screen)
            
        #draw message if any
        if self.message:
            self.renderer.draw_message(self.message)
            
        #draw win message
        if self.game_state.win and self.game_state.level == 2:
            self._draw_win_screen()
            
        pygame.display.flip()
        
    def _draw_win_screen(self):
        #draw semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        #draw win message
        win_text = self.font.render("CONGRATULATIONS!", True, WHITE)
        score_text = self.font.render("Final Score: %d" % self.game_state.score, True, WHITE)
        
        self.screen.blit(win_text, win_text.get_rect(center=(self.width // 2, self.height // 2 - 30)))
        self.screen.blit(score_text, score_text.get_rect(center=(self.width // 2, self.height // 2 + 20)))
