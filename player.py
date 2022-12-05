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
        
        self.x = (globals.DISPLAY_WIDTH / 2) - (self.get_width() / 2)
        self.y = globals.DISPLAY_HEIGHT - (self.get_height() + 30) # 30 being the distance from the bottom
        
        self.speedX = 3
        self.speedY = 0

        self.curSpeedX = 0
        self.curSpeedY = 0


    ######################################################################
    # GETTERS

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()


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
        oldX = self.x
        oldY = self.y

        self.x += self.curSpeedX
        self.y += self.curSpeedY

        if globals.collision(self, self.spritesDict["walls"]):
            self.x = oldX
            self.y = oldY

    
    def blit(self):
        self.screen.blit(self.image, (self.x, self.y))


    ######################################################################
    # SPECIAL

    def shoot(self):
        self.spritesDict["bullets"].append(bullet.Bullet(self.screen, self.spritesDict, self.x, self.y))
