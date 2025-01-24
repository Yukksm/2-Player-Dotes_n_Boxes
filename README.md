# Dots and Boxes - 2 Player Game

## Overview
A classic two-player strategy game implemented using Pygame where players take turns drawing lines to complete boxes.

## Game Rules
- Players take turns drawing lines between adjacent dots
- Use arrow keys to draw lines in the current selected cell
- Complete a box to earn a point and take another turn
- Game ends when all boxes are filled
- Player with the most boxes wins

## Controls
- **Mouse Click**: Select a cell
- **Arrow Keys**: Draw lines
  - UP: Draw top line
  - RIGHT: Draw right line
  - DOWN: Draw bottom line
  - LEFT: Draw left line

## Gameplay
- Player 1 plays as 'X' (green)
- Player 2 plays as 'O' (red)
- Current player's turn is indicated by an underline

## Game End
- When all boxes are filled
- Game over screen shows the winner
- Options:
  - Press 'R' to restart
  - Press 'Q' to quit

## Requirements
- Python 3.x
- Pygame library

## Installation
```bash
pip install pygame
```

## Running the Game
```bash
python dots_and_boxes.py
```


