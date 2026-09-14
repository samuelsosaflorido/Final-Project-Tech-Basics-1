import pygame

class Character():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("pixil-frame-0(5).png").convert_alpha()
        self.transformed_image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.transformed_image.get_rect(topleft=(x, y))
        self.hitbox = pygame.Rect(x, y + 50, 60, 20) 

    def draw(self, screen):
        screen.blit(self.transformed_image, self.rect)
        pygame.draw.rect(screen, "red", self.hitbox, 2)

    def update_hitbox(self):
        self.hitbox.x = self.rect.x + 25
        self.hitbox.y = self.rect.y + 80

    def set_pos(self, x, y):
        self.rect.topleft = (x, y)
        self.update_hitbox()

    def move(self, objects):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= 5
            self.update_hitbox()
            if self.check_collision(objects):
                self.rect.x +=5
                self.update_hitbox()

        if keys[pygame.K_d]:
            self.rect.x += 5
            self.update_hitbox()
            if self.check_collision(objects):
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

    def update(self, objects):
        self.move(objects)
        #self.update_hitbox()
        self.check_walls()