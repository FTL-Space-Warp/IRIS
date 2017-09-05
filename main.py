#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import pygame as pg

pg.init()
size = width, height = 600, 500
screen = pg.display.set_mode(size)
done = False


class Entity():
    def __init__(self, pos, size, color):
        self.pos = pos
        self.size = size
        self.color = color
        self.rect = pg.Rect((0, 0), size)
        self.rect.center = pos

    def draw(self, surface):
        pg.draw.rect(surface, self.color, self.rect)


class Ant(Entity):
    def __init__():
        Entity.__init__()


def event_loop():
    global done
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True


def main_loop():
    asd = Entity((345, 290), (34, 42), (88, 200, 255))
    asd.draw(screen)


while not done:
    event_loop()
    main_loop()
    pg.display.flip()


