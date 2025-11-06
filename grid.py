# grid.py
"""Grid management for the manor (5x9)."""

from typing import Optional, List, Tuple
import random

class Room:
    """Représentation minimale d'une salle dans la grille."""
    def __init__(self, name: str = "Unknown", color: Tuple[int,int,int]=(70,70,70), cost_gems:int=0):
        self.name = name
        self.color = color
        self.cost_gems = cost_gems
        # portes: dict direction -> lock level (0,1,2) ; not fully used yet
        self.doors = {"up": None, "down": None, "left": None, "right": None}
        # objets présents (simplifié)
        self.items = []

    def is_placeholder(self) -> bool:
        return self.name == "Unknown"

class Grid:
    """Gestion de la grille 5x9, salles connues vs inconnues."""

    def __init__(self, rows: int = 5, cols: int = 9):
        self.rows = rows
        self.cols = cols
        # None = vide / non découvert; Room instance = salle présente
        self._cells: List[List[Optional[Room]]] = [[None for _ in range(cols)] for _ in range(rows)]
        # initial room: Entrance Hall (placer en bas gauche par convention)
        start_r = rows - 1
        start_c = 0
        entrance = Room(name="Entrance Hall", color=(200,180,120), cost_gems=0)
        self._cells[start_r][start_c] = entrance
        # target (Antechamber) préférence: top-right ou top center? Place top row center as placeholder
        # (we don't place it yet — c'est à tirer ultérieurement)
    
    def in_bounds(self, r:int, c:int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def get_room(self, r:int, c:int) -> Optional[Room]:
        if not self.in_bounds(r,c): return None
        return self._cells[r][c]

    def set_room(self, r:int, c:int, room: Room):
        if not self.in_bounds(r,c):
            raise IndexError("Position hors de la grille")
        self._cells[r][c] = room

    def neighbors(self, r:int, c:int) -> dict:
        """Retourne coordonnéés des voisins valides."""
        result = {}
        dirs = {"up": (r-1,c), "down": (r+1,c), "left": (r,c-1), "right": (r,c+1)}
        for k,(nr,nc) in dirs.items():
            if self.in_bounds(nr,nc):
                result[k] = (nr,nc)
        return result

    def is_discovered(self, r:int, c:int) -> bool:
        return self.get_room(r,c) is not None

    def possible_open_door(self, from_r:int, from_c:int, to_r:int, to_c:int) -> bool:
        """Simplified: check bounds and not pointing outside; further rules later."""
        if not self.in_bounds(to_r,to_c): return False
        # if already discovered, it's open
        if self.is_discovered(to_r,to_c):
            return True
        # else position valid (not outside)
        return True

    def draw_textual(self):
        """Debug: affiche la grille en ASCII."""
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append('X' if self.is_discovered(r,c) else '.')
            print(''.join(row))
