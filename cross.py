import pygame
import globals
import random

class Cross():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen, spritesDict):
        self.screen = screen
        self.spritesDict = spritesDict
        
        self.image = pygame.image.load("./media/images/cross.png")

        bgSortedXCoords = self.spritesDict["background"][0].get_x_sorted_coords()
        leftXCoord = bgSortedXCoords[0] if self.spritesDict["background"][0].speedX > 0 else bgSortedXCoords[-1] - self.image.get_width()
        topYCoord = random.randint(
            self.spritesDict["player"][0].jumpMaxHeight, 
            globals.DISPLAY_HEIGHT - globals.DIST_FROM_BOTTOM - self.image.get_height()
        )

        self.rect = self.image.get_rect()
        self.rect.move_ip(leftXCoord, topYCoord)
        
        self.speedX = self.spritesDict["background"][0].speedX
        self.speedY = 0

        self.shouldDelete = False

    ######################################################################
    # OPTIONAL

    def update_location(self):
        self.rect = self.rect.move(self.speedX, self.speedY)

        stillOnBackground = True if self.rect.collidelist(self.spritesDict["background"][0].rectsArr) >= 0 else False
        collidedWithPlayer = True if self.rect.collidelist(self.spritesDict["player"]) >= 0 else False

        if not stillOnBackground or collidedWithPlayer:
            self.shouldDelete = True
            self.spritesDict["cross"].append(Cross(self.screen, self.spritesDict))

    def blit(self):
        self.screen.blit(self.image, self.rect)