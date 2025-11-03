"""
Module de gestion de l'inventaire.
Jour 1 : Inventaire basique.
"""

from models.item import Steps, Keys, Gems, Coins, ConsumableItem


class Inventory:
    """Gère l'inventaire du joueur."""
    
    def __init__(self):
        # Objets consommables de départ
        self.steps = Steps(70)
        self.keys = Keys(0)
        self.gems = Gems(2)
        self.coins = Coins(0)
    
    def add_item(self, item_name: str, quantity: int = 1):
        """Ajoute un objet à l'inventaire."""
        if item_name == "steps":
            self.steps.add(quantity)
        elif item_name == "keys":
            self.keys.add(quantity)
        elif item_name == "gems":
            self.gems.add(quantity)
        elif item_name == "coins":
            self.coins.add(quantity)
    
    def display(self):
        """Affiche l'inventaire."""
        print(f"📊 Inventory:")
        print(f"  Steps: {self.steps.quantity}")
        print(f"  Keys: {self.keys.quantity}")
        print(f"  Gems: {self.gems.quantity}")
        print(f"  Coins: {self.coins.quantity}")


# Test basique
if __name__ == "__main__":
    inv = Inventory()
    inv.display()
    inv.add_item("keys", 3)
    inv.add_item("coins", 10)
    inv.display()