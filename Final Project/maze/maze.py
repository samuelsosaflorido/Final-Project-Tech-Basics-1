import pygame

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 300
BACKGROUND_COLOR = (255, 255, 255)

# Setup
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("maze.py")
clock = pygame.time.Clock()

maze = pygame.image.load("maze.png").convert()
maze = pygame.transform.scale(maze, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Main loop: without this, the window opens and closes instantly
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)
    screen.blit(maze, (0, 0))
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
