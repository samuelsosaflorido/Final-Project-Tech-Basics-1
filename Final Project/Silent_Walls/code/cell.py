import pygame
import random

import os
import sys

from character import Character
from inventory import Inventory

# Setzt den Pfad immer relativ zur .py Datei
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#class Object():
    #def __init__(self, x, y, image):
        #self.x = x
        #self.y = y
        #self.image = image
        #self.rect = self.image.get_rect(topleft=(x, y))

    #def draw(self, screen):
        #screen.blit(self.image, self.rect)

    #def update(self):
        #pass 


class Cell():
    def __init__(self, character):
        self.character = character
        self.table_x = 980
        self.table_y = 480

        self.toilet = Toilet(550, 220)
        self.chest = Chest(90, 260)
        self.shackles = Shackles(460, 80)
        self.key = Key(900,290)
        self.table = Table(290, 200)
        self.bed = Bed(680, 190)

        #list of objects in cell, so that not every object has to be called upon itself
        self.objects = [self.table, self.toilet, self.chest, self.shackles, self.key, self.bed]

        self.font = pygame.font.SysFont("Arial", 20)
        self.background = pygame.image.load("cell_wall.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (980, 480))


    def is_near(self, obj, distance=80):
        return self.character.hitbox.colliderect(
            obj.rect.inflate(distance, distance)
        )

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        #objects drawn over background
        for obj in self.objects:
            if obj == self.key:
                self.key.draw(screen, show_hint=self.is_near(self.key))
            else:
                obj.draw(screen)

        if not self.key.collected and self.is_near(self.key):
            self.key.show_hint(screen)

        self.character.draw(screen)

    def update(self, events, inventory):
        self.character.update(self.objects)

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.check_interaction(inventory)

    def check_interaction(self, inventory):
        if not self.key.collected and self.is_near(self.key):
            self.key.collected = True
            self.objects.remove(self.key)
            inventory.add_item("Key (Cell)")
            print("Key found!")



class Table():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load ("cell_table.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, "red", self.rect, 2)
    
    def update(self):
        pass 

class Bed():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load ("cell_bed.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, "red", self.rect, 2)
    
    def update(self):
        pass

class Toilet():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load ("cell_toilet.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, "red", self.rect, 2)

    def update(self):
        pass 

class Key():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load ("cell_key.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collected = False 
        self.font = pygame.font.SysFont("Arial", 20)

    def draw(self, screen, show_hint=False):
        if not self.collected:
            screen.blit(self.image, self.rect)
            pygame.draw.rect(screen, "red", self.rect, 2)

            if show_hint:
                self.show_hint(screen)

    #def draw_hint(self, screen):
        #hint = self.font.render("Press E to pick up", True, "white")
        #screen.blit(hint, (self.rect.x - 30, self.rect.y - 30))

    def show_hint(self, screen):
        hint = self.font.render ("E drücken, um aufzuheben", True, "white")
        screen.blit(hint, (self.rect.x - 30, self.rect.y - 30))

    def update(self):
        pass 

class Chest():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load ("cell_chest.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, "red", self.rect, 2)

    def update(self):
        pass 

class Shackles():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load ("cell_shackles.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, "red", self.rect, 2)

    def update(self):
        pass 

inventory = Inventory()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode ((980, 480))
    clock = pygame.time.Clock()

    character = Character(300, 300)
    cell = Cell(character)

    running = True
    while running:
        events = pygame.event.get()
        for event in events: 
            if event.type == pygame.QUIT:
                running = False

        try:
            cell.update(events, inventory)
            cell.draw(screen)
        except Exception as e:
            print(e)
            running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

#Character.update()

