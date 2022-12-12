import pygame
import globals

class Pointer():

    ######################################################################
    # CONSTRUCTOR
    
    # x and y should be the coordinates of the ship (at least in the base game)
    def __init__(self, screen, spritesDict):
        self.screen = screen
        self.spritesDict = spritesDict
        
        self.image = pygame.image.load("./media/images/pointer.png")
        self.rect = self.image.get_rect()

    def blit(self):
        self.screen.blit(self.image, self.rect)

    ######################################################################
    # OPTIONAL

    def update_location(self):
        mouseXyPos = pygame.mouse.get_pos()
        self.rect.center = mouseXyPos