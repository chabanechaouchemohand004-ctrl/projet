from abc import ABC, abstractmethod

class Item(ABC):
    """
    Classe abstraite représentant un objet du jeu.
    Cours CM6 : Utilisation de l'abstraction pour définir un comportement commun.
    """
    
    def __init__(self, name: str, description: str):
        """
        Constructeur de la classe Item.
        
        Args:
            name (str): Nom de l'objet
            description (str): Description de l'objet
        """
        self.name = name
        self.description = description
    
    @abstractmethod
    def use(self, player):
        """
        Méthode abstraite pour utiliser l'objet.
        Doit être implémentée par les classes filles.
        
        Args:
            player: Instance du joueur
        """
        pass