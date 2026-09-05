# So this is basically the main file for the main screen
# I have used the design from the presentation as the main screen file so I added the constants, rendered the image and added some text box welcoming the player and adding the function to either continue playing or exit the game
# Maybe we might need to also import the other sections of the game in this main file but we can do that later
# Is still a small demo so maybe we need to find 
# I also kept the names in the order that was in the presentation
# I also used this repository https://github.com/educ8s/Python-Tetris-Game-Pygame/blob/main/main.py as a source of inspiration 


import pygame
import sys

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 60

pygame.init()

def run_title_screen(screen, clock):
    title_bg = pygame.image.load("main_screen.png").convert()
    title_bg = pygame.transform.scale(title_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))

    in_title = True
    while in_title:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    in_title = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.blit(title_bg, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)

def show_intro_message(screen, clock):
    pygame.time.delay(150)
    pygame.event.clear()

    title_bg = pygame.image.load("main_screen.png").convert()
    title_bg = pygame.transform.scale(title_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))

    dim_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    dim_overlay.fill((10, 8, 12, 170))

    font_large = pygame.font.Font(None, 34)
    font_small = pygame.font.Font(None, 24)

    text_surf_1 = font_large.render("Prepare to begin this adventure!", False, (240, 235, 215))
    text_surf_2 = font_small.render("We hope you do enjoy it :)", False, (170, 220, 150))
    hint_surf = font_small.render("[ENTER] Continue    [ESC] Exit", False, (160, 155, 150))

    box_w, box_h = 580, 190
    box_x = (WINDOW_WIDTH - box_w) // 2
    box_y = (WINDOW_HEIGHT - box_h) // 2

    dialog_surface = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    dialog_surface.fill((20, 16, 24, 230))
    pygame.draw.rect(dialog_surface, (50, 45, 60), (0, 0, box_w, box_h), 4)
    pygame.draw.rect(dialog_surface, (110, 160, 115), (4, 4, box_w - 8, box_h - 8), 2)

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.blit(title_bg, (0, 0))
        screen.blit(dim_overlay, (0, 0))
        screen.blit(dialog_surface, (box_x, box_y))
        screen.blit(text_surf_1, (WINDOW_WIDTH // 2 - text_surf_1.get_width() // 2, box_y + 40))
        screen.blit(text_surf_2, (WINDOW_WIDTH // 2 - text_surf_2.get_width() // 2, box_y + 85))
        screen.blit(hint_surf, (WINDOW_WIDTH // 2 - hint_surf.get_width() // 2, box_y + 135))

        pygame.display.flip()
        clock.tick(FPS)

def main():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Silent Walls")
    clock = pygame.time.Clock()

    run_title_screen(screen, clock)
    show_intro_message(screen, clock)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
