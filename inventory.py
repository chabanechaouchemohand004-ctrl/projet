# inventory.py
"""Inventory management: consumables and permanents."""

from dataclasses import dataclass

@dataclass
class Inventory:
    """
    Inventaire simple.
    Consumables:
        - steps: nombre de pas (initial 70)
        - gold: pièces d'or
        - gems: gemmes
        - keys: clefs
        - dice: dés
    Permanents: booleans representant objets trouvés.
    """
    steps: int = 70
    gold: int = 0
    gems: int = 2
    keys: int = 0
    dice: int = 0

    shovel: bool = False
    hammer: bool = False
    picklock_kit: bool = False
    metal_detector: bool = False
    rabbit_foot: bool = False

    def decrement_steps(self, n: int = 1):
        """Retire des pas (pas négatifs ignorés)."""
        self.steps = max(0, self.steps - n)

    def add_steps(self, n: int):
        """Ajoute des pas (n positif)."""
        self.steps += n

    def add_gems(self, n: int):
        self.gems += n

    def use_gems(self, n: int) -> bool:
        """Essaie de dépenser des gemmes. Retourne True si ok."""
        if self.gems >= n:
            self.gems -= n
            return True
        return False

    def add_keys(self, n: int):
        self.keys += n

    def use_key(self, n: int = 1) -> bool:
        if self.keys >= n:
            self.keys -= n
            return True
        return False

    def add_dice(self, n: int):
        self.dice += n

    def use_die(self) -> bool:
        if self.dice > 0:
            self.dice -= 1
            return True
        return False

    def is_dead(self) -> bool:
        """Perdu si plus de pas."""
        return self.steps <= 0
