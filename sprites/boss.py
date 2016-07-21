import random

import pygame


class Boss(pygame.sprite.Sprite):
    '''class for gameover screen'''

    def __init__(self):
        '''initializer method'''
        pygame.sprite.Sprite.__init__(self)

        # loads image and rect
        self.__sprites = [pygame.image.load('images\\boss\\tank' + str(i) + '.png').convert_alpha() for i in range(2)]
        self.__explosion = [pygame.image.load('images\\tank\\4\\' + str(i) + '.png').convert_alpha() for i in
                            range(17, 42)]

        self.image = self.__sprites[0].copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (865, 283)

        # initializes parameters
        self.__health = 3000
        self.__active = False
        self.__animation = 0
        self.__delay = 0
        self.__attack = 0
        self.__dying = False
        self.__dead = False
        self.__hurt = False
        self.__frame = 0
        # sound
        self.__explode = pygame.mixer.Sound('sounds\\explosion.wav')

    def start(self):
        '''called when the player sees the tank and the tank starts to attack'''
        self.__active = True

    def get_attack(self):
        '''returns the current attack'''
        return self.__attack

    def hurt(self, damage):
        '''reduces health'''
        self.__health -= damage
        self.__hurt = True

    def get_dead(self):
        '''returns True when the boss death animation is over'''
        return self.__dead

    def update(self, *args):
        '''update method'''
        # checks if boss is dead
        if not self.__dying and self.__health <= 0:
            self.__dying = True
            self.__delay = 0
            self.__explode.play()

        # death animation
        if self.__dying:
            self.image = self.__explosion[self.__delay // 3]
            self.__prev = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = self.__prev
            self.__delay += 1
            if self.__delay >= len(self.__explosion) * 3:
                self.kill()
                self.__dead = True
        # while alive
        elif self.__active:
            # picks random attack
            if not self.__animation:
                self.__animation = random.randint(0, 2)
                self.__delay = 0
            # shoot cannon every half second
            if self.__animation == 1:
                self.image = self.__sprites[0].copy()
                if self.__delay in (30, 60, 90):
                    self.__attack = 1
                if self.__delay in (31, 61, 91):
                    self.__attack = 0
                # stops shooting after 3 seconds
                elif self.__delay == 150:
                    self.__animation = 0
                    self.__delay == 0
            # laser cannon
            elif self.__animation == 2:
                # changes tank image
                if self.__delay == 0:
                    self.__frame = 1
                    # starts shooting
                elif self.__delay == 60:
                    self.__frame = 0
                    self.__attack = 2
                elif self.__delay == 61:
                    self.__attack = 0
                # stops shooting
                elif self.__delay == 150:
                    self.__animation = 0
                    self.__delay = 0

            # clears image
            self.image = self.__sprites[self.__frame].copy()
            # flashes red when hurt
            if self.__hurt:
                self.image.fill((200, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
                self.__hurt = False

        self.__delay += 1