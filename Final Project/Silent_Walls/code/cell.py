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


class Cell():
    def __init__(self, your_character):
        self.your_character = your_character
        self.table_x = 980
        self.table_y = 250

        self.toilet = Toilet(200, 200)
        self.chest = Chest(100, 200)
        self.shackles = Shackles(300, 400)
        self.key = Key(600,200)
        self.table = Table(400, 200)
        self.bed = Bed(500, 200)

        #list of objects in cell, so that not every object has to be called upon itself
        self.objects = [self.table, self.toilet, self.chest, self.shackles, self.key, self.bed]

        self.background = pygame.image.load("pixil-layer-Windows_line.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (980, 250))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        #objects drawn over background
        for obj in self.objects:
            obj.draw(screen)



class Table():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load ("pixil-layer-Table.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def update(self):
        pass 

class Bed():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load ("pixil-layer-Bed_lines.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def update(self):
        pass


class Toilet():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load ("pixil-layer-Toilet.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass 


class Key():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load ("pixil-layer-KEy.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass 

class Chest():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load ("pixil-layer-Chest.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass 

class Shackles():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load ("pixil-layer-Shackles.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass 

class Table():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load ("pixil-layer-Table.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass 


class Character():
    def __init__(self, x, y):
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


pygame.init()
screen = pygame.display.set_mode ((980, 480))
clock = pygame.time.Clock()

character = Character(100, 100)
cell = Cell(character)

running = True
while running:
    events = pygame.event.get()
    for event in events: 
        if event.type == pygame.QUIT:
            running = False

    cell.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

#Character.update()

