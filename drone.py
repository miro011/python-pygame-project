import pygame
import globals

class Drone():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen, spritesDict):
        self.screen = screen
        self.spritesDict = spritesDict

        self.nextImgNum = 0
        self.image = pygame.image.load(f"./media/images/drone/{self.nextImgNum}.gif")
        self.rect = self.image.get_rect()

        self.nextImageTimer = globals.RepeatTimer(0.07, self.set_image)
        self.nextImageTimer.start()

    ######################################################################
    # OPTIONAL

    def update_location(self):
        newRect = self.rect.copy()
        newRect.center = (self.spritesDict["player"][0].rect.center[0], self.image.get_height()/2)
        if newRect.collidelist(self.spritesDict["walls"]) == -1:
            self.rect = newRect

    def blit(self):
        self.screen.blit(self.image, self.rect)

    ######################################################################
    # OTHER

    def set_image(self):
        while True:
            try:
                self.image = pygame.image.load(f"./media/images/drone/{self.nextImgNum}.gif")
                break
            except:
                self.nextImgNum = 0

        self.nextImgNum += 1