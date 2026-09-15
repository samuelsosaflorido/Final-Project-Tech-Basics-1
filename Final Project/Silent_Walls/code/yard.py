# Yard = Room by Samuel

# So this is a demo of the yard I have made some dialogue and options and used the pixel art image that we showed during the presentation as a test
# Okay I have changed a lot in relation to how the code was earlier. I had to use the videos cited in the documentation and also some Gemini help to get some feedback
# It has been challenging in terms to understanding everything, writing everything and trying to comprehend the logic behind it
# I also tried to make it more clean this time as last time was extremely chaotic and needed refinement

import math
import os
import pygame


# Basic pygame setup
pygame.init()
screen = pygame.display.set_mode((980, 480))
clock = pygame.time.Clock()

WINDOW_WIDTH = 980
WINDOW_HEIGHT = 480
WORD_TO_GUESS = "AWAKENING"


# Base class for all interactable objects in the scene
class Object:
    def __init__(self, x, y, image, name="object"):
        self.x = x
        self.y = y
        self.name = name
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def interact(self, yard):
        pass


# Subclasses for yard objects
class Weights(Object):
    def interact(self, yard):
        yard.show_note = True
        yard.has_letter_yard = True
        yard.feedback_message = "You examine the weights and check the letter."
        yard.feedback_timer = 120


class Dumbbells(Object):
    def interact(self, yard):
        yard.feedback_message = "Heavy dumbbells covered in dust. Nothing else is under them."
        yard.feedback_timer = 90


class Gallows(Object):
    def interact(self, yard):
        yard.feedback_message = "This gallows seems odd and shady."
        yard.feedback_timer = 90


