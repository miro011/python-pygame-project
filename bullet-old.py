import pygame
import enemy

class Bullet():

    ######################################################################
    # CONSTRUCTOR
    
    # x and y should be the coordinates of the ship (at least in the base game)
    def __init__(self, screen, spritesDict, x, y):
        self.screen = screen
        self.spritesDict = spritesDict
        
        self.image = pygame.image.load("./media/images/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        self.speedX = 0
        self.speedY = -10

        self.shouldDelete = False


    ######################################################################
    # OPTIONAL

    def update_location(self):
        newRect = self.rect.move(self.speedX, self.speedY)
        if newRect.collidelist(self.spritesDict["walls"]) == -1:
            self.rect = newRect
        else:
            self.shouldDelete = True
            return

        enemyIndexesHitArr = self.rect.collidelistall(self.spritesDict["enemies"])
        for enemyIndex in enemyIndexesHitArr:
            self.spritesDict["enemies"][enemyIndex].shouldDelete = True
            self.spritesDict["enemies"].append(enemy.Enemy(self.screen, self.spritesDict))

    def blit(self):
        self.screen.blit(self.image, self.rect)