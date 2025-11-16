<<<<<<< HEAD
# Blue Prince — Python OOP Project (Simplified Game Version) by Juan, Christian and Mohand
A simplified re-implementation of **Blue Prince**, developed as part of a university Object-Oriented Programming project.  
The game is written in **Python 3.10+**, using **Pygame** for the graphical interface, and follows a clean modular architecture based on classes and managers.

---

## Game Overview

The game takes place inside a **mansion (manoir)** represented as a **5 × 9 grid** of rooms.  
The player starts at the bottom-left corner of the mansion and can explore by opening doors, discovering new rooms, and collecting or using various items.

### Core Mechanics:
- Move using **ZQSD** (or arrow keys).
- Select a tile with the cursor and enter it using **SPACE**.
- When entering an *undiscovered* tile, you draw **three random rooms** and must choose one.
- Moving between rooms consumes **steps** (initially 70).
- Items such as **gems, keys, dice, gold, food, and permanent tools** modify gameplay.
- The **Exit** is located in the **top-center** of the grid — reaching it ends the game.

---

## Features Implemented

### ✔ Object-Oriented Architecture
- `GameManager` for overall control (loop, events, updates, drawing)
- `Grid` for room placement, discovery system, and exit management
- `Room` class describing room type, image, and effects
- `Inventory` storing consumables and permanent items
- `Player` handling movement and cursor selection
- `UI` module for drawing the grid, inventory panel, modal dialogues
- `Effects` module applying logical effects of rooms (food, treasure, trap, dice, etc.)

### ✔ Gameplay Mechanics
- Movement with steps consumption  
- Random room drawing modal  
- Inventory gain/loss  
- Food items restoring steps  
- Permanent items unlocking new interactions  
- Dice allowing re-roll of room choices  
- Exit detection and completion  

### ✔ Visual Interface (Pygame)
- 800×600 window (configurable)  
- Grid display (5×9)  
- Colored or image-based rooms  
- Cursor highlight + player indicator  
- Inventory panel with icons  
- Modal room selection overlay  

### ✔ Asset System
All graphical, audio, and font files are stored inside:

### ✔ Menu Inteface
- Its possible to save the game  
- Its possible to pause



# ============================================================================
# STRUCTURE DES DOSSIERS DU PROJET
# ============================================================================
"""
blue_prince/
│
├── main.py                    
├── game_manager.py            
├── grid.py                    
├── player.py                  
├── inventory.py               
├── effects.py                 
├── ui.py                      
├── constants.py               
├── menu.py                    
├── save_manager.py            
├── item.py                    
├── room.py                    
├── door.py                    
├── rooms_catalog.py           
├── sound_manager.py           
│
├── assets/
│   ├── rooms/                 
│   │   ├── entry.png          
│   │   ├── sortie.png         
│   │   ├── bibliotheque.png   
│   │   ├── atelier.png        
│   │   ├── salle_tresor.png   
│   │   ├── piege.png          
│   │   ├── coffre.png         
│   │   ├── casiers.png        
│   │   ├── creuser.png        
│   │   ├── room_default.png   
│   │   ├── bedroom.png        
│   │   ├── corridor.png       
│   │   └── ...                
│   │
│   ├── icons/                 
│   │   ├── steps.png          
│   │   ├── gem.png            
│   │   ├── key.png            
│   │   ├── dice.png           
│   │   ├── gold.png           
│   │   ├── pelle.png          
│   │   ├── marteau.png        
│   │   ├── picklock.png       
│   │   ├── detecteur.png      
│   │   └── pattelapin.png     
│   │
│   ├── fonts/                 
│   │   └── OpenSans-Regular.ttf
│   │
│   └── audio/                 
│       ├── main_theme.mp3     
│       └── effects/           
│
└── saves/                     
    └── save.json              
"""
=======
# Blue Prince - Projet POO 2025

## Jour 1 - Structure initiale

### Fonctionnalités implémentées
- Classes de base pour les objets (Item, ConsumableItem)
- Types d'objets spécifiques (Steps, Keys, Gems, Coins)
- Système d'inventaire basique

### Structure actuelle
```
blue-prince/
├── models/
│   ├── __init__.py
│   ├── item.py
│   └── inventory.py
└── README.md
```

### TODO
- [ ] Système de portes
- [ ] Système de pièces
- [ ] Classe joueur
<<<<<<< HEAD
- [ ] Interface graphique
=======
- [ ] Interface graphique
>>>>>>> c343a1a982c6bf044146c116f2111bc16a1b61fa
>>>>>>> 77d1b6072328da5125230b02303c13432aa1f6e2
