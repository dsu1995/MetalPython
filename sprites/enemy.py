import os
import random

import pygame


class Enemy(pygame.sprite.Sprite):
    '''enemy class'''
    __sprites = [[[pygame.image.load(
        'images\\enemy\\' + str(orientation) + '\\' + str(animation) + '\\' + str(frame) + '.png').convert_alpha() for
                   frame in range(len(os.listdir('images\\enemy\\' + str(orientation) + '\\' + str(animation))))] for
                  animation in range(3)] for orientation in range(2)]
    # sound
    __shoot = pygame.mixer.Sound('sounds\\enemy.wav')
    __death = [pygame.mixer.Sound('sounds\\soldier' + str(i) + '.wav') for i in range(1, 6)]

    def __init__(self, midbottom):
        '''initializer that accepts the midbottom coordinates as a parameter'''
        pygame.sprite.Sprite.__init__(self)

        # initializes animation
        self.__orientation = 1
        self.__animation = 0
        self.__frame = 0

        # loads image and rect
        self.image = Enemy.__sprites[self.__orientation][self.__animation][self.__frame]
        self.rect = self.image.get_rect()
        self.rect.midbottom = midbottom
        self.__shotcounter = 0
        self.__speed = 15

    def get_shooting(self):
        '''returns True when the enemy is shooting'''
        if self.__animation == 1 and self.__frame == 9:
            Enemy.__shoot.play()
            return True

    def get_direction(self):
        '''returns the direction'''
        return self.__orientation

    def die(self):
        '''starts death animation'''
        if self.__animation != 2:
            self.__animation = 2
            self.__frame = 0
            Enemy.__death[random.randint(0, 4)].play()

    def get_dying(self):
        '''returns True when the enemy is in its death animation'''
        return self.__animation == 2

    def update(self, player):
        '''update method that receives the player as a parameter'''
        self.__player = player

        # death animation
        if self.__animation == 2:
            self.__prev = self.rect.midbottom
            # updates image and rect
            self.image = Enemy.__sprites[self.__orientation][self.__animation][self.__frame // 3]
            self.rect = self.image.get_rect()
            self.rect.midbottom = self.__prev
            self.__frame += 1

            # removes enemy from all groups once the death animation is over
            if self.__frame >= len(self.__sprites[self.__orientation][self.__animation]) * 3:
                self.kill()

                # while alive
        else:
            # changes orientation
            if self.__player.rect.centerx < self.rect.centerx:
                self.__orientation = 1
            elif self.__player.rect.centerx > self.rect.centerx:
                self.__orientation = 0
            # starts shooting
            if self.__shotcounter >= 75 and self.rect.left - 480 <= self.__player.rect.centerx < +self.rect.right + 480:
                self.__shotcounter = 0
                self.__animation = 1
                self.__frame = 0
                self.__speed = 3
            # stands still
            elif self.__shotcounter == 15:
                self.__animation = 0
                self.__frame = 0
                self.__speed = 15

            self.__prev = self.rect.midbottom
            # updates image
            self.image = Enemy.__sprites[self.__orientation][self.__animation][self.__frame // self.__speed]
            self.rect = self.image.get_rect()
            self.rect.midbottom = self.__prev

            self.__frame += 1
            if self.__frame >= len(Enemy.__sprites[self.__orientation][self.__animation]) * self.__speed:
                self.__frame = 0

            self.__shotcounter += 1