# mainly by Katharina Noske (other coding parts form Samuel Sosa Florido or Karoline Fischer will be pointed out)

# unfortunately we started with coding the game separately in different files
# so we faced the issue to combine it into ONE compleet game
# so we did needed to reorganization the code (the file structure and the files themselves)
# so this is the attempt to put it all together in one game without bugs (with a main structure and then the separated rooms)

import pygame
from sys import *
from cafeteria import *

from scipy._lib.pyprima.cobyla import update

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

# your character
class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("pixil-frame-0(5).png").convert_alpha()
        self.transform_image = pygame.transform.scale(self.image, (50, 70))
        self.rect = self.transform_image.get_rect(topleft= (x, y))

    def draw(self, screen):
        screen.blit(self.transform_image, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= 3
        if keys[pygame.K_a]:
            self.rect.x -= 3
        if keys[pygame.K_s]:
            self.rect.y += 3
        if keys[pygame.K_d]:
            self.rect.x += 3

    def update(self):
        pass




your_character = pygame.image.load("pixil-frame-0(5).png").convert_alpha()

# define a new width and height for your_character
new_width = 70
new_height = 80

# update the new scaled image of your_character
your_character = pygame.transform.scale(your_character, (new_width, new_height))
your_character_rect = your_character.get_rect(topleft = (500, 300))

#cafeteria =  Cafeteria("your_character")
#table = Object(300, 300, your_character)
#chair = Object(2000, 400, your_character)
#test2 = Table(100, 200, your_character)
character = Character(500, 300)



# back to the basic pygame-setup to run the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    character.move()

        #if your_character_rect.colliderect(chair.rect) and chair.rect.collidepoint(event.pos) and event.type == pygame.mouse.get_pressed():
           #print('Hello')

    # basic background color (to draw over - blanc canvas to start with / reset the background at every frame)
    screen.fill((background))

    # put the separated game sections together
    screen.blit(base, (0, 230))
    screen.blit(your_character, your_character_rect)
    character.draw(screen)
    #cafeteria.draw(screen)
    #if cafeteria.completed:
        #table.draw(screen)

    #chair.draw(screen)

    #test2.draw(screen)



    #cafeteria.update()
    character.update()
    pygame.display.update()

    # limits FPS to 60
    clock.tick(60)
