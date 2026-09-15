# Cell = Room from Karo

import pygame
import random

import os
import sys

from silent_walls_character import Character
from silent_walls_inventory import Inventory

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

        self.chest = Chest(90, 260)
        self.chest_popup = ChestPopup()

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
            #key
            if obj == self.key:
                self.key.draw(screen, show_hint=self.is_near(self.key))
            #chest
            elif obj == self.chest:
                self.chest.draw(screen, show_hint=self.is_near(self.chest))
            else:
                obj.draw(screen)

        #key
        if not self.key.collected and self.is_near(self.key):
            self.key.show_hint(screen)

        self.character.draw(screen)
        #chest
        self.chest_popup.draw(screen)

    def update(self, events, inventory):
        self.character.update(self.objects)
        #chest animation

        was_animate = self.chest.animate
        self.chest.update()
        if was_animate and not self.chest.animate:
            self.chest_popup.show()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.check_interaction(inventory)

            self.chest_popup.handle_input(event, inventory)

    def check_interaction(self, inventory):
        if not self.key.collected and self.is_near(self.key):
            self.key.collected = True
            self.objects.remove(self.key)
            inventory.add_item("Key (Cell)")
            print("Key found!")

        if not self.chest.is_open and self.is_near(self.chest) and not self.chest.animate:
            self.chest.open()



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
        self.image_closed = pygame.image.load ("cell_chest.png").convert_alpha()
        self.image_open1 = pygame.image.load ("cell_chest_open1.png").convert_alpha()
        self.image_open2 = pygame.image.load ("cell_chest_open2.png").convert_alpha()
        self.image = self.image_closed 
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_open = False
        self.font = pygame.font.SysFont("Arial", 20)

        #Chest mini animation
        self.animate = False 
        self.animate_step = 0
        self.animate_timer = 0
        self.animate_delay = 300

    def show_hint(self, screen):
        hint = self.font.render("Press E to open", True, "white")
        screen.blit(hint, (self.rect.x - 30, self.rect.y - 30))

    def open(self):
        self.animate = True
        self.animate_step = 1
        self.image = self.image_open1
        self.animate_timer = pygame.time.get_ticks()

    def update(self):
        if self.animate:
            now = pygame.time.get_ticks()

            #Frame1
            if self.animate_step == 1:
                #self.rect = self.image.get_rect(topleft=(self.x, self.y - 10))
                if now - self.animate_timer > self.animate_delay:
                    self.animate_step = 2
                    self.image = self.image_open2
                    self.rect = self.image.get_rect(topleft=(self.x, self.y - 30))
                    self.animate_timer = now

            elif self.animate_step == 2:
                if now - self.animate_timer > self.animate_delay:
                    self.animate = False
                    self.is_open = True

    def draw(self, screen, show_hint=False):
            screen.blit(self.image, self.rect)
            pygame.draw.rect(screen, "red", self.rect, 2)
    
            if show_hint and not self.is_open and not self.animate:
                self.show_hint(screen)


class ChestPopup():
    def __init__(self):
        self.active = False
        self.image = pygame.image.load("cell_chest_inside.png").convert_alpha()  # ← Bild von innen
        self.image = pygame.transform.scale(self.image, (400, 300))
        self.font = pygame.font.SysFont("Arial", 24)
        self.small_font = pygame.font.SysFont ("Arial", 18)

        self.color_boxes = [
            (255, 130, 171), #rot 
            (152, 255, 152), #grün
            (0, 191, 255), #blau
        ]

        self.input_boxes = ["", "", ""]
        self.selected_box = 0
        self.correct_answers = ["7", "3", "4"]
        self.solved = False
        self.code = "734"
        self.show_code = False

    def show(self):
        self.active = True
        self.input_boxes = ["", "", ""]
        self.selected_box = 0
        self.show_code = False

    def close(self):
        self.active = False

    def check_answers(self):
        for i, answer in enumerate(self.correct_answers):
            if self.input_boxes[i] != answer:
                return False 
        return True

    def draw(self, screen):
        if not self.active:
            return
        
        #dark background
        overlay = pygame.Surface((980, 480), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        #background of popup
        popup_x = (980 - 400) // 2
        popup_y = (480 - 300) // 2
        screen.blit(self.image, (popup_x, popup_y))

        box_size = 60
        gap = 20

        #boxes width
        total_width = 3 * box_size + 2 * gap
        start_x = popup_x + 400

        #colors upper boxes
        upper_y = popup_y + 60
        for i, color in enumerate(self.color_boxes):
            x = start_x + i * (box_size + gap)
            pygame.draw.rect(screen, color, (x, upper_y, box_size, box_size))
            pygame.draw.rect(screen, "white", (x, upper_y, box_size, box_size), 2)

        lower_y = upper_y + box_size + 40
        for i in range(3):
            x = start_x + i * (box_size + gap)

            border_color = "yellow" if i == self.selected_box else "white"
            pygame.draw.rect(screen, (30, 30, 30), (x, lower_y, box_size, box_size))
            pygame.draw.rect(screen, border_color, (x, lower_y, box_size, box_size), 2)

            if self.input_boxes[i]:
                number = self.font.render(self.input_boxes[i], True, "white")
                number_x = x + (box_size - number.get_width()) // 2
                number_y = lower_y + (box_size - number.get_height()) // 2
                screen.blit(number, (number_x, number_y)) 

        hint = self.small_font.render("Zahlen eingeben, TAB zum Wechseln, ENTER zum Bestätigen", True, "white")
        screen.blit(hint, (popup_x + 20, popup_y + 340))

        if self.show_code:
            code_text = self.font.render(f"Code: {self.code}", True, "yellow")
            screen.blit(code_text, (popup_x + 600//2 - code_text.get_width()//2, popup_y + 300))

        esc_hint = self.small_font.render("ESC zum Schließen", True, "gray")
        screen.blit(esc_hint, (popup_x + 20, popup_y + 370))

        # Schließen Hinweis
        hint = self.font.render("ESC to close", True, "white")
        screen.blit(esc_hint, (popup_x + 20, popup_y + 370))

    def handle_input(self, event, inventory):
        if not self.active:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()

            elif event.key == pygame.K_TAB:
                self.selected_box = (self.selected_box + 1) %3

            elif event.key == pygame.K_RETURN:
                if not self.solved and self.check_answers():
                    self.solved = True
                    self.show_code = True
                    inventory.add_item("Letter (Cell)")
                    print(f"You solved it! Code: {self.code}")

            elif event.key == pygame.K_BACKSPACE:
                self.input_boxes[self.selected_box] = ""

            elif event.unicode.isdigit():
                self.input_boxes[self.selected_box] = event.unicode
                #automatically to the next box
                if self.selected_box < 2:
                    self.selected_box += 1 

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

