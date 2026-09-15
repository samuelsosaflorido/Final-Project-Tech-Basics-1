# the basic room code is by Kathi
# The rest of the code has been completed by Samuel trying to not to modify anything that has been established before
# Plus adding making that the items can be used to unlock the areas after the player has completed the game 

import sys
import random
import inventory
import pygame
from silent_walls_character import *
from silent_walls_intro_text import *
from silent_walls_endings import *

pygame.init()


class Hospital():
    def __init__(self):
        self.bed = Bed(15, 100)
        self.table = Table(570, 340)
        self.door1 = DoorK(800, 70)
        self.door2 = DoorC(500, 70)
        self.skeleton = Skeleton(300, 70)

        self.background = pygame.image.load("cell_wall.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (980, 480))

        self.objects = [self.bed, self.table, self.door1, self.door2, self.skeleton]
        self.intro_shown = False

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        for obj in self.objects:
            obj.draw(screen)

    def update(self, character, events, screen, clock):
        if not self.intro_shown:
            show_intro_text(screen, clock)
            self.intro_shown = True
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

                if character.rect.colliderect(self.door2.rect):
                    if character.letters >= 3:
                        btn_width, btn_height = 160, 50
                        spacing = 40
                        start_x = (980 - (btn_width * 3 + spacing * 2)) // 2
                        btn_y = 260

                        codes = ["734", "379", "715"]
                        random.shuffle(codes)

                        options = [
                            {"rect": pygame.Rect(start_x, btn_y, btn_width, btn_height), "code": codes[0]},
                            {"rect": pygame.Rect(start_x + btn_width + spacing, btn_y, btn_width, btn_height),
                             "code": codes[1]},
                            {"rect": pygame.Rect(start_x + (btn_width + spacing) * 2, btn_y, btn_width, btn_height),
                             "code": codes[2]},
                        ]

                        overlay = pygame.Surface((980, 480))
                        overlay.set_alpha(180)
                        overlay.fill((0, 0, 0))

                        font = pygame.font.Font(None, 36)
                        selected_code = None

                        while selected_code is None:
                            mouse_pos = pygame.mouse.get_pos()

                            for opt_event in pygame.event.get():
                                if opt_event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if opt_event.type == pygame.MOUSEBUTTONDOWN and opt_event.button == 1:
                                    for opt in options:
                                        if opt["rect"].collidepoint(opt_event.pos):
                                            selected_code = opt["code"]
                                            break

                            screen.blit(overlay, (0, 0))
                            prompt_surf = font.render("Select the correct code:", True, (255, 255, 255))
                            prompt_rect = prompt_surf.get_rect(center=(490, 180))
                            screen.blit(prompt_surf, prompt_rect)

                            for opt in options:
                                is_hovered = opt["rect"].collidepoint(mouse_pos)
                                bg_color = (90, 90, 90) if is_hovered else (45, 45, 45)
                                border_color = (255, 255, 255) if is_hovered else (150, 150, 150)

                                pygame.draw.rect(screen, bg_color, opt["rect"])
                                pygame.draw.rect(screen, border_color, opt["rect"], 2)

                                text_surf = font.render(opt["code"], True, (255, 255, 255))
                                text_rect = text_surf.get_rect(center=opt["rect"].center)
                                screen.blit(text_surf, text_rect)

                            pygame.display.flip()
                            clock.tick(60)

                        if selected_code == "734":
                            show_ending(screen, clock, "letters_734")
                        elif selected_code == "379":
                            show_ending(screen, clock, "letters_379")
                        elif selected_code == "715":
                            show_ending(screen, clock, "letters_715")

                        pygame.quit()
                        sys.exit()
                    else:
                        print("For this door it is required a code. Maybe I can find this somewhere")

                elif character.rect.colliderect(self.door1.rect):
                    if character.keys >= 3:
                        show_ending(screen, clock, "keys")
                        pygame.quit()
                        sys.exit()
                    else:
                        print("This door requires three keys to be unlocked. Maybe I need to look somewhere")

                elif character.rect.colliderect(self.bed.rect):
                    print("This bed gives a strange feeling...")

                elif character.rect.colliderect(self.table.rect):
                    if character.medication >= 3:
                        show_ending(screen, clock, "medication")
                        pygame.quit()
                        sys.exit()
                    else:
                        print("It a weird looking table but seems something is needed here.")


class Bed():
    def __init__(self, x, y):
        self.image = pygame.image.load("hospital_bed.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (350, 250))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Table():
    def __init__(self, x, y):
        self.image = pygame.image.load("hospital_table.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 150))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class DoorK():
    def __init__(self, x, y):
        self.image = pygame.image.load("hospital_door_key.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 220))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class DoorC():
    def __init__(self, x, y):
        self.image = pygame.image.load("hospital_door_code.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (140, 220))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Skeleton():
    def __init__(self, x, y):
        self.image = pygame.image.load("hospital_skeleton_poster.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 140))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
