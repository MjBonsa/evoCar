import datetime
import math
from math import sin, radians, cos

import pygame

BORDER_COLOR = (255, 255, 255, 255)
WHITE_COLOR = (0, 0, 0, 255)


class Vehicle(pygame.sprite.Sprite):

    def __init__(self, surface, x, y, rot):
        super().__init__()
        self.dists_x_y = []
        self.lidar_points = []
        self.work_time = 10
        self.start_time = datetime.datetime.now()
        self.image_orig = surface
        self.pos_x = x
        self.pos_y = y
        self.is_destroyed = False
        self.lidar_lines = []
        self.pos_rotation = rot
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.boost = 0  # acceleration
        self.car_half_h = self.rect.height / 2
        self.car_half_w = self.rect.width / 2
        # calculate angel
        x1, y1 = self.rect.center
        x2, y2 = self.rect.bottomright
        # РЕДАКТИРОВАТЬ ЗНАЧЕНИЕ ПОСЛЕ МИНУСА ЕСЛИ НЕ СОВПАДАЮТ УГЛЫ СПРАЙТА ЗНАЧЕНИЕ ПОСЛЕ МИНУСА
        self.car_top_l = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1 / 2) - 12
        self.car_bot_l = self.car_top_l + 12
        self.reward = 0
        self.max_boost = 8

    def point_distanse(self, screen, g_map):
        dists = []
        dists_x_y = []
        for i, degree in enumerate([-90, -125, -55, 0, -180]):
            length = 0
            xx, yy = self.rect.center
            x = xx
            y = yy

            while g_map.get_at((x, y)) == WHITE_COLOR and length < 250:
                length = length + 1
                x = int(xx + math.cos(math.radians(360 - (self.pos_rotation + degree))) * length)
                y = int(yy + math.sin(math.radians(360 - (self.pos_rotation + degree))) * length)

            # Calculate Distance To Border And Append To Radars List
            dist = int(math.sqrt(math.pow(x - xx, 2) + math.pow(y - yy, 2)))
            dists.append(dist)
            dists_x_y.append([x, y])

        self.dists_x_y = dists_x_y
        return dists

    def draw_lidars(self, screen):
        for dist in self.dists_x_y:
            pygame.draw.line(screen, (255, 0, 0), [self.rect.center[0], self.rect.center[1]], [dist[0], dist[1]], 2)
            pygame.draw.circle(screen, (0, 255, 0), [dist[0], dist[1]], 5)

    # Use moveUp and moveDown if inertia is not needed
    def moveUp(self):
        a = pygame.math.Vector2(self.pos_x + 5 * sin(radians(self.pos_rotation)),
                                self.pos_y + 5 * cos(radians(self.pos_rotation)))

        self.pos_x += 5 * sin(radians(self.pos_rotation))
        self.pos_y += 5 * cos(radians(self.pos_rotation))
        self.rect = self.image.get_rect(center=a)

    def moveDown(self):
        a = pygame.math.Vector2(self.pos_x - 5 * sin(radians(self.pos_rotation)),
                                self.pos_y - 5 * cos(radians(self.pos_rotation)))

        self.pos_x -= 5 * sin(radians(self.pos_rotation))
        self.pos_y -= 5 * cos(radians(self.pos_rotation))
        self.rect = self.image.get_rect(center=a)

    def rotation_l(self):
        self.pos_rotation = (self.pos_rotation + 3) % 360
        tmp = pygame.transform.rotate(self.image_orig, self.pos_rotation)
        old_center = self.rect.center
        self.image = tmp
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def rotation_r(self):
        self.pos_rotation = (self.pos_rotation - 3) % 360
        tmp = pygame.transform.rotate(self.image_orig, self.pos_rotation)
        old_center = self.rect.center
        self.image = tmp
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def boost_up(self):
        if self.boost > -self.max_boost:
            self.boost -= 0.15

    def boost_down(self):
        if self.boost < 0:
            self.boost += 0.1
        else:
            self.boost += 0.05

    def brake(self):
        if (self.boost < 0.3) and (self.boost > -0.3):
            self.boost = 0
            return
        if self.boost < 0:
            self.boost += 0.3
        else:
            self.boost -= 0.3

    def update(self, screen):
        a = pygame.math.Vector2(self.pos_x - self.boost * sin(radians(self.pos_rotation)),
                                self.pos_y - self.boost * cos(radians(self.pos_rotation)))

        self.pos_x -= self.boost * sin(radians(self.pos_rotation))
        self.pos_y -= self.boost * cos(radians(self.pos_rotation))

        self.rect = self.image.get_rect(center=a)
        if self.boost < 0:
            self.boost += 0.03
        if self.boost > 0:
            self.boost -= 0.03
        if not self.is_destroyed:
            self.draw_lidars(screen)

    def destroy(self, dists):
        # return checkpoints
        flag = 0
        # if int(self.pos_x) == 80 and int(self.pos_y) == 300:
        #    flag = 1
        # if abs((datetime.datetime.now()-self.start_time).seconds) > 2:
        #    flag = 1
        if dists[0] < self.car_half_h:
            self.is_destroyed = True
        # if abs((datetime.datetime.now()-self.start_time).seconds) > self.work_time:
        #    flag = 1

        if self.is_destroyed:
            self.pos_x = -10000
            self.pos_y = -10000
            self.boost = 0
            self.pos_rotation = 0.001
            return True
        return False
