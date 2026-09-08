# Okay there are a bunch of problems with this code in terms of the movement gthat I had to fix but also there's more stuff to add
# Like the game interprets the hearts and the HP bar as part of the environment, so maybe we might need to define specific class for this
# I had to use Claude even though I was writing the code on my own but I also added comments so for you is also more easy to follow. 
# Basically I defined the variables, the two classes, Player and Rat (right now the player is a yellow dot, we might need to import some design as a png and change the variables within it
# Also spent a lot on defining the movements as some of the rats just got stuck so I had to use Claude a lot to unblock them so this is the main reason why there are pieces of the code that are more complex 
# I also defined the walls because in the first version the player could go through it, as well as the rats, being a little bit weird lol 


import pygame
import random

# Constant variables
BACKGROUND_COLOR = (12, 28, 52)
PLAYER_COLOR = (255, 200, 0)
MAX_WINDOW_SIZE = 700

pygame.init()

# Defining the classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((14, 14))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self, keys, walls, speed):
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -speed
        if keys[pygame.K_RIGHT]:
            dx = speed
        if keys[pygame.K_UP]:
            dy = -speed
        if keys[pygame.K_DOWN]:
            dy = speed

        # Move horizontally and check wall collisions
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall):
                if dx > 0:
                    self.rect.right = wall.left
                elif dx < 0:
                    self.rect.left = wall.right

        # Move vertically and check wall collisions
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall):
                if dy > 0:
                    self.rect.bottom = wall.top
                elif dy < 0:
                    self.rect.top = wall.bottom

        # Never let the player leave the visible window, even through a gap
        self.rect.clamp_ip(pygame.Rect(0, 0, window_width, window_height))

class Rat(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)

        # I tried drawing the rats lol
        pygame.draw.circle(self.image, (110, 110, 110), (10, 10), 8)
        pygame.draw.circle(self.image, (230, 150, 150), (16, 10), 3)

        # For the collision
        self.rect = pygame.Rect(x, y, 8, 8)

        # Movements lol
        self.speed = 4
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(self.directions)
        self.dx, self.dy = random.choice(self.directions)

    def update(self, walls, window_width, window_height):
        # Move forward in the current direction
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        hit_wall = False
        for wall in walls:
            if self.rect.colliderect(wall):
                hit_wall = True
                break

        # Treat the window edges as walls too, so rats never leave the screen
        out_of_bounds = (
            self.rect.left < 0 or self.rect.right > window_width or
            self.rect.top < 0 or self.rect.bottom > window_height
        )

        if hit_wall or out_of_bounds or random.random() < 0.03:
            if hit_wall or out_of_bounds:
                self.rect.x -= self.dx * self.speed
                self.rect.y -= self.dy * self.speed

            valid_directions = []
            for ndx, ndy in self.directions:
                test_rect = self.rect.copy()
                test_rect.x += ndx * self.speed
                test_rect.y += ndy * self.speed

                blocked = False
                if (test_rect.left < 0 or test_rect.right > window_width or
                        test_rect.top < 0 or test_rect.bottom > window_height):
                    blocked = True
                else:
                    for wall in walls:
                        if test_rect.colliderect(wall):
                            blocked = True
                            break
                if not blocked:
                    valid_directions.append((ndx, ndy))

            # Pick a new direction
            if valid_directions:
                self.dx, self.dy = random.choice(valid_directions)
            else:
                self.dx, self.dy = -self.dx, -self.dy

        # Every so often, jump to a random open spot elsewhere in the maze,
        # so rats explore the whole map instead of getting stuck in one area
        if random.random() < 0.003:
            for _ in range(30):  # try up to 30 random spots
                candidate = pygame.Rect(
                    random.randint(0, window_width - self.rect.width),
                    random.randint(0, window_height - self.rect.height),
                    self.rect.width, self.rect.height,
                )
                if not any(candidate.colliderect(wall) for wall in walls):
                    self.rect.topleft = candidate.topleft
                    break

# Loading image
maze = pygame.image.load("maze.png")
original_width, original_height = maze.get_size()

# Scales for the image
scale = min(MAX_WINDOW_SIZE / original_width, MAX_WINDOW_SIZE / original_height)
window_width = int(original_width * scale)
window_height = int(original_height * scale)

# Screen display
screen = pygame.display.set_mode((window_width, window_height))
clock = pygame.time.Clock()

# Preparing the maze image for the game
maze = maze.convert()
maze = pygame.transform.scale(maze, (window_width, window_height))

# Scanning the image to create solid walls:
walls = []
for x in range(0, window_width, 2):
    for y in range(0, window_height, 2):
        # EXCLUSION ZONE: Skip scanning if we are inside the top-left UI area where the HP bar sits
        if x < int(220 * scale) and y < int(55 * scale):
            continue

        color = maze.get_at((x, y))
        # Ignore heart red colors (color.r < 180) so they don't act as solid walls
        if (color.g > 110 and color.b > 110 and color.r < 180) or (
                color.r > 140 and color.g > 140 and color.b > 140 and color.g < 200):
            walls.append(pygame.Rect(x, y, 2, 2))

# CORRECCIÓN DE AJUSTE FINO: Se desplaza ligeramente a la izquierda y abajo para evitar colisión con el borde derecho del hueco
player_start_x = (window_width // 2) - 15
player_start_y = int(12 * scale)
player = Player(player_start_x, player_start_y)

# Create a group of rats
# (coordinates checked against the real walls list so none spawn inside one)
rats = pygame.sprite.Group()
rats.add(
    Rat(28, 76),
    Rat(334, 52),
    Rat(124, 190),
    Rat(310, 232),
    Rat(94, 340),
    Rat(328, 340),
)

# Loops for the game to function in a dynamic way
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of all keyboard buttons and move the player
    keys = pygame.key.get_pressed()
    player.move(keys, walls, 3)

    # Update all the rats positions automatically
    rats.update(walls, window_width, window_height)

    # Draw the screen
    screen.fill(BACKGROUND_COLOR)
    screen.blit(maze, (0, 0))  # This is to draw the maze

    # Drawing the rats
    for rat in rats:
        screen.blit(rat.image, (rat.rect.x - 5, rat.rect.y - 5))

    # Draw the player instance on top of the maze every frame
    screen.blit(player.image, player.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
