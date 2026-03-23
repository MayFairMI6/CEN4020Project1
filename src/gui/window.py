#!/usr/bin/env python

import pygame
import sys
from .board_renderer import BoardRenderer
from .colors import *
from .timer import Timer
from .sound import valid_sound, invalid_sound
#import completion logger for Story 7
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from completion_logger import CompletionLogger, CompletionRecord, iso_now

# #sound effects for User Story 2 and 6
# pygame.mixer.init(44100, -16, 2, 2048)

# valid_sound = pygame.mixer.Sound("Sprint1Story2.wav")
# invalid_sound = pygame.mixer.Sound("Sprint1Story6.wav")


class Button:
    def __init__(self, x, y, width, height, text, font, danger=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.is_hovered = False
        self.danger = danger    #use red color for danger buttons like Quit
        self.show_restart_popup = False #User Story 16 : restart confirmation 
        
    def draw(self, screen):
        #determine button color
        if self.danger:
            color = BUTTON_DANGER_HOVER if self.is_hovered else BUTTON_DANGER
        else:
            color = BUTTON_HOVER if self.is_hovered else BUTTON_NORMAL
            
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
    def __init__(self, width=600, height=720):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Matrix Game - Level 1")
        self.clock = pygame.time.Clock()
        self.running = True
        
        
        #User Story 15: Sound On/Off
        self.sound_on = True
        #User Story 16
        self.show_restart_popup = False
    
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
        self.level3_logic = None
        
        #UI state
        self.hover_cell = None
        self.message = ""
        self.message_timer = 0
        
        #completion logger for Story 7
        self.logger = CompletionLogger("game_log.txt")
        self.level1_logged = False   #track if Level 1 completion was logged
        self.level2_logged = False   #track if Level 2 completion was logged
        self.level3_logged = False
        
        #User Story 11: per-level time limits (0 = no limit)
        self.time_limits = {1: 0, 2: 0, 3: 0}
        self.timers = {1: Timer(), 2: Timer(), 3: Timer()}
        #flags to ensure score delta is applied exactly once per level
        self.timer_score_applied = {1: False, 2: False, 3: False}
        #flag to show "Time's up!" message only once per level
        self.timer_expired_shown = {1: False, 2: False, 3: False}
        
        #set player name after authentication
        self.player_name = "Player"
        
        #create buttons
        self._create_buttons()
        
    def _create_buttons(self):
        #buttons at bottom of screen - centered layout
        btn_width = 90
        btn_height = 35
        btn_spacing = 15
        
        #row 1: Undo and Clear (centered)
        #board ends at ~610 for level 2 (120 offset + 7*70 cells), so start buttons at 620
        row1_y = 620
        row1_total_width = 2 * btn_width + btn_spacing
        row1_start_x = (self.width - row1_total_width) // 2.67
        
        
        self.btn_undo = Button(row1_start_x, row1_y, btn_width, btn_height, "Undo", self.small_font)
        self.btn_clear = Button(row1_start_x + btn_width + btn_spacing, row1_y, btn_width, btn_height, "Clear", self.small_font)

        #User Story 15 Sound On/Off Button
        self.btn_sound_off = Button(50, row1_y - 10, btn_width, btn_height, "-", self.small_font)
        self.btn_sound_on = Button(225, row1_total_width/2 - 35, btn_width + 40, btn_height, "Sound: ON", self.small_font)

        self.btn_auto = Button(row1_start_x + 2 * (btn_width + btn_spacing), row1_y, btn_width, btn_height, "Auto", self.small_font)

        
        #row 2: Quit button (centered, red)
        row2_y = row1_y + btn_height + 8
        quit_x = (self.width - btn_width) // 2
        self.btn_quit = Button(quit_x, row2_y, btn_width, btn_height, "Quit", self.small_font, danger=True)
        
        
        #User Story 16 : restart confirmation
        # restart popup buttons (centered)
        popup_y = 350
        popup_btn_w = 80
        popup_btn_h = 35
        gap = 20

        center_x = self.width // 2
        self.btn_restart_yes = Button(center_x - popup_btn_w - gap//2, popup_y,
                                    popup_btn_w, popup_btn_h, "Yes", self.small_font)

        self.btn_restart_no = Button(center_x + gap//2, popup_y,
                                    popup_btn_w, popup_btn_h, "No", self.small_font)
                
        self.buttons = [self.btn_undo, self.btn_clear, self.btn_auto, self.btn_quit, self.btn_sound_on]
        
        
    def set_game_components(self, game_state, level1_logic, level2_logic, level3_logic):
        #set game components from main
        self.game_state = game_state
        self.level1_logic = level1_logic
        self.level2_logic = level2_logic
        self.level3_logic = level3_logic
    
    def set_player_name(self, name):
        #set authenticated player name
        self.player_name = name

    def set_time_limits(self, limits: dict):
        """Store per-level time limits and reset tracking state.
        limits: {1: int, 2: int, 3: int}  –  0 means no time limit.
        """
        self.time_limits = {1: limits.get(1, 0),
                            2: limits.get(2, 0),
                            3: limits.get(3, 0)}
        self.timer_score_applied = {1: False, 2: False, 3: False}
        self.timer_expired_shown  = {1: False, 2: False, 3: False}

    def start_level_timer(self, level: int):
        """Start the countdown timer for *level* if a limit was configured."""
        limit = self.time_limits.get(level, 0)
        if limit > 0:
            self.timers[level].start(limit)

    def _apply_timer_score(self, level: int):
        """Stop the timer for *level* and apply its bonus/penalty to the score."""
        if self.timer_score_applied[level]:
            return
        limit = self.time_limits.get(level, 0)
        if limit == 0:
            return
        timer = self.timers[level]
        if timer.running:
            timer.stop()
        delta = timer.calculate_score()
        self.game_state.score += delta
        self.timer_score_applied[level] = True
        if delta > 0:
            self.show_message("Time bonus: +%d pts!" % delta, 3000)
        elif delta < 0:
            self.show_message("Time penalty: %d pts!" % delta, 3000)
        
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
        self.hover_cell = self.renderer.get_cell_at_pos(mouse_pos[0], mouse_pos[1], self.game_state.level)
            
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
        # handle restart popup first
        if self.show_restart_popup:
            if self.btn_restart_yes.is_clicked(mouse_pos):
                self.show_restart_popup = False
                if self.game_state.level == 1:
                    self.game_state.reset_level1()
                else:
                    self.game_state.reset_lv2()
            elif self.btn_restart_no.is_clicked(mouse_pos):
                self.show_restart_popup = False
            return
        #check button clicks
        if self.btn_quit.is_clicked(mouse_pos):
            self.running = True
            return
        
        #undo - only allow if more than just "1" is placed (current_num > 2) and game not won
        if self.btn_undo.is_clicked(mouse_pos) and not self.game_state.win:
            self.game_state.undo()
        
        #clear - disabled on win screen****
        # if self.btn_clear.is_clicked(mouse_pos) and not self.game_state.win:
        #     if self.game_state.level == 1:
        #         self.game_state.reset_level1()
        #     else:
        #         self.game_state.reset_lv2()
        #         self.game_state.board
        if self.btn_clear.is_clicked(mouse_pos) and not self.game_state.win:
            self.show_restart_popup = True
            return
        
        if self.btn_auto.is_clicked(mouse_pos) and not self.game_state.win:
            match self.game_state.level:
                case 1:
                    logic = self.level1_logic
                case 2:
                    logic = self.level2_logic
                case 3: 
                    logic = self.level3_logic
            
            if not self.game_state.autocomplete(logic):
                self.show_message("Board is impossible to complete from here")
                invalid_sound(self.sound_on)
        
        #check board click
        if self.game_state.win:
            return   #don't accept clicks if level is won (transition happens automatically)
            
        if self.game_state.level == 1:
            cell = self.renderer.get_cell_at_pos(mouse_pos[0], mouse_pos[1], level=1)
            if cell:
                self._handle_level1_click(cell)
        elif self.game_state.level == 2:
            cell = self.renderer.get_cell_at_pos(mouse_pos[0], mouse_pos[1], level=2)
            if cell:
                self._handle_level2_click(cell)
                
        else:
            cell = self.renderer.get_cell_at_pos(mouse_pos[0], mouse_pos[1], level=3)
            if cell:
                self._handle_level3_click(cell)
                
        # User Story 15 : Sound On/Off Button
        if self.btn_sound_on.is_clicked(mouse_pos):
            self.sound_on = not self.sound_on
            self.btn_sound_on.text = "Sound: ON" if self.sound_on else "Sound: OFF"
            return
        #User Story 16 
        if self.btn_clear.is_clicked(mouse_pos) and not self.game_state.win:
            self.show_restart_popup = True
            return     
                    
    def _handle_level1_click(self, cell):
        row, col = cell
        success, error = self.level1_logic.place_number(row, col)
        
        if success:
            #placeholder for sound (story 2)
            valid_sound(self.sound_on)
        else:
            #placeholder for error sound (story 6)
            invalid_sound(self.sound_on)
            if error == "out_of_bounds":
                self.show_message("Cell is out of bounds!")
            elif error == "cell_occupied":
                self.show_message("Cell is already occupied!")
            elif error == "not_adjacent":
                self.show_message("Must be adjacent to previous number!")
                
                
    def _handle_level2_click(self, cell):
        ring_row, ring_col = cell
        
        #check if clicking on inner board (not allowed in level 2)
        if 1 <= ring_row <= 5 and 1 <= ring_col <= 5:
            self.show_message("Inner board is locked in Level 2!")
            return
            
        success, error = self.level2_logic.place_number(ring_row, ring_col)
        
        if success:
            #placeholder for sound (story 2)
            valid_sound(self.sound_on)
        else:
            invalid_sound(self.sound_on)
            #placeholder for error sound (story 6)
            if error == "not_ring_cell":
                self.show_message("Click on the outer ring!")
            elif error == "cell_occupied":
                self.show_message("Cell is already occupied!")
            elif error == "invalid_position":
                self.show_message("Invalid position for this number!")
    
    def _handle_level3_click(self, cell):
        row, col = cell
        success, error = self.level3_logic.place_number(row, col)
        
        if success:
            #placeholder for sound (story 2)
            valid_sound(self.sound_on)
        else:
            #placeholder for error sound (story 6)
            invalid_sound(self.sound_on)
            if error == "out_of_bounds":
                self.show_message("Cell is out of bounds!")
            elif error == "cell_occupied":
                self.show_message("Cell is already occupied!")
            elif error == "not_adjacent":
                self.show_message("Must be adjacent to previous number!")

            elif error == "outside_ring_position":
                self.show_message("Must be aligned with ring position!")

                
    def _update(self):
        #update game state
        
        #clear message if timer expired
        if self.message and pygame.time.get_ticks() > self.message_timer:
            self.message = ""
        
        #User Story 11: warn player once when the timer hits zero
        level = self.game_state.level
        if not self.game_state.win:
            limit = self.time_limits.get(level, 0)
            if limit > 0 and not self.timer_expired_shown[level]:
                timer = self.timers[level]
                if timer.running and timer.left() == 0:
                    self.show_message("Time's up! Extra seconds cost points.", 3000)
                    self.timer_expired_shown[level] = True
            
        #check for level transition
        if self.game_state.level == 1 and self.game_state.win:
            self._apply_timer_score(1)
            self._transition_to_level2()
        
        #log Level 2 completion (Story 7)
        if self.game_state.level == 2 and self.game_state.win:
            self._apply_timer_score(2)
            self._transition_to_level3()
        
        #apply timer score when level 3 is completed
        if self.game_state.level == 3 and self.game_state.win:
            self._apply_timer_score(3)
              
    def _log_completion(self, level):
        #log game completion for Story 7 with human-readable board format
        #use authenticated player name
        if level == 1:
            record = CompletionRecord(
                player_name=self.player_name,
                timestamp_iso=iso_now(),
                level=level,
                points=self.game_state.score,
                board=[row[:] for row in self.game_state.board],  #copy 2D board
                outer_ring=None
            )
        else:
            record = CompletionRecord(
                player_name=self.player_name,
                timestamp_iso=iso_now(),
                level=level,
                points=self.game_state.score,
                board=[row[:] for row in self.game_state.board],  #copy 2D board
                outer_ring=dict(self.game_state.outer_ring)  #copy outer ring
            )
        self.logger.append_record(record)
        
    def _transition_to_level2(self):
        #log Level 1 completion (Story 7)
        if not self.level1_logged:
            self._log_completion(1)
            self.level1_logged = True
        
        #save completed level 1 board
        completed_board = [row[:] for row in self.game_state.board]
        
        #start level 2
        self.game_state.start_level2(completed_board)
        self._update_window_title()
        self.show_message("Level 1 Complete! Starting Level 2...")
        
        #User Story 11: start timer for the new level
        self.start_level_timer(2)
    
    def _transition_to_level3(self):
        if not self.level2_logged:
            self._log_completion(2)
            self.level2_logged = True
        
        #save completed level 2 board
        completed_ring = self.game_state.outer_ring.copy()
        
        self.game_state.start_level3(completed_ring)
        self._update_window_title()
        self.show_message("Level 2 Complete! Starting Level 3...")
        
        #User Story 11: start timer for the new level
        self.start_level_timer(3)
    
    def _update_window_title(self):
        pygame.display.set_caption("Matrix Game - Level %d" % self.game_state.level)
        
    def _draw(self):
        #clear screen
        self.screen.fill(WHITE)
        
        #User Story 11: compute timer display values for the header
        level = self.game_state.level
        time_left_display = None
        is_overtime = False
        limit = self.time_limits.get(level, 0)
        if limit > 0:
            timer = self.timers[level]
            left = timer.left()
            if left is not None and left > 0:
                time_left_display = left
                is_overtime = False
            elif timer.running or timer.has_run():
                time_left_display = timer.overtime()
                is_overtime = True
        
        #draw header bar
        self.renderer.draw_header_bar(
            self.game_state.score,
            self.game_state.current_num,
            self.game_state.level,
            self.width,
            time_left=time_left_display,
            is_overtime=is_overtime
        )
        
        #center board for current level
        self.renderer.center_board(self.game_state.level)
        
        #draw board based on current level
        if self.game_state.level == 1:
            self.renderer.draw_level1_board(
                self.game_state.board,
                last_pos=self.game_state.last_pos,
                hover_cell=self.hover_cell,
                auto_completed_from=self.game_state.auto_completed_from[0]
            )
        elif self.game_state.level == 2:
            self.renderer.draw_level2_board(
                self.game_state.board,
                self.game_state.outer_ring,
                hover_cell=self.hover_cell,
                auto_completed_from=self.game_state.auto_completed_from
            )
        else:
            self.renderer.draw_level3_board(
                self.game_state.board,
                self.game_state.outer_ring,
                hover_cell=self.hover_cell,
                auto_completed_from=self.game_state.auto_completed_from
            )
            
        #draw buttons
        for btn in self.buttons:
            btn.draw(self.screen)
            
        #draw message if any
        if self.message:
            self.renderer.draw_message(self.message)
            
        #draw win message
        if self.game_state.win and self.game_state.level == 3:
            self._draw_win_screen()
            
        # draw restart popup if needed
        if self.show_restart_popup:
            self._draw_restart_popup()
            
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
        
    def _draw_restart_popup(self):
    # dark overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # popup box
        box_w, box_h = 300, 150
        box_x = (self.width - box_w) // 2
        box_y = (self.height - box_h) // 2
        pygame.draw.rect(self.screen, (240, 240, 240), (box_x, box_y, box_w, box_h), border_radius=10)
        pygame.draw.rect(self.screen, (60, 60, 60), (box_x, box_y, box_w, box_h), 2, border_radius=10)

        # text
        text = self.font.render("Restart the game?", True, (0, 0, 0))
        self.screen.blit(text, text.get_rect(center=(self.width//2, box_y + 40)))

        # draw buttons
        self.btn_restart_yes.draw(self.screen)
        self.btn_restart_no.draw(self.screen)
