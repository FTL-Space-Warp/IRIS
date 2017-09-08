#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import pygame as pg
import irismath as imath
import math
from numpy import random


class Entity():
    def __init__(self, pos, size=(1, 1), color=(0, 0, 0), visible=False, solid=False):
        self.size = size
        self.color = color
        self.rect = pg.Rect((0, 0), size)
        self.rect.center = pos
        self.visible = visible
        self.time = 0
        self.solid = solid
        self.follow = False

    def draw(self, surface):
        if self.visible:
            pg.draw.rect(surface, self.color, self.rect)

    def update(self):
        self.time += 1
        if self.follow:
            self.rect.center = self.follow.rect.center

    def colliding(self, solid_only):
        touching = self.rect.collidelistall([e.rect for e in entities if e is not self and ((not solid_only) or e.solid)])
        if touching != -1:
            return touching  # returns entity's class name
        return False

    def remove(self):
        global entities
        for i, e in enumerate(entities):
            if e is self:
                del entities[i]


class Spawn(Entity):
    def __init__(self, pos, entity, attributes):
        super().__init__(pos, (5, 5))
        self.entity = entity
        self.attributes = attributes

    def update(self):
        super().update()
        global entities
        if len([e for e in entities if isinstance(e, Ant)]) < 1 and not self.colliding(1):
            if self.entity == "ant":
                entities.append(Ant(self.rect.center, eval(*self.attributes)))


class Ant(Entity):
    def __init__(self, pos, angle=0, size=(5, 5), speed=2, smell_area=(8, 8)):
        super().__init__(pos, size, (0, 0, 0), True, True)
        self.angle = angle
        self.speed = speed
        self.smell_rect = pg.Rect(self.rect.center, smell_area)
        self.job = 'scout'
        self.inventory = ''

    def touch(self, coll_indices):
        collided = []
        for i in coll_indices:
            collided.append(entities[i])

        for entity in collided:
            etype = type(entity)
            if etype is Ant:
                yield etype, entity.job
            elif etype is Food:
                yield [etype]
            else:
                yield ['obstacle']

    def turn(self, coll_indices):
        touch = self.touch(coll_indices)
        for shared_info in touch:
            if shared_info[0] is Ant:
                if shared_info[1] == 'scout' and self.job == 'scout':
                    # TODO better coordination
                    self.angle += 180
            elif shared_info[0] is Food:
                pass
            else:
                self.angle = random.randint(0, 361)


    def move(self, offset):
        old_pos = self.rect.center
        self.rect.move_ip(offset)
        collided = self.colliding(1)
        if collided:
            for e in collided:
                if type(e) is Food and self.job == 'scouting':
                    self.grab(e)

            for i in range(self.speed):
                if self.colliding(1):
                    self.rect[0] += (1 if offset[0] < 0 else -1)  # Rect[0] -> upper-left angle's x
                    self.rect[1] += (1 if offset[1] < 0 else -1)  # Rect[1] -> upper-left angle's y
                else:
                    break
            else:
                self.rect.center = old_pos
            self.turn(collided)

    def trail(self, signal):
        trail_left = False
        touching_pheromones = [p for p in self.colliding(False) if type(p) is Pheromones]
        for p in touching_pheromones:
            if p.signal == signal:
                p.strengthen()
                trail_left = True
        if not trail_left:
            entities.append(Pheromones(self.rect.center, signal, 0.1))

    def smell(self):
        self.smell_rect.center = self.rect.center
        for i in self.smell_rect.collidelistall([e.rect for e in entities if e is not self]):
            entity = entities[i]
            if type(entity) is Food:
                return imath.direction(self.rect.center, entity.rect.center)
        return None 

    def grab(self, entity):
        entity.follow = self
        entity.visible = False

    def update(self):
        super().update()
        cspeed = imath.speed_on_coord((self.speed, self.angle))
        self.move(cspeed)
        smell_vector = self.smell()
        if smell_vector:
            self.angle = smell_vector[1]
        else:
            self.angle += random.choice((-10, -5, 0, 5, 10), 1, p=(0.125, 0.25, 0.25, 0.25, 0.125))


class Food(Entity):
    def __init__(self, pos, size, quantity):
        super().__init__(pos, size, (0, 102, 0), True, True)
        self.quantity = quantity

    def update(self):
        super().update()
        if self.time >= 3600:
            self.time = 0
            self.quantity -= 0.1  # TODO more realistic rotting
            if self.quantity <= 0:
                self.remove()



class Pheromones(Entity):
    def __init__(self, pos, signal, intensity):
        super().__init__(pos, (3, 3), (255, 153, 255), True)
        self.signal = signal
        self.intensity = intensity

    def strengthen(self, ant):
        if self.intensity < 1:
            self.intensity += 0.1

    def update(self):
        super().update()
        global entities
        if self.time >= 120:
            self.intensity -= 0.1
            self.time = 0
        if self.intensity <= 0:
            self.remove()


def event_handle():
    global done
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_buttons = pg.mouse.get_pressed()

            if mouse_buttons[0] == True:
                entities.append(Food(event.pos, (2, 2), 1))


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

size = width, height = 300, 200
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
