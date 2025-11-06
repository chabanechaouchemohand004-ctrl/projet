# ui.py
"""Rendering utilities: draw grid, player, inventory panel and simple modal for 'tirage'."""

import pygame
from constants import *
from typing import Tuple, List
from grid import Grid, Room

FONT_SIZE = 18

def draw_grid(surface: pygame.Surface, grid: Grid, player_pos: Tuple[int,int], cursor_pos: Tuple[int,int]):
    """
    Dessine la grille sur la surface: left area (GRID_AREA_WIDTH x GRID_AREA_HEIGHT).
    - grid: objet Grid
    - player_pos: (row, col)
    - cursor_pos: (row, col)
    """
    area_w = GRID_AREA_WIDTH
    area_h = GRID_AREA_HEIGHT
    cell_w = area_w // grid.cols
    cell_h = area_h // grid.rows

    # Background for grid area
    grid_rect = pygame.Rect(0, 0, area_w, area_h)
    pygame.draw.rect(surface, DARK_GRAY, grid_rect)

    # Cells
    for r in range(grid.rows):
        for c in range(grid.cols):
            x = c * cell_w
            y = r * cell_h
            cell_rect = pygame.Rect(x, y, cell_w, cell_h)
            room = grid.get_room(r, c)
            if room is None:
                pygame.draw.rect(surface, UNKNOWN_ROOM_COLOR, cell_rect)
            else:
                pygame.draw.rect(surface, room.color, cell_rect)

            # grid lines
            pygame.draw.rect(surface, GRID_LINE_COLOR, cell_rect, 1)

    # Player highlight
    pr, pc = player_pos
    prow = pygame.Rect(pc * cell_w, pr * cell_h, cell_w, cell_h)
    pygame.draw.rect(surface, BLUE, prow, 4)

    # Cursor rectangle (selection)
    cr, cc = cursor_pos
    crect = pygame.Rect(cc * cell_w, cr * cell_h, cell_w, cell_h)
    pygame.draw.rect(surface, CURSOR_COLOR, crect, 3)

def draw_inventory(surface: pygame.Surface, inventory, font: pygame.font.Font):
    """
    Dessine le panneau d'inventaire sur la droite.
    """
    x0 = GRID_AREA_WIDTH
    panel = pygame.Rect(x0, 0, PANEL_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(surface, GRAY, panel)

    margin = 12
    y = margin
    # Title
    title_s = font.render("INVENTAIRE", True, BLACK)
    surface.blit(title_s, (x0 + margin, y))
    y += 30

    # Consumables
    lines = [
        f"Pas: {inventory.steps}",
        f"Gemmes: {inventory.gems}",
        f"Clés: {inventory.keys}",
        f"Dés: {inventory.dice}",
        f"Pièces: {inventory.gold}",
    ]
    for line in lines:
        s = font.render(line, True, BLACK)
        surface.blit(s, (x0 + margin, y))
        y += 24

    y += 8
    # Permanents
    perm_title = font.render("Objets permanents:", True, BLACK)
    surface.blit(perm_title, (x0 + margin, y))
    y += 22
    perms = [
        ("Pelle", inventory.shovel),
        ("Marteau", inventory.hammer),
        ("Kit crochetage", inventory.picklock_kit),
        ("Detecteur", inventory.metal_detector),
        ("Patte lapin", inventory.rabbit_foot),
    ]
    for name, have in perms:
        s = font.render(f"{name}: {'✓' if have else '✗'}", True, BLACK)
        surface.blit(s, (x0 + margin, y))
        y += 20

def draw_message(surface: pygame.Surface, font: pygame.font.Font, message: str):
    """Petit texte en bas center."""
    s = font.render(message, True, WHITE)
    rect = s.get_rect(center=(GRID_AREA_WIDTH // 2, WINDOW_HEIGHT - 20))
    surface.blit(s, rect)
