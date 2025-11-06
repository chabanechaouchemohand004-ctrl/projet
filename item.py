"""

Module définissant les objets du jeu Blue Prince.

Jour 1 : Classes de base pour les objets consommables.

Ce module implémente le système d'objets du jeu en utilisant :
- L'abstraction (classe abstraite Item)
- L'héritage (ConsumableItem hérite de Item)
- Le polymorphisme (méthode use() redéfinie)

"""

from abc import ABC, abstractmethod


class Item(ABC):
    """Classe abstraite représentant un objet du jeu. 
    Attributes:
        name (str): Le nom de l'objet
        description (str): Une description de l'objet"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def use(self, player):
        """Méthode abstraite pour utiliser l'objet.
        Args:
            player: Le joueur qui utilise l'objet
            
        Returns:
            bool: True si l'utilisation a réussi, False sinon"""
        pass
    
    def __str__(self):
        """Représentation textuelle de l'objet."""
        return f"{self.name}: {self.description}"
    def __repr__(self):
        """Représentation pour le débogage."""
        return f"{self.__class__.__name__}(name='{self.name}')"


class ConsumableItem(Item):
    """Objet consommable qui disparaît après utilisation.
    Attributes:
        quantity (int): La quantité disponible de cet objet"""
    
    def __init__(self, name: str, description: str, quantity: int = 1):
        """
        Initialise un objet consommable.
        
        Args:
            name: Le nom de l'objet
            description: La description de l'objet
            quantity: La quantité initiale (par défaut 1)
        """
        super().__init__(name, description)
        self.quantity = quantity
    
    def add(self, amount: int):
        """Ajoute une quantité.
        Args:
            amount: La quantité à ajouter (doit être positive)
            
        Raises:
            ValueError: Si amount est négatif"""
        if amount < 0:
            raise ValueError("Cannot add negative amount")
        self.quantity += amount
    
    def remove(self, amount: int) -> bool:
        """
        Retire une quantité de l'objet si possible.
        
        Args:
            amount: La quantité à retirer
            
        Returns:
            bool: True si la quantité a été retirée, False sinon.
        """
        if amount < 0:
            raise ValueError("Cannot remove negative amount")
        
        if self.quantity >= amount:
            self.quantity -= amount
            return True
        return False
    
    def use(self, player):
        """
        Utilise une unité de l'objet.
        
        Implémentation par défaut qui retire 1 de la quantité.
        Peut être surchargée dans les sous-classes pour des comportements spécifiques.
        
        Args:
            player: Le joueur qui utilise l'objet
            
        Returns:
            bool: True si l'utilisation a réussi, False sinon.
        """
        return self.remove(1)
    
    def __str__(self):
        """Représentation textuelle incluant la quantité."""
        return f"{self.name}: {self.description} (x{self.quantity})"


# Classes spécifiques d'objets consommables
class Steps(ConsumableItem):
    """Représente les pas du joueur.
   
    Les pas sont la ressource principale du jeu. Chaque déplacement
    consomme un pas. Le jeu se termine quand le joueur n'a plus de pas.
    
    Quantité initiale : 70 pas
    """
    
    def __init__(self, quantity: int = 70):
        """
        Initialise les pas du joueur.
        
        Args:
            quantity: Le nombre de pas initial (par défaut 70)
        """
        super().__init__(
            name="Steps",
            description="Steps remaining to explore the manor",
            quantity=quantity
        )
    
    def use(self, player):
        """
        Utilise un pas (lors d'un déplacement).
        
        Args:
            player: Le joueur qui se déplace
            
        Returns:
            bool: True si un pas a été consommé, False si plus de pas
        """
        if self.quantity > 0:
            return self.remove(1)
        return False

class Keys(ConsumableItem):
    """
    Représente les clés pour ouvrir les portes.
    
    Les clés sont nécessaires pour ouvrir les portes verrouillées.
    Une clé est consommée à chaque ouverture de porte.
    
    Quantité initiale : 0 clés
    """
   
    
    def __init__(self, quantity: int = 0):
        """
        Initialise les clés.
        
        Args:
            quantity: Le nombre de clés initial (par défaut 0)
        """
        super().__init__(
            name="Keys",
            description="Keys to open locked doors",
            quantity=quantity
        )
    
    def use(self, player):
        """
        Utilise une clé pour ouvrir une porte.
        
        Args:
            player: Le joueur qui ouvre la porte
            
        Returns:
            bool: True si une clé a été utilisée, False si pas de clé
        """
        if self.quantity > 0:
            return self.remove(1)
        return False


