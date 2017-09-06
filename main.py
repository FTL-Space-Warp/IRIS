#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import pygame as pg
import math
import random

pg.init()
size = width, height = 600, 500
screen = pg.display.set_mode(size)
clock = pg.time.Clock()

done = False
entities = []
mouse_buttons = ()


class Entity():
    def __init__(self, pos, size, color, visible=False):
        self.pos = pos
        self.size = size
        self.color = color
        self.rect = pg.Rect((0, 0), size)
        self.rect.center = pos
        self.visible = visible

    def draw(self, surface):
        if self.visible:
            pg.draw.rect(surface, self.color, self.rect)

    def update(self):
        pass


class Ant(Entity):
    def __init__(self, pos, size = (5,5), direction = 0, speed = 5):
        Entity.__init__(self, pos, size, (0,0,0), True)
        self.direction = direction
        self.speed = speed
        self.walk = "convoluted"

    def update(self):
        if self.direction == 0: # up
            self.rect.y -= self.speed
        if self.direction == 1: # right
            self.rect.x += self.speed
        if self.direction == 2: # down
            self.rect.y += self.speed
        if self.direction == 3: # left
            self.rect.x -= self.speed

        self.direction += random.randint(-1,1)
        if self.direction >= 5:
            self.direction = 0
        if self.direction <= -1:
            self.direction = 4


def event_handle():
    global done

    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_buttons = pg.mouse.get_pressed()

            if mouse_buttons[0] == True:
                    entities.append(Ant(list(event.pos)))



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



main()

