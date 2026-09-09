# Rats:
# dictionary
rat_color = "red"
rat_size = 50
rat_x = 250
rat_y = 250
rat_x_movement = 5
rat_y_movement = 5

# define update to rat position
def update_rat_position():
    global rat_x
    global rat_y
    global rat_x_movement
    global rat_y_movement
    # movement on the x-axis
    if rat_x_movement > 0:
        if rat_x < 930:
            rat_x += rat_x_movement
        else:
            rat_x_movement *= -1
    elif rat_x_movement < 0:
        if rat_x > 50:
            rat_x += rat_x_movement
        else:
            rat_x_movement *= -1
    # movement on the y-axis
    if rat_y_movement > 0:
        if rat_y < 430:
            rat_y += rat_y_movement
        else:
            rat_y_movement *= -1
    elif rat_y_movement < 0:
        if rat_y > 50:
            rat_y += rat_y_movement
        else:
            rat_y_movement *= -1

# update rat
rat = pygame.draw.circle(screen, rat_color, (rat_x, rat_y), rat_size)