# Hangman puzzle mini-game
class HangmanPuzzle:
    def __init__(self, word=WORD_TO_GUESS):
        self.word = word
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.max_wrong = 6
        self.solved = False
        self.failed = False
        self.is_open = False
        self.letter_buttons = {}

    def start(self):
        self.is_open = True

    def close(self):
        self.is_open = False

    def guess(self, letter):
        if letter in self.guessed_letters or self.solved or self.failed:
            return

        self.guessed_letters.append(letter)
        if letter not in self.word:
            self.wrong_guesses += 1
            if self.wrong_guesses >= self.max_wrong:
                self.failed = True
        else:
            if all(c in self.guessed_letters for c in self.word):
                self.solved = True

    def reset(self):
        self.guessed_letters = []
        self.wrong_guesses = 0
        self.solved = False
        self.failed = False

    def draw(self, screen, font, big_font):
        if not self.is_open:
            return

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (0, 0))

        box = pygame.Rect(130, 90, 720, 290)
        pygame.draw.rect(screen, (15, 10, 15), box, border_radius=6)
        pygame.draw.rect(screen, (140, 20, 25), box, 2, border_radius=6)

        display = " ".join(c if c in self.guessed_letters else "_" for c in self.word)
        screen.blit(big_font.render(display, True, (120, 180, 130)), (box.x + 40, box.y + 40))

        mistakes = f"Mistakes left: {max(0, self.max_wrong - self.wrong_guesses)}"
        screen.blit(font.render(mistakes, True, (200, 30, 35)), (box.x + 540, box.y + 45))

        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.letter_buttons.clear()
        for i, char in enumerate(alphabet):
            bx = box.x + 35 + (i % 13) * 33
            by = box.y + 95 + (i // 13) * 33
            r = pygame.Rect(bx, by, 28, 28)
            self.letter_buttons[char] = r

            color = (50, 40, 45) if char in self.guessed_letters else (140, 20, 25)
            pygame.draw.rect(screen, color, r, border_radius=4)
            pygame.draw.rect(screen, (220, 215, 200), r, 1, border_radius=4)
            txt = font.render(char, True, (220, 215, 200))
            screen.blit(txt, (bx + 8, by + 6))

        if self.solved:
            screen.blit(font.render("Skeleton Ghost of the Yard: 'You are worthy. Take the Medication.'", True, (212, 175, 55)), (box.x + 40, box.y + 195))
        elif self.failed:
            screen.blit(font.render("You have failed. Click Retry.", True, (200, 30, 35)), (box.x + 40, box.y + 195))


# Yard room controller
class Yard:
    def __init__(self, your_character):
        self.your_character = your_character
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        self.font = pygame.font.SysFont(None, 22)
        self.small_font = pygame.font.SysFont(None, 18)
        self.big_font = pygame.font.SysFont(None, 34)

        # Background layers
        self.bg = self._load_canvas_layer("yard_background.png", alpha=False)
        self.weights_layer = self._load_canvas_layer("yard_weights.png", alpha=True)
        self.dumbbell_layer = self._load_canvas_layer("yard_dumbbells.png", alpha=True)
        self.gallows_layer = self._load_canvas_layer("yard_gallows_pole.png", alpha=True)

        # Skeleton ghost NPC
        raw_ghost_path = os.path.join(self.base_dir, "yard_skeleton_ghost_npc.png")
        if os.path.exists(raw_ghost_path):
            raw_ghost = pygame.image.load(raw_ghost_path).convert_alpha()
            ghost_img = pygame.transform.scale(raw_ghost, (88, 108))
        else:
            ghost_img = pygame.Surface((88, 108), pygame.SRCALPHA)
            ghost_img.fill((180, 50, 60, 200))

        self.ghost = Object(530, 315, ghost_img, name="ghost")

        # Ground key prop (yard_key.png)
        raw_key_path = os.path.join(self.base_dir, "yard_key.png")
        if os.path.exists(raw_key_path):
            raw_key = pygame.image.load(raw_key_path).convert_alpha()
            key_img = pygame.transform.scale(raw_key, (36, 36))
        else:
            key_img = pygame.Surface((36, 36), pygame.SRCALPHA)
            key_img.fill((212, 175, 55))
        self.key_prop = Object(160, 385, key_img, name="key")

        # Letter prop (yard_letter.png)
        raw_letter_path = os.path.join(self.base_dir, "yard_letter.png")
        if os.path.exists(raw_letter_path):
            raw_letter = pygame.image.load(raw_letter_path).convert_alpha()
            letter_ground_img = pygame.transform.scale(raw_letter, (36, 28))
            self.letter_img = pygame.transform.scale(raw_letter, (720, 360))
        else:
            letter_ground_img = pygame.Surface((36, 28), pygame.SRCALPHA)
            letter_ground_img.fill((230, 220, 190))
            self.letter_img = pygame.Surface((720, 360), pygame.SRCALPHA)
            self.letter_img.fill((230, 220, 190))

        self.letter_prop = Object(245, 385, letter_ground_img, name="letter_prop")

        # Medication prop placed right next to the skeleton ghost (x=625, y=370)
        raw_med_path = os.path.join(self.base_dir, "yard_medication.png")
        if os.path.exists(raw_med_path):
            raw_med = pygame.image.load(raw_med_path).convert_alpha()
            med_img = pygame.transform.scale(raw_med, (34, 34))
        else:
            med_img = pygame.Surface((34, 34), pygame.SRCALPHA)
            med_img.fill((200, 40, 40))
        self.medication_prop = Object(625, 370, med_img, name="medication")

        # Interactive hitboxes for yard objects
        weights_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
        dumbbells_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
        gallows_surface = pygame.Surface((160, 100), pygame.SRCALPHA)

        self.weights = Weights(65, 260, weights_surface, name="weights")
        self.dumbbells = Dumbbells(220, 310, dumbbells_surface, name="dumbbells")
        self.gallows = Gallows(720, 240, gallows_surface, name="gallows")

        self.interactive_props = [self.weights, self.dumbbells, self.gallows]

        # Solid obstacles for feet collision
        self.obstacles = [
            pygame.Rect(75, 360, 70, 30),     # Weights base
            pygame.Rect(225, 360, 70, 30),    # Dumbbells base
            pygame.Rect(550, 410, 48, 15),    # Ghost feet base only (walk behind enabled)
            pygame.Rect(675, 350, 205, 50),   # Gallows legs touching floor
        ]

        # Floor boundary: Character feet cannot walk into the wall above this line
        self.wall_limit_y = 370

        # Item & interaction states
        self.puzzle = HangmanPuzzle(WORD_TO_GUESS)
        self.state = "EXPLORE"
        self.show_note = False
        self.has_letter_yard = False
        self.found_key_yard = False
        self.found_medication_yard = False
        self.feedback_message = ""
        self.feedback_timer = 0

        # Buttons
        self.dialogue_btn1 = pygame.Rect(0, 0, 0, 0)
        self.dialogue_btn2 = pygame.Rect(0, 0, 0, 0)
        self.puzzle_retry_btn = pygame.Rect(0, 0, 0, 0)
        self.puzzle_exit_btn = pygame.Rect(0, 0, 0, 0)

        # Dialogue tree
        self.current_dialogue = "intro"
        self.dialogue_nodes = {
            "intro": {
                "speaker": "The Skeleton Ghost of the Yard:",
                "text": "You are looking for answers. I see it. You seek a way out, am I wrong?",
                "opt1": "Please. I need to escape. Can you please help me?",
                "opt2": "Step away. (Leave)"
            },
            "challenge_prompt": {
                "speaker": "The Skeleton Ghost of the Yard:",
                "text": "You need to prove that you are worthy. Here is my challenge.",
                "opt1": "Step up to the gallows (Start Hangman game)",
                "opt2": "I don't trust you. (Leave)"
            }
        }

    def _load_canvas_layer(self, filename, alpha=True):
        full_path = os.path.join(self.base_dir, filename)
        if os.path.exists(full_path):
            img = pygame.image.load(full_path)
            img = img.convert_alpha() if alpha else img.convert()
            return pygame.transform.scale(img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        return pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA if alpha else 0)

    def handle_click(self, mouse_pos):
        player_x = self.your_character.rect.centerx
        player_y = self.your_character.rect.centery

        # Close note overlay if open
        if self.show_note:
            self.show_note = False
            return

        # Handle hangman puzzle input
        if self.puzzle.is_open:
            if not self.puzzle.solved and not self.puzzle.failed:
                for char, r in self.puzzle.letter_buttons.items():
                    if r.collidepoint(mouse_pos):
                        self.puzzle.guess(char)
                        break

            if self.puzzle.failed and self.puzzle_retry_btn.collidepoint(mouse_pos):
                self.puzzle.reset()
            elif self.puzzle_exit_btn.collidepoint(mouse_pos):
                self.puzzle.close()
                self.state = "EXPLORE"
            return

        # Handle dialogue choices
        if self.state == "DIALOGUE":
            if self.dialogue_btn1.collidepoint(mouse_pos):
                if self.current_dialogue == "intro":
                    self.current_dialogue = "challenge_prompt"
                elif self.current_dialogue == "challenge_prompt":
                    self.state = "EXPLORE"
                    self.puzzle.start()
            elif self.dialogue_btn2.collidepoint(mouse_pos):
                self.state = "EXPLORE"
            return

        # Handle exploration clicks
        if self.state == "EXPLORE":
            # 1. Pick up key from ground
            if not self.found_key_yard and self.key_prop.rect.collidepoint(mouse_pos):
                dist = math.hypot(self.key_prop.rect.centerx - player_x, self.key_prop.rect.centery - player_y)
                if dist < 120:
                    self.found_key_yard = True
                    self.feedback_message = "You have picked up 'Key (Yard)'!"
                    self.feedback_timer = 150
                else:
                    self.feedback_message = "You need to come closer to pick up the key"
                    self.feedback_timer = 90
                return

            # 2. Pick up letter from ground
            if not self.has_letter_yard and self.letter_prop.rect.collidepoint(mouse_pos):
                dist = math.hypot(self.letter_prop.rect.centerx - player_x, self.letter_prop.rect.centery - player_y)
                if dist < 120:
                    self.has_letter_yard = True
                    self.show_note = True
                    self.feedback_message = "You picked up and read 'Letter (Yard)'."
                    self.feedback_timer = 150
                else:
                    self.feedback_message = "You need to come closer to pick up the letter"
                    self.feedback_timer = 90
                return

            # 3. Pick up medication placed next to the skeleton ghost
            if self.puzzle.solved and not self.found_medication_yard and self.medication_prop.rect.collidepoint(mouse_pos):
                dist = math.hypot(self.medication_prop.rect.centerx - player_x, self.medication_prop.rect.centery - player_y)
                if dist < 120:
                    self.found_medication_yard = True
                    self.feedback_message = "You obtained 'Medication (Yard)'!"
                    self.feedback_timer = 160
                else:
                    self.feedback_message = "You need to come closer to grab the medication"
                    self.feedback_timer = 90
                return

            # 4. Skeleton Ghost dialogue trigger
            if self.ghost.rect.collidepoint(mouse_pos):
                dist = math.hypot(self.ghost.rect.centerx - player_x, self.ghost.rect.centery - player_y)
                if dist < 140:
                    if self.found_medication_yard:
                        self.feedback_message = "The Skeleton Ghost watches quietly. You already proved your worth."
                        self.feedback_timer = 110
                    elif self.puzzle.solved:
                        self.feedback_message = "Skeleton Ghost: 'The Medication is right there. Take it.'"
                        self.feedback_timer = 110
                    else:
                        self.state = "DIALOGUE"
                        self.current_dialogue = "intro"
                else:
                    self.feedback_message = "You need to come closer to speak with the Skeleton Ghost"
                    self.feedback_timer = 90
                return

            # 5. Yard props (re-read letter from weights if already collected)
            for prop in self.interactive_props:
                if prop.rect.collidepoint(mouse_pos):
                    dist = math.hypot(prop.rect.centerx - player_x, prop.rect.centery - player_y)
                    if dist < 120:
                        prop.interact(self)
                    else:
                        self.feedback_message = "You need to come closer as there is something interesting here"
                        self.feedback_timer = 90
                    break

    def handle_key(self, event):
        if self.puzzle.is_open and not self.puzzle.solved and not self.puzzle.failed:
            if pygame.K_a <= event.key <= pygame.K_z:
                char = chr(event.key).upper()
                self.puzzle.guess(char)

    def update(self):
        if self.feedback_timer > 0:
            self.feedback_timer -= 1

    def draw(self, screen):
        # Draw background and environment layers
        screen.blit(self.bg, (0, 0))
        screen.blit(self.weights_layer, (0, 0))
        screen.blit(self.dumbbell_layer, (0, 0))
        screen.blit(self.gallows_layer, (0, 0))

        # Only draw ground key if not yet collected
        if not self.found_key_yard:
            self.key_prop.draw(screen)

        # Only draw ground letter if not yet collected
        if not self.has_letter_yard:
            self.letter_prop.draw(screen)

        # Draw medication prop right next to the ghost after solving hangman
        if self.puzzle.solved and not self.found_medication_yard:
            self.medication_prop.draw(screen)

        # Depth-ordered rendering for character and ghost
        if self.your_character.rect.bottom < self.ghost.rect.bottom:
            self.your_character.draw(screen)
            self.ghost.draw(screen)
        else:
            self.ghost.draw(screen)
            self.your_character.draw(screen)

        # Draw feedback text
        if self.feedback_timer > 0:
            txt = self.small_font.render(self.feedback_message, True, (212, 175, 55))
            screen.blit(txt, (WINDOW_WIDTH // 2 - txt.get_width() // 2, 440))

        # Large inspection overlay for letter
        if self.show_note:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 185))
            screen.blit(overlay, (0, 0))

            if self.letter_img:
                lx = WINDOW_WIDTH // 2 - self.letter_img.get_width() // 2
                ly = WINDOW_HEIGHT // 2 - self.letter_img.get_height() // 2
                screen.blit(self.letter_img, (lx, ly))

            hint = self.small_font.render("[Click anywhere to close]", True, (220, 215, 200))
            screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, 435))

        # Dialogue box overlay
        elif self.state == "DIALOGUE":
            node = self.dialogue_nodes[self.current_dialogue]
            box = pygame.Rect(140, 320, 700, 130)
            pygame.draw.rect(screen, (10, 8, 12), box, border_radius=5)
            pygame.draw.rect(screen, (140, 20, 25), box, 2, border_radius=5)

            screen.blit(self.font.render(node["speaker"], True, (212, 175, 55)), (box.x + 20, box.y + 12))
            screen.blit(self.small_font.render(node["text"], True, (220, 215, 200)), (box.x + 20, box.y + 42))

            self.dialogue_btn1 = pygame.Rect(box.x + 20, box.y + 80, 300, 32)
            self.dialogue_btn2 = pygame.Rect(box.x + 340, box.y + 80, 160, 32)
            pygame.draw.rect(screen, (140, 20, 25), self.dialogue_btn1, border_radius=4)
            pygame.draw.rect(screen, (140, 20, 25), self.dialogue_btn2, border_radius=4)

            txt1 = self.small_font.render(node["opt1"], True, (220, 215, 200))
            txt2 = self.small_font.render(node["opt2"], True, (220, 215, 200))
            screen.blit(txt1, (self.dialogue_btn1.x + 10, self.dialogue_btn1.y + 8))
            screen.blit(txt2, (self.dialogue_btn2.x + 10, self.dialogue_btn2.y + 8))

        # Hangman mini-game overlay
        if self.puzzle.is_open:
            self.puzzle.draw(screen, self.small_font, self.big_font)
            self.puzzle_exit_btn = pygame.Rect(720, 330, 80, 28)
            pygame.draw.rect(screen, (140, 20, 25), self.puzzle_exit_btn, border_radius=4)
            screen.blit(self.small_font.render("Exit", True, (220, 215, 200)), (self.puzzle_exit_btn.x + 25, self.puzzle_exit_btn.y + 6))

            if self.puzzle.failed:
                self.puzzle_retry_btn = pygame.Rect(170, 330, 90, 28)
                pygame.draw.rect(screen, (140, 20, 25), self.puzzle_retry_btn, border_radius=4)
                screen.blit(self.small_font.render("Retry", True, (220, 215, 200)), (self.puzzle_retry_btn.x + 25, self.puzzle_retry_btn.y + 6))


