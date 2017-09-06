import math

# def velocity_vector(cspeed):
#     """ Takes the speed on each coordinate and returns the velocity."""
# 
#     if cspeed[0] == 0 and cspeed[1] > 0:
#         angle = 90
#     elif cspeed[0] == 0 and cspeed[1] < 0:
#         angle = -90
#     elif cspeed[1] == 0 and cspeed[0] >= 0:
#         angle = 0
#     elif cspeed[1] == 0 and cspeed[0] < 0:
#         angle = 180
#     else:
#         angle = math.degrees(math.atan(cspeed[1]/cspeed[0]))
#     speed = math.sqrt(cspeed[0] ** 2 + cspeed[1] ** 2)
#     return [speed, angle]


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
