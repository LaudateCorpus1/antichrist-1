import random
import math


from constants import *


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class Actor:
    def __init__(self, name, pos, levels, level, tile, health, color=COLOR_WHITE):
        self.name = name
        self.pos = pos
        self.level = level
        self.levels = levels
        self.tile = tile
        self.health = health
        self.inventory = []
        self.levels[self.level].actors.append(self)
        self.is_alive = True
        self.color = color
        self.base_color = color

    def move(self, dx, dy):
        self.pos.x += dx
        self.pos.y += dy

    def receive_damage(self, damage, damager):
        if not self.is_alive: return
        self.health -= damage
        self.color = COLOR_RED
        if self.health <= 0:
            self.is_alive = False
            self.tile = ord('%')
            self.base_color = COLOR_RED

    def get_damage(self):
        return 1

    def update(self, ticks):
        if self.base_color != self.color:
            self.color = self.base_color


class Player(Actor):
    pass


class NPC(Actor):
    def __init__(self, name, pos, levels, level, tile, health, profession):
        super().__init__(name, pos, levels, level, tile, health)
        self.triggers = []
        self.relations = dict()
        self.objects = []
        self.profession = profession
        self.current_action = None
        self.house = None
        self.target_point = None
        self.target = None
        self.wait_timer = 0
        self.work_zone = None
        self.is_in_home = False


    def get_damage(self):
        return 4


    def receive_damage(self, damage, damager):
        super().receive_damage(damage, damager)
        self.target = damager
        self.current_action = 'attack'
        self.change_relations(damager.name, -damage * 4)


    def change_relations(self, name, delta):
        if self.relations.get(name, None) is None:
            self.relations[name] = 0
        self.relations[name] += delta

    def update_relations(self):
        for actor in self.levels[self.level].actors:
            if self.pos.distance(actor.pos) > 15:
                continue
            if self.relations.get(actor.name, None) is None:
                self.relations[actor.name] = random.randint(0, 1)
                for item in actor.inventory:
                    if item.item_type == 'weapon':
                        if item.equipped:
                            self.change_relations(actor2.name, -10)
                        else:
                            self.change_relations(actor2.name, -3)
            if not actor.is_alive:
                if self.relations[actor.name] > 80:
                    for actor2 in self.levels[self.level].actors:
                        if self.pos.distance(actor2.pos) > 15:
                            continue
                        if actor.pos.distance(actor2.pos) < 4:
                            self.change_relations(actor2.name, -80)
        for actor in self.levels[self.level].actors:
            if self.pos.distance(actor.pos) > 15:
                continue
            if self.relations.get(actor.name, 0) < 0:
                self.current_action = 'kill'
                self.target = actor
                break


    def define_current_action(self, ticks):
        if self.current_action == 'talk':
            return
        if self.current_action == 'kill':
            if self.target.level != self.level or self.target is None or not self.target.is_alive or self.relations[self.target.name] >= 0:
                self.current_action = None
                self.define_current_action(ticks)
            else:
                return
        if self.profession == 'farmer':
            if 5000 < ticks or ticks < 500:
                self.current_action = 'go sleep'
            elif ticks < 1500:
                self.current_action = 'work'
            elif ticks < 2000:
                self.current_action = 'rest'
            elif ticks < 4000:
                self.current_action = 'work'
            else:
                self.current_action = 'rest'
        elif self.profession == 'guardian':
            if 5800 < ticks or ticks < 200:
                self.current_action = 'go sleep'
            elif ticks < 1500:
                self.current_action = 'work'
            elif ticks < 2000:
                self.current_action = 'rest'
            elif ticks < 4000:
                self.current_action = 'work'
            else:
                self.current_action = 'rest'
            

    def act(self):
        if not self.is_alive: return
        if self.current_action == 'go sleep':
            if self.is_in_home:
                self.current_action = 'sleep'
            else:
                self.current_action = 'home'
        self.update_relations()
        if self.current_action == 'kill':
            self.action_kill()
        if self.current_action == 'home':
            self.action_stay_home()
        elif self.current_action == 'work':
            self.action_work()

    def action_stay_home(self):
        if self.target_point is None:
            self.target_point = (random.randint(self.house.shape[0] + 1, self.house.shape[2] - 1),
                                  random.randint(self.house.shape[1] + 1, self.house.shape[3] - 1))
            self.wait_timer = random.randint(0, 40)
        if self.pos.x > self.target_point[0]:
            self.pos.x -= 1
        elif self.pos.x < self.target_point[0]:
            self.pos.x += 1

        if self.pos.y > self.target_point[1]:
            self.pos.y -= 1
        elif self.pos.y < self.target_point[1]:
            self.pos.y += 1

        if self.pos.x == self.target_point[0] and self.pos.y == self.target_point[1]:
            self.is_in_home = True
            if self.wait_timer == 0:
                self.target_point = (random.randint(self.house.shape[0] + 1, self.house.shape[2] - 1),
                                     random.randint(self.house.shape[1] + 1, self.house.shape[3] - 1))
                self.wait_timer = random.randint(10, 40)
            else:
                self.wait_timer -= 1

    def action_work(self):
        
        self.is_in_home = False
        if self.profession == 'farmer':
            self.action_farm()
        elif self.profession == 'guardian':
            self.action_patrol()


    def move_to_target(self):
        if self.pos.x > self.target_point[0]:
            self.pos.x -= 1
        elif self.pos.x < self.target_point[0]:
            self.pos.x += 1

        if self.pos.y > self.target_point[1]:
            self.pos.y -= 1
        elif self.pos.y < self.target_point[1]:
            self.pos.y += 1


    def action_farm(self):
        if self.target_point is None:
            self.target_point = (random.randint(self.work_zone.shape[0], self.work_zone.shape[2]),
                                 random.randint(self.work_zone.shape[1], self.work_zone.shape[3]))
            self.wait_timer = random.randint(0, 40)
        
        self.move_to_target()
        
        if self.pos.x == self.target_point[0] and self.pos.y == self.target_point[1]:
            if self.wait_timer == 0:
                self.target_point = (random.randint(self.work_zone.shape[0], self.work_zone.shape[2]),
                                     random.randint(self.work_zone.shape[1], self.work_zone.shape[3]))
                self.wait_timer = random.randint(10, 40)
            else:
                self.wait_timer -= 1

    def action_patrol(self):
        if self.target_point is None:
            self.target_point = (random.randint(self.work_zone[0].shape[0], self.work_zone[0].shape[2]),
                                 random.randint(self.work_zone[0].shape[1], self.work_zone[0].shape[3]))
            self.work_zone = self.work_zone[1:] + [self.work_zone[0]]

        self.move_to_target()

        if self.pos.x == self.target_point[0] and self.pos.y == self.target_point[1]:
            self.target_point = (random.randint(self.work_zone[0].shape[0], self.work_zone[0].shape[2]),
                                 random.randint(self.work_zone[0].shape[1], self.work_zone[0].shape[3]))
            self.work_zone = self.work_zone[1:] + [self.work_zone[0]]

    def action_kill(self):
        self.target_point = (self.target.pos.x, self.target.pos.y)
        if abs(self.target.pos.x - self.pos.x) <= 1 and abs(self.target.pos.y - self.pos.y) <= 1:
            self.target.pos.x += (self.target.pos.x - self.pos.x) * self.get_damage() // 2
            self.target.pos.y += (self.target.pos.y - self.pos.y) * self.get_damage() // 2
            self.target.receive_damage(self.get_damage(), self)
        else:
            self.move_to_target()

