import pygame
import globals
import random

class Enemy():

    ######################################################################
    # CONSTRUCTOR

    def __init__(self, screen, spritesDict):
        self.screen = screen
        self.spritesDict = spritesDict
        
        self.image = pygame.image.load("./media/images/ufo.png")
        self.rect = self.image.get_rect()
        # +/- 1 is so that they don't collide with a wall on spawn
        x = random.randint(0 + (self.image.get_width() / 2) + 1, globals.DISPLAY_WIDTH - (self.image.get_width() / 2) - 1)
        y = random.randint(0 + (self.image.get_height() / 2) + 1, globals.DISPLAY_HEIGHT - (self.image.get_height() / 2) - 1)
        self.rect.center = (x,y)


        self.speedX = 1
        self.speedY = 0

        self.shouldDelete = False

    ######################################################################
    # OPTIONAL

    def update_location(self):
        newRect = self.rect.move(self.speedX, self.speedY)

        wallIndexesHitArr = newRect.collidelistall(self.spritesDict["walls"])
        if wallIndexesHitArr:
            for wallIndex in wallIndexesHitArr:
                wallDescription = self.spritesDict["walls"][wallIndex].description
                if wallDescription in ["top", "bottom"]:
                    self.shouldDelete = True
                    return
                elif wallDescription in ["left", "right"]:
                    self.speedX *= -1
                    self.rect = self.rect.move(0, 30)
        else:
            self.rect = newRect
            
    def blit(self):
        self.screen.blit(self.image, self.rect)
        
