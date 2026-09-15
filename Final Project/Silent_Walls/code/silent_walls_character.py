# the basic-character-code (example: movement) is by Kathi and the interaction-code is by Karo

import pygame

#Collision by Karo Fischer (help and explanations by ChatAI Anthropic Claude Sonnet 4.6)
#also code for room "cell" by Karo 
class Character():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("silent_walls_character.png").convert_alpha()
        self.transformed_image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.transformed_image.get_rect(topleft=(x, y))
        self.hitbox = pygame.Rect(x, y + 50, 60, 20) 

        #jump for minigame 
        self.velocity_y = 0
        self.on_ground = True 
        self.jump_power = -30
        self.gravity = 0.8
        self.ground_y = 380

    def draw(self, screen):
        screen.blit(self.transformed_image, self.rect)

    def update_hitbox(self):
        self.hitbox.x = self.rect.x + 25
        self.hitbox.y = self.rect.y + 80

    def set_pos(self, x, y):
        self.rect.topleft = (x, y)
        self.update_hitbox()

    def move(self, objects, chest=None):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= 5
            self.update_hitbox()
            if chest and self.hitbox.colliderect(chest.rect):
                chest.push(-1, 5, objects)
            elif self.check_collision(objects):
                self.rect.x +=5
                self.update_hitbox()

        if keys[pygame.K_d]:
            self.rect.x += 5
            self.update_hitbox()
            if chest and self.hitbox.colliderect(chest.rect):
                chest.push(1, 5, objects)
            elif self.check_collision(objects):
                self.rect.x -=5
                self.update_hitbox()

        if keys[pygame.K_w]:
            self.rect.y -= 5
            self.update_hitbox()
            if self.check_collision(objects):
                self.rect.y +=5
                self.update_hitbox()

        if keys[pygame.K_s]:
            self.rect.y += 5
            self.update_hitbox()
            if self.check_collision(objects):
                self.rect.y -=5
                self.update_hitbox()

        if chest and self.hitbox.colliderect(chest.rect):
                    chest.push(-1, 5, objects)

        self.update_hitbox()


    def check_collision(self, objects):
        for obj in objects:
            if self.hitbox.colliderect(obj.rect):
                return True
        return False

    def check_walls(self):
        if self.rect.left < 0:
            self.hitbox.left = 0
            self.rect.left = 0
        if self.rect.right > 980:
            self.hitbox.left = 980
            self.rect.right = 980
        if self.rect.top < 200:
            self.hitbox.left = 200
            self.rect.top = 200
        if self.rect.bottom > 480:
            self.hitbox.left = 480
            self.rect.bottom = 480

    def update(self, objects, chest=None):
        self.move(objects, chest)
        #self.update_hitbox()
        self.check_walls()