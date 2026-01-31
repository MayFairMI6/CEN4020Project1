# Matrix Game - Source Code

## Overview
This is a Pygame-based implementation of the Matrix Game with two levels.

**Implemented User Stories:**
- Story 1: GUI with click-to-place and random initial placement of 1
- Story 8: Level 2 expansion with outer ring

**Left for teammates to implement:**
- Story 2: Sound on valid click
- Story 3: Next number auto-display
- Story 4: Clear board feature
- Story 5: Undo/rollback feature
- Story 6: Sound on invalid click
- Story 7: Save/log completed games

## How to Run
```bash
# Install dependencies
pip install pygame

# Run the game
python src/main.py
```

## Project Structure
```
src/
├── main.py              # Entry point - starts the game
├── game_logic/
│   ├── game_state.py    # Shared game state (board, score, level)
│   ├── level1.py        # Level 1 logic (5x5 board)
│   └── level2.py        # Level 2 logic (outer ring)
└── gui/
    ├── window.py        # Main Pygame window and game loop
    ├── board_renderer.py # Draws boards for both levels
    └── colors.py        # Color constants
```

## Architecture

### Game State (`game_logic/game_state.py`)
Central data class holding:
- `board` - 5x5 inner board (2D list)
- `outer_ring` - Level 2 ring cells (dict with (row, col) keys)
- `current_num` - Next number to place
- `score` - Player score
- `level` - Current level (1 or 2)
- `move_history` - Placeholder for undo feature (Story 5)

### Level 1 Logic (`game_logic/level1.py`)
- `is_valid_move(row, col)` - Checks if placement is valid
- `place_number(row, col)` - Places number, updates score
- `get_valid_cells()` - Returns list of valid cells

### Level 2 Logic (`game_logic/level2.py`)
- `get_valid_ring_cells(num)` - Returns valid ring positions for a number
- `place_number(ring_row, ring_col)` - Places number in outer ring
- Placement rules: row/column ends + diagonal corners for numbers on diagonals

### GUI (`gui/window.py`)
- Pygame window with game loop
- Click detection maps mouse to board cells
- Automatic transition from Level 1 to Level 2 on completion


