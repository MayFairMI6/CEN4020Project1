#!/usr/bin/env python


import sys
import os

#add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_logic.game_state import GameState
from game_logic.level1 import Level1Logic
from game_logic.level2 import Level2Logic
from game_logic.level3 import Level3Logic
from gui.window import GameWindow
from gui.time_limit_screen import TimeLimitScreen
from auth.user_manager import UserManager
from auth.auth_screen import AuthScreen


def main():
    #authenticate user before starting game
    user_manager = UserManager()
    auth_screen = AuthScreen(user_manager)
    
    #show login/register screen
    username = auth_screen.run()
    
    if not username:
        #user closed auth screen without logging in
        return
    
    #User Story 11: show time-limit configuration screen
    time_limit_screen = TimeLimitScreen()
    time_limits = time_limit_screen.run()
    
    #create game state
    game_state = GameState()
    
    #create logic handlers
    level1_logic = Level1Logic(game_state)
    level2_logic = Level2Logic(game_state)
    level3_logic = Level3Logic(game_state)
    
    #create game window
    window = GameWindow()
    window.set_game_components(game_state, level1_logic, level2_logic, level3_logic)
    
    #set authenticated player name
    window.set_player_name(username)
    
    #User Story 11: apply chosen time limits
    window.set_time_limits(time_limits)
    
    #start game with random placement of 1 (User Story 1 requirement)
    game_state.start_level1_with_random_one()
    
    #User Story 11: start the timer for level 1
    window.start_level_timer(1)
    
    #show welcome message with player name
    window.show_message(f"Welcome, {username}!")
    
    #run the game
    window.run()


if __name__ == "__main__":
    main()