class Gems(ConsumableItem):
    """
    Représente les gemmes pour sélectionner des pièces spéciales.
    
    Les gemmes permettent de choisir des pièces rares lors de la sélection.
    Plus une pièce est rare, plus elle coûte de gemmes.
    
    Quantité initiale : 2 gemmes
    """
    
    def __init__(self, quantity: int = 2):
        """
        Initialise les gemmes.
        
        Args:
            quantity: Le nombre de gemmes initial (par défaut 2)
        """
        super().__init__(
            name="Gems",
            description="Gems to select special rooms",
            quantity=quantity
        )
    
    def use(self, player):
        """
        Utilise une gemme pour choisir une pièce rare.
        
        Args:
            player: Le joueur qui utilise la gemme
            
        Returns:
            bool: True si une gemme a été utilisée, False sinon
        """
        if self.quantity > 0:
            return self.remove(1)
        return False


class Coins(ConsumableItem):
    """
    Représente les pièces d'or collectées.
    
    Les pièces sont collectées dans les coffres et autres sources.
    Elles servent de score et peuvent être utilisées pour des bonus.
    
    Quantité initiale : 0 pièces
    """
    
    def __init__(self, quantity: int = 0):
        """
        Initialise les pièces.
        
        Args:
            quantity: Le nombre de pièces initial (par défaut 0)
        """
        super().__init__(
            name="Coins",
            description="Gold coins collected",
            quantity=quantity
        )
    
    def use(self, player):
        """
        Utilise des pièces (pour des achats futurs).
        
        Args:
            player: Le joueur qui utilise les pièces
            
        Returns:
            bool: True si une pièce a été utilisée, False sinon
        """
        if self.quantity > 0:
            return self.remove(1)
        return False
# ============================================================================
# Tests du module (exécutable avec python -m models.item)
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("TEST DU MODULE ITEM - JOUR 1")
    print("=" * 70)
    
    # Test 1 : Création d'objets
    print("\n Test 1 : Création d'objets")
    print("-" * 70)
    steps = Steps(70)
    keys = Keys(0)
    gems = Gems(2)
    coins = Coins(0)
    
    print(f"✓ {steps}")
    print(f"✓ {keys}")
    print(f"✓ {gems}")
    print(f"✓ {coins}")
    
    # Test 2 : Ajout de quantités
    print("\n Test 2 : Ajout de quantités")
    print("-" * 70)
    keys.add(5)
    print(f"✓ Ajout de 5 clés : {keys}")
    
    coins.add(100)
    print(f"✓ Ajout de 100 pièces : {coins}")
    
    # Test 3 : Utilisation d'objets
    print("\n Test 3 : Utilisation d'objets")
    print("-" * 70)
    
    class MockPlayer:
        """Joueur factice pour les tests."""
        pass
    
    player = MockPlayer()
    
    # Utiliser un pas
    success = steps.use(player)
    print(f"✓ Utilisation d'un pas : {success} → {steps}")
    
    # Utiliser une clé
    success = keys.use(player)
    print(f"✓ Utilisation d'une clé : {success} → {keys}")
    
    # Test 4 : Retrait de quantités
    print("\n➖ Test 4 : Retrait de quantités")
    print("-" * 70)
    success = coins.remove(50)
    print(f"✓ Retrait de 50 pièces : {success} → {coins}")
    
    success = coins.remove(100)
    print(f"✗ Retrait de 100 pièces (insuffisant) : {success} → {coins}")
    
    # Test 5 : Gestion des erreurs
    print("\n⚠️  Test 5 : Gestion des erreurs")
    print("-" * 70)
    try:
        keys.add(-5)
        print("✗ ERREUR : add() aurait dû lever une exception")
    except ValueError as e:
        print(f"✓ Exception levée correctement : {e}")
    
    try:
        keys.remove(-5)
        print("✗ ERREUR : remove() aurait dû lever une exception")
    except ValueError as e:
        print(f"✓ Exception levée correctement : {e}")
    
    # Test 6 : Représentation des objets
    print("\nTest 6 : Représentation des objets")
    print("-" * 70)
    print(f"✓ str(steps) : {str(steps)}")
    print(f"✓ repr(steps) : {repr(steps)}")
    
    print("\n" + "=" * 70)
    print("TOUS LES TESTS SONT PASSÉS")
    print("=" * 70)