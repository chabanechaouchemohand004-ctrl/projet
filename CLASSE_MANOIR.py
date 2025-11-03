class Manor:
    """
    Représente le manoir (grille 5×9).
    Cours CM4 : Agrégation - le manoir contient des pièces.
    """
    
    def __init__(self, height: int = 5, width: int = 9):
        """
        Initialise le manoir.
        
        Args:
            height (int): Nombre de rangées
            width (int): Nombre de colonnes
        """
        self.height = height
        self.width = width
        # Grille de pièces (None = pas encore découvert)
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        
        # Position de départ (Entrance Hall)
        self.entrance_position = (height - 1, width // 2)
        
        # Position d'arrivée (Antechamber)
        self.exit_position = (0, width // 2)
    
    def place_room(self, room: Room, position: tuple):
        """
        Place une pièce dans la grille.
        
        Args:
            room (Room): Pièce à placer
            position (tuple): (row, col) position
        """
        row, col = position
        if 0 <= row < self.height and 0 <= col < self.width:
            self.grid[row][col] = room
    
    def get_room(self, position: tuple) -> Room:
        """Récupère la pièce à une position donnée."""
        row, col = position
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.grid[row][col]
        return None
    
    def is_position_valid(self, position: tuple) -> bool:
        """Vérifie si une position est dans la grille."""
        row, col = position
        return 0 <= row < self.height and 0 <= col < self.width