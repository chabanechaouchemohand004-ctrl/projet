# game_manager.py
"""GameManager: orchestrates the game, events, update and draw calls."""

import pygame
import random
from constants import *
from grid import Grid, Room
from player import Player
from inventory import Inventory
from ui import draw_grid, draw_inventory, draw_message

class GameManager:
    """Classe principale du jeu (GameManager)."""

    def __init__(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT):
        pygame.init()
        pygame.display.set_caption("Blue Prince - Prototype POO")
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.running = True

        # core model
        self.grid = Grid(rows=GRID_ROWS, cols=GRID_COLS)
        self.inventory = Inventory()
        # Player starts where grid placed entrance (bottom-left)
        start_r = self.grid.rows - 1
        start_c = 0
        self.player = Player(start_row=start_r, start_col=start_c, inventory=self.inventory)

        # UI / fonts
        self.font = pygame.font.SysFont("arial", 16)
        self.large_font = pygame.font.SysFont("arial", 20, bold=True)

        # State
        self.message = "ZQSD pour déplacer le curseur. Espace pour entrer. Entrée pour choisir une salle."
        self.in_modal = False
        self.modal_options = []  # list of Room choices
        self.selected_choice_idx = 0
        self.modal_target_pos = None  # where we will place the chosen room

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if self.in_modal:
                    self._handle_modal_key(event.key)
                    continue

                # Movement of cursor: Z (up), S (down), Q (left), D (right)
                if event.key in (pygame.K_z, pygame.K_UP):
                    self.player.move_cursor(-1, 0, self.grid.rows, self.grid.cols)
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    self.player.move_cursor(1, 0, self.grid.rows, self.grid.cols)
                elif event.key in (pygame.K_q, pygame.K_LEFT):
                    self.player.move_cursor(0, -1, self.grid.rows, self.grid.cols)
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    self.player.move_cursor(0, 1, self.grid.rows, self.grid.cols)

                elif event.key == pygame.K_SPACE:
                    # Try to move into selected tile if adjacent
                    sr, sc = self.player.sel_row, self.player.sel_col
                    if self.player.can_move_to(sr, sc):
                        # if discovered, just move
                        if self.grid.is_discovered(sr, sc):
                            self.player.move_to(sr, sc)
                            self.message = f"Déplacé en ({sr},{sc}). Pas restants: {self.inventory.steps}"
                        else:
                            # open door: tirage de 3 salles aléatoires (simplified)
                            self.open_door_modal(sr, sc)
                    else:
                        self.message = "La destination doit être adjacente au joueur."

                elif event.key == pygame.K_RETURN:
                    # (Dans l'écran de tirage, ENTER confirm; ici on use ENTER pour réinitialiser curseur)
                    self.player.reset_cursor_to_player()
                    self.message = "Curseur recentré."

                elif event.key == pygame.K_p:
                    self.running = False

    def _handle_modal_key(self, key):
        # navigation left/right with q/d or arrows, confirm enter, cancel esc
        if key in (pygame.K_q, pygame.K_LEFT):
            self.selected_choice_idx = max(0, self.selected_choice_idx - 1)
        elif key in (pygame.K_d, pygame.K_RIGHT):
            self.selected_choice_idx = min(len(self.modal_options) - 1, self.selected_choice_idx + 1)
        elif key == pygame.K_RETURN:
            # attempt to choose the option (check gem cost)
            choice = self.modal_options[self.selected_choice_idx]
            cost = choice.cost_gems
            if cost > 0:
                ok = self.inventory.use_gems(cost)
                if not ok:
                    self.message = f"Pas assez de gemmes pour choisir {choice.name} (coût {cost})."
                    return
            # place room and close modal
            tr, tc = self.modal_target_pos
            self.grid.set_room(tr, tc, choice)
            # move player into that room immediately and spend 1 step
            self.player.move_to(tr, tc)
            self.in_modal = False
            self.modal_options = []
            self.selected_choice_idx = 0
            self.modal_target_pos = None
            self.message = f"Salle '{choice.name}' choisie et placée en ({tr},{tc})."
        elif key == pygame.K_ESCAPE:
            # cancel
            self.in_modal = False
            self.modal_options = []
            self.message = "Choix annulé."

    def open_door_modal(self, target_r:int, target_c:int):
        """Crée 3 options aléatoires pour la salle à placer."""
        choices = []
        # Simplified random generator: colors and costs; ensure at least one cost 0
        for i in range(3):
            rarity = random.choice([0, 1, 2, 3])  # placeholder
            # cost depends on rarity sometimes
            cost = 0 if random.random() < 0.5 else random.choice([1,2,3])
            name = f"Room_{random.randint(1,200)}"
            color = (random.randint(80,230), random.randint(60,220), random.randint(60,220))
            choices.append(Room(name=name, color=color, cost_gems=cost))
        # ensure at least one cost 0
        if all(c.cost_gems > 0 for c in choices):
            choices[0].cost_gems = 0

        self.in_modal = True
        self.modal_options = choices
        self.selected_choice_idx = 0
        self.modal_target_pos = (target_r, target_c)
        self.message = "Choisissez une salle avec Q/D ou flèches et validez avec Entrée."

    def update(self):
        # game over condition
        if self.inventory.is_dead():
            self.message = "Vous n'avez plus de pas. Partie terminée."
            # we stop the game loop after short delay (or immediately)
            self.running = False

    def draw(self):
        # clear
        self.screen.fill(BLACK)

        # draw grid and UI
        draw_grid(self.screen, self.grid, (self.player.row, self.player.col), (self.player.sel_row, self.player.sel_col))
        draw_inventory(self.screen, self.inventory, self.font)
        draw_message(self.screen, self.font, self.message)

        # If modal open, draw choices on top center
        if self.in_modal and self.modal_options:
            self._draw_modal()

    def _draw_modal(self):
        # semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0,0,0,180))
        self.screen.blit(overlay, (0,0))

        # modal rect
        w, h = 520, 220
        x = (WINDOW_WIDTH - w) // 2
        y = (WINDOW_HEIGHT - h) // 2
        pygame.draw.rect(self.screen, WHITE, (x, y, w, h))
        pygame.draw.rect(self.screen, BLACK, (x, y, w, h), 3)

        # draw three choice boxes
        spacing = 20
        box_w = (w - 4*spacing) // 3
        box_h = h - 80
        bx = x + spacing
        by = y + 40

        for idx, room in enumerate(self.modal_options):
            rect = pygame.Rect(bx + idx*(box_w + spacing), by, box_w, box_h)
            pygame.draw.rect(self.screen, room.color, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 2)
            # name & cost text
            txt = self.font_render(room.name + f" (cost {room.cost_gems})")
            self.screen.blit(txt, (rect.x + 6, rect.y + 6))
            # highlight selection
            if idx == self.selected_choice_idx:
                pygame.draw.rect(self.screen, CURSOR_COLOR, rect, 4)

    def font_render(self, text:str):
        return self.font.render(text, True, BLACK)

    def run(self):
        """Boucle principale du jeu."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
