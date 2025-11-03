class Inventory:
    """
    Gère l'inventaire du joueur.
    Cours CM4 : Composition - l'inventaire CONTIENT des objets.
    """
    
    def __init__(self):
        """Initialise l'inventaire avec les valeurs de départ."""
        # Objets consommables (section 2.1 de l'énoncé)
        self.steps = Steps(70)
        self.coins = ConsumableItem("Coins", "Gold coins", 0)
        self.gems = Gems(2)
        self.keys = Keys(0)
        self.dice = ConsumableItem("Dice", "Reroll room selection", 0)
        
        # Objets permanents
        self.permanent_items = {
            "shovel": None,
            "hammer": None,
            "lockpick_kit": None,
            "metal_detector": None,
            "rabbit_foot": None
        }
    
    def add_item(self, item_name: str, quantity: int = 1):
        """
        Ajoute un objet à l'inventaire.
        
        Args:
            item_name (str): Nom de l'objet
            quantity (int): Quantité à ajouter
        """
        if item_name == "steps":
            self.steps.add(quantity)
        elif item_name == "coins":
            self.coins.add(quantity)
        elif item_name == "gems":
            self.gems.add(quantity)
        elif item_name == "keys":
            self.keys.add(quantity)
        elif item_name == "dice":
            self.dice.add(quantity)
    
    def has_item(self, item_name: str) -> bool:
        """Vérifie si le joueur possède un objet permanent."""
        return self.permanent_items.get(item_name) is not None
    
    def display(self):
        """Affiche le contenu de l'inventaire."""
        print(f"Steps: {self.steps.quantity}")
        print(f"Coins: {self.coins.quantity}")
        print(f"Gems: {self.gems.quantity}")
        print(f"Keys: {self.keys.quantity}")
        print(f"Dice: {self.dice.quantity}")