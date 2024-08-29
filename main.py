import pygame
import random
import sqlite3
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Game dimensions
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 8)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

COLORS = [CYAN, YELLOW, PURPLE, BLUE, ORANGE, GREEN, RED]

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Initialize the font
font = pygame.font.Font(None, 36)

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = COLORS[SHAPES.index(self.shape)]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

class Game:
    def __init__(self):
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False

    def new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        if self.check_collision(self.current_piece):
            self.game_over = True

    def check_collision(self, piece):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    if (piece.x + x < 0 or piece.x + x >= GRID_WIDTH or
                        piece.y + y >= GRID_HEIGHT or
                        self.grid[piece.y + y][piece.x + x] != BLACK):
                        return True
        return False

    def lock_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece.y + y][self.current_piece.x + x] = self.current_piece.color
        self.clear_lines()
        self.new_piece()

    def clear_lines(self):
        lines_to_clear = [i for i, row in enumerate(self.grid) if all(cell != BLACK for cell in row)]
        for line in lines_to_clear:
            del self.grid[line]
            self.grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
        self.score += len(lines_to_clear) ** 2 * 100
        self.lines_cleared += len(lines_to_clear)
        self.level = self.lines_cleared // 10 + 1

    def move(self, dx, dy):
        self.current_piece.x += dx
        self.current_piece.y += dy
        if self.check_collision(self.current_piece):
            self.current_piece.x -= dx
            self.current_piece.y -= dy
            if dy > 0:
                self.lock_piece()

    def rotate_piece(self):
        original_shape = self.current_piece.shape
        self.current_piece.rotate()
        if self.check_collision(self.current_piece):
            self.current_piece.shape = original_shape

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('tetris_scores.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS scores
                              (name TEXT, score INTEGER)''')
        self.conn.commit()

    def add_score(self, name, score):
        self.cursor.execute("INSERT INTO scores VALUES (?, ?)", (name, score))
        self.conn.commit()

    def get_top_scores(self, limit=10):
        self.cursor.execute("SELECT * FROM scores ORDER BY score DESC LIMIT ?", (limit,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_game(game):
    screen.fill(BLACK)
    for y, row in enumerate(game.grid):
        for x, color in enumerate(row):
            pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1))

    for y, row in enumerate(game.current_piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, game.current_piece.color,
                                 ((game.current_piece.x + x) * BLOCK_SIZE,
                                  (game.current_piece.y + y) * BLOCK_SIZE,
                                  BLOCK_SIZE - 1, BLOCK_SIZE - 1))

    # Draw next piece
    next_piece_text = font.render("Next:", True, WHITE)
    screen.blit(next_piece_text, (GRID_WIDTH * BLOCK_SIZE + 20, 20))
    for y, row in enumerate(game.next_piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, game.next_piece.color,
                                 (GRID_WIDTH * BLOCK_SIZE + 20 + x * BLOCK_SIZE,
                                  60 + y * BLOCK_SIZE,
                                  BLOCK_SIZE - 1, BLOCK_SIZE - 1))

    # Draw score and level
    score_text = font.render(f"Score: {game.score}", True, WHITE)
    level_text = font.render(f"Level: {game.level}", True, WHITE)
    screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 20, 180))
    screen.blit(level_text, (GRID_WIDTH * BLOCK_SIZE + 20, 220))

def draw_menu():
    screen.fill(BLACK)
    title = font.render("TETRIS", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

    start_button = Button(SCREEN_WIDTH // 2 - 100, 150, 200, 50, "Start Game", WHITE, BLACK)
    ranking_button = Button(SCREEN_WIDTH // 2 - 100, 250, 200, 50, "View Ranking", WHITE, BLACK)
    exit_button = Button(SCREEN_WIDTH // 2 - 100, 350, 200, 50, "Exit", WHITE, BLACK)

    start_button.draw(screen)
    ranking_button.draw(screen)
    exit_button.draw(screen)

    return start_button, ranking_button, exit_button

def draw_ranking(scores):
    screen.fill(BLACK)
    title = font.render("Top Scores", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))

    for i, (name, score) in enumerate(scores):
        text = font.render(f"{i+1}. {name}: {score}", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 100 + i * 40))

    back_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Back to Menu", WHITE, BLACK)
    back_button.draw(screen)

    return back_button

def main():
    clock = pygame.time.Clock()
    game = Game()
    db = Database()

    fall_time = 0
    fall_speed = 0.5
    fall_speed_fast = 0.05

    state = "menu"

    running = True
    while running:
        if state == "menu":
            start_button, ranking_button, exit_button = draw_menu()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if start_button.is_clicked(event.pos):
                        state = "game"
                        game = Game()
                    elif ranking_button.is_clicked(event.pos):
                        state = "ranking"
                    elif exit_button.is_clicked(event.pos):
                        running = False

        elif state == "game":
            fall_time += clock.get_rawtime()
            clock.tick()

            if fall_time >= fall_speed * 1000:
                game.move(0, 1)
                fall_time = 0

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        game.move(-1, 0)
                    elif event.key == K_RIGHT:
                        game.move(1, 0)
                    elif event.key == K_DOWN:
                        fall_speed = fall_speed_fast
                    elif event.key == K_UP:
                        game.rotate_piece()
                    elif event.key == K_SPACE:
                        while not game.check_collision(game.current_piece):
                            game.move(0, 1)
                        game.move(0, -1)
                        game.lock_piece()
                elif event.type == KEYUP:
                    if event.key == K_DOWN:
                        fall_speed = 0.5 - (game.level - 1) * 0.05

            if game.game_over:
                name = input("Game Over! Enter your name: ")
                db.add_score(name, game.score)
                state = "menu"
            else:
                draw_game(game)

        elif state == "ranking":
            back_button = draw_ranking(db.get_top_scores())
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    if back_button.is_clicked(event.pos):
                        state = "menu"

        pygame.display.flip()

    db.close()
    pygame.quit()

if __name__ == "__main__":
    main()