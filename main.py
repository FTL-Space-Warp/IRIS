#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import pygame as pg
import math


pg.init()
size = width, height = 600, 500
screen = pg.display.set_mode(size)
clock = pg.time.Clock()

done = False
entities = []
mouse_buttons = ()


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


def event_handle():
    global done

    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_buttons = pg.mouse.get_pressed()

            if mouse_buttons[0] == True:
                    entities.append(Entity(event.pos, (10,10), (100, 100, 100)))



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
        clock.tick(60)



main()

