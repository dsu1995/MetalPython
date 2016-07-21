import pygame


class Background(pygame.sprite.Sprite):
    """
    scrolling background sprite
    """

    IMAGES = ['images/bkgd.png', 'images/bossbkgd2.png']

    def __init__(self, player, level=0):
        """
        initializer method with player and level number as parameters
        """
        super(Background, self).__init__()

        # loads image and rect
        self.image = pygame.image.load(Background.IMAGES[level]).convert()
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 0
        # adjusts the screen centering
        self.adjustment = 100 + player.rect.width

    def update(self, player):
        """
        updates background with respect to the players
        """
        if player.get_direction():
            if self.adjustment <= 150:
                self.adjustment += 5
            player_side = player.rect.right
        else:
            if self.adjustment >= -150:
                self.adjustment -= 5
            player_side = player.rect.left

        # calculates position of the background
        self.rect.left = 320 - player_side + self.adjustment
        # stops scrolling once it reaches either side of the screen
        if self.rect.left > 0:
            self.rect.left = 0
        elif self.rect.right < 640:
            self.rect.right = 640