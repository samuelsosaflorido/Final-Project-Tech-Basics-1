# by Samuel Sosa Florido

# So this is a demo of the yard I have made some dialogue and options and used the pixel art image that we showed during the presentation as a test
# I added some rudimentary Inventory option that can be activated with the TAB, similar to other games such as Resident Evil, The Elder Scrolls, Fallout or Silent Hill 2 
# We might need to change this when the inventory file is completed 
# I have added a stickman only just to try out how it will look like with the animations. Looks a bit wonky lol but fun
# I have implemented within the code the different puzzles, the ghost one, the key fragment and the medication fragment so I hope it works right
# We might need to change stuff since I am still not convinced with the visuals and maybe I might need to improve this a little bit more 
# But the overall idea is here I have added comments on the different sections 
# It has been challengng to write the code and I also used some help with Gemini and also some tutorials I hope everything looks clean and understandable :)

import pygame
import math
from silent_walls import Inventory 


# Configuration
# Here I have defined the main variables as well as the requisites for the puzzle and the width and height for the screens
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 338
WORD_TO_GUESS = "AWAKENING"
MAX_WRONG_GUESSES = 6
FPS = 60

# Coordinates given by the ghost once solved (Bad ending route)
# We might need to change these coordinates and visualize the map. The coordinates are nearby the gallows pole, so I hope this makes any sense
DIG_TARGET_X = 680
DIG_TARGET_Y = 295
MEDICATION_COORDINATES = f"X: {DIG_TARGET_X}, Y: {DIG_TARGET_Y}"

# Color Palette
# I have defined the main color palette for the screen for the dialogues. This is just something temporary as we might need to change this to make it more visually appealing
COLOR_VOID = (6, 4, 8)
COLOR_BLOOD = (140, 15, 20)
COLOR_BLOOD_BRIGHT = (200, 30, 35)
COLOR_SICKLY = (150, 180, 140)
COLOR_BONE = (210, 205, 190)
COLOR_FOG = (40, 10, 15)
COLOR_GOLD = (212, 175, 55)
COLOR_STICKMAN = (235, 230, 220) # oh yeah, I did this just to test it out lol
COLOR_DIRT = (60, 35, 25)
COLOR_NOTE = (230, 220, 190)

pygame.init()


# Hangman Puzzle for the Ghost ending (Bad Ending)
# Here I defined the class for the Hangman puzzle and also made different options for the game to work
# This section basically handles whether player succeeds in solving the word game or not, with the corresponding functions

class HangmanPuzzle:
    def __init__(self, word=WORD_TO_GUESS, max_wrong=MAX_WRONG_GUESSES):
        self.word = word.upper()
        self.max_wrong = max_wrong
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.solved = False
        self.failed = False
        self.reward_claimed = False

    def guess(self, letter):
        letter = letter.upper()
        if self.solved or self.failed or letter in self.guessed_letters:
            return

        self.guessed_letters.add(letter)
        if letter in self.word:
            if all(char in self.guessed_letters for char in self.word):
                self.solved = True
        else:
            self.wrong_guesses += 1
            if self.wrong_guesses >= self.max_wrong:
                self.failed = True

    def reset(self):
        self.guessed_letters = set()
        self.wrong_guesses = 0
        self.solved = False
        self.failed = False

    def display_word(self):
        return " ".join(letter if letter in self.guessed_letters else "_" for letter in self.word)


# Drawing functions
# In this section I had to use the help of Gemini. Nevertheless, I wrote the code by myself trying to understand how to draw the different boxes
def draw_dialogue_box(screen, font, small_font, dialogue_data):
    # Renders dialogue text and player branching options
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((*COLOR_FOG, 200))
    screen.blit(overlay, (0, 0))

    # This defines the main dimensions of the dialogue box
    box_width, box_height = 700, 125
    box_x = (WINDOW_WIDTH - box_width) // 2
    box_y = WINDOW_HEIGHT - box_height - 15
    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

    pygame.draw.rect(screen, COLOR_VOID, box_rect, border_radius=5)
    pygame.draw.rect(screen, COLOR_BLOOD, box_rect, 2, border_radius=5)

    speaker_surf = font.render(dialogue_data["speaker"], True, COLOR_GOLD)
    screen.blit(speaker_surf, (box_x + 18, box_y + 10))

    msg_surf = small_font.render(dialogue_data["text"], True, COLOR_BONE) # This basically turns the text with the mentioned color at the end of the code
    screen.blit(msg_surf, (box_x + 18, box_y + 35))

    opt_y = box_y + 62
    for opt_key, opt_text in dialogue_data["options"].items():
        opt_color = (120, 200, 140) if "1" in opt_key else COLOR_BLOOD_BRIGHT
        opt_surf = small_font.render(f"[{opt_key}] {opt_text}", True, opt_color)
        screen.blit(opt_surf, (box_x + 18, opt_y))
        opt_y += 22

