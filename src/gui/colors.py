#!/usr/bin/env python

#color constants for the game GUI

#basic colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)

#game colors - inner board (Level 1 and inner square in Level 2)
CELL_EMPTY = (230, 245, 255)        #very light blue empty cell
CELL_FILLED = (230, 245, 255)       #very light blue cell with a number
CELL_HOVER = (210, 230, 245)        #slightly darker when hovered
CELL_VALID = (230, 245, 255)        #same light color
CELL_INVALID = (230, 245, 255)      #same light color
CELL_LAST = (230, 245, 255)         #same light color for last placed

#level 2 specific colors - outer ring stays darker blue
RING_CELL_EMPTY = (173, 216, 230)   #light blue outer ring
RING_CELL_FILLED = (173, 216, 230)  #light blue outer ring with number
RING_CORNER = (255, 255, 0)         #bright yellow corner cells
INNER_BOARD_LOCKED = (230, 245, 255) #very light blue - matches inner board

#text colors
TEXT_DARK = (30, 30, 30)
TEXT_LIGHT = (250, 250, 250)
TEXT_BLUE = (0, 70, 180)            #blue text for inner board numbers

#header bar colors
HEADER_BG = (240, 245, 250)         #light gray-blue background
HEADER_LABEL = (120, 120, 130)      #muted gray for labels
SCORE_COLOR = (40, 160, 120)        #teal/green for score value
LEVEL_COLOR = (220, 80, 80)         #coral/red for level value

#button colors
BUTTON_NORMAL = (100, 150, 200)
BUTTON_HOVER = (120, 170, 220)
BUTTON_PRESSED = (80, 130, 180)
BUTTON_TEXT = (255, 255, 255)
BUTTON_DANGER = (220, 80, 80)       #red for quit button
BUTTON_DANGER_HOVER = (240, 100, 100)  #lighter red on hover

#border color
BORDER_COLOR = (50, 50, 50)
GRID_LINE = (100, 100, 100)
