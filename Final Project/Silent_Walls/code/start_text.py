# The text to begin the adventure done by Samuel Domingo Sosa Florido
# Created the narrative elements for the text that needs to be shown after the main screen after the player clicks to start playing

import sys
import pygame


def show_start_screen(screen, clock):
    font = pygame.font.Font(None, 28)
    font_hint = pygame.font.Font(None, 24)

    # Intro text message for when the game begins
    lines = [
        "You wake up in a strange prison",
        "You don't remember how you came here",
        "Not even how long have you been here...",
        "You have even forgotten who you are",
        "You only want to escape.",
        "Find the way out.",
    ]

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

        screen.fill((0, 0, 0))

        # This is for painting the centered text
        y = 90
        for line in lines:
            text_surf = font.render(line, True, (200, 200, 200))
            x = screen.get_width() // 2 - text_surf.get_width() // 2
            screen.blit(text_surf, (x, y))
            y += 35

        # Hint to continue the game
        hint_surf = font_hint.render(
            "[ Click anywhere with the mouse to start ]", True, (130, 130, 130)
        )
        hint_x = screen.get_width() // 2 - hint_surf.get_width() // 2
        screen.blit(hint_surf, (hint_x, 340))

        pygame.display.flip()
        clock.tick(60)
