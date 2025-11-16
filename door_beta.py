"""
Module de gestion des portes du manoir.

Ce module implémente le système de portes avec leurs différents niveaux
de verrouillage selon les règles du jeu Blue Prince.

Auteur: Chabane Chaouche (213 241 50)
Projet: POO - Blue Prince
"""


class Door:
    """
    Représente une porte du manoir avec son niveau de verrouillage.
    
    Les portes peuvent avoir trois niveaux de verrouillage:
    - Niveau 0 (UNLOCKED): porte déverrouillée, s'ouvre sans clé
    - Niveau 1 (LOCKED): porte verrouillée, nécessite une clé ou un kit de crochetage
    - Niveau 2 (DOUBLE_LOCKED): porte à double tour, nécessite une clé (le kit ne fonctionne pas)
    
    Attributes:
        lock_level (int): Le niveau de verrouillage (0, 1 ou 2)
        is_open (bool): Indique si la porte est ouverte
    
    Constants:
        UNLOCKED (int): Constante pour porte déverrouillée (0)
        LOCKED (int): Constante pour porte verrouillée simple (1)
        DOUBLE_LOCKED (int): Constante pour porte à double tour (2)
    """
    
    # Constantes pour les niveaux de verrouillage
    UNLOCKED = 0
    LOCKED = 1
    DOUBLE_LOCKED = 2
    
    def __init__(self, lock_level: int = UNLOCKED):
        """
        Initialise une porte avec un niveau de verrouillage donné.
        
        Args:
            lock_level: Le niveau de verrouillage initial (0, 1 ou 2)
        """
        self.lock_level = lock_level
        self.is_open = False
    
    def get_lock_level_name(self) -> str:
        """
        Retourne le nom textuel du niveau de verrouillage.
        
        Returns:
            str: Le nom du niveau de verrouillage
        """
        lock_names = {
            Door.UNLOCKED: "déverrouillée",
            Door.LOCKED: "verrouillée",
            Door.DOUBLE_LOCKED: "doublement verrouillée"
        }
        return lock_names.get(self.lock_level, "état inconnu")
    
    def get_state_name(self) -> str:
        """
        Retourne le nom complet de l'état de la porte.
        
        Returns:
            str: La description complète de l'état
        """
        status = "ouverte" if self.is_open else "fermée"
        lock_state = self.get_lock_level_name()
        return f"{status} ({lock_state})"
    
    def can_open(self, player) -> tuple[bool, str]:
        """
        Vérifie si le joueur peut ouvrir la porte.
        
        Règles d'ouverture:
        - Porte déverrouillée: toujours ouvrable
        - Porte verrouillée (niveau 1): nécessite une clé ou un kit de crochetage
        - Porte à double tour (niveau 2): nécessite une clé (le kit ne fonctionne pas)
        
        Args:
            player: Le joueur qui tente d'ouvrir la porte
            
        Returns:
            tuple[bool, str]: (peut_ouvrir, message_explicatif)
        """
        if self.lock_level == Door.UNLOCKED:
            return True, "Porte déverrouillée"
        
        if self.lock_level == Door.LOCKED:
            # Le kit de crochetage peut ouvrir les portes de niveau 1
            if player.inventory.has_permanent_item('lockpick_kit'):
                return True, "Peut ouvrir avec kit de crochetage"
            if player.inventory.keys.quantity > 0:
                return True, "Peut ouvrir avec une clé"
            return False, "Clé ou kit de crochetage nécessaire"
        
        if self.lock_level == Door.DOUBLE_LOCKED:
            # Le kit ne fonctionne pas sur les portes de niveau 2
            if player.inventory.keys.quantity > 0:
                return True, "Peut ouvrir avec une clé (double verrou)"
            return False, "Clé nécessaire (double verrou)"
        
        return False, "Impossible d'ouvrir"
    
    def open(self, player) -> bool:
        """
        Tente d'ouvrir la porte.
        
        Si la porte peut être ouverte:
        - Ouvre la porte
        - Consomme une clé si nécessaire (sauf si kit de crochetage utilisé)
        
        Args:
            player: Le joueur qui tente d'ouvrir la porte
            
        Returns:
            bool: True si la porte a été ouverte, False sinon
        """
        can_open, message = self.can_open(player)
        
        if can_open:
            # Si kit de crochetage utilisé pour niveau 1, pas de consommation de clé
            if self.lock_level == Door.LOCKED and player.inventory.has_permanent_item('lockpick_kit'):
                self.is_open = True
                return True
            # Sinon, consomme une clé si la porte est verrouillée
            elif self.lock_level > 0:
                player.inventory.keys.use(player)
                self.is_open = True
                return True
            else:
                # Porte déverrouillée, pas de clé nécessaire
                self.is_open = True
                return True
        
        return False
    
    def __str__(self):
        """Représentation textuelle de la porte."""
        state_name = self.get_state_name()
        return f"Porte ({state_name})"
    
    def __repr__(self):
        """Représentation pour le débogage."""
        return f"Door(lock_level={self.lock_level}, is_open={self.is_open})"