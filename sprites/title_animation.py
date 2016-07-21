import pygame


class TitleAnimation(pygame.sprite.Sprite):
    '''title animations'''

    def __init__(self, num):
        '''initializer method with the image number as the parameter'''
        pygame.sprite.Sprite.__init__(self)

        # loads image and rect
        self.__image = pygame.image.load('images\\' + ('metal', 'python')[num] + '.png').convert_alpha()
        self.rect = self.__image.get_rect()
        self.rect.center = (160, 80 + 50 * num)

        self.__frame = 0
        self.__size = self.__image.get_size()

    def get_done(self):
        '''returns True when the animation is over'''
        return self.__frame == 20

    def update(self):
        '''update method'''
        if self.__frame < 20:
            self.image = pygame.transform.scale(self.__image.copy(), self.__size)
            self.__prev = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = self.__prev
            # makes image 98% smaller each frame
            self.__size = tuple(map(lambda x: int(0.98 * x), self.__size))
            self.__frame += 1