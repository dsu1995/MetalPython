import pygame


class PistolBullet(pygame.sprite.Sprite):
    '''class for pistol bullet'''

    def __init__(self, bkgd, player):
        '''initializer method with the background and player as parameters'''
        pygame.sprite.Sprite.__init__(self)
        # loads all required sprites
        self.__sprites = [pygame.image.load(
            'images\\bullet\\' + str(player.get_direction()) + '\\0\\' + str(frame) + '.png').convert_alpha() for frame
                          in range(2)] + [pygame.image.load('images\\bullet\\bullet0.png').convert_alpha()]
        # loads image and rect
        self.image = self.__sprites[0]
        self.rect = self.image.get_rect()
        # sets x and y velocity
        self.rect.centery = player.rect.top + 24
        if player.get_direction():
            self.rect.right = player.rect.left
            self.__vx = -20
        else:
            self.rect.left = player.rect.right
            self.__vx = 20
        self.__player = player
        self.__frame = 0
        self.__bkgd = bkgd

    def update(self, *args):
        '''update method'''
        # first 2 frames are muzzle flash, third frame becomes the bullet
        if self.__frame in (1, 2):
            self.__prev = self.rect.center
            self.image = self.__sprites[self.__frame]
            self.rect = self.image.get_rect()
            self.rect.center = self.__prev

            # bullet starts moving in third frame
        if self.__frame > 1:
            self.rect.left += self.__vx

        # checks if bullet is out of the screen
        if self.rect.right < -self.__bkgd.rect.left or self.rect.left > -self.__bkgd.rect.left + 640 or self.rect.top < 0 or self.rect.bottom > 480:
            self.kill()

        self.__frame += 1