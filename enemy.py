import pygame
import globals
import random
import repeattimer

class Enemy():

    ######################################################################
    # CONSTRUCTOR

    def __init__(self, screen, regulator, spritesDict, shouldSpanwOnTheRight=None):
        self.screen = screen
        self.regulator = regulator
        self.spritesDict = spritesDict

        self.startSide = self.get_start_side(shouldSpanwOnTheRight)


        self.image = pygame.image.load(f"./media/images/enemy/0.gif")
        self.rect = self.image.get_rect()
        self.set_rect_location()

        self.nextImgNum = 0
        self.nextImageTimer = self.regulator.get_new_repeat_timer(0.1, self.set_image)

        self.offScreenSpeed = 5 if self.startSide == -1 else -5
        self.baseVectorSpeed = 2

        self.shouldDelete = False

    ######################################################################
    # OPTIONAL

    def update_location(self):
        if "enemies" not in self.spritesDict: return # when the game-over menu is toggled, sprites.py continues looping through the rest of the enemies

        if self.is_off_screen():
            self.rect = self.rect.move(self.offScreenSpeed, 0)
        else:
            vectorSpeed = self.get_vector_speed()

            # calculate movement, collisions etc.
            startV = pygame.Vector2(self.rect.center)
            finalV = pygame.Vector2(self.spritesDict["player"][0].rect.center)
            numUpdates = int(startV.distance_to(finalV) / vectorSpeed)

            if numUpdates < 10: # using this to detect collision with player so it can be looser (lower = looser aka less likely to collide)
                self.spritesDict["over_menu"][0].toggle_menu()
                return

            progress = 1 / numUpdates
            self.rect.center = startV.lerp(finalV, progress)

        # collision with bullet
        if self.rect.collidelist(self.spritesDict["bullets"]) != -1:
            self.spritesDict["hud"][0].kills += 1
            self.respawn()
            
    def blit(self):
        if "enemies" not in self.spritesDict: return
        self.screen.blit(self.image, self.rect)

    ######################################################################
    # SPECIAL

    def respawn(self, shouldSpanwOnTheRight=None):
        self.nextImageTimer.cancel()
        self.shouldDelete = True
        self.spritesDict["enemies"].append(Enemy(self.screen, self.regulator, self.spritesDict, shouldSpanwOnTheRight))


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

    def get_start_side(self, shouldSpanwOnTheRight):
        if not shouldSpanwOnTheRight:
            shouldSpanwOnTheRight = self.regulator.calculate_chancery(globals.ENEMY_SPAWN_ON_THE_RIGHT_CHANCE)
        return 1 if shouldSpanwOnTheRight else -1 # -1 left / 1 right

    def set_rect_location(self):
        randomXCoordOnScreen = random.randint(0, globals.DISPLAY_WIDTH)

        leftXCoord = None
        if self.startSide == -1:
            leftXCoord = 0 - randomXCoordOnScreen # spanw the enemy outside the screen on the left
        else:
            leftXCoord = globals.DISPLAY_WIDTH + randomXCoordOnScreen # spawn outside the screen on the right

        topYCoord = random.randint(0, globals.DISPLAY_HEIGHT - globals.DIST_FROM_BOTTOM - self.image.get_height())

        self.rect.move_ip(leftXCoord, topYCoord)

    def is_off_screen(self):
        if self.rect.center[0] < 0 or self.rect.center[0] > globals.DISPLAY_WIDTH:
            return True
        else:
            return False

    # makes it so that the enemy faster when going towards player
    def get_vector_speed(self):
        vectorSpeed = self.baseVectorSpeed
        playerSprite = self.spritesDict["player"][0]

        if playerSprite.direction == 1 and self.rect.left > playerSprite.rect.left:
            vectorSpeed *= 3
        elif playerSprite.direction == -1 and self.rect.right < playerSprite.rect.right:
            vectorSpeed *= 3

        return vectorSpeed