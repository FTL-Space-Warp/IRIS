#!/usr/bin/python3.6
# -*- coding: utf-8 -*-

import pygame as pg
import irismath as imath
import math
from numpy import random


class Entity():
    def __init__(self, pos, size=(1, 1), color=(0, 0, 0), visible=False, solid=False, weight=0):
        self.size = size
        self.color = color
        self.rect = pg.Rect((0, 0), size)
        self.rect.center = pos
        self.visible = visible
        self.time = 0
        self.solid = solid
        if solid:
            self.weight = weight
        self.follow = False

    def draw(self, surface):
        if self.visible:
            pg.draw.rect(surface, self.color, self.rect)

    def update(self):
        self.time += 1
        if self.follow:
            self.rect.center = self.follow.rect.center

    def colliding(self, solid_only):
        elist = [e for e in entities if e is not self and ((not solid_only) or e.solid)]
        icoll = self.rect.collidelistall([e.rect for e in elist])
        if icoll == -1:
            return False
        else:
            ecoll = []
            for i in icoll:
                ecoll.append(elist[i])
        return ecoll

    def remove(self):
        global entities
        for i, e in enumerate(entities):
            if e is self:
                del entities[i]


class Spawn(Entity):
    def __init__(self, pos, entity, attributes):
        super().__init__(pos, (10, 10))
        self.entity = entity
        self.attributes = attributes

    def update(self):
        super().update()
        global entities
        if len([e for e in entities if isinstance(e, Ant)]) < 50 \
                and not self.colliding(1):
            if self.entity == "ant":
                entities.append(Ant(self.rect.center, eval(*self.attributes)))


