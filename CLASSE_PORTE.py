class Door:
    """
    Représente une porte dans le manoir.
    Section 2.6 : Les portes ont 3 niveaux de verrouillage.
    """
    
    # Constantes pour les niveaux de verrouillage
    UNLOCKED = 0
    LOCKED = 1
    DOUBLE_LOCKED = 2
    
    def __init__(self, lock_level: int = UNLOCKED):
        """
        Initialise une porte.
        
        Args:
            lock_level (int): Niveau de verrouillage (0, 1 ou 2)
        """
        self.lock_level = lock_level
        self.is_open = False
    
    def can_open(self, player) -> tuple[bool, str]:
        """
        Vérifie si le joueur peut ouvrir la porte.
        
        Returns:
            tuple[bool, str]: (peut_ouvrir, message)
        """
        # Porte déverrouillée
        if self.lock_level == Door.UNLOCKED:
            return True, "Door unlocked"
        
        # Porte niveau 1 : peut utiliser kit de crochetage
        if self.lock_level == Door.LOCKED:
            if player.inventory.has_item("lockpick_kit"):
                return True, "Opened with lockpick kit"
            elif player.inventory.keys.quantity > 0:
                return True, "Opened with key"
            else:
                return False, "Need a key or lockpick kit"
        
        # Porte niveau 2 : seulement avec clé
        if self.lock_level == Door.DOUBLE_LOCKED:
            if player.inventory.keys.quantity > 0:
                return True, "Opened with key"
            else:
                return False, "Need a key (double-locked door)"
        
        return False, "Cannot open door"
    
    def open(self, player) -> bool:
        """
        Tente d'ouvrir la porte.
        
        Returns:
            bool: True si réussi, False sinon
        """
        can_open, message = self.can_open(player)
        print(message)
        
        if can_open:
            # Consomme une clé si nécessaire
            if self.lock_level > 0 and not player.inventory.has_item("lockpick_kit"):
                player.inventory.keys.use(player)
            elif self.lock_level == Door.DOUBLE_LOCKED:
                player.inventory.keys.use(player)
            
            self.is_open = True
            return True
        
        return False