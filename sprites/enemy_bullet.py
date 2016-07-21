import pygame


class EnemyBullet(pygame.sprite.Sprite):
    '''enemy bullet class'''

    def __init__(self, enemy, player):
        '''initializer method with the enemy and player as parameters'''
        pygame.sprite.Sprite.__init__(self)

        # loads all required sprites
        self.__sprites = [pygame.image.load(
            'images\\bullet\\' + str(enemy.get_direction()) + '\\0\\' + str(frame) + '.png').convert_alpha() for frame
                          in range(2)] + [pygame.image.load('images\\bullet\\bullet1.png').convert_alpha()]

        # loads image and rect
        self.image = self.__sprites[0]
        self.rect = self.image.get_rect()
        self.rect.centery = enemy.rect.top + 24

        # calculates slope
        try:
            self.__slope = float(enemy.rect.centery - player.rect.centery) // (enemy.rect.centerx - player.rect.centerx)
        except ZeroDivisionError:
            self.__slope = 100000000

        # calculates x and y velocities
        if enemy.get_direction():
            self.rect.right = enemy.rect.left
            self.__vx = -(20 // (self.__slope ** 2 + 1)) ** 0.5
        else:
            self.rect.left = enemy.rect.right
            self.__vx = (20 // (self.__slope ** 2 + 1)) ** 0.5

        self.__vy = self.__slope * self.__vx

        self.__frame = 0

    def update(self, *args):
        '''update method'''
        # changes image in second and third frames
        if self.__frame in (1, 2):
            self.__prev = self.rect.center
            self.image = self.__sprites[self.__frame]
            self.rect = self.image.get_rect()
            self.rect.center = self.__prev
            # starts moving the sprite after the first 2 frames, which are muzzle flashes
        if self.__frame > 1:
            self.rect.left += self.__vx
            self.rect.top += self.__vy

        # kills the bullet once it is outside the background
        if self.rect.right <= 0 or self.rect.left >= 3945 or self.rect.top < 0 or self.rect.bottom > 480:
            self.kill()

        self.__frame += 1