import pygame

class Background():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen):
        self.screen = screen

        self.image = pygame.image.load("./media/images/stars.png")
        self.rect = self.image.get_rect()

    ######################################################################
    # OPTIONAL

    def blit(self):
        self.screen.blit(self.image, self.rect)