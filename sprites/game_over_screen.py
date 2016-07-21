import pygame


class GameOverScreen(pygame.sprite.Sprite):
    '''class for gameover screen'''

    def __init__(self):
        '''initializer method'''
        pygame.sprite.Sprite.__init__(self)
        # loads background image and rect
        self.__bkgd = pygame.image.load('images\\gameover.jpg').convert()
        self.rect = self.__bkgd.get_rect()
        self.rect.topleft = (0, 0)
        # initial tint
        self.__colour = 0

    def get_done(self):
        '''returns True once the animation is over'''
        return self.__colour >= 300

    def update(self):
        '''update method'''
        # colour goes from dark to bright
        if self.__colour <= 255:
            self.image = self.__bkgd.copy()
            self.image.fill((self.__colour,) * 3, special_flags=pygame.BLEND_RGB_MULT)
        else:
            self.image = self.__bkgd

        # lightens colour
        self.__colour += 1