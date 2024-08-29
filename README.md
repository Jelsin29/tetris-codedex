# Tetris Game

## Project Overview

This Tetris game is the final project for "The Legend of Python" course. It demonstrates the application of various Python programming concepts learned throughout the course.

## Features

- Classic Tetris gameplay
- Score tracking and level progression
- Next piece preview
- High score system with SQLite database integration
- Menu system with game start, rankings, and exit options

## Requirements

To run this game, you'll need:

- Python 3.x
- Pygame library
- SQLite3 (It comes with Python)

## Installation

1. Ensure you have Python installed on your system.
2. Install Pygame by running:
   ```
   pip install pygame
   ```
3. Clone this repository or download the source code.

## How to Play

1. Run the game by executing the Python script:
   ```
   python tetris.py
   ```
2. Use the arrow keys to control the falling pieces:
   - Left/Right: Move piece horizontally
   - Down: Soft drop
   - Up: Rotate piece
   - Space: Hard drop (instantly places the piece at the bottom)
3. Clear lines to score points and increase your level.
4. The game ends when the pieces stack up to the top of the play area.
5. You can register you points in the terminal after you lose.

## Code Structure

- `Tetromino` class: Represents each Tetris piece
- `Game` class: Manages the game state and logic
- `Database` class: Handles high score storage and retrieval
- `Button` class: Creates clickable buttons for the menu system
- Main game loop: Handles events, updates game state, and renders graphics

## Acknowledgements

This project was created as the final assignment for "The Legend of Python" course. Special thanks to the course instructors and fellow students for their support and inspiration.

## License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).
