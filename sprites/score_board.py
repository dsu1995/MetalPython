import pygame


class ScoreBoard(pygame.sprite.Sprite):
    '''scoreboard sprite'''

    def __init__(self, player, tank=None):
        '''initializer method with the player and the tank as parameters'''
        pygame.sprite.Sprite.__init__(self)

        # loads background and font
        self.__background = pygame.image.load('images\\scoreboard.png').convert_alpha()
        self.__font = pygame.font.Font('fonts\\Square.ttf', 20)
        self.__player = player
        self.__tank = tank
        self.rect = pygame.Rect(0, 0, 1, 1)

    def update(self, current_player):
        '''update method'''
        self.image = self.__background.copy()
        # blits labels
        self.image.blit(self.__font.render(
            ('life     ', 'armour')[current_player == self.__tank] + ' ' * 30 + 'ammo' + ' ' * 7 +
            ('grenade', 'cannon')[current_player == self.__tank], True, (223, 221, 209)), (5, 5))
        # draws health bar frame
        pygame.draw.rect(self.image, (0, 0, 0), (4, 24, 202, 22), 1)
        # draws health bar
        pygame.draw.rect(self.image, ((75, 196, 81), (255, 130, 37))[current_player == self.__tank],
                         (5, 25, current_player.get_health(), 20))
        # blits ammo and grenade count
        if type(current_player.get_ammo()) != int:
            self.__ammo = current_player.get_ammo()
        else:
            self.__ammo = str(current_player.get_ammo())
        self.image.blit(self.__font.render(self.__ammo.center(3) + ' ' * 15 + str(current_player.get_grenades()), True,
                                           (241, 125, 4)), (230, 25))