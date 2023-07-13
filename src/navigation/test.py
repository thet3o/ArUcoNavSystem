import pygame
import sys


pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRID_SIZE = 20

rows = height // GRID_SIZE
cols = width // GRID_SIZE
map_data = [[0 for _ in range(cols)] for _ in range(rows)]

# Set some example obstacles
map_data[2][3] = 1  # Obstacle at (3, 2)
map_data[5][8] = 1  # Obstacle at (8, 5)

def draw_map():
    for row in range(rows):
        for col in range(cols):
            color = WHITE if map_data[row][col] == 0 else BLACK
            pygame.draw.rect(screen, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)
    draw_map()
    pygame.display.flip()
