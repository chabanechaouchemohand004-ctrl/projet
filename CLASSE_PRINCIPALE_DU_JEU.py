import pygame

class BluePrinceGame:
    """
    Classe principale gérant la boucle de jeu.
    Cours CM4 : Architecture MVC (Model-View-Controller).
    """
    
    def __init__(self):
        """Initialise le jeu."""
        # Initialisation de Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Blue Prince")
        self.clock = pygame.time.Clock()
        
        # Initialisation du modèle
        self.manor = Manor()
        self.player = Player(self.manor.entrance_position)
        self.room_catalog = self.create_room_catalog()
        self.random_manager = RandomManager()
        
        # État du jeu
        self.running = True
        self.game_over = False
        self.victory = False
    
    def create_room_catalog(self) -> list:
        """
        Crée le catalogue de pièces disponibles.
        Section 2.3 : Catalogue de pièces.
        
        Returns:
            list: Liste des pièces disponibles
        """
        catalog = []
        
        # Exemple : Entrance Hall
        entrance = Room(
            name="Entrance Hall",
            color=RoomColor.BLUE,
            rarity=0,
            gem_cost=0,
            doors={'north': Door(Door.UNLOCKED)}
        )
        catalog.append(entrance)
        
        # Exemple : Vault (Figure 3a)
        vault = Room(
            name="Vault",
            color=RoomColor.BLUE,
            rarity=3,
            gem_cost=3,
            doors={'south': Door()},
            items=['coins'] * 40  # 40 pièces d'or
        )
        catalog.append(vault)
        
        # TODO: Ajouter toutes les autres pièces du wiki
        
        return catalog
    
    def handle_door_opening(self, direction: str):
        """
        Gère l'ouverture d'une porte.
        Section 2.7 : Tirage de pièces.
        
        Args:
            direction (str): Direction de la porte ('north', 'south', 'east', 'west')
        """
        current_room = self.manor.get_room(self.player.position)
        
        if direction not in current_room.doors:
            print("No door in this direction!")
            return
        
        door = current_room.doors[direction]
        
        # Tente d'ouvrir la porte
        if door.is_open:
            # Pièce déjà découverte, se déplace directement
            new_pos = self.get_adjacent_position(self.player.position, direction)
            self.player.move(new_pos, self.manor)
        else:
            # Porte fermée, essaye de l'ouvrir
            if door.open(self.player):
                # Tire 3 pièces pour le choix
                drawn_rooms = self.random_manager.draw_rooms(self.room_catalog, 3)
                # Affiche le choix au joueur
                self.show_room_selection(drawn_rooms, direction)
    
    def show_room_selection(self, rooms: list, direction: str):
        """
        Affiche l'interface de sélection de pièce.
        
        Args:
            rooms (list): Liste des pièces proposées
            direction (str): Direction de la porte ouverte
        """
        # TODO: Implémenter l'interface pygame
        pass
    
    def get_adjacent_position(self, position: tuple, direction: str) -> tuple:
        """
        Calcule la position adjacente dans une direction.
        
        Args:
            position (tuple): Position actuelle
            direction (str): Direction
        
        Returns:
            tuple: Nouvelle position
        """
        row, col = position
        
        if direction == 'north':
            return (row - 1, col)
        elif direction == 'south':
            return (row + 1, col)
        elif direction == 'east':
            return (row, col + 1)
        elif direction == 'west':
            return (row, col - 1)
        
        return position
    
    def update(self):
        """Met à jour l'état du jeu."""
        # Vérifie victoire
        if self.player.has_won(self.manor):
            self.victory = True
            self.game_over = True
        
        # Vérifie défaite
        if self.player.has_lost():
            self.victory = False
            self.game_over = True
    
    def render(self):
        """Affiche le jeu."""
        self.screen.fill((0, 0, 0))  # Fond noir
        
        # TODO: Dessiner la grille du manoir
        # TODO: Dessiner l'inventaire
        # TODO: Dessiner le curseur
        
        pygame.display.flip()
    
    def run(self):
        """Boucle principale du jeu."""
        while self.running:
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_input(event.key)
            
            # Mise à jour
            self.update()
            
            # Affichage
            self.render()
            
            # FPS
            self.clock.tick(60)
        
        pygame.quit()
    
    def handle_input(self, key):
        """
        Gère les entrées clavier.
        
        Args:
            key: Touche pressée (pygame.K_*)
        """
        if key == pygame.K_z:  # Nord
            self.handle_door_opening('north')
        elif key == pygame.K_s:  # Sud
            self.handle_door_opening('south')
        elif key == pygame.K_q:  # Ouest
            self.handle_door_opening('west')
        elif key == pygame.K_d:  # Est
            self.handle_door_opening('east')


# Point d'entrée
if __name__ == "__main__":
    game = BluePrinceGame()
    game.run()
```

---

## **📊 DIAGRAMME UML (Pour Syscom/ISI/ROB/MeDH)**
```
┌─────────────────────┐
│      <<abstract>>   │
│        Item         │
├─────────────────────┤
│ - name: str         │
│ - description: str  │
├─────────────────────┤
│ + __init__()        │
│ + use(): void       │
└─────────────────────┘
          △
          │ (héritage)
          │
    ┌─────┴──────┬──────────────┐
    │            │              │
┌───┴──────┐ ┌──┴──────┐ ┌────┴────┐
│Consumable│ │Permanent│ │  Food   │
│   Item   │ │  Item   │ │         │
└──────────┘ └─────────┘ └─────────┘


┌──────────────────┐      ┌──────────────┐
│     Player       │◆────→│  Inventory   │
├──────────────────┤      ├──────────────┤
│- position: tuple │      │- steps: Steps│
├──────────────────┤      │- coins: Coins│
│+ move(): bool    │      │- gems: Gems  │
│+ has_won(): bool │      │- keys: Keys  │
└──────────────────┘      └──────────────┘


┌──────────────────┐      ┌──────────────┐
│      Manor       │◇────→│     Room     │
├──────────────────┤      ├──────────────┤
│- grid: list[][]  │      │- name: str   │
│- height: int     │      │- color: Enum │
│- width: int      │      │- rarity: int │
├──────────────────┤      │- doors: dict │
│+ place_room()    │      ├──────────────┤
│+ get_room()      │      │+ enter()     │
└──────────────────┘      │+ collect()   │
                          └──────────────┘