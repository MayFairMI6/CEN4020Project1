#!/usr/bin/env python


import sys
import os

#add src directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game_logic.game_state import GameState
from game_logic.level1 import Level1Logic
from game_logic.level2 import Level2Logic
from gui.window import GameWindow


def main():
    #create game state
    game_state = GameState()
    
    #create logic handlers
    level1_logic = Level1Logic(game_state)
    level2_logic = Level2Logic(game_state)
    
    #create game window
    window = GameWindow()
    window.set_game_components(game_state, level1_logic, level2_logic)
    
    #start game with random placement of 1 (User Story 1 requirement)
    game_state.start_level1_with_random_one()
    
    #show welcome message
    window.show_message("Welcome To The Matrix Game!")
    
    #run the game
    window.run()


if __name__ == "__main__":
    main()
