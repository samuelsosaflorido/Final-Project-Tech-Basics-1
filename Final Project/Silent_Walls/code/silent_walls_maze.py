# by Samuel Domingo Sosa Florido
# I had to use a lot of Gemini to help me during this process
# It was extremely challenging to make the rat moving across the maze so I had to test it over and over
# Most of the previous maze was taken as a basis and had to refactor a lot everything
# With the designs and previous code (that also was used for the structure of this new code) made by Karo and Kathi the whole area improved a lot and it was even better in terms of implementing the mechanics
# After fixing a lot of the structure I would say that it was an interesting learning experience but extremely challenging at the same

import math
import os
import sys
from collections import deque
import pygame

from silent_walls_character import Character

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Window settings matching maze aspect ratio
WINDOW_WIDTH = 980
WINDOW_HEIGHT = 400
FPS = 60

PLAYER_MAX_HEALTH = 5
RAT_MAX_HEALTH = 5
ATTACK_COOLDOWN_FRAMES = 20
RAT_HIT_COOLDOWN_FRAMES = 60

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OFFSET_Y = 40

#guaranteed clear corridor waypoints in maze
WAYPOINTS = [
    (115, 335),
    (310, 85),
    (485, 230),
    (720, 85),
    (905, 335),
    (740, 340),
    (35, 75)
]

#exits from the maze
EXIT_ZONE_LEFT = pygame.Rect(17, 240, 30, 20)
EXIT_ZONE_RIGHT = pygame.Rect(920, 108, 30, 20)
EXIT_ZONE_BOTTOM = pygame.Rect(450, 350, 25, 20)

# pygame.init()
# screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# pygame.display.set_caption("Silent Walls - The Maze")
# clock = pygame.time.Clock()

def _find_file(filenames):
    for name in filenames:
        for folder in [BASE_DIR, "", os.getcwd()]:
            full_p = os.path.join(folder, name) if folder else name
            if os.path.exists(full_p):
                return full_p
    return None



# Load background
# bg_filenames = ["maze_background.png", "maze_background.jpg", "maze.png"]
# maze_file = None
# for name in bg_filenames:
#     for folder in [BASE_DIR, "", os.getcwd()]:
#         full_p = os.path.join(folder, name) if folder else name
#         if os.path.exists(full_p):
#             maze_file = full_p
#             break
#     if maze_file:
#         break

# if not maze_file:
#     print("Error: maze image not found!")
#     pygame.quit()
#     sys.exit()

# maze_raw = pygame.image.load(maze_file).convert()
# maze = pygame.transform.scale(maze_raw, (WINDOW_WIDTH, WINDOW_HEIGHT))

# # Generate sealed walkable mask via Flood Fill
# walkable_mask = pygame.Mask((WINDOW_WIDTH, WINDOW_HEIGHT))
# visited = set()
# queue = deque([(35, 75)])
# visited.add((35, 75))

# while queue:
#     cx, cy = queue.popleft()
#     walkable_mask.set_at((cx, cy), 1)
#     for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
#         if 0 <= nx < WINDOW_WIDTH and 0 <= ny < WINDOW_HEIGHT:
#             if (nx, ny) not in visited:
#                 visited.add((nx, ny))
#                 col = maze.get_at((nx, ny))
#                 if (col.r > 35 or col.g > 35 or col.b > 45) and (col.r + col.g + col.b > 105):
#                     queue.append((nx, ny))


# def is_clear(x, y):
#     ix, iy = int(x), int(y)
#     if ix < 6 or ix >= WINDOW_WIDTH - 6 or iy < 6 or iy >= WINDOW_HEIGHT - 6:
#         return False
#     return walkable_mask.get_at((ix, iy)) == 1


# # Load character sprite
# char_paths = [
#     os.path.join(BASE_DIR, "your_character.png"),
#     "your_character.png",
#     os.path.join(BASE_DIR, "silent_walls_character.png"),
#     "silent_walls_character.png"
# ]
# loaded_char = None
# for p in char_paths:
#     if os.path.exists(p):
#         try:
#             loaded_char = pygame.image.load(p).convert_alpha()
#             break
#         except Exception:
#             pass

# if not loaded_char:
#     loaded_char = pygame.Surface((20, 26), pygame.SRCALPHA)
#     loaded_char.fill((255, 200, 0))

