# The text to begin the adventure done by Samuel Domingo Sosa Florido
# Created the narrative elements for the text that needs to be shown after the main screen after the player clicks to start playing

# start_text.py
# by Samuel Domingo Sosa Florido

import sys
import pygame


def show_intro_text(text, clock):
    font = pygame.font.Font(None, 26)
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
    TEXT_SPEED = 2
    PAUSE_LINE = 35
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
                    line_idx = len(lines)
                    finished = True
                else:
                    return

        if not finished:
            if pause_timer > 0:
                pause_timer -= 1
            else:
                text_timer += 1
                if text_timer >= TEXT_SPEED:
                    text_timer = 0
                    char_idx += 1

                    if char_idx > len(lines[line_idx]):
                        line_idx += 1
                        char_idx = 0
                        pause_timer = PAUSE_LINE
                        if line_idx >= len(lines):
                            finished = True

        screen.fill((0, 0, 0))

        y = 70
        for i in range(min(line_idx, len(lines))):
            surf = font.render(lines[i], True, (210, 210, 210))
            x = screen.get_width() // 2 - surf.get_width() // 2
            screen.blit(surf, (x, y))
            y += 34

        if not finished and line_idx < len(lines):
            curr_text = lines[line_idx][:char_idx]
            surf = font.render(curr_text, True, (245, 245, 245))
            x = screen.get_width() // 2 - surf.get_width() // 2
            screen.blit(surf, (x, y))

        if finished:
            hint = font_hint.render(
                "[ Click or press Space to start ]", True, (100, 100, 100)
            )
            screen.blit(
                hint, (screen.get_width() // 2 - hint.get_width() // 2, 350)
            )

        pygame.display.flip()
        clock.tick(60)
