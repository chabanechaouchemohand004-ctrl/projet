"""
Module de gestion des pièces du manoir.

Ce module implémente le système de pièces avec:
- Énumération pour les couleurs de pièces
- Système de rareté et coût en gemmes
- Effets spéciaux d'entrée et de tirage
- Catalogue complet de pièces

Auteur: Chabane Chaouche (213 241 50)
Projet: POO - Blue Prince
"""

from enum import Enum
from .door import Door
import copy
import random

class RoomColor(Enum):
    """
    Énumération des couleurs de pièces.
    
    Chaque couleur représente un type thématique de pièce:
    - BLUE: Pièces standards, bibliothèques
    - YELLOW: Cuisines, nourriture, magasins
    - GREEN: Nature, jardins, ateliers
    - PURPLE: Magie, trésors, études
    - ORANGE: Chance, armureries
    - RED: Secret, danger
    
    Cette énumération illustre l'utilisation des Enum en Python,
    un concept important de la POO.
    """
    BLUE = "blue"
    YELLOW = "yellow"
    GREEN = "green"
    PURPLE = "purple"
    ORANGE = "orange"
    RED = "red"


class Room:
    """
    Représente une pièce du manoir.
    
    Les pièces sont les éléments centraux du jeu. Chaque pièce a:
    - Un nom et une couleur
    - Un niveau de rareté (0 = commun, 3 = très rare)
    - Un coût en gemmes pour la sélectionner
    - Des portes vers d'autres pièces
    - Des objets à collecter
    - Des effets spéciaux optionnels
    
    Attributes:
        name (str): Nom de la pièce
        color (RoomColor): Couleur/thème de la pièce
        rarity (int): Niveau de rareté (0-3)
        gem_cost (int): Coût en gemmes pour sélectionner
        doors (dict): Dictionnaire des portes (direction -> Door)
        items (list): Liste des objets présents
        visited (bool): Indique si la pièce a été visitée
        on_enter_effect (callable): Fonction appelée à l'entrée (optionnel)
        on_draw_effect (callable): Fonction appelée au tirage (optionnel)
    """
    
    def __init__(
        self,
        name: str,
        color: RoomColor,
        rarity: int = 0,
        gem_cost: int = 0,
        items: list = None,
        on_enter_effect=None,
        on_draw_effect=None
    ):
        """
        Initialise une pièce.
        
        Args:
            name: Nom de la pièce
            color: Couleur de la pièce (RoomColor)
            rarity: Niveau de rareté (0=commun, 1=peu commun, 2=rare, 3=très rare)
            gem_cost: Coût en gemmes pour sélectionner cette pièce
            items: Liste d'objets dans la pièce (par défaut vide)
            on_enter_effect: Fonction appelée quand le joueur entre (optionnel)
            on_draw_effect: Fonction appelée quand la pièce est tirée (optionnel)
        """
        self.name = name
        self.color = color
        self.rarity = rarity
        self.gem_cost = gem_cost
        self.doors = {}
        self.items = items if items is not None else []
        self.visited = False
        self.on_enter_effect = on_enter_effect
        self.on_draw_effect = on_draw_effect
    
    def add_door(self, direction: str, door: Door):
        """
        Ajoute une porte à la pièce.
        
        Args:
            direction: Direction de la porte ("north", "south", "east", "west")
            door: Objet Door à ajouter
        """
        self.doors[direction] = door
    
    def get_available_directions(self) -> list:
        """
        Retourne les directions où des portes sont disponibles.
        
        Returns:
            list: Liste des directions avec portes
        """
        return list(self.doors.keys())
    
    def get_probability_weight(self) -> float:
        """
        Calcule le poids de probabilité pour le tirage au sort.
        
        Les pièces plus rares ont un poids plus faible, donc une probabilité
        d'être tirées plus faible. La formule est: 1 / (3^rarity)
        
        Exemples:
        - Rareté 0 (commun): poids = 1.0
        - Rareté 1 (peu commun): poids = 0.333
        - Rareté 2 (rare): poids = 0.111
        - Rareté 3 (très rare): poids = 0.037
        
        Returns:
            float: Poids de probabilité
        """
        return 1.0 / (3 ** self.rarity)
    
    def can_be_placed(self, position: tuple, manor_size: tuple) -> bool:
        """
        Vérifie si la pièce peut être placée à une position donnée.
        
        Args:
            position: Position (row, col) dans le manoir
            manor_size: Taille du manoir (height, width)
            
        Returns:
            bool: True si la position est valide, False sinon
        """
        row, col = position
        height, width = manor_size
        return 0 <= row < height and 0 <= col < width
    
    def enter(self, player):
        """
        Actions exécutées quand le joueur entre dans la pièce.
        
        Cette méthode:
        1. Marque la pièce comme visitée
        2. Applique l'effet d'entrée si présent
        3. Donne les objets de la pièce au joueur
        
        Args:
            player: Le joueur qui entre dans la pièce
        """
        if not self.visited:
            self.visited = True
            
            # Applique l'effet d'entrée si présent
            if self.on_enter_effect:
                self.on_enter_effect(player, self)
            
            # Donne les objets de la pièce
            self._give_room_items(player)
    
    def on_draw(self, player):
        """
        Actions exécutées quand la pièce est tirée au sort.
        
        Certaines pièces ont des effets qui se déclenchent au moment
        où elles sont proposées au joueur lors de la sélection.
        
        Args:
            player: Le joueur qui tire la pièce
        """
        if self.on_draw_effect:
            self.on_draw_effect(player, self)
    
    def _give_room_items(self, player):
        """
        Donne les objets de la pièce au joueur.
        
        Cette méthode gère différents types d'objets:
        - Objets consommables standards (coins, keys, gems, dice, steps)
        - Nourriture (food_apple, food_banana, etc.)
        - Objets permanents (permanent_shovel, permanent_hammer, etc.)
        - Coffres avec récompenses aléatoires
        
        Args:
            player: Le joueur qui reçoit les objets
        """
        for item in self.items:
            if item.startswith("food_"):
                # Nourriture: retire le préfixe "food_"
                food_type = item.replace("food_", "")
                player.inventory.add_food(food_type, 1)
            
            elif item.startswith("permanent_"):
                # Objet permanent: retire le préfixe "permanent_"
                permanent_type = item.replace("permanent_", "")
                player.inventory.add_permanent_item(permanent_type)
            
            elif item == "chest":
                # Coffre: donne une récompense aléatoire
                import random
                rewards = [
                    ("coins", random.randint(10, 30)),
                    ("keys", random.randint(1, 3)),
                    ("gems", random.randint(1, 2)),
                    ("dice", 1)
                ]
                reward_type, amount = random.choice(rewards)
                player.inventory.add_item(reward_type, amount)
            
            else:
                # Objet consommable standard
                player.inventory.add_item(item, 1)
    
    def __str__(self):
        """Représentation textuelle de la pièce."""
        return f"{self.name} ({self.color.value}, rarity {self.rarity}, cost {self.gem_cost} gems)"
    
    def __repr__(self):
        """Représentation pour le débogage."""
        return f"Room('{self.name}', {self.color}, rarity={self.rarity})"


