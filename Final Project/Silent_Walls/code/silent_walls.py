# mainly by Katharina Noske (other coding parts form Samuel Sosa Florido or Karoline Fischer will be pointed out)

# unfortunately we started with coding the game separately in different files
# so we faced the issue to combine it into ONE compleet game
# so we did needed to reorganization the code (the file structure and the files themselves)
# so this is the attempt to put it all together in one game without bugs (with a main structure and then the separated rooms)

import pygame

# import (from other files in our main file)
from sys import *
# from inventory import *
# from maze import *
# from hospital import *
from cafeteria import *
# from yard import *
from cell import *
from character import Character
# from scipy._lib.pyprima.cobyla import update

import os
import sys

# Setzt den Pfad immer relativ zur .py Datei
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# basic pygame-setup to run the game
pygame.init()
screen = pygame.display.set_mode((980, 480))
clock = pygame.time.Clock()

# make the window "pretty" (Name of the window)
pygame.display.set_caption("silent walls")
background = "gray"
base_color = "black"


base = pygame.Surface((980, 250))
base.fill(base_color)

#image = "pixil-frame-0(5).png"

# your character
# collision by Karo Fischer 



# I got help from AI for the main Game Loop here

# Basic Class for all the Rooms
class Room:
    def __init__(self, name):
        self.name = name
        self.exits = {}  # name -> pygame.Rect

    def draw(self, screen):
        pass

    def check_exits(self, character):
        """gibt den Namen des Ausgangs zurück, falls der Spieler ihn berührt"""
        for exit_name, exit_rect in self.exits.items():
            if character.rect.colliderect(exit_rect):
                return exit_name
        return None

# Placeholder for the Rooms
class SimpleRoom(Room):
    def __init__(self, name, color, entry_pos=(50, 200)):
        super().__init__(name)
        self.color = color
        self.entry_pos = entry_pos
        # an exit that is allways goining back to the maze
        self.exits = {"maze": pygame.Rect(900, 200, 40, 40)}

    def draw(self, screen):
        screen.fill(self.color)
        pygame.draw.rect(screen, (255, 0, 0), self.exits["maze"])

# from the Maze to our Rooms
class Maze(Room):
    def __init__(self):
        super().__init__("maze")
        self.entry_pos = (50, 200)

        # 3 feste Positionen im Maze
        self.exit_rects = {
            "exit_1": pygame.Rect(900, 50, 40, 40),
            "exit_2": pygame.Rect(900, 200, 40, 40),
            "exit_3": pygame.Rect(900, 350, 40, 40),
        }

        # hier steht, welcher Raum hinter exit_1/2/3 liegt
        self.destinations = []

    def set_destinations(self, destinations):
        """destinations = Liste mit 3 Raum-Namen in Reihenfolge exit_1, exit_2, exit_3"""
        self.destinations = destinations

    def draw(self, screen):
        screen.fill((40, 40, 40))
        for rect in self.exit_rects.values():
            pygame.draw.rect(screen, (0, 255, 0), rect)

    def check_exits(self, character):
        for i, rect in enumerate(self.exit_rects.values()):
            if character.rect.colliderect(rect):
                return self.destinations[i]
        return None

# basic Game Loop
class Game:
    ALL_ROOMS = ["cell", "hospital", "cafeteria", "yard"]

    def __init__(self):
        self.character = Character(50, 200)

        self.rooms = {
            "cell": SimpleRoom("cell", (100, 100, 150)),
            "hospital": SimpleRoom("hospital", (200, 200, 200)),
            "cafeteria": SimpleRoom("cafeteria", (150, 100, 50)),
            "yard": SimpleRoom("yard", (50, 150, 50)),
        }
        self.maze = Maze()

        # Startzustand: Spieler beginnt in der Zelle
        self.current_state = "cell"
        self.previous_room = "cell"  # merkt sich, woher der Spieler zuletzt kam

    def enter_maze(self, coming_from):
        """berechnet die 3 Ausgänge des Maze je nachdem, aus welchem Raum man kommt"""
        if coming_from == "cell":
            destinations = ["hospital", "cafeteria", "yard"]
        else:
            # Startraum + die beiden anderen Räume (außer dem aktuellen)
            destinations = [r for r in self.ALL_ROOMS if r != coming_from]

        self.maze.set_destinations(destinations)
        self.current_state = "maze"
        self.character.set_pos(*self.maze.entry_pos)

    def enter_room(self, room_name):
        self.current_state = room_name
        self.previous_room = room_name
        self.character.set_pos(*self.rooms[room_name].entry_pos)

    def update(self):
        self.character.move()

        if self.current_state == "maze":
            objects = self.maze.objects if hasattr(self.maze, 'objects') else []
        else:
            current_room = self.rooms[self.current_state]
            objects = current_room.objects if hasattr(current_room, 'objects') else []

        self.character.update(objects)

        if self.current_state == "maze":
            result = self.maze.check_exits(self.character)
            if result:
                self.enter_room(result)
        else:
            current_room = self.rooms[self.current_state]
            result = current_room.check_exits(self.character)
            if result == "maze":
                self.enter_maze(self.previous_room)

    def draw(self, screen):
        if self.current_state == "maze":
            self.maze.draw(screen)
        else:
            self.rooms[self.current_state].draw(screen)

        self.character.draw(screen)

# AI help end





character = Character(500, 300)
game = Game()

# back to the basic pygame-setup to run the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    game.update()
    screen.fill((background))
    screen.blit(base, (0, 230))
    game.draw(screen)

    pygame.display.update()
    # limits FPS to 60
    clock.tick(60)

    #character.draw(screen)
    


    #character.move(objects)
        #if your_character_rect.colliderect(chair.rect) and chair.rect.collidepoint(event.pos) and event.type == pygame.mouse.get_pressed():
           #print('Hello')

    # basic background color (to draw over - blanc canvas to start with / reset the background at every frame)
    

    # put the separated game sections together
    



    #cafeteria.update()
    #character.update()
    

    
