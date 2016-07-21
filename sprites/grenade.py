import pygame


class Grenade(pygame.sprite.Sprite):
    '''grenade class'''
    __explosion = [pygame.image.load('images\\grenade\\' + str(frame) + '.png').convert_alpha() for frame in range(21)]
    __grenade = pygame.image.load('images\\grenade\\grenade.png').convert_alpha()
    # sound
    __explode = pygame.mixer.Sound('sounds\\explosion.wav')

    def __init__(self, player):
        '''initializer method with the player as the parameter'''
        pygame.sprite.Sprite.__init__(self)

        # initializes angle
        self.__angle = [-45, 45][player.get_direction()]
        # rotates the image and get the rect
        self.image = pygame.transform.rotate(Grenade.__grenade, self.__angle)
        self.rect = self.image.get_rect()

        # sets starting location and velocity
        if player.get_direction():
            self.rect.bottomright = player.rect.midtop
            self.__vx = -15
        else:
            self.rect.bottomleft = player.rect.midtop
            self.__vx = 15

        self.__vy = -10
        self.__explode = False
        self.__frame = 0

    def explode(self):
        '''starts explosion animation'''
        self.__explode = True
        Grenade.__explode.play()

    def update(self, *args):
        '''update method'''
        # while exploding
        if self.__explode:
            self.__prev = self.rect.midbottom
            self.image = Grenade.__explosion[self.__frame]
            self.rect = self.image.get_rect()
            self.rect.midbottom = self.__prev

            self.__frame += 1
            # kills sprite once explosion is over
            if self.__frame >= 21:
                self.kill()
        # in the air
        else:
            # rotates image
            self.image = pygame.transform.rotate(Grenade.__grenade, self.__angle)
            if self.__angle < 0:
                self.__angle -= 5
            else:
                self.__angle += 5
            # moves sprite horizontally
            self.rect.left += self.__vx
            # gravity
            self.__vy += 1.1
            self.rect.top += self.__vy