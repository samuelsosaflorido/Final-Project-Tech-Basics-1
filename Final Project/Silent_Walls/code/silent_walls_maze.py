# by Samuel Domingo Sosa Florido
# I had to use a lot of Gemini to help me during this process
# It was extremely challenging to make the rat moving across the maze so I had to test it over and over
# Most of the previous maze was taken as a basis and had to refactor a lot everything
# With the designs and previous code (that also was used for the structure of this new code) made by Karo and Kathi the whole area improved a lot and it was even better in terms of implementing the mechanics
# After fixing a lot of the structure I would say that it was an interesting learning experience but extremely challenging at the same

import math
import os
import random
import sys
from collections import deque
import pygame

# Window settings matching maze aspect ratio
WINDOW_WIDTH = 980
WINDOW_HEIGHT = 400
FPS = 60

PLAYER_MAX_HEALTH = 5
RAT_MAX_HEALTH = 5
ATTACK_COOLDOWN_FRAMES = 20
RAT_HIT_COOLDOWN_FRAMES = 60

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Silent Walls - The Maze")
clock = pygame.time.Clock()

# Load background
bg_filenames = ["maze_background.png", "maze_background.jpg", "maze.png"]
maze_file = None
for name in bg_filenames:
    for folder in [BASE_DIR, "", os.getcwd()]:
        full_p = os.path.join(folder, name) if folder else name
        if os.path.exists(full_p):
            maze_file = full_p
            break
    if maze_file:
        break

if not maze_file:
    print("Error: maze image not found!")
    pygame.quit()
    sys.exit()

