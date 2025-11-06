# player.py
"""Player class: position, movement, selection cursor and reference to inventory."""

from typing import Tuple

class Player:
    """
    Représente le joueur / curseur dans la grille.

    Attributes:
        row (int): ligne actuelle du joueur (0..rows-1).
        col (int): colonne actuelle du joueur (0..cols-1).
        inventory (Inventory): référence à l'objet Inventory (injecté).
    """
    def __init__(self, start_row: int = 4, start_col: int = 0, inventory=None):
        # par défaut on place l'entrée en bas gauche (modifiable)
        self.row = start_row
        self.col = start_col
        # Cursor for selection (start on player)
        self.sel_row = self.row
        self.sel_col = self.col
        self.inventory = inventory

    def move_cursor(self, drow: int, dcol: int, max_rows: int, max_cols: int):
        """Déplace le curseur de sélection (ZQSD)."""
        nr = max(0, min(max_rows - 1, self.sel_row + drow))
        nc = max(0, min(max_cols - 1, self.sel_col + dcol))
        self.sel_row, self.sel_col = nr, nc

    def reset_cursor_to_player(self):
        """Replace le curseur sur la position du joueur."""
        self.sel_row, self.sel_col = self.row, self.col

    def can_move_to(self, dest_row: int, dest_col: int) -> bool:
        """Vérification simple: adjacency 4-voisin (ne vérifie pas portes)."""
        dr = abs(self.row - dest_row)
        dc = abs(self.col - dest_col)
        return (dr + dc) == 1

    def move_to(self, dest_row: int, dest_col: int):
        """
        Déplace le joueur physiquement (consomme un pas).
        Ne fait pas de vérification de validité ici (GameManager doit vérifier portes, salle).
        """
        if self.inventory is not None:
            self.inventory.decrement_steps(1)
        self.row, self.col = dest_row, dest_col
        # after move bring cursor to player
        self.reset_cursor_to_player()
