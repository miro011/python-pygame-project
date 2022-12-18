import pygame
import globals
import random
import repeattimer

class Enemy():

    ######################################################################
    # CONSTRUCTOR

    def __init__(self, screen, spritesDict):
        self.screen = screen
        self.spritesDict = spritesDict

        self.startSide = random.randint(0,1) # 0 left / 1 right

        self.nextImgNum = 0
        self.image = pygame.image.load(f"./media/images/enemy/0.gif")
        self.rect = self.image.get_rect()
        leftXCoord = 0 if self.startSide == 0 else globals.DISPLAY_WIDTH - (self.image.get_width()/2)
        topYCoord = random.randint(0, globals.DISPLAY_HEIGHT - globals.DIST_FROM_BOTTOM - self.image.get_height())
        self.rect.move_ip(leftXCoord, topYCoord)

        self.nextImageTimer = repeattimer.RepeatTimer(0.1, self.set_image)
        self.nextImageTimer.daemon = True
        self.nextImageTimer.start()

        self.speed = 5

        self.shouldDelete = False

    ######################################################################
    # OPTIONAL

    def update_location(self):
        if "player" not in self.spritesDict: return # when the game over menu is toggled, sprites.py continues looping through the rest of the enemies

        startV = pygame.Vector2(self.rect.center)
        finalV = pygame.Vector2(self.spritesDict["player"][0].rect.center)
        numUpdates = int(startV.distance_to(finalV) / self.speed)
        if numUpdates < 10: # using this to detect collision with player and purposefully a bit loose so player can avoid
            self.spritesDict["over_menu"][0].toggle_menu()
            return
        progress = 1 / numUpdates
        self.rect.center = startV.lerp(finalV, progress)

        if self.rect.collidelist(self.spritesDict["bullets"]) != -1:
            self.nextImageTimer.cancel()
            self.shouldDelete = True
            self.respawn()
            
    def blit(self):
        self.screen.blit(self.image, self.rect)

    ######################################################################
    # RESPAWN

    def respawn(self):
        result = random.randint(0, globals.ENEMY_SPLIT_CHANCE)
        shouldSplit = True if 0 <= result <= globals.ENEMY_SPLIT_CHANCE else False
        numOfNewSpawns = 2 if shouldSplit else 1
        for i in range(numOfNewSpawns):
            self.spritesDict["enemies"].append(Enemy(self.screen, self.spritesDict))


    ######################################################################
    # OTHER

    def set_image(self):
        while True:
            try:
                self.image = pygame.image.load(f"./media/images/enemy/{self.nextImgNum}.gif")
                break
            except:
                self.nextImgNum = 0

        self.nextImgNum += 1
        
