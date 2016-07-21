import os

import pygame


class Tank(pygame.sprite.Sprite):
    '''tank sprite'''

    def __init__(self, prev_tank=None):
        '''intializer method'''
        pygame.sprite.Sprite.__init__(self)
        # loads all animations
        self.__sprites = [
            [pygame.image.load('images\\tank\\' + str(animation) + '\\' + str(frame) + '.png').convert_alpha() for frame
             in range(len(os.listdir('images\\tank\\' + str(animation))))] for animation in range(5)]
        # loads mg turret image
        self.__mg = pygame.image.load('images\\tank\\turret.png').convert_alpha()

        # sets initial animation
        self.__animation = 0
        self.__frame = 0

        # loads image and rect
        self.image = self.__sprites[self.__animation][self.__frame].copy()
        self.rect = self.image.get_rect()
        if prev_tank:
            self.rect.bottomleft = (50, 432)
        else:
            self.rect.bottomleft = (1450, 450)

        # sets attributes
        self.__prev_bottom = self.rect.bottom
        self.__vx = 0
        self.__vy = 0
        self.__falling = False
        self.__shooting_cannon = False
        self.__shooting_mg = False
        self.__speed = 15
        self.__angle = 0
        if prev_tank:
            self.__shells = int(prev_tank.get_grenades())
            self.__health = int(prev_tank.get_health())
        else:
            self.__shells = 10
            self.__health = 200
        self.__hurt = 0

        # sound
        self.__cannon = pygame.mixer.Sound('sounds\\cannon.wav')
        self.__mg_sound = pygame.mixer.Sound('sounds\\mg.wav')
        self.__explode = pygame.mixer.Sound('sounds\\explosion.wav')

    def get_grenades(self):
        '''returns the number of tank shells left'''
        return self.__shells

    def get_ammo(self):
        '''returns the ammount of ammo left'''
        return u'∞'

    def get_health(self):
        '''return the amount of health left'''
        return self.__health

    def hurt(self, damage):
        '''decrements health and makes image flash red'''
        if not self.__hurt:
            self.__health -= damage // 2
            self.__hurt = 30

    def jump(self):
        '''starts jumping'''
        if not self.__falling and self.__animation != 3:
            self.rect.top -= 1
            self.__vy = -17
            self.__falling = True

    def move(self, vx):
        '''moves the tank horizontally'''
        self.__vx = vx

    def collide_wall(self, wall, level=0):
        '''handles collision with the wall'''
        if level:
            self.rect.right = wall.rect.left
        else:
            self.rect.left = wall.rect.right
        self.__vx = 0

    def fall(self):
        '''called when the tank is not on any platform'''
        self.__falling = True

    def get_angle(self):
        '''returns the angle of the machine gun turret'''
        return self.__angle

    def land(self, platform):
        '''lands the tank on a platform'''
        # checks if the tank drove off a platform and touched a higher platform
        if not self.__falling and self.rect.bottom > platform + 1:
            self.__falling = True
        # checks if the tank was completely above the platform at some point
        elif self.__prev_bottom <= platform:
            self.rect.bottom = platform + 1
            self.__vy = 0
            self.__falling = False

    def shoot_cannon(self):
        '''initiates shooting animation'''
        if self.__shells > 0:
            self.__shooting_cannon = True
            self.__shells -= 1
            self.__cannon.play()
            return True

    def shoot_mg(self):
        '''plays the shooting sound'''
        self.__mg_sound.play()

    def die(self):
        '''called when the player exited the tank'''
        if self.__animation != 4:
            self.__animation = 4
            self.__frame = 0
            self.__explode.play()

    def rotate(self, angle):
        '''rotates the turret'''
        self.__angle += angle

    def get_direction(self):
        '''returns the direction the tank is facing'''
        return 0

    def get_dying(self):
        '''returns whether the tank is in its death animation'''
        return self.__animation == 4

    def get_turret(self):
        '''returns the coordinates of the center of the turret'''
        return self.__temp_rect.centerx + self.rect.left, self.__temp_rect.centery + self.rect.top

    def update(self, *args):
        '''update method'''
        # runs the die() method once the tank is out of health
        if self.__health <= 0 and self.__animation != 4:
            self.die()

        # updates previous bottom
        self.__prev_bottom = self.rect.bottom

        # falling
        if self.__falling:
            self.__vy += 1.1
            self.rect.bottom += self.__vy

        # death animation
        if self.__animation == 4:
            # updates image
            if self.__frame < len(self.__sprites[self.__animation]) * 3:
                self.image = self.__sprites[self.__animation][self.__frame // 3]
            else:
                # kills sprite once out of animations
                self.kill()

                # updates rect while keeping the old bottomleft
            self.__prev = self.rect.bottomleft
            self.rect = self.image.get_rect()
            self.rect.bottomleft = self.__prev

            self.__frame += 1

            # while alive
        else:
            # horizontal movement
            self.rect.left += self.__vx * 8

            # checks if the tank is outside the map
            if self.rect.left <= 0:
                self.rect.left = 0

                # animation
            # shooting
            if self.__shooting_cannon:
                if self.__animation != 2:
                    self.__frame = 0
                    self.__animation = 2
                    self.__speed = 2
            # still
            elif self.__animation and not self.__vx and not self.__vy:
                self.__frame = 0
                self.__speed = 15
                self.__animation = 0
                # jumping
            elif self.__animation != 3 and self.__vy:
                self.__frame = 0
                self.__speed = 1
                self.__animation = 3
            # running
            elif self.__animation != 1 and self.__vx and not self.__vy:
                self.__frame = 0
                self.__speed = 2
                self.__animation = 1

                # updates image
            self.image = self.__sprites[self.__animation][self.__frame // self.__speed].copy()

            self.__prev = self.rect.bottomleft
            self.rect = self.image.get_rect()
            self.rect.bottomleft = self.__prev

            # mg turret
            self.__temp = pygame.transform.rotate(self.__mg, self.__angle)
            self.__temp_rect = self.__temp.get_rect()
            self.__temp_rect.center = ((46, self.image.get_height() - 59), (48, 100))[self.__animation == 3]
            self.image.blit(self.__temp, self.__temp_rect)

            # flashed red while hurt
            if self.__hurt > 0:
                if self.__hurt % 5 == 0:
                    self.image.fill((200, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
                self.__hurt -= 1

            self.__frame += 1

            # cycles animation frames
            if self.__frame >= len(self.__sprites[self.__animation]) * self.__speed:
                self.__frame = 0
            # resets horizontal velocity and __shooting_cannon after the animation is over
            self.__vx = 0
            if self.__shooting_cannon and self.__frame == 0:
                self.__shooting_cannon = False