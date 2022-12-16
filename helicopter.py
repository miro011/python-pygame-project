import pygame
import globals

class Helicopter():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen, spritesDict):
        self.screen = screen
        self.spritesDict = spritesDict

        self.image = None
        self.rect = None

        self.nextImgNum = 0
        self.set_image()

        self.nextImageTimer = globals.RepeatTimer(0.04, self.set_image)
        self.nextImageTimer.start()

    ######################################################################
    # OPTIONAL

    def blit(self):
        self.screen.blit(self.image, self.rect)

    ######################################################################
    # OTHER

    def set_image(self):
        while True:
            try:
                self.image = pygame.image.load(f"./media/images/helicopter/{self.nextImgNum}.gif")
                break
            except:
                self.nextImgNum = 0

        self.nextImgNum += 1

        self.rect = self.image.get_rect()
        self.rect.move_ip(20, 20)