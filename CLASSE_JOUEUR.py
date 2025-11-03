class Player:
    """
    Représente le joueur.
    Cours CM4 : Le joueur possède un inventaire (composition).
    """
    
    def __init__(self, start_position: tuple):
        """
        Initialise le joueur.
        
        Args:
            start_position (tuple): Position de départ (row, col)
        """
        self.position = start_position
        self.inventory = Inventory()
    
    def move(self, new_position: tuple, manor: Manor) -> bool:
        """
        Déplace le joueur vers une nouvelle position.
        
        Args:
            new_position (tuple): Nouvelle position
            manor (Manor): Le manoir
        
        Returns:
            bool: True si déplacement réussi
        """
        # Vérifie si on a assez de pas
        if self.inventory.steps.quantity <= 0:
            print("Not enough steps!")
            return False
        
        # Consomme un pas (section 2.1)
        self.inventory.steps.use(self)
        
        # Met à jour la position
        self.position = new_position
        
        # Entre dans la nouvelle pièce
        room = manor.get_room(new_position)
        if room:
            room.enter(self)
        
        return True
    
    def has_won(self, manor: Manor) -> bool:
        """Vérifie si le joueur a gagné."""
        return self.position == manor.exit_position
    
    def has_lost(self) -> bool:
        """Vérifie si le joueur a perdu."""
        return self.inventory.steps.quantity <= 0