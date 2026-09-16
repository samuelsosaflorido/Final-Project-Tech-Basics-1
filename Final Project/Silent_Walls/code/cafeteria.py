# Cafeteria = Room by Kathi
# adjusted by Karo Fischer to make room/maze/hospital connection possible + iron out bugs

#import objects
# I did draw all images by myself except for the background wall - the background is from Karo

import pygame
from silent_walls_character import *

pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 24)


class Cafeteria():
    def __init__(self):
        self.food = Food(250, 190)
        self.table1 = Table1(30, 320)
        self.table2 = Table2(700, 300)
        self.trash = Trash(550, 250)
        self.letter = Letter(730, 220)     # on the Table with the Letter
        self.key = Key(50, 10)             # in the Trash
        self.medicine = Medicine(600, 90)  # the Skeleton has the medicine

        self.letter_visible = False
        self.key_found = False
        self.medicine_given = False

        # Skelett-Question
        self.talking_to_skeleton = False
        self.question_answered = False
        self.question = "Germans are known for the love for bread, but how many types of bread do they have?"
        self.answers = ["more than 2.200", "more than 3.200", "more than 4.200"]
        self.correct_answer_index = 1  # the correct answer: "more than 3.200"

        self.objects_always = [self.food, self.table1, self.table2, self.trash]

        self.background = pygame.image.load("cell_wall.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (980, 480))

    def draw(self, screen, character):
        screen.blit(self.background, (0, 0))

        for obj in self.objects_always:
            obj.draw(screen)

        if self.letter_visible:
            self.letter.draw(screen)

        if self.key_found:
            self.key.draw(screen)

        if self.medicine_given:
            self.medicine.draw(screen)

        character.draw(screen)

        if self.talking_to_skeleton and not self.question_answered:
            self.draw_question(screen)

    # AI helped me here a bit for the Question-Code and the collision with the objects
    def draw_question(self, screen):
        overlay = pygame.Surface((980, 480), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        line1 = "Germans are known for the love for bread,"
        line2 = "but how many types of bread do they have?"

        line1_surface = FONT.render(line1, True, (255, 255, 255))
        line2_surface = FONT.render(line2, True, (255, 255, 255))
        screen.blit(line1_surface, (300, 130))
        screen.blit(line2_surface, (300, 160))

        for i, answer in enumerate(self.answers):
            answer_surface = FONT.render(f"{i + 1}: {answer}", True, (255, 255, 0))
            screen.blit(answer_surface, (300, 200 + i * 40))

    def update(self, character, events, inventory):
        character.update(self.objects_always, None)

        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Show Letter: Character touches Table2 AND pressed the mouse
                if character.rect.colliderect(self.table2.rect) and self.table2.rect.collidepoint(mouse_pos):
                    self.letter_visible = True

                # Finding the key: Character touches the Trash AND pressed the mouse
                if character.rect.colliderect(self.trash.rect) and self.trash.rect.collidepoint(mouse_pos):
                    if not self.key_found:
                        self.key_found = True
                        inventory.add_item("Key (Cafeteria)")

                # Talk to the Skeleton: Character touches Food AND pressed the mouse
                if character.rect.colliderect(self.food.rect) and self.food.rect.collidepoint(mouse_pos):
                    if not self.medicine_given:
                        self.talking_to_skeleton = True

            if event.type == pygame.KEYDOWN and self.talking_to_skeleton and not self.question_answered:
                if event.key == pygame.K_1:
                    self.check_answer(0, character)
                elif event.key == pygame.K_2:
                    self.check_answer(1, character)
                elif event.key == pygame.K_3:
                    self.check_answer(2, character)

    def check_answer(self, index, inventory):
        if index == self.correct_answer_index:
            self.question_answered = True
            self.medicine_given = True
            inventory.add_item("Medication (Cafeteria)")
        self.talking_to_skeleton = False

    # AI help end



class Food():
    def __init__(self, x, y):
        self.image = pygame.image.load("cafeteria_food.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (290, 170))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Table1():
    def __init__(self, x, y):
        self.image = pygame.image.load("cafeteria_table.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 150))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collision_rect = pygame.Rect(x + 60, y + 100, 80, 30) 

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Table2():
    def __init__(self, x, y):
        self.image = pygame.image.load("cafeteria_table_with_letter.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (240, 150))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Trash():
    def __init__(self, x, y):
        self.image = pygame.image.load("cafeteria_trash.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Letter():
    def __init__(self, x, y):
        self.image = pygame.image.load("cafeteria_letter.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 400))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Key():
    def __init__(self, x, y):
        self.image = pygame.image.load("cafeteria_key.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Medicine():
    def __init__(self, x, y):
        self.image = pygame.image.load("cafeteria_medicine.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)