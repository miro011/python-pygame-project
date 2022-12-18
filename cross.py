import pygame
import globals
import random
import enemy

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

        if collidedWithPlayer:
            self.kill_enemies()
            self.respawn()
        if not stillOnBackground:
            self.respawn()
            

    def blit(self):
        self.screen.blit(self.image, self.rect)

    ######################################################################
    # OTHER

    def respawn(self):
        self.shouldDelete = True
        self.spritesDict["cross"].append(Cross(self.screen, self.spritesDict))

    def kill_enemies(self):
        for enemySprite in self.spritesDict["enemies"]:
            enemySprite.nextImageTimer.cancel()
            enemySprite.shouldDelete = True

        for i in range(globals.ENEMY_DF_NUMBER):
            self.spritesDict["enemies"].append(enemy.Enemy(self.screen, self.spritesDict))