class Ant(Entity):
    def __init__(self, pos, angle=0, size=(5, 5), weight=1, speed=2):
        super().__init__(pos, size, (0, 0, 0), True, True, weight)
        self.angle = angle
        self.speed = speed
        self.smell_rect = pg.Rect(self.rect.center, (30, 30))
        self.job = 'scout'
        self.inventory = None
        self.strength = self.weight * 10

    def touch(self, ecoll):
        for entity in ecoll:
            etype = type(entity)
            if etype is Ant:
                yield etype, entity.job, entity.inventory
            elif etype is Food:
                yield [etype]
            else:
                yield ['obstacle']

    def turn(self, ecoll):
        touch = self.touch(ecoll)
        for shared_info in touch:
            if shared_info[0] is Ant:
                if shared_info[1] == 'scout' and self.job == 'scout':
                    if type(shared_info[2]) is Food:
                        return self.angle \
                                    + random.choice((-90, 90), p=(0.5, 0.5))
                    # TODO better coordination
                    return self.angle + 180
            else:
                return random.randint(0, 361)

    def move(self, offset):
        old_pos = self.rect.center
        self.rect.move_ip(offset)
        collided = self.colliding(0)
        if collided:
            for e in collided:
                if type(e) is Food and self.job == 'scout' \
                        and not self.inventory:
                    self.grab(e)
                elif type(e) is Spawn and self.job == 'scout' \
                        and type(self.inventory) is Food:
                    self.drop()

            for i in range(self.speed):
                if self.colliding(1):
                    # Rect[0] -> upper-left angle's x
                    self.rect[0] += (1 if offset[0] < 0 else -1)
                    # Rect[1] -> upper-left angle's y
                    self.rect[1] += (1 if offset[1] < 0 else -1)
                else:
                    break
            else:
                self.rect.center = old_pos

            for e in collided:
                if e.solid:  # ants turn only if touching something solid
                    return self.turn(collided)
        return None

    def trail(self, signal):
        trail_left = False
        touching_pheromones = \
            [p for p in self.colliding(False) if type(p) is Pheromones]
        for p in touching_pheromones:
            if p.signal == signal:
                p.strengthen(self)
                trail_left = True
        if not trail_left:
            entities.append(Pheromones(self.rect.center, signal, 0.1))

    def smell(self):
        self.smell_rect.center = self.rect.center
        elist = [e for e in entities if e is not self and not e.follow]

        for i in self.smell_rect.collidelistall([e.rect for e in elist]):
            entity = elist[i]
            etype = type(entity)

            if etype is Food and not self.inventory:
                return imath.direction(self.rect.center, entity.rect.center)[0]

            elif etype is Pheromones:
                angle = imath.direction(self.rect.center,
                                        entity.rect.center)[0]
                if entity.signal == 'food'  \
                                    and self.job == 'scout' \
                                    and not self.inventory \
                                    :
                            #        and entity not in self.last_smell:

                    # ants won't always follow the trail
                    if random.choice((0, 1),
                                     p=(1-entity.intensity, entity.intensity)):
                        # only look for pheromones in front of ants so that
                        # they can follow the trails without turning back
                        if ((angle - self.angle) % 360) > 270:
                            return self.angle - 20  # turn left
                        elif ((angle - self.angle) % 360) < 90:
                            return self.angle + 20  # turn right

        return None

    def grab(self, entity):
        if not self.inventory and self.strength >= entity.weight \
                and entity.solid:
            entity.follow = self
            entity.visible = False
            entity.solid = False
            self.inventory = entity
            self.color = (255, 0, 0)

    def drop(self):
        if self.inventory:
            self.inventory.follow = False
            self.inventory.solid = True
            drop_distance = (math.sqrt(2 * (self.size[0] ** 2)) +
                             math.sqrt(self.inventory.size[0] ** 2 +
                                       self.inventory.size[1] ** 2)) / 2
            # (ant's diagonal + item's diagonal) / 2
            self.inventory.rect.center = (
                self.inventory.rect.center[0] +
                imath.speed_on_coord((drop_distance, self.angle))[0],
                self.inventory.rect.center[1] +
                imath.speed_on_coord((drop_distance, self.angle))[1]
                )
            self.inventory = None
            self.color = (0, 0, 0)

    def update(self):
        super().update()
        cspeed = imath.speed_on_coord((self.speed, self.angle))
        angle = self.move(cspeed)

        if angle:  # makes sure move() has priority over smell()
            self.angle = angle
        elif type(self.inventory) is Food and self.job == 'scout':
            self.angle = imath.direction(
                    self.rect.center,
                    [e.rect.center
                        for e in entities if type(e) is Spawn][0])[0]
        #    self.angle += random.choice((-20, 0, 20), p=(0.3, 0, 0.7))
        else:
            angle = self.smell()
            if angle:
                self.angle = angle
            else:
                self.angle += random.choice((-10, -5, 0, 5, 10), p=(0.125, 0.25, 0.25, 0.25, 0.125))

        if type(self.inventory) is Food and self.job == 'scout':
            self.trail('food')


class Food(Entity):
    def __init__(self, pos, size, weight=1):
        super().__init__(pos, size, (0, 102, 0), True, True, weight)

    def update(self):
        super().update()
        if self.time >= 36000 and not self.follow:
            self.time = 0
            self.remove()  # TODO more realistic rotting
        else:
            for e in self.colliding(0):
                if type(e) is Spawn:
                    self.remove()
                    break


class Pheromones(Entity):
    def __init__(self, pos, signal, intensity):
        super().__init__(pos, (3, 3), (255, 153, 255), True)
        self.signal = signal
        self.intensity = intensity
        self.last_ant = None

    def strengthen(self, ant):
        if (self.intensity + 0.2) < 1 and ant is not self.last_ant:
            self.intensity += 0.2
            self.last_ant = ant

    def update(self):
        super().update()
        global entities
        if self.time >= 100:
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

            if mouse_buttons[0]:
                entities.append(Food(event.pos, (2, 2), 1))
#                entities.append(Pheromones(event.pos, 'food', 1))


def render():
    pg.display.set_caption(f"""IRIS - {math.ceil(clock.get_fps())}
                               FPS - {len(entities)} Entities""")
    screen.fill((255, 255, 255))
    for entity in entities:
#        if type(entity) is Ant:
#            pg.draw.rect(screen, (0, 255, 0), entity.smell_rect)
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

size = width, height = 600, 400
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

