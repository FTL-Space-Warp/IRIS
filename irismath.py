import math

def speed_on_coord(velocity):
    """ Returns speed on x and y from velocity """

    angle = math.radians(velocity[1])
    speed_x = math.cos(angle)*velocity[0]
    speed_y = math.sin(angle)*velocity[0]
    cspeed = [speed_x, speed_y]
    return cspeed


def pos_on_screen(pos, screen_pos, zoom):
    pixel_pos = (pos[0]*zoom, pos[1]*zoom)
    pos_on_screen = (pixel_pos[0]-screen_pos[0], pixel_pos[1]-screen_pos[1])
    return pos_on_screen


def direction(pos1, pos2):
    x_d = pos2[0] - pos1[0]
    y_d = pos2[1] - pos1[1]
    cdistance = (x_d, y_d)

    distance = math.sqrt(cdistance[0] ** 2 + cdistance[1] ** 2)

    if cdistance[0] == 0 and cdistance[1] > 0:
        angle = 90
    elif cdistance[0] == 0 and cdistance[1] < 0:
        angle = -90
    elif cdistance[1] == 0 and cdistance[0] >= 0:
        angle = 0
    elif cdistance[1] == 0 and cdistance[0] < 0:
        angle = 180
    else:
        print(cdistance)
        angle = math.degrees(math.acos(cdistance[0]/distance))
        if pos1[1] > pos2[1]:
            if pos1[0] < pos2[0]:
                angle -= 90
            else:
                angle += 90

    return [angle, distance]
