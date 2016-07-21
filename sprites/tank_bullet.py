import math
import random

import pygame


class TankBullet(pygame.sprite.Sprite):
    '''tank bullet sprite'''
    __sprite = pygame.image.load('images\\bullet\\bullet3.png').convert_alpha()

    def __init__(self, bkgd, tank):
        '''initializer method with the background and tank as parameters'''
        pygame.sprite.Sprite.__init__(self)
        # rotates image
        self.image = pygame.transform.rotate(TankBullet.__sprite, tank.get_angle())
        # gets rect and positions it
        self.rect = self.image.get_rect()
        self.rect.center = tank.get_turret()
        # calculate x and y velocities
        self.__vx = -math.sin(math.radians(tank.get_angle())) * 30 + random.randint(-1, 1)
        self.__vy = -math.cos(math.radians(tank.get_angle())) * 30 + random.randint(-1, 1)

        self.__frame = 0
        self.__bkgd = bkgd

    def update(self, *args):
        '''update method'''
        # bullet starts moving during second frame
        if self.__frame:
            self.rect.left += self.__vx
            self.rect.top += self.__vy
        # kills bullet once it is outside the screen
        if self.rect.right < -self.__bkgd.rect.left or self.rect.left > -self.__bkgd.rect.left + 640 or self.rect.bottom < 0 or self.rect.top > 480:
            self.kill()

        self.__frame += 1