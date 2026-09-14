import pygame

class Chair():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft= (x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass

class Table():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft= (x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass

class Meal():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft= (x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass



class Cafeteria():
    def __init__(self, your_character):
        self.your_character = your_character
        self.table_x = 500
        self.table_y = 300
        self.completed = False

    def draw(self, screen):
        background = "gray"
        base_color = "black"

        base = pygame.Surface((980, 250))
        base.fill(base_color)

        # table

        table = pygame.image.load("silent_walls_character.png").convert_alpha()

        # define a new width and height for the table
        new_width_table = 70
        new_height_table = 80

        # meal service

        meal_service = pygame.image.load("silent_walls_character.png").convert_alpha()

        # define a new width and height for the meal_service
        new_width_meal_service = 90
        new_height_meal_service = 120

        # update the new scaled image of your_character
        meal_service = pygame.transform.scale(meal_service, (new_width_meal_service, new_height_meal_service))
        meal_service_rect = meal_service.get_rect(topleft=(200, 130))

        # basic background color (to draw over - blanc canvas to start with / reset the background at every frame)
        screen.fill((background))

        # put the separated game sections together
        screen.blit(base, (0, 230))
        screen.blit(meal_service, meal_service_rect)

    def update(self):
        pass
