# by Samuel Domingo Sosa Florido

# So this is a demo of the yard I have made some dialogue and options and used the pixel art image that we showed during the presentation as a test
# Okay I have changed a lot in relation to how the code was earlier. I had to use the videos cited in the documentation and also some Gemini help to get some feedback
# It has been challenging in terms to understanding everything, writing everything and trying to comprehend the logic behind it
# I also tried to make it more clean this time as last time was extremely chaotic and needed refinement 

import math
import os
import pygame
import inventory 


# Basic pygame setup
pygame.init()
screen = pygame.display.set_mode((980, 480))
clock = pygame.time.Clock()

WINDOW_WIDTH = 980
WINDOW_HEIGHT = 480
WORD_TO_GUESS = "AWAKENING"
DIG_TARGET_X = 680
DIG_TARGET_Y = 370


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
        yard.feedback_message = "You found 'Letter (Yard)'. It is covered in blood."
        yard.feedback_timer = 150


class Dumbbells(Object):
    def interact(self, yard):
        if not yard.found_key_yard:
            yard.found_key_yard = True
            yard.feedback_message = "You have found 'Key (Yard)'. Maybe it can help you escape."
            yard.feedback_timer = 150
        else:
            yard.feedback_message = "You already searched here. Nothing else is under the dumbbells."
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
            screen.blit(font.render("Skeleton Ghost of the Yard: 'You are worthy. Take the Spade.'", True, (212, 175, 55)), (box.x + 40, box.y + 195))
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

        # Skeleton ghost NPC - dimensions match original canvas drawing exactly, shifted forward
        raw_ghost_path = os.path.join(self.base_dir, "yard_skeleton_ghost_npc.png")
        if os.path.exists(raw_ghost_path):
            raw_ghost = pygame.image.load(raw_ghost_path).convert_alpha()
            ghost_img = pygame.transform.scale(raw_ghost, (88, 108))
        else:
            ghost_img = pygame.Surface((88, 108), pygame.SRCALPHA)
            ghost_img.fill((180, 50, 60, 200))

        self.ghost = Object(530, 315, ghost_img, name="ghost")

        # Interactive yard objects
        weights_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
        dumbbells_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
        gallows_surface = pygame.Surface((160, 100), pygame.SRCALPHA)

        self.weights = Weights(65, 260, weights_surface, name="weights")
        self.dumbbells = Dumbbells(220, 310, dumbbells_surface, name="dumbbells")
        self.gallows = Gallows(720, 240, gallows_surface, name="gallows")

        self.interactive_props = [self.weights, self.dumbbells, self.gallows]

        # Digging target zone near the gallows
        self.dig_zone = pygame.Rect(DIG_TARGET_X - 40, DIG_TARGET_Y - 30, 90, 70)

        # Solid obstacles for feet collision
        self.obstacles = [
            pygame.Rect(75, 360, 70, 30),     # Weights base
            pygame.Rect(225, 360, 70, 30),    # Dumbbells base
            pygame.Rect(550, 410, 48, 15),    # Ghost feet base only (walk behind enabled)
            pygame.Rect(675, 350, 205, 50),   # Gallows legs touching floor
        ]

        # Floor boundary: Character feet cannot walk into the wall above this line
        self.wall_limit_y = 370

        # Item & interaction states matching standard item names
        self.puzzle = HangmanPuzzle(WORD_TO_GUESS)
        self.state = "EXPLORE"
        self.show_note = False
        self.has_letter_yard = False
        self.found_key_yard = False
        self.has_spade = False
        self.found_medication_yard = False
        self.feedback_message = ""
        self.feedback_timer = 0

        # Riddle note contents
        self.note_text = [
            "Block B",
            "",
            "Seven crows stare from the wired fence...",
            "Two big towers staring at the cursed one...",
            "Only five minutes before the accursed judgement",
            "I still remember that cursed day",
            "I am so sorry. I could have saved you...",
            "I cannot stand this agony",
            "The sorrow, the pain watching you slowly fade away",
            "",
            "Forgive me.                          -S",
            "",
            "[Click anywhere to close]"
        ]

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

        # Close note if open
        if self.show_note:
            self.show_note = False
            return

        # Handle hangman puzzle input
        if self.puzzle.is_open:
            if not self.puzzle.solved and not self.puzzle.failed:
                for char, r in self.puzzle.letter_buttons.items():
                    if r.collidepoint(mouse_pos):
                        self.puzzle.guess(char)
                        if self.puzzle.solved:
                            self.has_spade = True
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
            # Digging spot near the gallows
            if self.dig_zone.collidepoint(mouse_pos):
                dist = math.hypot(self.dig_zone.centerx - player_x, self.dig_zone.centery - player_y)
                if dist < 130:
                    if self.has_spade:
                        if not self.found_medication_yard:
                            self.found_medication_yard = True
                            self.feedback_message = "You dug up the soft earth and found 'Medication (Yard)'!"
                            self.feedback_timer = 160
                        else:
                            self.feedback_message = "You already unearthed 'Medication (Yard)' from this spot."
                            self.feedback_timer = 90
                    else:
                        self.feedback_message = "The dirt looks disturbed here, but you need a Spade to dig."
                        self.feedback_timer = 110
                else:
                    self.feedback_message = "You need to come closer as there is something interesting here"
                    self.feedback_timer = 90
                return

            # Skeleton Ghost dialogue trigger
            if self.ghost.rect.collidepoint(mouse_pos):
                dist = math.hypot(self.ghost.rect.centerx - player_x, self.ghost.rect.centery - player_y)
                if dist < 140:
                    if self.has_spade:
                        self.feedback_message = "The Skeleton Ghost watches quietly. You already obtained the Spade."
                        self.feedback_timer = 110
                    else:
                        self.state = "DIALOGUE"
                        self.current_dialogue = "intro"
                else:
                    self.feedback_message = "You need to come closer to speak with the Skeleton Ghost"
                    self.feedback_timer = 90
                return

            # Yard props
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
        # Keyboard letter input directly for the Hangman mini-game
        if self.puzzle.is_open and not self.puzzle.solved and not self.puzzle.failed:
            if pygame.K_a <= event.key <= pygame.K_z:
                char = chr(event.key).upper()
                self.puzzle.guess(char)
                if self.puzzle.solved:
                    self.has_spade = True

    def update(self):
        if self.feedback_timer > 0:
            self.feedback_timer -= 1

    def draw(self, screen):
        # Draw background and environment layers
        screen.blit(self.bg, (0, 0))
        screen.blit(self.weights_layer, (0, 0))
        screen.blit(self.dumbbell_layer, (0, 0))
        screen.blit(self.gallows_layer, (0, 0))

        # Drawing the ghost and character in correct depth order
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

        # Draw note overlay
        if self.show_note:
            box = pygame.Rect(260, 60, 460, 360)
            pygame.draw.rect(screen, (235, 225, 200), box)
            pygame.draw.rect(screen, (140, 20, 25), box, 2)

            curr_y = box.y + 15
            for line in self.note_text:
                txt = self.small_font.render(line, True, (30, 20, 25))
                screen.blit(txt, (box.x + 25, curr_y))
                curr_y += 22

        # Draw dialogue box
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

        # Draw hangman puzzle overlay
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
    inventory_open = getattr(inventory, "is_open", False)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # TAB key toggles inventory open/closed
            if event.key == pygame.K_TAB:
                if hasattr(inventory, "toggle"):
                    inventory.toggle()
                elif hasattr(inventory, "is_open"):
                    inventory.is_open = not inventory.is_open
            else:
                # Only pass keys to Yard (Hangman typing) if inventory is closed
                if not inventory_open:
                    yard.handle_key(event)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Route mouse clicks to inventory if open, else to yard exploration
            if inventory_open:
                if hasattr(inventory, "handle_click"):
                    inventory.handle_click(event.pos)
            else:
                yard.handle_click(event.pos)

    # Move player only when not paused by dialogue, note, puzzle, or open inventory
    if yard.state == "EXPLORE" and not yard.puzzle.is_open and not yard.show_note and not inventory_open:
        player.move(yard.obstacles, yard.wall_limit_y)

    player.update()
    yard.update()

    # Base scene rendering
    yard.draw(screen)

    # Render inventory overlay on top of everything when open
    if inventory_open and hasattr(inventory, "draw"):
        inventory.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
