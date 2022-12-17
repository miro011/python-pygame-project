import pygame
import enemy

class Bullet():

    ######################################################################
    # CONSTRUCTOR
    
    # x and y should be the coordinates of the ship (at least in the base game)
    def __init__(self, screen, spritesDict):
        self.screen = screen
        self.spritesDict = spritesDict

        # https://www.reddit.com/r/pygame/comments/rnskta/comment/hpx5swn/?utm_source=share&utm_medium=web2x&context=3
        droneRect = self.spritesDict["drone"][0].rect
        self.startV = pygame.Vector2(droneRect.center[0], droneRect.bottom)
        self.finalV = pygame.Vector2(self.spritesDict["pointer"][0].rect.center)
        
        self.image = pygame.image.load("./media/images/bullet.png")
        self.rect = self.image.get_rect()

        self.speed = 20

        self.counter = 0
        self.numUpdates = int(self.startV.distance_to(self.finalV) / self.speed) # number of updates required, in order to get uniform speed

        self.shouldDelete = False


    ######################################################################
    # OPTIONAL

    def update_location(self):
        progress = self.counter / self.numUpdates
        #self.rect = self.image.get_rect()
        self.rect.center = self.startV.lerp(self.finalV, progress)
        self.counter += 1

        if progress == 1: self.shouldDelete = True

        '''enemyIndexesHitArr = self.rect.collidelistall(self.spritesDict["enemies"])
        for enemyIndex in enemyIndexesHitArr:
            self.spritesDict["enemies"][enemyIndex].shouldDelete = True
            self.spritesDict["enemies"].append(enemy.Enemy(self.screen, self.spritesDict))'''

    def blit(self):
        self.screen.blit(self.image, self.rect)