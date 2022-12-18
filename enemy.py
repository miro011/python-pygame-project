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

        shouldSpanwOnTheRight = self.calculate_chancery(globals.ENEMY_SPAWN_ON_THE_RIGHT_CHANCE)
        self.startSide = 1 if shouldSpanwOnTheRight else -1 # -1 left / 1 right


        self.image = pygame.image.load(f"./media/images/enemy/0.gif")
        self.rect = self.image.get_rect()
        leftXCoord = random.randint(0, globals.DISPLAY_WIDTH)
        leftXCoord = 0 - leftXCoord if self.startSide == -1 else globals.DISPLAY_WIDTH + leftXCoord # spanwn outside the screen
        topYCoord = random.randint(0, globals.DISPLAY_HEIGHT - globals.DIST_FROM_BOTTOM - self.image.get_height())
        self.rect.move_ip(leftXCoord, topYCoord)

        self.nextImgNum = 0
        self.nextImageTimer = repeattimer.RepeatTimer(0.1, self.set_image)
        self.nextImageTimer.daemon = True
        self.nextImageTimer.start()

        self.offScreenSpeed = 5 if self.startSide == -1 else -5
        self.baseVectorSpeed = 2

        self.shouldDelete = False

    ######################################################################
    # OPTIONAL

    def update_location(self):
        if "player" not in self.spritesDict: return # when the game over menu is toggled, sprites.py continues looping through the rest of the enemies

        # move normally
        if self.rect.center[0] < 0 or self.rect.center[0] > globals.DISPLAY_WIDTH:
            self.rect = self.rect.move(self.offScreenSpeed, 0)
        else:
            speed = self.baseVectorSpeed

            # make it so that the enemy is slower when following player and faster when going towards player
            playerDir = self.spritesDict["player"][0].direcion
            playerRect = self.spritesDict["player"][0].rect
            if (self.rect.left > playerRect.right and playerDir == 1) or (self.rect.right < playerRect.left and playerDir == -1):
                speed *= 3

            # calculate movement, collisions etc.
            startV = pygame.Vector2(self.rect.center)
            finalV = pygame.Vector2(self.spritesDict["player"][0].rect.center)
            numUpdates = int(startV.distance_to(finalV) / speed)
            if numUpdates < 10: # using this to detect collision with player and purposefully a bit loose so player can somewhat avoid
                self.spritesDict["over_menu"][0].toggle_menu()
                return
            progress = 1 / numUpdates
            self.rect.center = startV.lerp(finalV, progress)

        if self.rect.collidelist(self.spritesDict["bullets"]) != -1:
            self.respawn()
            
    def blit(self):
        self.screen.blit(self.image, self.rect)

    ######################################################################
    # RESPAWN

    def respawn(self):
        self.nextImageTimer.cancel()
        self.shouldDelete = True

        globals.ENEMY_SPLIT_CHANCE += 1

        shouldSplit = self.calculate_chancery(globals.ENEMY_SPLIT_CHANCE)
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

    # returns true or false - it relates to the name of whatever variable is plugged into "percentValue"
    # for example: chanceToDie = 70 . If this function retruns true it means "yes, you will die"
    def calculate_chancery(self, percentValue):
        # have to do this because it seems it will generate more small numbers when it is 1,100
        percentValue = int(percentValue/10)
        result = random.randint(0, 10)
        return True if 0 <= result <= percentValue else False