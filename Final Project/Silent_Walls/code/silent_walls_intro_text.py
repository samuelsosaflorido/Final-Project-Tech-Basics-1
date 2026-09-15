# The text to begin the adventure done by Samuel Domingo Sosa Florido
# Created the narrative elements for the text that needs to be shown after the main screen after the player clicks to start playing

import sys
import pygame


def show_intro_text(screen, clock):
    font = pygame.font.Font(None, 28)
    font_hint = pygame.font.Font(None, 20)

    lines = [
        "You wake up in a strange prison",
        "You don't remember how you came here",
        "Not even how long have you been here...",
        "You have even forgotten who you are",
        "You only want to escape.",
        "Find the way out.",
    ]

    line_idx = 0
    char_idx = 0
    text_timer = 0
    TEXT_SPEED = 5
    PAUSE_LINE = 60
    pause_timer = 0
    finished = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if not finished:
                    char_idx = len(lines[line_idx])
                else:
                    return

        if not finished:
            if pause_timer > 0:
                pause_timer -= 1
                if pause_timer == 0:
                    line_idx += 1
                    char_idx = 0
                    if line_idx >= len(lines):
                        finished = True
            else:
                text_timer += 1
                if text_timer >= TEXT_SPEED:
                    text_timer = 0
                    char_idx += 1

                    if char_idx > len(lines[line_idx]):
                        pause_timer = PAUSE_LINE

        screen.fill((0, 0, 0))

        if not finished and line_idx < len(lines):
            curr_text = lines[line_idx][:char_idx]
            surf = font.render(curr_text, True, (240, 240, 240))
            x = screen.get_width() // 2 - surf.get_width() // 2
            y = screen.get_height() // 2 - surf.get_height() // 2
            screen.blit(surf, (x, y))

        if finished:
            last_text = lines[-1]
            surf = font.render(last_text, True, (240, 240, 240))
            x = screen.get_width() // 2 - surf.get_width() // 2
            y = screen.get_height() // 2 - surf.get_height() // 2
            screen.blit(surf, (x, y))

            hint = font_hint.render(
                "[ Click or press Space to start ]", True, (120, 120, 120)
            )
            screen.blit(
                hint, (screen.get_width() // 2 - hint.get_width() // 2, 400)
            )

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((980, 480))
    clock = pygame.time.Clock()

    show_intro_text(screen, clock)

    pygame.quit()
