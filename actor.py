import random
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Actor:
    def __init__(self, name, pos, level, tile, health):
        self.name = name
        self.pos = pos
        self.level = level
        self.tile = tile
        self.health = health
        self.inventory = []

    def move(dx, dy):
        self.pos.x += dx
        self.pos.y += dy


class Player(Actor):
    pass


class NPC(Actor):
    def __init__(self, name, pos, level, tile, health, profession):
        super().__init__(name, pos, level, tile, health)
        self.triggers = []
        self.relations = []
        self.objects = []
        self.profession = profession
        self.current_action = None
        self.home = None
        self.target_point = None
        self.wait_timer = 0
        self.work_zone = None


    def define_current_action(self, ticks):
        if self.current_action == 'talk':
            return
        if 5000 < ticks or ticks < 500:
            self.current_action = 'home'
        elif ticks < 1500:
            self.current_action = 'work'
        elif ticks < 2000:
            self.current_action = 'rest'
        elif ticks < 4000:
            self.current_action = 'work'
        else:
            self.current_action = 'rest'

    def act(self):
        if self.current_action == 'home':
            self.stay_home()
        elif self.current_action == 'work':
            self.work()

    def stay_home(self):
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
            if self.wait_timer == 0:
                self.target_point = (random.randint(self.house.shape[0] + 1, self.house.shape[2] - 1),
                                     random.randint(self.house.shape[1] + 1, self.house.shape[3] - 1))
                self.wait_timer = random.randint(10, 40)
            else:
                self.wait_timer -= 1

    def work(self):
        if self.profession == 'farmer':
            self.farm()
        elif self.profession == 'guardian':
            self.patrol()

    def farm(self):
        if self.target_point is None:
            self.target_point = (random.randint(self.work_zone.shape[0], self.work_zone.shape[2]),
                                 random.randint(self.work_zone.shape[1], self.work_zone.shape[3]))
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
            if self.wait_timer == 0:
                self.target_point = (random.randint(self.work_zone.shape[0], self.work_zone.shape[2]),
                                     random.randint(self.work_zone.shape[1], self.work_zone.shape[3]))
                self.wait_timer = random.randint(10, 40)
            else:
                self.wait_timer -= 1

    def patrol(self):
        if self.target_point is None:
            self.target_point = (random.randint(1, 99),
                                 random.randint(1, 99))
        if self.pos.x > self.target_point[0]:
            self.pos.x -= 1
        elif self.pos.x < self.target_point[0]:
            self.pos.x += 1

        if self.pos.y > self.target_point[1]:
            self.pos.y -= 1
        elif self.pos.y < self.target_point[1]:
            self.pos.y += 1

        if self.pos.x == self.target_point[0] and self.pos.y == self.target_point[1]:
            self.target_point = (random.randint(self.work_zone.shape[0], self.work_zone.shape[2]),
                                 random.randint(self.work_zone.shape[1], self.work_zone.shape[3]))
