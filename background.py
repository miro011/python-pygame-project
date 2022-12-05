import pygame

class Background():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen):
        self.screen = screen

        self.image = pygame.image.load("./media/images/stars.png")
        self.x = 0
        self.y = 0

    ######################################################################
    # OPTIONAL

    def blit(self):
        self.screen.blit(self.image, (self.x, self.y))