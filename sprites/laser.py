import pygame


class Laser(pygame.sprite.Sprite):
    '''laser attack for boss'''

    def __init__(self):
        '''initializer method'''
        pygame.sprite.Sprite.__init__(self)
        # loads image and rect
        self.__sprites = [pygame.image.load('images\\boss\\laser\\' + str(i) + '.png') for i in range(4)]
        self.image = self.__sprites[0]
        self.rect = self.image.get_rect()
        self.hide()
        self.__frame = 0

    def reset(self):
        '''activates laser'''
        self.rect.midright = (910, 390)
        self.__active = True
        self.__frame = 0

    def hide(self):
        '''hides laser by moving it offscreen'''
        self.__active = False
        self.rect.bottom = -1

    def update(self, *args):
        '''update method'''
        # changes pictures
        if self.__active:
            if not self.__frame:
                self.image = self.__sprites[0]
            elif self.__frame == 20:
                self.image = self.__sprites[1]
            elif self.__frame == 40:
                self.image = self.__sprites[2]
            elif self.__frame == 45:
                self.image = self.__sprites[3]
            elif self.__frame == 50:
                self.hide()

            # recenters image
            self.__prev = self.rect.midright
            self.rect = self.image.get_rect()
            self.rect.midright = self.__prev

            self.__frame += 1