# # Load rat sprite
# rat_paths = [
#     os.path.join(BASE_DIR, "maze_rat.png"),
#     "maze_rat.png"
# ]
# loaded_rat = None
# for p in rat_paths:
#     if os.path.exists(p):
#         try:
#             loaded_rat = pygame.image.load(p).convert_alpha()
#             break
#         except Exception:
#             pass

# if not loaded_rat:
#     loaded_rat = pygame.Surface((18, 18), pygame.SRCALPHA)
#     pygame.draw.circle(loaded_rat, (130, 125, 125), (9, 9), 7)
#     pygame.draw.circle(loaded_rat, (220, 20, 20), (12, 7), 2)



class Rat:
    def __init__(self, x, y, maze):
        self.maze = maze  # brauchen wir für is_clear() statt der globalen Funktion

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
                if nxt not in came_from and self.maze.is_clear(nxt[0] + 2, nxt[1] + 2):
                    came_from[nxt] = curr
                    q.append(nxt)
        return []

    def move(self):
        dist_player = math.hypot(self.maze.player_x - self.pos_x, self.maze.player_y - self.pos_y)
        self.repath_timer += 1

        if dist_player < 160:
            target_goal = (self.maze.player_x, self.maze.player_y)
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
                if self.maze.is_clear(self.pos_x + cdx * self.speed, self.pos_y + cdy * self.speed):
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

    def draw(self, screen, offset_y=0):
        r = self.rect.copy()
        r.y += offset_y
        screen.blit(self.image, r)

class Maze:
    def __init__(self):
        self.name = "maze"

        # load background picture
        bg_filenames = ["maze_background.png", "maze_background.jpg", "maze.png"]
        maze_file = _find_file(bg_filenames)
        if not maze_file:
            print("Error: maze image not found!")
            pygame.quit()
            sys.exit()

        maze_raw = pygame.image.load(maze_file).convert()
        self.image = pygame.transform.scale(maze_raw, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # walkable space
        self.walkable_mask = pygame.Mask((WINDOW_WIDTH, WINDOW_HEIGHT))
        self._flood_fill_walkable((35, 75))

        # the rat
        self.rat = Rat(905, 335, self)

        # --- Spielerposition im Maze ---
        # eigene, kleine float-Position statt der 100x100-Hitbox vom
        # gemeinsamen Character, weil der viel zu groß für die Gänge ist
        self.entry_pos = (35, 75)
        self.player_x = float(self.entry_pos[0])
        self.player_y = float(self.entry_pos[1])
        self.speed = 3.0

        # --- Ausgänge ---
        self.exit_zones = {
            "left": EXIT_ZONE_LEFT,
            "right": EXIT_ZONE_RIGHT,
            "bottom": EXIT_ZONE_BOTTOM,
        }
        self.destinations = {}

        # Wiedereinstiegspunkte, wenn man aus einem Raum zurückkommt -
        # jeweils ein Stück innerhalb der Ausgangs-Zone, damit man nicht
        # sofort wieder rausgeschubst wird
        self.reentry_points = {
            "left": (EXIT_ZONE_LEFT.right + 15, EXIT_ZONE_LEFT.centery),
            "right": (EXIT_ZONE_RIGHT.left - 15, EXIT_ZONE_RIGHT.centery),
            "bottom": (EXIT_ZONE_BOTTOM.centerx, EXIT_ZONE_BOTTOM.top - 15),
        }

        self.offset_y = OFFSET_Y

    def set_destinations(self, mapping):
        """mapping = {"left": "cell", "right": "yard", "bottom": "cafeteria"}"""
        self.destinations = mapping

    def _flood_fill_walkable(self, start):
        visited = set()
        queue = deque([start])
        visited.add(start)

        while queue:
            cx, cy = queue.popleft()
            self.walkable_mask.set_at((cx, cy), 1)
            for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                if 0 <= nx < WINDOW_WIDTH and 0 <= ny < WINDOW_HEIGHT:
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        col = self.image.get_at((nx, ny))
                        if (col.r > 35 or col.g > 35 or col.b > 45) and (col.r + col.g + col.b > 105):
                            queue.append((nx, ny))

    def is_clear(self, x, y):
        ix, iy = int(x), int(y)

        # in den Ausgangs-Zonen darf man auch bis ganz an den Rand,
        # sonst kommt man da nie durch
        for zone in self.exit_zones.values():
            if zone.collidepoint(ix, iy):
                return True

        if ix < 6 or ix >= WINDOW_WIDTH - 6 or iy < 6 or iy >= WINDOW_HEIGHT - 6:
            return False
        return self.walkable_mask.get_at((ix, iy)) == 1

    def enter_from(self, room_name):
        """setzt die Spielerposition auf den Wiedereinstiegspunkt des Ausgangs,
        über den man in room_name gegangen ist"""
        for zone_name, dest in self.destinations.items():
            if dest == room_name and zone_name in self.reentry_points:
                x, y = self.reentry_points[zone_name]
                self.player_x = float(x)
                self.player_y = float(y)
                return
        self.player_x, self.player_y = self.entry_pos

    def move_player(self, character):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])

        if dx != 0:
            tx = self.player_x + dx * self.speed
            if self.is_clear(tx, self.player_y):
                self.player_x = tx

        if dy != 0:
            ty = self.player_y + dy * self.speed
            if self.is_clear(self.player_x, ty):
                self.player_y = ty

        # den gemeinsamen Character nur fürs Zeichnen an die Maze-Position hängen
        character.rect.centerx = int(self.player_x)
        character.rect.centery = int(self.player_y) + self.offset_y
        character.update_hitbox()

    def update(self, character):
        self.move_player(character)
        self.rat.move()

    def check_exits(self):
        px, py = self.player_x, self.player_y

        if EXIT_ZONE_LEFT.collidepoint(px, py):
            print("LEFT zone erreicht, destination:", self.destinations.get("left"))
            return self.destinations.get("left")
        if EXIT_ZONE_RIGHT.collidepoint(px, py):
            print("RIGHT zone erreicht, destination:", self.destinations.get("right"))
            return self.destinations.get("right")
        if EXIT_ZONE_BOTTOM.collidepoint(px, py):
            print("BOTTOM zone erreicht, destination:", self.destinations.get("bottom"))
            return self.destinations.get("bottom")
        return None

    def draw(self, screen, character):
        screen.blit(self.image, (0, self.offset_y))
        self.rat.draw(screen, self.offset_y)

        # make character smaller so she fits in the maze
        small = pygame.transform.scale(character.transformed_image, (34, 34))
        rect = small.get_rect(center=(int(self.player_x), int(self.player_y) + self.offset_y))
        screen.blit(small, rect)

        debug_font = pygame.font.SysFont("Arial", 16)
        pos_text = debug_font.render(f"x={int(self.player_x)} y={int(self.player_y)}", True, (255, 255, 0))
        screen.blit(pos_text, (10, self.offset_y - 25))

        for zone in self.exit_zones.values():
            debug_rect = zone.copy()
            debug_rect.y += self.offset_y
            pygame.draw.rect(screen, (0, 255, 255), debug_rect, 2)


