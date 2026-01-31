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

## Adding New Features

### To add sounds (Stories 2 & 6):
Look for comments `#placeholder for sound` in `window.py` methods:
- `_handle_level1_click()` - Add success/error sounds
- `_handle_level2_click()` - Add success/error sounds

### To add undo (Story 5):
1. Use `move_history` list in `GameState`
2. Record moves in `place_number()` methods
3. Add `undo_move()` methods to Level1Logic and Level2Logic
4. Add Undo button in `window.py`

### To add save/log (Story 7):
1. Create a file handler in `src/utils/`
2. Hook into level completion in `window.py` `_transition_to_level2()` and win state

### To add clear (Story 4):
1. Add Clear button in `window.py` `_create_buttons()`
2. Call `game_state.start_level1_with_random_one()` for Level 1
3. Reset `outer_ring` for Level 2
