# mainly by Katharina Noske (other coding parts form Samuel Sosa Florido or Karoline Fischer will be pointed out)
# adjusted by Karo Fischer to make room/maze/hospital connection possible + iron out bugs

# unfortunately we started with coding the game separately in different files
# so we faced the issue to combine it into ONE compleet game
# so we did needed to reorganization the code (the file structure and the files themselves)
# so this is the attempt to put it all together in one game without bugs (with a main structure and then the separated rooms)
# The screen part was also done with some help with Gemini as we found out that the game started with the main text and not with the main screen

import pygame

# import (from other files in our main file)
from sys import *
from silent_walls_character import Character
from silent_walls_intro_text import show_intro_text
from cafeteria import Cafeteria
from yard import Yard
from cell import Cell
from silent_walls_maze import *
# from scipy._lib.pyprima.cobyla import update
from silent_walls_endings import *
from silent_walls_inventory import Inventory
from hospital import Hospital

import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# basic pygame-setup to run the game
pygame.init()
screen = pygame.display.set_mode((980, 480))
clock = pygame.time.Clock()

# make the window "pretty" (Name of the window)
pygame.display.set_caption("silent walls")


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


class HospitalUnlockedPopup():
    def __init__(self):
        self.active = False
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont("Arial", 18)

    def show(self):
        self.active = True

    def draw(self, screen):
        if not self.active:
            return

        overlay = pygame.Surface((980, 480), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        popup_rect = pygame.Rect(190, 150, 600, 180)
        pygame.draw.rect(screen, (15, 10, 15), popup_rect, border_radius=6)
        pygame.draw.rect(screen, (140, 30, 30), popup_rect, 2, border_radius=6)

        line1 = self.font.render("You've been to every room now.", True, (230, 225, 210))
        line2 = self.font.render("Do you want to try your luck at the hospital", True, (230, 225, 210))
        line3 = self.font.render("or keep exploring?", True, (230, 225, 210))

        screen.blit(line1, (popup_rect.x + 20, popup_rect.y + 20))
        screen.blit(line2, (popup_rect.x + 20, popup_rect.y + 55))
        screen.blit(line3, (popup_rect.x + 20, popup_rect.y + 85))

        h_hint = self.small_font.render("[H] Go to Hospital", True, (200, 180, 120))
        explore_hint = self.small_font.render("[ESC] Keep Exploring", True, (200, 180, 120))

        screen.blit(h_hint, (popup_rect.x + 20, popup_rect.y + 140))
        screen.blit(explore_hint, (popup_rect.x + 300, popup_rect.y + 140))

    def handle_input(self, event):
        if not self.active:
            return None

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                self.active = False
                return "hospital"
            if event.key == pygame.K_ESCAPE:
                self.active = False
                return "explore"

        return None

    # Placeholder for the Rooms


class SimpleRoom(Room):
    def __init__(self, name, color, entry_pos=(50, 200)):
        super().__init__(name)
        self.color = color
        self.entry_pos = entry_pos
        self.exits = {"maze": pygame.Rect(900, 200, 40, 40)}

    def draw(self, screen):
        screen.fill(self.color)
        pygame.draw.rect(screen, (255, 0, 0), self.exits["maze"])


# basic Game Loop
class Game:
    ALL_ROOMS = ["cell", "cafeteria", "yard"]

    def __init__(self):
        self.character = Character(50, 200)
        self.inventory = Inventory()
        self.cell = Cell(self.character)
        self.hospital = Hospital()

        self.hospital_popup = HospitalUnlockedPopup()
        self.hospital_unlocked = False

        self.completed_rooms = {
            "cell": False,
            "cafeteria": False,
            "yard": False,
        }

        self.cell = Cell(self.character)
        self.yard = Yard(self.character)
        self.cafeteria = Cafeteria()

        self.maze = Maze()
        self.maze.set_destinations({
            "left": "cell",
            "right": "yard",
            "bottom": "cafeteria",
        })

        self.current_state = "maze"

    def complete_room(self, room_name):
        self.completed_rooms[room_name] = True

        if all(self.completed_rooms.values()) and not self.hospital_unlocked:
            self.hospital_unlocked = True
            self.hospital_popup.show()

    def enter_maze(self, coming_from):
        self.current_state = "maze"
        self.maze.enter_from(coming_from)

    ROOM_ENTRY_POINTS = {
        "cell": (50, 300),
        "cafeteria": (200, 300),
        "yard": (200, 390),
    }

    def enter_room(self, room_name):
        self.current_state = room_name
        x, y = self.ROOM_ENTRY_POINTS.get(room_name, (50, 300))
        self.character.set_pos(x, y)

    def enter_hospital(self):
        self.current_state = "hospital"
        self.character.set_pos(450, 400)

    def update(self, events):
        for event in events:
            result = self.hospital_popup.handle_input(event)
            if result == "hospital":
                self.enter_hospital()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h and self.hospital_unlocked:
                    if self.current_state == "maze":
                        self.enter_hospital()

        if self.hospital_popup.active:
            return

        if self.current_state == "maze":
            self.maze.update(self.character)
            result = self.maze.check_exits()
            if result:
                self.enter_room(result)

        elif self.current_state == "cell":
            self.cell.update(events, self.inventory)
            if self.character.rect.left <= 0:
                self.complete_room("cell")
                self.enter_maze("cell")

        elif self.current_state == "cafeteria":
            self.cafeteria.update(self.character, events, self.inventory)
            if self.character.rect.left <= 0:
                self.complete_room("cafeteria")
                self.enter_maze()

        elif self.current_state == "yard":
            if self.yard.state == "EXPLORE" and not self.yard.puzzle.is_open and not self.yard.show_note:
                self.yard.move_character(self.character)
            for event in events:
                if event.type == pygame.KEYDOWN:
                    self.yard.handle_key(event)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.yard.handle_click(event.pos)
            self.yard.update()
            if self.character.rect.left <= 0:
                self.complete_room("yard")
                self.enter_maze("yard")

        elif self.current_state == "hospital":
            self.character.update([], None)
            self.hospital.update(self.character, events)
            if self.character.rect.left <= 0:
                self.enter_maze("hospital")

    def draw(self, screen):
        if self.current_state == "maze":
            self.maze.draw(screen, self.character)

            if self.hospital_unlocked:
                font = pygame.font.SysFont("Arial", 18)
                hint = font.render("[H] Go to Hospital", True, (200, 180, 120))
                screen.blit(hint, (20, 20))

        elif self.current_state == "cell":
            self.cell.draw(screen)

        elif self.current_state == "cafeteria":
            self.cafeteria.draw(screen, self.character)

        elif self.current_state == "yard":
            self.yard.draw(screen)

        elif self.current_state == "hospital":
            self.hospital.draw(screen, self.character)

        self.hospital_popup.draw(screen)


# START SCREEN
def show_start_screen(screen):
    frame = pygame.image.load("silent_walls_start_frame.png").convert_alpha()
    start_btn = pygame.image.load("silent_walls_start_button.png").convert_alpha()
    ctrl_btn = pygame.image.load("silent_walls_controls_button.png").convert_alpha()

    frame = pygame.transform.scale(frame, (980, 480))

    btn_w, btn_h = 160, 55
    start_btn = pygame.transform.scale(start_btn, (btn_w, btn_h))
    ctrl_btn = pygame.transform.scale(ctrl_btn, (btn_w, btn_h))

    y_pos = 360
    start_rect = start_btn.get_rect(center=(400, y_pos))
    ctrl_rect = ctrl_btn.get_rect(center=(580, y_pos))

    waiting = True
    showing_controls = False
    clock_menu = pygame.time.Clock()
    font_ctrl = pygame.font.SysFont("Arial", 22, bold=True)
    font_sub = pygame.font.SysFont("Arial", 18)

    while waiting:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if showing_controls:
                    showing_controls = False
                else:
                    if start_rect.collidepoint(mouse_pos):
                        waiting = False
                    elif ctrl_rect.collidepoint(mouse_pos):
                        showing_controls = True

            if event.type == pygame.KEYDOWN and showing_controls:
                showing_controls = False

        screen.blit(frame, (0, 0))
        screen.blit(start_btn, start_rect)
        screen.blit(ctrl_btn, ctrl_rect)

        if showing_controls:
            overlay = pygame.Surface((980, 480), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))

            panel = pygame.Rect(240, 90, 500, 300)
            pygame.draw.rect(screen, (30, 20, 35), panel, border_radius=8)
            pygame.draw.rect(screen, (90, 30, 45), panel, 3, border_radius=8)

            t1 = font_ctrl.render("CONTROLS", True, (240, 220, 180))
            t2 = font_sub.render("- Movement: Arrow Keys / WASD", True, (220, 220, 220))
            t3 = font_sub.render("- Interact / Actions: Left Click & Keys", True, (220, 220, 220))
            t4 = font_sub.render("- Hospital Shortcut: [H] (when unlocked)", True, (220, 220, 220))
            t_back = font_sub.render("Click anywhere to return", True, (180, 160, 100))

            screen.blit(t1, (panel.centerx - t1.get_width() // 2, panel.y + 25))
            screen.blit(t2, (panel.x + 40, panel.y + 80))
            screen.blit(t3, (panel.x + 40, panel.y + 120))
            screen.blit(t4, (panel.x + 40, panel.y + 160))
            screen.blit(t_back, (panel.centerx - t_back.get_width() // 2, panel.y + 240))

        pygame.display.flip()
        clock_menu.tick(60)


# RUN SEQUENCE
show_start_screen(screen)
show_intro_text(screen, clock)

game = Game()
game.current_state = "maze"

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    game.update(events)
    screen.fill((0, 0, 0))
    game.draw(screen)
    pygame.display.update()
    clock.tick(60)
 
    

    
