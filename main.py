#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import pygame as pg
import irismath as imath
import math
from numpy import random


class Entity():
    def __init__(self, pos, size=(1, 1), color=(0, 0, 0), visible=False, solid=False):
        self.pos = pos
        self.size = size
        self.color = color
        self.rect = pg.Rect((0, 0), size)
        self.rect.center = pos
        self.visible = visible
        self.time = 0
        self.solid = solid

    def draw(self, surface):
        if self.visible:
            pg.draw.rect(surface, self.color, self.rect)

    def update(self):
        self.time += 1

    def colliding(self):
        if self.rect.collidelist([e.rect for e in entities if e is not self and e.solid]) != -1:
            return True
        return False


class Spawn(Entity):
    def __init__(self, pos, entity, attributes):
        super().__init__(pos, (5, 5))
        self.entity = entity
        self.attributes = attributes

    def update(self):
        super().update()
        global entities
        if len([e for e in entities if isinstance(e, Ant)]) < 50 and not self.colliding():
            if self.entity == "ant":
                entities.append(Ant(self.pos, eval(*self.attributes)))


class Ant(Entity):
    def __init__(self, pos, angle=0, size=(5, 5), speed=8):
        super().__init__(pos, size, (0, 0, 0), True, True)
        self.angle = angle
        self.speed = speed

    def move(self, offset):
        old_pos = self.rect.center
        self.rect.move_ip(offset)
        if self.colliding():
            for i in range(self.speed):
                if self.colliding():
                    self.rect[0] += (1 if offset[0] < 0 else -1)  # Rect[0] -> upper-left angle's x
                    self.rect[1] += (1 if offset[1] < 0 else -1)  # Rect[1] -> upper-left angle's y
                else:
                    break
            else:
                self.rect.center = old_pos
            self.angle = random.randint(0, 361)



    def update(self):
        super().update()
        cspeed = imath.speed_on_coord((self.speed, self.angle))
        self.move(cspeed)


#        self.rect.x += cspeed[0]
#        self.rect.y += cspeed[1]

#        for i in range(1, self.speed+1, -1)):
#
#            if self.colliding():
#                self.rect.x -= math.copysign(i, cspeed[0])
#                self.rect.y -= math.copysign(i, cspeed[1])

        self.angle += random.choice((-10, -5, 0, 5, 10), 1, p=(0.125, 0.25, 0.25, 0.25, 0.125))


def event_handle():
    global done

    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

#        if event.type == pg.MOUSEBUTTONDOWN:
#            mouse_buttons = pg.mouse.get_pressed()
#
#            if mouse_buttons[0] == True:
#                entities.append(Spawn(list(event.pos), "ant", ["random.randint(0,361)"]))


def render():
    pg.display.set_caption(f"IRIS - {math.ceil(clock.get_fps())} FPS - {len(entities)} Entities")
    screen.fill((255, 255, 255))
    for entity in entities:
        entity.draw(screen)
    pg.display.flip()


def main():
    while not done:
        event_handle()
        render()
        for entity in entities:
            entity.update()
        clock.tick(60)


pg.init()

size = width, height = 600, 500
screen = pg.display.set_mode(size)
screen_rect = screen.get_rect()
clock = pg.time.Clock()
screen_pos = (0, 0)
done = False
entities = [Spawn([width/2, height/2], "ant", ["random.randint(0,361)"])]
entities.append(Entity((width/2, 0), (width, 5), (0, 0, 0), True, True))  # top wall
entities.append(Entity((width, height/2), (5, height), (0, 0, 0), True, True))  # right wall
entities.append(Entity((width/2, height), (width, 5), (0, 0, 0), True, True))  # bottom wall
entities.append(Entity((0, height/2), (5, height), (0, 0, 0), True, True))  # left wall
mouse_buttons = ()

main()




