# The different endings coded by Samuel Domingo Sosa Florido
# I really enjoyed writing the narrative part of it and with some Gemini help I was able to finish the entire part
# I hope it is coherent with the rest of the videogame

import sys
import pygame

ENDINGS = {
    "letters": [
        "You managed to unlock the door...",
        ""
        "But all of a sudden, you just wake up.",
        ""
        "You realize that the light is so bright.",
        ""
        "'How long have I been here...?'.",
        ""
        "'Wait, was all this a dream?'",
        ""
        "You then remember...",
        ""
        "You have been all this time in a coma.",
        ""
        "You feel again alive.",
        ""
        "You have finally escaped.",
        "Ready to embrace a new life.",
    ],
    "medication": [
        "You combine all the different pieces of the medication",
        ""
        "As the Ghosts suggested.",
        ""
        "You wake up.",
        ""
        "'Huh? Where am I?...'",
        ""
        "You try to move.",
        ""
        "But something strange happens.",
        ""
        "You feel it inside.",
        ""
        "You barely are able to speak.",
        ""
        "You start coughing.",
        ""
        "You cannot control it.",
        ""
        "You feel every part of your body slowly fading away.",
        ""
        "And all of a sudden...",
        ""
        "Everything just becomes obscure and numb.",
    ],
    "keys": [
        "You manage to unlock the door...",
        ""
        "With those different keys that you have been collecting.",
        ""
        "'I hope this works.'",
        ""
        "'Finally I can be free.'",
        ""
        "The world suddenly changes.",
        ""
        "You find yourself in the very beginning.",
        ""
        "'Wait, what? What is going on?!'",
        ""
        "You then realize...",
        ""
        "You are still in the prison",
        ""
        "Ready to begin the story again",
    ],
}

def show_ending(screen, clock, ending_type):
    font = pygame.font.Font(None, 28)
    font_hint = pygame.font.Font(None, 20)

    if ending_type not in ENDINGS:
        return

    lines = ENDINGS[ending_type]

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
                    # This allows each line to jump to the other one 
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

        # This is for drawing the lines needed the help of Gemini to explain me how to do it so I wrote it down
        if not finished and line_idx < len(lines):
            curr_text = lines[line_idx][:char_idx]
            surf = font.render(curr_text, True, (240, 240, 240))
            x = screen.get_width() // 2 - surf.get_width() // 2
            y = screen.get_height() // 2 - surf.get_height() // 2
            screen.blit(surf, (x, y))

        if finished:
            # This is for every message
            last_text = lines[-1]
            surf = font.render(last_text, True, (240, 240, 240))
            x = screen.get_width() // 2 - surf.get_width() // 2
            y = screen.get_height() // 2 - surf.get_height() // 2
            screen.blit(surf, (x, y))

            hint = font_hint.render(
                "[ Click to continue ]", True, (120, 120, 120)
            )
            screen.blit(
                hint, (screen.get_width() // 2 - hint.get_width() // 2, 400)
            )

        pygame.display.flip()
        clock.tick(60)

def trigger_player_decision(screen, clock, medication_count, keys_count, letters_count):
    if medication_count >= 3:
        show_ending(screen, clock, "medication")
        return "medication"
    elif keys_count >= 3:
        show_ending(screen, clock, "keys")
        return "keys"
    elif letters_count >= 3:
        show_ending(screen, clock, "letters")
        return "letters"
    return None

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((980, 480))
    clock = pygame.time.Clock()

    # Change the name ("letters", "medication" o "keys") to see each ending 
    show_ending(screen, clock, "keys")

    pygame.quit()
