import random

import pygame


class MGIcon(pygame.sprite.Sprite):
    '''machine gun pickup'''

    def __init__(self):
        '''initializer method'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('images\\mgicon.png')
        self.rect = self.image.get_rect()
        self.hide()

    def hide(self):
        '''hides image'''
        self.__active = False
        self.rect.bottom = -1

    def update(self, *args):
        if self.__active:
            # moves image down
            self.rect.bottom += 5
            if self.rect.bottom >= 480:
                # hides image again when it is below the screen
                self.hide()
        else:
            # randomly respawns it at a random x location
            if random.randint(1, 750) == 1:
                self.__active = True
                self.rect.centerx = random.randint(300, 800)