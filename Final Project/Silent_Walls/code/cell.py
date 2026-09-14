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
    def __init__(self, character):
        self.character = character
        self.table_x = 980
        self.table_y = 480

        self.toilet = Toilet(0, 0)
        self.chest = Chest(0, 0)
        self.shackles = Shackles(0, 0)
        self.key = Key(0,0)
        self.table = Table(0, 0)
        self.bed = Bed(0, 0)

        #list of objects in cell, so that not every object has to be called upon itself
        self.objects = [self.table, self.toilet, self.chest, self.shackles, self.key, self.bed]

        self.background = pygame.image.load("cell_wall.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (980, 480))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        #objects drawn over background
        for obj in self.objects:
            obj.draw(screen)

        self.character.draw(screen)

    def update(self):
        self.character.update(self.objects)



class Table():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load ("cell_table.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
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

    def update(self):
        pass 

class Key():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load ("cell_key.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

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

    def update(self):
        pass 

class Shackles():
    #def __init__(self, x, y):
        #self.x = x
        #self.y = y
        #self.image = pygame.image.load ("cell_shackles.png").convert_alpha()
        #self.rect = self.image.get_rect(topleft=(x, y))

    #def draw(self, screen):
        #screen.blit(self.image, self.rect)

    #def update(self):
        pass 



class Character():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("pixil-frame-0(5).png").convert_alpha()
        self.transformed_image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.transformed_image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.transformed_image, self.rect)

    def move(self, objects):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= 5
            if self.check_collision(objects):
                self.rect.x +=5

        if keys[pygame.K_d]:
            self.rect.x += 5
            if self.check_collision(objects):
                            self.rect.x -=5

        if keys[pygame.K_w]:
            self.rect.y -= 5
            if self.check_collision(objects):
                            self.rect.x +=5

        if keys[pygame.K_s]:
            self.rect.y += 5
            if self.check_collision(objects):
                            self.rect.x -=5

    def check_collision(self, objects):
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                return True
        return False

    def check_walls(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 980:
            self.rect.right = 980
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom < 480:
            self.rect.bottom = 480

    def update(self, objects):
        self.move(objects)
        self.check_walls()


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

    cell.update()
    cell.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

#Character.update()

