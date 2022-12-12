import pygame
import globals
import bullet

class Player():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen, spritesDict):
        self.screen = screen
        self.spritesDict = spritesDict
        
        self.image = pygame.image.load("./media/images/spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = (globals.DISPLAY_WIDTH/2, globals.DISPLAY_HEIGHT-40)
        
        self.speedX = 3
        self.speedY = 3

        self.curSpeedX = 0
        self.curSpeedY = 0


    ######################################################################
    # OPTIONAL
        
    def user_input(self, eventsQueueArr):
        for event in eventsQueueArr:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.curSpeedX = self.speedX
                if event.key == pygame.K_LEFT:
                    self.curSpeedX = self.speedX * -1
                if event.key == pygame.K_DOWN:
                    self.curSpeedY = self.speedY
                if event.key == pygame.K_UP:
                    self.curSpeedY = self.speedY * -1
                if event.key == pygame.K_SPACE:
                    self.shoot()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    self.curSpeedX = 0
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    self.curSpeedY = 0


    def update_location(self):
        newRect = self.rect.move(self.curSpeedX, self.curSpeedY)
        if newRect.collidelist(self.spritesDict["walls"]) == -1:
            self.rect = newRect
    
    def blit(self):
        self.screen.blit(self.image, self.rect)


    ######################################################################
    # SPECIAL

    def shoot(self):
        self.spritesDict["bullets"].append(bullet.Bullet(self.screen, self.spritesDict, self.rect.center[0], self.rect.top))
