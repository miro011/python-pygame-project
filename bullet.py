import pygame
import enemy

class Bullet():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen, spritesDict):
        self.screen = screen
        self.spritesDict = spritesDict

        self.image = pygame.image.load("./media/images/bullet.png")
        self.rect = self.image.get_rect()

        self.startV = None
        self.finalV = None
        self.set_vector_points()
        
        self.speed = 20

        self.counter = 0
        self.numUpdates = int(self.startV.distance_to(self.finalV) / self.speed) # number of updates required, in order to get uniform speed (aka num times screen has to refresh)

        self.shouldDelete = False


    ######################################################################
    # OPTIONAL

    def update_location(self):
        progress = self.counter / self.numUpdates
        self.rect.center = self.startV.lerp(self.finalV, progress)
        self.counter += 1

        if progress == 1:
            self.shouldDelete = True
            self.spritesDict["drone"][0].isShooting = False

    def blit(self):
        self.screen.blit(self.image, self.rect)

    ######################################################################
    # OTHER

    def set_vector_points(self):
        droneRect = self.spritesDict["drone"][0].rect
        self.startV = pygame.Vector2(droneRect.center[0], droneRect.bottom)

        pointerRect = self.spritesDict["pointer"][0].rect
        self.finalV = pygame.Vector2(pointerRect.center)