# I thought it was a good idea to introduce some monologues within the game
# Particularly when the main character encounters certain situations or obtains specific object
# I also added the coordinates of the dialogue box

def draw_monologue_box(screen, font, small_font, speaker_name, text_line):
    # This section basically renders the protagonist thinking 
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((*COLOR_FOG, 190))
    screen.blit(overlay, (0, 0))

    box_width, box_height = 700, 100
    box_x = (WINDOW_WIDTH - box_width) // 2
    box_y = WINDOW_HEIGHT - box_height - 20
    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

    pygame.draw.rect(screen, COLOR_VOID, box_rect, border_radius=5)
    pygame.draw.rect(screen, (80, 120, 160), box_rect, 2, border_radius=5)

    speaker_surf = font.render(speaker_name, True, (130, 180, 220))
    screen.blit(speaker_surf, (box_x + 18, box_y + 10))

    msg_surf = small_font.render(text_line, True, COLOR_BONE)
    screen.blit(msg_surf, (box_x + 18, box_y + 38))

    hint_surf = small_font.render("[Press SPACE or E to continue...]", True, (140, 140, 140))
    screen.blit(hint_surf, (box_x + box_width - hint_surf.get_width() - 18, box_y + box_height - 24))


def draw_note_reading(screen, font, small_font, text_lines):
    # Renders the inspectable note document
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((*COLOR_VOID, 230))
    screen.blit(overlay, (0, 0))

    note_w, note_h = 600, 240
    note_x = (WINDOW_WIDTH - note_w) // 2
    note_y = (WINDOW_HEIGHT - note_h) // 2
    note_rect = pygame.Rect(note_x, note_y, note_w, note_h)

    pygame.draw.rect(screen, COLOR_NOTE, note_rect, border_radius=6)
    pygame.draw.rect(screen, COLOR_DIRT, note_rect, 3, border_radius=6)

    title = font.render("-- STRANGE NOTE --", True, (40, 30, 20))
    screen.blit(title, (note_x + note_w // 2 - title.get_width() // 2, note_y + 15))

    curr_y = note_y + 50
    for line in text_lines:
        color = COLOR_BLOOD_BRIGHT if "[" in line and "]" in line else (30, 25, 20)
        line_surf = small_font.render(line, True, color) # This is for generating the text
        screen.blit(line_surf, (note_x + 30, curr_y))
        curr_y += 22

    close_surf = small_font.render("[Press SPACE, E or ESC to close]", True, COLOR_BLOOD)
    screen.blit(close_surf, (note_x + note_w // 2 - close_surf.get_width() // 2, note_y + note_h - 26))


# This entire function is for defining the hangman and the different parts of it
# It took quite a lot to program but I thought it was a good idea to develop this within the game
def draw_hangman_figure(screen, x, y, wrong_guesses):
    # This draws the hangman according to the different answers that the player gives 
    color = COLOR_BONE
    pygame.draw.line(screen, COLOR_BLOOD, (x, y + 130), (x + 70, y + 130), 3)
    pygame.draw.line(screen, color, (x + 15, y + 130), (x + 15, y), 3)
    pygame.draw.line(screen, color, (x + 15, y), (x + 60, y), 3)
    pygame.draw.line(screen, color, (x + 60, y), (x + 60, y + 18), 3)

# For this part I had to use the help of Gemini but basically this part of the code represents the body itself of the hangman figure
    parts = [
        lambda: pygame.draw.circle(screen, color, (x + 60, y + 28), 9, 2),
        lambda: pygame.draw.line(screen, color, (x + 60, y + 37), (x + 60, y + 75), 2),
        lambda: pygame.draw.line(screen, color, (x + 60, y + 45), (x + 45, y + 65), 2),
        lambda: pygame.draw.line(screen, color, (x + 60, y + 45), (x + 75, y + 65), 2),
        lambda: pygame.draw.line(screen, color, (x + 60, y + 75), (x + 45, y + 105), 2),
        lambda: pygame.draw.line(screen, color, (x + 60, y + 75), (x + 75, y + 105), 2),
    ]

    for i in range(min(wrong_guesses, len(parts))):
        parts[i]()


def draw_hangman_popup(screen, puzzle, font, small_font, big_font):
    # This draws the interface of the minigame 
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((*COLOR_FOG, 230))
    screen.blit(overlay, (0, 0))

    box_width, box_height = 640, 270
    box_x = (WINDOW_WIDTH - box_width) // 2
    box_y = (WINDOW_HEIGHT - box_height) // 2
    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

    pygame.draw.rect(screen, COLOR_VOID, box_rect, border_radius=6)
    pygame.draw.rect(screen, COLOR_BLOOD, box_rect, 2, border_radius=6)

    title = font.render("The Ghost of the Yard Puzzle", True, COLOR_BONE)
    screen.blit(title, (box_x + box_width // 2 - title.get_width() // 2, box_y + 12))

    draw_hangman_figure(screen, box_x + 40, box_y + 40, puzzle.wrong_guesses)

    word_surface = big_font.render(puzzle.display_word(), True, COLOR_SICKLY)
    screen.blit(word_surface, (box_x + 190, box_y + 65))

    wrong_letters = sorted(letter for letter in puzzle.guessed_letters if letter not in puzzle.word)
    wrong_text = font.render("Wrong: " + " ".join(wrong_letters), True, COLOR_BLOOD_BRIGHT)
    screen.blit(wrong_text, (box_x + 190, box_y + 115))

    if puzzle.solved:
        msg1 = small_font.render("The ghost whispers: 'You are worthy. Here, take this shovel...'", True, (120, 200, 140)) # Added some dialogue options to make the experience more interactive
        msg2 = small_font.render(f"The ghost smiles in a strange way and whispers: [{MEDICATION_COORDINATES}]", True, COLOR_GOLD)
        msg3 = small_font.render("Press ESC to return to the Yard.", True, (160, 160, 160))

        screen.blit(msg1, (box_x + box_width // 2 - msg1.get_width() // 2, box_y + 175))
        screen.blit(msg2, (box_x + box_width // 2 - msg2.get_width() // 2, box_y + 200))
        screen.blit(msg3, (box_x + box_width // 2 - msg3.get_width() // 2, box_y + 230))

    elif puzzle.failed:
        fail_surface = font.render("You failed. Press R to restart.", True, COLOR_BLOOD_BRIGHT)
        screen.blit(fail_surface, (box_x + box_width // 2 - fail_surface.get_width() // 2, box_y + 195))

    else:
        hint_surface = small_font.render("Guess the letters with your keyboard  (ESC to leave)", True, (150, 145, 150))
        screen.blit(hint_surface, (box_x + box_width // 2 - hint_surface.get_width() // 2, box_y + 210))

# Added the weights minigame which is required for the good ending. The function is basically that the player has to press ESCAPE in order to obtain the note
def draw_weights_minigame(screen, progress, font, small_font):
    # This draws the smashing screen where the player has to press SPACE couple of times 
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((*COLOR_FOG, 220))
    screen.blit(overlay, (0, 0))

    box_w, box_h = 540, 200
    box_x = (WINDOW_WIDTH - box_w) // 2
    box_y = (WINDOW_HEIGHT - box_h) // 2
    box_rect = pygame.Rect(box_x, box_y, box_w, box_h)

    pygame.draw.rect(screen, COLOR_VOID, box_rect, border_radius=6)
    pygame.draw.rect(screen, COLOR_BLOOD, box_rect, 2, border_radius=6)

    title = font.render("Heavy Weights Puzzle", True, COLOR_BONE)
    hint = small_font.render("Press [SPACE] quickly to lift the bar | [ESC] to give up", True, (160, 160, 160))
    screen.blit(title, (box_x + box_w // 2 - title.get_width() // 2, box_y + 20))
    screen.blit(hint, (box_x + box_w // 2 - hint.get_width() // 2, box_y + 50))

    # Background bar
    bar_w, bar_h = 320, 22
    bar_x = box_x + (box_w - bar_w) // 2
    bar_y = box_y + 90
    pygame.draw.rect(screen, (25, 20, 25), (bar_x, bar_y, bar_w, bar_h), border_radius=4)

    # Filled progress bar
    fill_w = int((progress / 100.0) * bar_w)
    if fill_w > 0:
        pygame.draw.rect(screen, COLOR_BLOOD_BRIGHT, (bar_x, bar_y, fill_w, bar_h), border_radius=4)

    pygame.draw.rect(screen, COLOR_BONE, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=4)


# Defining the class of the main character and the ghost

class StickmanPlayer:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.speed = 2.5
        self.facing = 1
        self.anim_timer = 0
        self.is_moving = False

    def move(self, dx, dy, obstacles):
        self.is_moving = (dx != 0 or dy != 0)
        if dx != 0:
            self.facing = 1 if dx > 0 else -1

        new_x = self.x + dx * self.speed
        test_rect_x = pygame.Rect(int(new_x - 8), int(self.y - 6), 16, 8)
        if 20 <= new_x <= WINDOW_WIDTH - 20 and not any(test_rect_x.colliderect(obs) for obs in obstacles):
            self.x = new_x

        new_y = self.y + dy * self.speed
        test_rect_y = pygame.Rect(int(self.x - 8), int(new_y - 6), 16, 8)
        if 265 <= new_y <= 325 and not any(test_rect_y.colliderect(obs) for obs in obstacles):
            self.y = new_y

        if self.is_moving:
            self.anim_timer += 0.2

    def draw(self, screen):
        cx, cy = int(self.x), int(self.y)
        color = COLOR_STICKMAN
        line_w = 2

        # This is to draw the head and the eye of the character
        head_pos = (cx, cy - 36)
        pygame.draw.circle(screen, color, head_pos, 6, line_w)
        pygame.draw.circle(screen, (200, 50, 50), (head_pos[0] + (2 * self.facing), head_pos[1]), 1)

        # This is for the spine
        neck_pos = (cx, cy - 30)
        hip_pos = (cx, cy - 14)
        pygame.draw.line(screen, color, neck_pos, hip_pos, line_w)

        # Decided to add some timers and animations
        walk_swing = math.sin(self.anim_timer) * 5 if self.is_moving else 0

        # This is to define the structure of the torso including the shoulders and both hands/arms
        shoulder_pos = (cx, cy - 26)
        left_hand = (cx - int(7 * self.facing) - int(walk_swing), cy - 16)
        right_hand = (cx + int(7 * self.facing) + int(walk_swing), cy - 16)
        pygame.draw.line(screen, color, shoulder_pos, left_hand, line_w)
        pygame.draw.line(screen, color, shoulder_pos, right_hand, line_w)

        # I drew the legs
        left_foot = (cx - 5 - int(walk_swing), cy)
        right_foot = (cx + 5 + int(walk_swing), cy)
        pygame.draw.line(screen, color, hip_pos, left_foot, line_w)
        pygame.draw.line(screen, color, hip_pos, right_foot, line_w)

# The GhostNPC is basically the skeleton so I am gonna change this because it would be cool to have a better design of it
class GhostNPC:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def is_near(self, player):
        dist = math.hypot(self.rect.centerx - player.x, self.rect.centery - (player.y - 20))
        return dist < 65


# Here is where basically begins the main structure for this section of the game

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("The Ghost's Puzzle")
    clock = pygame.time.Clock()

    inventory = Inventory()

    font = pygame.font.SysFont(None, 22)
    small_font = pygame.font.SysFont(None, 18)
    big_font = pygame.font.SysFont(None, 34)

    # Load background image
    yard_bg = pygame.image.load("yard_background.png").convert()
    yard_bg = pygame.transform.scale(yard_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))

    player = StickmanPlayer(260, 290)
    ghost = GhostNPC(435, 190, 75, 100)

    # Interactive zone for the Weights bench
    weights_zone = pygame.Rect(230, 200, 70, 70)
    weights_progress = 0.0
    weights_cleared = False

    dumbbells_zone = pygame.Rect(100, 220, 50, 50)
    key_fragment_found = False

    # Static collision obstacles
    # Had to implement the collision because otherwise we would have the same problem as with the demo of the maze
    obstacles = [
        pygame.Rect(60, 190, 60, 80),
        pygame.Rect(180, 215, 60, 55),
        pygame.Rect(550, 160, 110, 100),
    ]

    puzzle = HangmanPuzzle(WORD_TO_GUESS)
    
    game_state = "EXPLORE"

    # Digging state variables
    hole_dug = False
    feedback_message = ""
    feedback_timer = 0

    # Variables for dialogues
    monologue_lines = []
    monologue_index = 0
    monologue_speaker = "Protagonist"

# This is the main text for when the protagonist finds the note after completing the Weights puzzle
    note_text = [
        "I do not know how long have I been here",
        "So confused...",
        "I hear voices sometimes",
        "I hear them scream",
        "I do not know what is going on here...",
        "I need to escape",
        "[ 7 4 - - - - ]",
    ]

    # Dialogue for the Ghost puzzle (aka hangman puzzle)
    dialogue_nodes = {
        "intro": {
            "speaker": "The Ghost of the Yard:",
            "text": "You are looking for answers. You seek a way out from this prison.",
            "options": {
                "1": "Please, I need to escape. I do not know where I am. Can you please help me? I will do whatever you want.",
                "2": "Step away. (Leave)"
            }
        },
        "medication_info": {
            "speaker": "The ghost of the Yard:",
            "text": "I help you, but only if you solve a small puzzle.",
            "options": {
                "1": "I will accept that challenge.",
                "2": "I do not trust you. (Leave)"
            }
        },
        "challenge_prompt": {
            "speaker": "The ghost of the Yard:",
            "text": "Then prove you are worthy for this challenge. Guess the word and I will help you escape.",
            "options": {
                "1": "Step up to the gallows (Start Hangman)",
                "2": "Step away. (Leave)"
            }
        }
    }
    current_dialogue = "intro"

    running = True
    while running:
        # Weights puzzle
        if game_state == "WEIGHTS_GAME":
            weights_progress = max(0.0, weights_progress - 0.5)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Inventory handlers
                if game_state == "EXPLORE":
                    if event.key in (pygame.K_i, pygame.K_TAB):
                        game_state = "INVENTORY"

                    # Talk with Ghost NPC
                    elif event.key == pygame.K_e and ghost.is_near(player):
                        game_state = "DIALOGUE"
                        current_dialogue = "intro"

                    # Interact with the weights bench
                    elif event.key == pygame.K_e:
                        dist_weights = math.hypot(weights_zone.centerx - player.x, weights_zone.centery - player.y)
                        dist_dumbbells = math.hypot(dumbbells_zone.centerx - player.x, dumbbells_zone.centery - player.y)

                        # Conditional loop for the Weight puzzle (Good ending)
                        if dist_weights < 55:
                            if not weights_cleared:
                                game_state = "WEIGHTS_GAME"
                                weights_progress = 0.0
                            else:
                                game_state = "READ_NOTE"

                        # Conditional loop for the Key fragment (Neutral/Loop ending)
                        elif dist_dumbbells < 50:
                            if not key_fragment_found:
                                key_fragment_found = True
                                inventory.add_item("Key Fragment 1")
                                monologue_lines = [
                                    "You try to move the heavy dumbbells to inspect as you have found something interesting",
                                    "Trapped underneath you discover a fragment of an old key.",
                                    "It looks like it needs to be combined with other parts",
                                    "It might be useful for the door that you found at the beginning.",
                                    "Without giving much thought, you decide to keep it. Just in case it might be useful"
                                ]

                                monologue_index = 0
                                monologue_speaker = "Protagonist"
                                game_state = "MONOLOGUE"
                            else:
                                feedback_message = "There is nothing else hidden beneath the dumbbells."
                                feedback_timer = 120

                    # Dig action with Shovel

                    elif event.key == pygame.K_SPACE:
                        if "Spade" in inventory.items:
                            dist_to_spot = math.hypot(player.x - DIG_TARGET_X, player.y - DIG_TARGET_Y)
                            if dist_to_spot < 35:
                                if not hole_dug:
                                    hole_dug = True
                                    inventory.add_item("Medication Fragment 1")
                                    feedback_message = "You managed to obtain the Medication fragment!"
                                    feedback_timer = 180
                                else:
                                    feedback_message = "You already excavated this spot."
                                    feedback_timer = 120
                            else:
                                feedback_message = "You dig into the hard ground, but find nothing of interest here..."
                                feedback_timer = 120
                        else:
                            feedback_message = "You need some sort of tool to dig here."
                            feedback_timer = 120

                # Monologue reaction box handler
                elif game_state == "MONOLOGUE":
                    if event.key in (pygame.K_SPACE, pygame.K_e, pygame.K_RETURN):
                        monologue_index += 1
                        if monologue_index >= len(monologue_lines):
                            game_state = "EXPLORE"
                    elif event.key == pygame.K_ESCAPE:
                        game_state = "EXPLORE"

                # Inventory usage with arrow keys
                # For the player basically to handle the inventory.
                elif game_state == "INVENTORY":
                    if event.key == pygame.K_RIGHT:
                        inventory.move_selection(1)
                    elif event.key == pygame.K_LEFT:
                        inventory.move_selection(-1)
                    elif event.key in (pygame.K_ESCAPE, pygame.K_i, pygame.K_TAB):
                        game_state = "EXPLORE"
                    elif event.key == pygame.K_e:
                        selected = inventory.get_selected_item()
                        if selected and "Strange Note" in selected:
                            game_state = "READ_NOTE"

                # Inner monologue after reading the note
                elif game_state == "READ_NOTE":
                    if event.key in (pygame.K_SPACE, pygame.K_ESCAPE, pygame.K_e):
                        monologue_lines = [
                            "After reading it carefully you then dedicate some minutes to reflect.",
                            "You get lost within your own thoughts. You feel so confused...",
                            "'I need to find a way out. Maybe this code can help me.'",
                            "You still cannot remove that strange feeling from yourself but you decide to move on",
                        ]
                        monologue_index = 0
                        monologue_speaker = "Protagonist"
                        game_state = "MONOLOGUE"

                # Dialogue with the Ghost handlers
                elif game_state == "DIALOGUE":
                    if event.key == pygame.K_1:
                        if current_dialogue == "intro":
                            current_dialogue = "medication_info"
                        elif current_dialogue == "medication_info":
                            current_dialogue = "challenge_prompt"
                        elif current_dialogue == "challenge_prompt":
                            game_state = "PUZZLE"

                    elif event.key in (pygame.K_2, pygame.K_ESCAPE):
                        game_state = "EXPLORE"

                # Hangman Puzzle handlers
                elif game_state == "PUZZLE":
                    if event.key == pygame.K_ESCAPE:
                        game_state = "EXPLORE"
                    elif event.key == pygame.K_r and puzzle.failed:
                        puzzle.reset()
                    elif pygame.K_a <= event.key <= pygame.K_z and not puzzle.solved:
                        puzzle.guess(chr(event.key))

                        if puzzle.solved and not puzzle.reward_claimed:
                            inventory.add_item("Spade")
                            puzzle.reward_claimed = True

                # Weights state handlers
                elif game_state == "WEIGHTS_GAME":
                    if event.key == pygame.K_SPACE:
                        weights_progress += 12.0
                        if weights_progress >= 100.0:
                            weights_cleared = True
                            if "Strange Note 1" not in inventory.items:
                                inventory.add_item("Strange Note 1")

                            # Reaction of the player
                            print("\nYour hands start shaking after lifting the weights")
                            print("You find some strange note. Your hands start shaking. You feel something familiar...")
                            print("You say to yourself: 'This is so odd...Why am I feeling like this?'")
                            print("'What is this blood...I do not know why I am doing this but need to figure it out. Need to continue'\n")

                            game_state = "READ_NOTE"

                    elif event.key == pygame.K_ESCAPE:
                        game_state = "EXPLORE"

        # Movement handling (arrow keys only)
        if game_state == "EXPLORE":
            keys = pygame.key.get_pressed()
            dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
            dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
            player.move(dx, dy, obstacles)

        # Render background
        screen.blit(yard_bg, (0, 0))

        # Render excavated hole marker
        if hole_dug:
            pygame.draw.ellipse(screen, COLOR_DIRT, (DIG_TARGET_X - 14, DIG_TARGET_Y - 6, 28, 12))
            pygame.draw.ellipse(screen, COLOR_VOID, (DIG_TARGET_X - 10, DIG_TARGET_Y - 4, 20, 8))

        # Render player
        player.draw(screen)

        # Render HUD elements
        if game_state == "EXPLORE":
            # Ghost interaction option
            if ghost.is_near(player):
                prompt_surf = small_font.render("Press [E] to speak with the Skeleton Ghost", True, COLOR_GOLD)
                screen.blit(prompt_surf, (WINDOW_WIDTH // 2 - prompt_surf.get_width() // 2, WINDOW_HEIGHT - 25))

            # Weights bench instructions
            # You get this message when you are nearby the weights bench
            dist_w = math.hypot(weights_zone.centerx - player.x, weights_zone.centery - player.y)
            if dist_w < 55 and not weights_cleared:
                w_surf = small_font.render("Press [E] to inspect the Weights Bench", True, COLOR_GOLD)
                screen.blit(w_surf, (WINDOW_WIDTH // 2 - w_surf.get_width() // 2, WINDOW_HEIGHT - 25))

            # Visual render for the dumbbells
            dist_d = math.hypot(dumbbells_zone.centerx - player.x, dumbbells_zone.centery - player.y)
            if dist_d < 50 and not key_fragment_found:
                d_surf = small_font.render("Press [E] to inspect the Dumbbells", True, COLOR_GOLD)
                screen.blit(d_surf, (WINDOW_WIDTH // 2 - d_surf.get_width() // 2, WINDOW_HEIGHT - 25))

            # Player coordinates display
            coords_surf = small_font.render(f"Pos: X: {int(player.x)}, Y: {int(player.y)}", True, (160, 160, 160))
            screen.blit(coords_surf, (WINDOW_WIDTH - 120, 10))

            # Inventory display
            # The idea of introducing the TAB option came from the Resident Evil games in which normally you press this button to use the inventory 
            inv_surf = small_font.render(f"Inventory [I/TAB]: {', '.join(inventory.items) if inventory.items else 'Empty'}", True, COLOR_BONE)
            screen.blit(inv_surf, (15, 10))

            # Dig action hint
            if "Spade" in inventory.items and not hole_dug:
                shovel_hint = small_font.render("Press [SPACE] to Dig with Shovel", True, (120, 200, 140))
                screen.blit(shovel_hint, (15, 28))

            # Feedback messages
            if feedback_timer > 0:
                feed_surf = small_font.render(feedback_message, True, COLOR_GOLD)
                screen.blit(feed_surf, (WINDOW_WIDTH // 2 - feed_surf.get_width() // 2, WINDOW_HEIGHT - 45))
                feedback_timer -= 1

        
        elif game_state == "DIALOGUE":
            draw_dialogue_box(screen, font, small_font, dialogue_nodes[current_dialogue])

        elif game_state == "PUZZLE":
            draw_hangman_popup(screen, puzzle, font, small_font, big_font)

        elif game_state == "WEIGHTS_GAME":
            draw_weights_minigame(screen, weights_progress, font, small_font)

        elif game_state == "INVENTORY":
            inventory.draw(screen, font, small_font)

        elif game_state == "READ_NOTE":
            draw_note_reading(screen, font, small_font, note_text)

        elif game_state == "MONOLOGUE":
            draw_monologue_box(screen, font, small_font, monologue_speaker, monologue_lines[monologue_index])

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
