import pygame
import random

import os
import sys

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


class Table():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.image.load ("")
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def update(self):
        pass 


class Toilet():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass 


class Key():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass 


class Cell():
    def __init__(self, your_character):
        self.your_character = your_character
        self.table_x = 500
        self.table_y = 300

    def draw(self, screen):
        background = "grey"
        base_color = "black"

        base = pygame.Surface(())


class Character():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.image.load("pixil-frame-0(5).png").convert_alpha()
        self.transformed_image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.transformed_image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.transformed_image, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5
        if keys[pygame.K_w]:
            self.rect.y -= 5
        if keys[pygame.K_s]:
            self.rect.y += 5

    def update(self):
        self.move()


Character.update()

