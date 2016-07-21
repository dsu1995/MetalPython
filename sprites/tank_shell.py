import random

import pygame


class TankShell(pygame.sprite.Sprite):
    '''tank shell sprite'''
    __explosion = [pygame.image.load('images\\grenade\\' + str(frame) + '.png').convert_alpha() for frame in range(21)]
    __shell = pygame.image.load('images\\grenade\\shell.png').convert_alpha()
    # sound
    __explode = pygame.mixer.Sound('sounds\\explosion.wav')

    def __init__(self, tank=None):
        '''initializer method with the tank as an optional parameter. if not present, assumes shell is fired from the boss'''
        pygame.sprite.Sprite.__init__(self)

        # sets key attributes
        if bool(tank):
            self.__angle = 0
            self.__vx = 20
            self.__vy = 0
            self.__da = -5  # change in angle
            self.__g = 1.1
        else:
            self.__angle = 135
            self.__vx = random.randint(-20, -1)
            self.__vy = -5
            self.__da = 2
            self.__g = 0.4

        # rotates the image and get the rect
        self.image = pygame.transform.rotate(TankShell.__shell, self.__angle)
        self.rect = self.image.get_rect()
        if bool(tank):
            self.rect.midleft = (tank.rect.left + 162, tank.rect.top + 50)
        else:
            self.rect.midright = (870, 290)

        self.__explode = False
        self.__frame = 0

    def explode(self):
        '''starts explosion animation'''
        if not self.__explode:
            self.__explode = True
            TankShell.__explode.play()

    def update(self, *args):
        '''update method'''
        # while exploding
        if self.__explode:
            self.__prev = self.rect.midbottom
            self.image = TankShell.__explosion[self.__frame]
            self.rect = self.image.get_rect()
            self.rect.midbottom = self.__prev

            self.__frame += 1
            # kills sprite once animation is over
            if self.__frame >= 21:
                self.kill()
        # while in the air
        else:
            # rotates image
            self.image = pygame.transform.rotate(TankShell.__shell, self.__angle)
            self.__angle += self.__da
            # moves image horizontally
            self.rect.left += self.__vx
            # gravity
            self.__vy += self.__g
            self.rect.top += self.__vy