# if __name__ == "__main__":
#     player = Character(35, 75)
#     rat = Rat(905, 335)

#     exit_to_yard = pygame.Rect(915, 330, 45, 50)


#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
#                 running = False

#         moved = player.move()

#         if player.attack_cooldown > 0:
#             player.attack_cooldown -= 1

#         if player.rect.colliderect(exit_to_yard):
#             print("Reached exit -> Transitioning to Yard")

#         if rat is not None:
#             rat.move(player)
#             colliding = player.rect.colliderect(rat.rect)

#             if colliding and moved and player.attack_cooldown == 0:
#                 rat.health -= 1
#                 player.attack_cooldown = ATTACK_COOLDOWN_FRAMES
#                 if rat.health <= 0:
#                     rat = None

#             if rat is not None and colliding and rat.hit_cooldown == 0:
#                 player.health -= 1
#                 rat.hit_cooldown = RAT_HIT_COOLDOWN_FRAMES

#                 if player.health <= 0:
#                     print("Game Over! Restarting...")
#                     player = Character(35, 75)
#                     rat = Rat(905, 335)

#         screen.fill((12, 28, 52))
#         screen.blit(maze, (0, 0))

#         if rat is not None:
#             rat.draw(screen)

#         player.draw(screen)
#         player.draw_health_bar(screen)

#         pygame.display.flip()
#         clock.tick(FPS)

#     pygame.quit()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT + OFFSET_Y * 2))
    pygame.display.set_caption("Silent Walls - The Maze (Test)")
    clock = pygame.time.Clock()

    from silent_walls_character import Character
    maze = Maze()
    player = Character(35, 75)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        maze.update(player)
        result = maze.check_exits()
        if result:
            print("Exit erreicht:", result)

        screen.fill((12, 28, 52))
        maze.draw(screen, player)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