# Character class with feet-based collision
class Character:
    def __init__(self, x, y):
        self.speed = 4
        if os.path.exists("your_character.png"):
            self.image = pygame.image.load("your_character.png").convert_alpha()
        else:
            self.image = pygame.Surface((50, 70))
            self.image.fill((60, 120, 200))

        self.transform_image = pygame.transform.scale(self.image, (50, 70))
        self.rect = self.transform_image.get_rect(topleft=(x, y))
        self.x = self.rect.x
        self.y = self.rect.y

    def get_feet_rect(self):
        return pygame.Rect(self.rect.x + 12, self.rect.bottom - 16, 26, 16)

    def draw(self, screen):
        screen.blit(self.transform_image, self.rect)

    def move(self, obstacles, wall_limit_y):
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed

        feet = self.get_feet_rect()

        # Horizontal movement and obstacle collision
        feet.x += dx
        for obs in obstacles:
            if feet.colliderect(obs):
                if dx > 0:
                    feet.right = obs.left
                elif dx < 0:
                    feet.left = obs.right

        # Vertical movement and obstacle collision
        feet.y += dy
        for obs in obstacles:
            if feet.colliderect(obs):
                if dy > 0:
                    feet.bottom = obs.top
                elif dy < 0:
                    feet.top = obs.bottom

        # Room boundary enforcement
        if feet.top < wall_limit_y:
            feet.top = wall_limit_y
        if feet.bottom > 460:
            feet.bottom = 460
        if feet.left < 35:
            feet.left = 35
        if feet.right > WINDOW_WIDTH - 35:
            feet.right = WINDOW_WIDTH - 35

        # Re-anchor sprite position strictly to feet
        self.rect.bottom = feet.bottom
        self.rect.centerx = feet.centerx
        self.x = self.rect.x
        self.y = self.rect.y

    def update(self):
        pass

    def set_pos(self, x, y):
        self.rect.topleft = (x, y)
        self.x = x
        self.y = y


# Main Game Loop
player = Character(200, 390)
yard = Yard(player)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            yard.handle_key(event)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            yard.handle_click(event.pos)

    # Move player only when not paused by dialogue, note or puzzle
    if yard.state == "EXPLORE" and not yard.puzzle.is_open and not yard.show_note:
        player.move(yard.obstacles, yard.wall_limit_y)

    player.update()
    yard.update()

    # Base scene rendering
    yard.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
