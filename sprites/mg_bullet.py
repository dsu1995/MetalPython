import random

import pygame


class MGBullet(pygame.sprite.Sprite):
    '''machine gun bullet class'''

    def __init__(self, bkgd, player, shotnum):
        '''initializer method with the background, player, and shot number as parameters'''
        pygame.sprite.Sprite.__init__(self)

        # loads all required sprites, shot number determines the muzzle flash image
        self.__sprites = (pygame.image.load(
            'images\\bullet\\' + str(player.get_direction()) + '\\1\\' + str(shotnum) + '.png').convert_alpha(),
                          pygame.image.load('images\\bullet\\bullet0.png').convert_alpha())

        # loads image and rect
        self.image = self.__sprites[0]
        self.rect = self.image.get_rect()
        self.rect.centery = player.rect.centery
        # decides the direction of the bullet, makes speed random
        if player.get_direction():
            self.rect.right = player.rect.left + 20
            self.__vx = -20 + random.randint(-1, 1)
        else:
            self.rect.left = player.rect.right - 20
            self.__vx = 20 + random.randint(-1, 1)
        # initializes attributes
        self.__player = player
        self.__frame = 0
        self.__bkgd = bkgd
        self.__vy = random.randint(-1, 1)

    def update(self, *args):
        # first frame is muzzle flash, all subsequent frames change to the bullet
        if self.__frame == 1:
            self.__prev = self.rect.center
            self.image = self.__sprites[1]
            self.rect = self.image.get_rect()
            self.rect.center = self.__prev

            # moves bullet
        self.rect.left += self.__vx
        self.rect.top += self.__vy

        # check if the bullet is outside the screen
        if self.rect.right < -self.__bkgd.rect.left or self.rect.left > -self.__bkgd.rect.left + 640 or self.rect.top < 0 or self.rect.bottom > 480:
            self.kill()

        self.__frame += 1