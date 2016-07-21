import os

import pygame


class Player(pygame.sprite.Sprite):
    '''player sprite'''

    def __init__(self, prev_player=None):
        '''initializer method with the player from the previous level as a parameter, if applicable, so that attributes can be inherited'''
        pygame.sprite.Sprite.__init__(self)

        # loads all animations into nested lists
        self.__sprites = [[[[pygame.image.load(
            'images\\player\\' + str(orientation) + '\\' + str(weapon) + '\\' + str(animation) + '\\' + str(
                frame) + '.png').convert_alpha() for frame in range(
            len(os.listdir('images\\player\\' + str(orientation) + '\\' + str(weapon) + '\\' + str(animation))))] for
                            animation in range(6)] for weapon in range(2)] for orientation in range(2)]

        # initializes animation
        self.__orientation = 0
        self.__animation = 0
        self.__frame = 0
        self.__speed = 15

        if prev_player:
            self.__weapon = prev_player.get_weapon()
        else:
            self.__weapon = 1

        # creates image and rect attributes
        self.image = self.__sprites[self.__orientation][self.__weapon][self.__animation][self.__frame]
        self.rect = self.image.get_rect()

        if prev_player:
            self.rect.bottomleft = (50, 432)
        else:
            self.rect.midtop = (320, 0)

        # previous height, used when landing on platforms
        self.__prev_bottom = self.rect.bottom

        # initializes movement
        self.__vx = 0
        self.__vy = 0
        self.__falling = not bool(prev_player)
        self.__shooting = False

        # delay for shooting pistol
        self.__shotdelay = 0

        # used for scoreboard
        if prev_player:
            self.__health = prev_player.get_health()
            self.__ammo = prev_player.get_ammo()
            self.__grenades = prev_player.get_grenades()
        else:
            self.__health = 200
            self.__ammo = 100
            self.__grenades = 10

        self.__dead = False
        self.__hurt = 0

        # sound
        self.__mg_sound = pygame.mixer.Sound('sounds\\mg.wav')
        self.__pistol_sound = pygame.mixer.Sound('sounds\\pistol.wav')
        self.__death = pygame.mixer.Sound('sounds\\marco.wav')

    def update(self, *args):
        '''update method'''
        # changes weapon to pistol once the mg is out of ammo
        if self.__ammo <= 0:
            self.__weapon = 0
        # kills player once health is 0
        if self.__health <= 0 and self.__animation != 6:
            self.__death.play()
            self.__animation = 6
            self.__weapon = 0
            self.__frame = 0

        # previous position for landing on platforms
        self.__prev_bottom = self.rect.bottom

        # falling
        if self.__falling:
            self.__vy += 1.1
            self.rect.bottom += self.__vy

            # death animation
        if self.__animation == 6:
            # changes picture every 3 frames
            if self.__frame < len(self.__sprites[self.__orientation][self.__weapon][self.__animation]) * 3:
                self.image = self.__sprites[self.__orientation][self.__weapon][self.__animation][self.__frame // 3]

            # recenters image
            if self.__orientation:
                self.__prev = self.rect.bottomright
                self.rect = self.image.get_rect()
                self.rect.bottomright = self.__prev
            else:
                self.__prev = self.rect.bottomleft
                self.rect = self.image.get_rect()
                self.rect.bottomleft = self.__prev

            self.__frame += 1
            if self.__frame >= 100:
                self.__dead = True

        # when alive
        else:
            # horizontal movement
            self.rect.left += self.__vx * 8

            # changes orientation
            if self.__vx > 0:
                self.__orientation = 0
            elif self.__vx < 0:
                self.__orientation = 1

            # prevents the player from moving off the sides of the level
            if self.rect.left <= 0:
                self.rect.left = 0

                # animation
            # shooting
            if self.__shooting:
                if self.__animation not in [3, 4, 5]:
                    self.__frame = 0
                if not self.__weapon:
                    self.__speed = 3
                else:
                    self.__speed = 1
                # while jumping
                if self.__vy:
                    self.__animation = 5
                # while running
                elif self.__vx:
                    self.__animation = 4
                # while standing still
                else:
                    self.__animation = 3
                    # still
            elif self.__animation and not self.__vx and not self.__vy:
                self.__frame = 0
                self.__speed = 15
                self.__animation = 0
                # running
            elif self.__animation != 1 and self.__vx and not self.__vy:
                self.__frame = 0
                self.__speed = 2
                self.__animation = 1
            # jumping
            elif self.__animation != 2 and self.__vy:
                self.__frame = 0
                self.__speed = 1
                self.__animation = 2

            # updates animation
            self.image = self.__sprites[self.__orientation][self.__weapon][self.__animation][
                self.__frame // self.__speed].copy()

            # flashes red when hurt every 5 frames
            if self.__hurt > 0:
                if self.__hurt % 5 == 0:
                    self.image.fill((200, 0, 0), special_flags=pygame.BLEND_RGB_MULT)
                self.__hurt -= 1

            # recenters image
            if self.__orientation:
                self.__prev = self.rect.bottomright
                self.rect = self.image.get_rect()
                self.rect.bottomright = self.__prev
            else:
                self.__prev = self.rect.bottomleft
                self.rect = self.image.get_rect()
                self.rect.bottomleft = self.__prev

            self.__frame += 1
            # cycles frame count
            if self.__frame >= len(self.__sprites[self.__orientation][self.__weapon][self.__animation]) * self.__speed:
                self.__frame = 0
            # resets horizontal velocity
            self.__vx = 0
            # stops shooting animation from looping
            if self.__shooting and self.__frame == 0:
                self.__shooting = False

    def pickup(self):
        '''called when the user picks up ammo'''
        self.__weapon = 1
        self.__ammo += 100

    def jump(self):
        '''makes player jump'''
        if not self.__falling and self.__animation != 6:
            self.rect.top -= 1
            self.__vy = -17
            self.__falling = True

    def move(self, vx):
        '''moves player vx pixels'''
        self.__vx = vx

    def collide_wall(self, wall, level=0):
        '''stops player when hitting a wall'''
        if level:
            self.rect.right = wall.rect.left
        else:
            self.rect.left = wall.rect.right
        self.__vx = 0

    def fall(self):
        '''called when the player is not colliding with the ground'''
        self.__falling = True

    def land(self, platform):
        '''called when landing on a platform'''
        # checks if the player walked off the edge and touches another higher platform
        if not self.__falling and self.rect.bottom > platform + 1:
            self.fall()
            # checks if player lands on top of the platform
        elif self.__prev_bottom <= platform:
            self.rect.bottom = platform + 1
            self.__vy = 0
            self.__falling = False

    def shoot(self):
        '''starts shooting, returns either true or the bullet number, depending on the current weapon'''
        self.__shooting = True
        # if using a pistol, returns True when the pistol is shooting
        if not self.__weapon and self.__frame == 1:
            self.__pistol_sound.play()
            return True
        # if using a mg, returns the bullet number used in animating the bullet, and decrements ammo count
        elif self.__weapon == 1:
            self.__ammo -= 1
            self.__mg_sound.play()
            return self.__frame // self.__speed

    def throw_grenade(self):
        '''reduces grenade count'''
        self.__grenades -= 1

    def get_health(self):
        '''returns the amount of health'''
        return self.__health

    def hurt(self, damage):
        '''lowers health and starts flashing'''
        if not self.__hurt:
            self.__health -= damage
            self.__hurt = 30

    def get_ammo(self):
        '''returns the ammount of ammo left'''
        if not self.__weapon:
            return u'∞'
        else:
            return self.__ammo

    def get_grenades(self):
        '''returns the amount of grenades left'''
        return self.__grenades

    def get_direction(self):
        '''returns the direction the player is facing'''
        return self.__orientation

    def get_weapon(self):
        '''returns the current weapon'''
        return self.__weapon

    def get_dying(self):
        '''returns whether the player is in the death animation'''
        if self.__dead:
            return 2
        return self.__animation == 6

    def respawn(self, tank):
        '''respawns player once the tank is destoryed'''
        if not self.alive():
            # repositions player
            self.rect.midbottom = tank.rect.midtop
            # resets attributes
            self.__orientation = 0
            self.__prev_bottom = self.rect.bottom
            self.__vx = 0
            self.__vy = -10
            self.__falling = True
            self.__shooting = False
            self.__shotdelay = 0