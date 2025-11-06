# constants.py
"""Constantes globales du projet (taille fenêtre, couleurs, etc.)."""

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 30

GRID_ROWS = 5
GRID_COLS = 9

# Layout: grid left, inventory right
PANEL_WIDTH = 260  # panel droit pour inventaire
GRID_AREA_WIDTH = WINDOW_WIDTH - PANEL_WIDTH
GRID_AREA_HEIGHT = WINDOW_HEIGHT

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
GREEN = (50, 200, 50)
RED = (200, 50, 50)
YELLOW = (230, 200, 50)
BLUE = (50, 100, 200)
CURSOR_COLOR = (255, 100, 100)
UNKNOWN_ROOM_COLOR = (30, 30, 30)
GRID_LINE_COLOR = (80, 80, 80)
