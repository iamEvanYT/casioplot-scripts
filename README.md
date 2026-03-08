# Casioplot Scripts

A collection of classic games and useful scripts implemented in MicroPython for Casio graphing calculators using the `casioplot` module.

## Games

| Script | Description |
|--------|-------------|
| `snake.py` | Classic Snake game |
| `tetris.py` | Tetris |
| `pac-man.py` | Pac-Man |
| `minesweeper.py` | Minesweeper |
| `blackjack.py` + `bj_ui.py` | Blackjack card game with graphical cards, pixel-art suit symbols, betting, splitting, insurance, and doubling down |
| `raycaster/` | First-person 3D raycaster using AABB slab and sphere intersection tests |

## Blackjack

Blackjack is a two-file project. Copy both files to your calculator:

- `blackjack.py` - Game logic, betting, split/insurance/double-down flow
- `bj_ui.py` - Card rendering with drawn card shapes, 5x5 pixel-art suit bitmaps, styled buttons, and colored results

**Controls:** Left/Right to select, OK to confirm, Back to exit.

## Raycaster

The raycaster is a multi-file project. Copy all three files to your calculator:

- `raycaster/main.py` - Entry point, input handling, collision detection
- `raycaster/engine.py` - Ray-AABB slab method, ray-sphere analytic test, column renderer with distance fog
- `raycaster/map_data.py` - Scene definition: 13 AABB walls, 4 sphere pillars, 5 wall color types

**Controls:** Arrow keys to move/turn, OK to start, Back to exit.
