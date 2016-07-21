import pygame


class Platform(pygame.sprite.Sprite):
    '''platform sprite'''

    def __init__(self, dimension):
        '''platform sprite kept for collision detection only'''
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(*dimension)