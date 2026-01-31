#!/usr/bin/env python

"""
Matrix Game - Main Entry Point

This is the main entry point for the Matrix Game with GUI.
Run this file to start the game.

Usage:
    python src/main.py

Controls:
    - Click on cells to place numbers
    - Press 'ESC' to quit
"""

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
    window.show_message("Welcome! Number 1 placed randomly. Place numbers 2-25!")
    
    #run the game
    window.run()


if __name__ == "__main__":
    main()
