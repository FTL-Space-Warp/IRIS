#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import pygame as pg

size = width, height = 600, 600
screen = pg.display.set_mode(size)
done = False


class Entity:
    def __init__():
        pass


class Ant(Entity):
    def __init__():
        Entity.__init__()


def main():
    global done
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True


while not done:
    main()
