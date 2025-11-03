"""
Module définissant les objets du jeu.
Jour 1 : Classes de base pour les objets.
"""

from abc import ABC, abstractmethod


class Item(ABC):
    """Classe abstraite représentant un objet du jeu."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def use(self, player):
        """Méthode abstraite pour utiliser l'objet."""
        pass
    
    def __str__(self):
        return f"{self.name}: {self.description}"


class ConsumableItem(Item):
    """Objet consommable qui disparaît après utilisation."""
    
    def __init__(self, name: str, description: str, quantity: int = 1):
        super().__init__(name, description)
        self.quantity = quantity
    
    def add(self, amount: int):
        """Ajoute une quantité."""
        self.quantity += amount
    
    def remove(self, amount: int) -> bool:
        """Retire une quantité si possible."""
        if self.quantity >= amount:
            self.quantity -= amount
            return True
        return False
    
    def use(self, player):
        """Utilise l'objet (à surcharger)."""
        return self.remove(1)


# Classes spécifiques basiques
class Steps(ConsumableItem):
    """Représente les pas du joueur."""
    
    def __init__(self, quantity: int = 70):
        super().__init__("Steps", "Steps remaining", quantity)
    
    def use(self, player):
        return self.remove(1)


class Keys(ConsumableItem):
    """Représente les clés."""
    
    def __init__(self, quantity: int = 0):
        super().__init__("Keys", "Keys to open doors", quantity)


class Gems(ConsumableItem):
    """Représente les gemmes."""
    
    def __init__(self, quantity: int = 2):
        super().__init__("Gems", "Gems to select special rooms", quantity)


class Coins(ConsumableItem):
    """Représente les pièces d'or."""
    
    def __init__(self, quantity: int = 0):
        super().__init__("Coins", "Gold coins", quantity)