# the basic room code is by Kathi

import pygame
from silent_walls_character import *

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

        self.background = pygame.image.load("cell_wall.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (980, 480))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        for obj in self.objects:
            obj.draw(screen)

    def update(self, character, events):
        pass



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