def create_room_catalog() -> list:
    """
    Crée le catalogue complet de pièces disponibles dans le jeu.
    
    Cette fonction utilise le pattern Factory pour créer toutes les pièces
    du jeu avec leurs caractéristiques et effets spécifiques.
    
    Organisation par rareté:
    - Rareté 0 (communes): 0 gemmes
    - Rareté 1 (peu communes): 1 gemme
    - Rareté 2 (rares): 2 gemmes
    - Rareté 3 (très rares): 3 gemmes
    
    Returns:
        list: Liste de toutes les pièces disponibles
    """
    catalog = []
    
    # =========================================================================
    # PIÈCES COMMUNES (rareté 0) - Coût: 0 gemmes
    # =========================================================================
    
    def library_effect(player, room):
        """Bibliothèque: donne des connaissances (pièces d'or)."""
        player.inventory.add_item("coins", 15)
    
    catalog.append(Room(
        "Library", RoomColor.BLUE, 0, 0,
        ["coins", "coins", "coins"],
        on_enter_effect=library_effect
    ))
    
    catalog.append(Room(
        "Kitchen", RoomColor.YELLOW, 0, 0,
        ["food_apple", "food_banana"]
    ))
    
    catalog.append(Room(
        "Hallway", RoomColor.BLUE, 0, 0,
        ["keys"]
    ))
    
    catalog.append(Room(
        "Storage Room", RoomColor.GREEN, 0, 0,
        ["chest"]
    ))
    
    catalog.append(Room(
        "Guard Room", RoomColor.ORANGE, 0, 0,
        ["keys", "keys"]
    ))
    
    catalog.append(Room(
        "Pantry", RoomColor.YELLOW, 0, 0,
        ["food_cake"]
    ))
    
    # =========================================================================
    # PIÈCES PEU COMMUNES (rareté 1) - Coût: 1 gemme
    # =========================================================================
    
    catalog.append(Room(
        "Bedroom", RoomColor.GREEN, 1, 1,
        ["chest", "coins"]
    ))
    
    catalog.append(Room(
        "Study", RoomColor.PURPLE, 1, 1,
        ["coins", "keys", "gems"]
    ))
    
    catalog.append(Room(
        "Armory", RoomColor.ORANGE, 1, 1,
        ["permanent_hammer"]
    ))
    
    catalog.append(Room(
        "Wine Cellar", RoomColor.RED, 1, 1,
        ["food_meal"]
    ))
    
    def workshop_effect(player, room):
        """Atelier: donne une pelle."""
        player.inventory.add_permanent_item("shovel")
    
    catalog.append(Room(
        "Workshop", RoomColor.GREEN, 1, 1,
        on_enter_effect=workshop_effect
    ))
    
    def shop_effect(player, room):
        """Magasin: permet d'acheter des objets."""
        # L'interaction se fera via l'interface de jeu
        pass
    
    catalog.append(Room(
        "Shop", RoomColor.YELLOW, 1, 1,
        on_enter_effect=shop_effect
    ))
    
    # =========================================================================
    # PIÈCES RARES (rareté 2) - Coût: 2 gemmes
    # =========================================================================
    
    def treasury_effect(player, room):
        """Trésorerie: richesses abondantes."""
        player.inventory.add_item("coins", 50)
        player.inventory.add_item("gems", 2)
    
    catalog.append(Room(
        "Treasury", RoomColor.PURPLE, 2, 2,
        ["chest", "chest"],
        on_enter_effect=treasury_effect
    ))
    
    catalog.append(Room(
        "Master Bedroom", RoomColor.GREEN, 2, 2,
        ["food_meal", "permanent_lockpick_kit"]
    ))
    
    def vault_effect(player, room):
        """Coffre-fort: grande quantité de pièces."""
        player.inventory.add_item("coins", 40)
    
    catalog.append(Room(
        "Vault", RoomColor.BLUE, 2, 2,
        on_enter_effect=vault_effect
    ))
    
    # =========================================================================
    # PIÈCES TRÈS RARES (rareté 3) - Coût: 3 gemmes
    # =========================================================================
    
    def dragon_hoard_effect(player, room):
        """Trésor du dragon: récompense ultime."""
        player.inventory.add_item("coins", 100)
        player.inventory.add_item("gems", 3)
        player.inventory.add_item("keys", 5)
    
    catalog.append(Room(
        "Dragon's Hoard", RoomColor.RED, 3, 3,
        on_enter_effect=dragon_hoard_effect
    ))
    
    return catalog

def create_45_rooms_catalog() -> list:
    """
    Crée un catalogue de 45 pièces pour le jeu.
    
    Returns:
        list: Liste de 45 objets Room
    """
    original_catalog = create_room_catalog()
    all_rooms = original_catalog.copy()
    
    # Pièces à dupliquer en priorité
    common_rooms_to_duplicate = [
        "Library", "Kitchen", "Hallway", "Storage Room", 
        "Pantry", "Guard Room", "Bedroom", "Study", "Workshop"
    ]
    
    # Dupliquer jusqu'à atteindre 45
    copy_number = 1
    while len(all_rooms) < 45:
        for room_name in common_rooms_to_duplicate:
            if len(all_rooms) >= 45:
                break
                
            original = next((r for r in original_catalog if r.name == room_name), None)
            if original:
                new_room = copy.deepcopy(original)
                new_room.name = f"{original.name} {copy_number}"
                new_room.visited = False
                all_rooms.append(new_room)
        
        copy_number += 1
    
    return all_rooms