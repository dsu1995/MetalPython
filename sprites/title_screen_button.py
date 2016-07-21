import pygame


class TitleScreenButton(pygame.sprite.Sprite):
    '''button class'''
    # sound
    __press = pygame.mixer.Sound('sounds\\button.wav')

    def __init__(self, num):
        '''initializer class with the button number'''
        pygame.sprite.Sprite.__init__(self)
        # loads font and text
        self.__font = pygame.font.Font('fonts\\Square.ttf', 30)
        self.__text = ('START', 'CONTROLS', 'QUIT', 'BACK', 'RESUME', 'RETURN TO TITLE SCREEN')[num]
        # loads image and rect
        self.image = self.__font.render(self.__text, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = ((160, 200), (160, 250), (160, 300), (280, 440), (320, 200), (320, 280))[num]

        self.__collided = False

    def get_pressed(self):
        '''returns whether the button is being pressed'''
        self.__collided = self.rect.collidepoint(pygame.mouse.get_pos())
        if self.__collided and pygame.mouse.get_pressed()[0]:
            TitleScreenButton.__press.play()
            return True

    def update(self):
        '''update method'''
        # turns red when mouse if hovering over it
        self.image = self.__font.render(self.__text, True, ((255, 255, 255), (255, 0, 0))[self.__collided])