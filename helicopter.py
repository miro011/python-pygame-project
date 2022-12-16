import pygame
import globals

class Helicopter():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen, spritesDict):
        self.screen = screen
        self.spritesDict = spritesDict

        self.imageCount = 0
        self.image = None
        self.rect = None

        self.set_image()

    ######################################################################
    # OPTIONAL

    def update_location(self):
        self.set_image()

    def blit(self):
        self.screen.blit(self.image, self.rect)

    ######################################################################
    # OTHER

    def set_image(self):
        while True:
            try:
                self.image = pygame.image.load(f"./media/images/helicopter/{self.imageCount}.gif")
                break
            except:
                self.imageCount = 0

        self.imageCount += 1

        self.rect = self.image.get_rect()
        self.rect.move_ip(20, 20)