maze_raw = pygame.image.load(maze_file).convert()
maze = pygame.transform.scale(maze_raw, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Generate sealed walkable mask via Flood Fill
walkable_mask = pygame.Mask((WINDOW_WIDTH, WINDOW_HEIGHT))
visited = set()
queue = deque([(35, 75)])
visited.add((35, 75))

while queue:
    cx, cy = queue.popleft()
    walkable_mask.set_at((cx, cy), 1)
    for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
        if 0 <= nx < WINDOW_WIDTH and 0 <= ny < WINDOW_HEIGHT:
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                col = maze.get_at((nx, ny))
                if (col.r > 35 or col.g > 35 or col.b > 45) and (col.r + col.g + col.b > 105):
                    queue.append((nx, ny))


def is_clear(x, y):
    ix, iy = int(x), int(y)
    if ix < 6 or ix >= WINDOW_WIDTH - 6 or iy < 6 or iy >= WINDOW_HEIGHT - 6:
        return False
    return walkable_mask.get_at((ix, iy)) == 1


# Load character sprite
char_paths = [
    os.path.join(BASE_DIR, "your_character.png"),
    "your_character.png",
    os.path.join(BASE_DIR, "silent_walls_character.png"),
    "silent_walls_character.png"
]
loaded_char = None
for p in char_paths:
    if os.path.exists(p):
        try:
            loaded_char = pygame.image.load(p).convert_alpha()
            break
        except Exception:
            pass

if not loaded_char:
    loaded_char = pygame.Surface((20, 26), pygame.SRCALPHA)
    loaded_char.fill((255, 200, 0))

# Load rat sprite
rat_paths = [
    os.path.join(BASE_DIR, "maze_rat.png"),
    "maze_rat.png"
]
loaded_rat = None
for p in rat_paths:
    if os.path.exists(p):
        try:
            loaded_rat = pygame.image.load(p).convert_alpha()
            break
        except Exception:
            pass

if not loaded_rat:
    loaded_rat = pygame.Surface((18, 18), pygame.SRCALPHA)
    pygame.draw.circle(loaded_rat, (130, 125, 125), (9, 9), 7)
    pygame.draw.circle(loaded_rat, (220, 20, 20), (12, 7), 2)


class Character:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(loaded_char, (20, 26))
        self.rect = self.image.get_rect(center=(x, y))
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.speed = 3.0
        self.health = PLAYER_MAX_HEALTH
        self.attack_cooldown = 0

    def move(self):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        moved = False

        if dx != 0:
            tx = self.pos_x + dx * self.speed
            if is_clear(tx, self.pos_y):
                self.pos_x = tx
                moved = True

        if dy != 0:
            ty = self.pos_y + dy * self.speed
            if is_clear(self.pos_x, ty):
                self.pos_y = ty
                moved = True

        self.rect.centerx = int(self.pos_x)
        self.rect.bottom = int(self.pos_y) + 6
        return moved

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def draw_health_bar(self, screen):
        bx, by, bw, bh = 20, 16, 140, 10
        pygame.draw.rect(screen, (15, 12, 20), (bx - 2, by - 2, bw + 4, bh + 4), border_radius=3)
        pygame.draw.rect(screen, (120, 20, 30), (bx, by, bw, bh))
        fill_w = int(bw * (self.health / PLAYER_MAX_HEALTH))
        if fill_w > 0:
            pygame.draw.rect(screen, (140, 60, 180), (bx, by, fill_w, bh))


# Guaranteed clear corridor waypoints distributed across the whole maze
WAYPOINTS = [
    (115, 335),
    (310, 85),
    (485, 230),
    (720, 85),
    (905, 335),
    (740, 340),
    (35, 75)
]


class Rat:
    def __init__(self, x, y):
        self.original_image = pygame.transform.scale(loaded_rat, (18, 18))
        self.image = self.original_image
        self.pos_x = float(x)
        self.pos_y = float(y)
        self.rect = self.image.get_rect(center=(int(x), int(y)))

        self.speed = 2.0
        self.dx = -1
        self.dy = 0
        self.health = RAT_MAX_HEALTH
        self.hit_cooldown = 0
        self.wp_idx = 0
        self.path = []
        self.repath_timer = 0

    def bfs_path(self, start_pos, target_pos):
        sx, sy = int(start_pos[0]), int(start_pos[1])
        gx, gy = int(target_pos[0]), int(target_pos[1])
        start_cell = (sx // 4 * 4, sy // 4 * 4)
        goal_cell = (gx // 4 * 4, gy // 4 * 4)

        q = deque([start_cell])
        came_from = {start_cell: None}

        while q:
            curr = q.popleft()
            if abs(curr[0] - goal_cell[0]) <= 8 and abs(curr[1] - goal_cell[1]) <= 8:
                path = []
                c = curr
                while c is not None:
                    path.append((c[0] + 2, c[1] + 2))
                    c = came_from[c]
                path.reverse()
                return path

            for dx, dy in [(4, 0), (-4, 0), (0, 4), (0, -4)]:
                nxt = (curr[0] + dx, curr[1] + dy)
                if nxt not in came_from and is_clear(nxt[0] + 2, nxt[1] + 2):
                    came_from[nxt] = curr
                    q.append(nxt)
        return []

    def move(self, target_player):
        dist_player = math.hypot(target_player.pos_x - self.pos_x, target_player.pos_y - self.pos_y)
        self.repath_timer += 1

        if dist_player < 160:
            target_goal = (target_player.pos_x, target_player.pos_y)
            if self.repath_timer >= 15 or not self.path:
                self.repath_timer = 0
                self.path = self.bfs_path((self.pos_x, self.pos_y), target_goal)
        else:
            target_goal = WAYPOINTS[self.wp_idx]
            if math.hypot(target_goal[0] - self.pos_x, target_goal[1] - self.pos_y) < 16:
                self.wp_idx = (self.wp_idx + 1) % len(WAYPOINTS)
                target_goal = WAYPOINTS[self.wp_idx]
                self.path = []

            if self.repath_timer >= 45 or not self.path:
                self.repath_timer = 0
                self.path = self.bfs_path((self.pos_x, self.pos_y), target_goal)

        if self.path:
            target_node = self.path[0]
            ndx = target_node[0] - self.pos_x
            ndy = target_node[1] - self.pos_y
            step_dist = math.hypot(ndx, ndy)

            if step_dist < self.speed + 1:
                self.pos_x, self.pos_y = target_node
                self.path.pop(0)
            else:
                self.dx = ndx / step_dist
                self.dy = ndy / step_dist
                self.pos_x += self.dx * self.speed
                self.pos_y += self.dy * self.speed
        else:
            for cdx, cdy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if is_clear(self.pos_x + cdx * self.speed, self.pos_y + cdy * self.speed):
                    self.dx, self.dy = cdx, cdy
                    self.pos_x += self.dx * self.speed
                    self.pos_y += self.dy * self.speed
                    break

        if self.dx < -0.1:
            self.image = pygame.transform.flip(self.original_image, True, False)
        elif self.dx > 0.1:
            self.image = self.original_image

        self.rect.center = (int(self.pos_x), int(self.pos_y))

        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)


player = Character(35, 75)
rat = Rat(905, 335)

exit_to_yard = pygame.Rect(915, 330, 45, 50)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    moved = player.move()

    if player.attack_cooldown > 0:
        player.attack_cooldown -= 1

    if player.rect.colliderect(exit_to_yard):
        print("Reached exit -> Transitioning to Yard")

    if rat is not None:
        rat.move(player)
        colliding = player.rect.colliderect(rat.rect)

        if colliding and moved and player.attack_cooldown == 0:
            rat.health -= 1
            player.attack_cooldown = ATTACK_COOLDOWN_FRAMES
            if rat.health <= 0:
                rat = None

        if rat is not None and colliding and rat.hit_cooldown == 0:
            player.health -= 1
            rat.hit_cooldown = RAT_HIT_COOLDOWN_FRAMES

            if player.health <= 0:
                print("Game Over! Restarting...")
                player = Character(35, 75)
                rat = Rat(905, 335)

    screen.fill((12, 28, 52))
    screen.blit(maze, (0, 0))

    if rat is not None:
        rat.draw(screen)

    player.draw(screen)
    player.draw_health_bar(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
