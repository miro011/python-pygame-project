import pygame
import globals

class Wall():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, description):
        self.description = description

        # the 100 is to make the walls go outside of the window, so that it can detect collisions
        self.rect = None
        if description == "top":
            self.rect = pygame.Rect(0, -100, globals.DISPLAY_WIDTH, 100) # left, top, width, height
        elif description == "bottom":
            self.rect = pygame.Rect(0, globals.DISPLAY_HEIGHT, globals.DISPLAY_WIDTH, 100)
        elif description == "left":
            self.rect = pygame.Rect(-100, 0, 100, globals.DISPLAY_HEIGHT)
        elif description == "right":
            self.rect = pygame.Rect(globals.DISPLAY_WIDTH, 0, 100, globals.DISPLAY_HEIGHT)
        else:
            self.rect = pygame.Rect(0, 0, 0, 0)