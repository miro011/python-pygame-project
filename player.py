import pygame
import globals
import repeattimer

class Player():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen, spritesDict):
        self.screen = screen
        self.spritesDict = spritesDict
        
        self.image = pygame.image.load(f"./media/images/player/0.gif")
        self.rect = self.image.get_rect()
        self.rect.center = (globals.DISPLAY_WIDTH/2, globals.DISPLAY_HEIGHT - (self.image.get_height()/2) - globals.DIST_FROM_BOTTOM)

        self.nextImgNum = 0
        self.nextImageTimerDfDelay = 0.05
        self.nextImageTimer = repeattimer.RepeatTimer(self.nextImageTimerDfDelay, self.set_image)
        self.nextImageTimer.daemon = True # will be terminated abruptly by the Python process once all other non-daemon threads are finished (in this case none). Otherwise it hangs.
        self.nextImageTimer.start()

        self.speedX = 8
        self.speedY = 15 # jump duration

        self.curSpeedX = 0
        self.curSpeedY = 0

        self.jumpInProg = False
        self.jumpMaxHeight = self.spritesDict["drone"][0].rect.bottom

        self.direcion = 1 # 1 = forward / -1 = backward

        self.kills = 0
        self.distanceTravelled = 0 # +60/s (going forward) | Target: 120x60=7200 = 10 miles | Calc Remaining: 10 - (10 * (x/7200))
        self.numEnemiesToEachSide = [0, 0] 


    ######################################################################
    # OPTIONAL
        
    def user_input(self, eventsQueueArr):
        for event in eventsQueueArr:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.curSpeedX = self.speedX
                    self.nextImageTimer.interval = self.nextImageTimerDfDelay / 1.5 if self.direcion == 1 else self.nextImageTimerDfDelay * 1.5 # make the animation faster/slower
                if event.key == pygame.K_LEFT:
                    self.curSpeedX = self.speedX * -1
                    self.nextImageTimer.interval = self.nextImageTimerDfDelay * 1.5 if self.direcion == 1 else self.nextImageTimerDfDelay / 1.5 # make the animation faster/slower
                if event.key == pygame.K_UP:
                    self.init_jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    self.curSpeedX = 0
                    self.nextImageTimer.interval = self.nextImageTimerDfDelay
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3: # 1-left 2-middle, 3-right, 4-scrollup, 5-scrolldown
                    self.toggle_direction()



    def update_location(self):
        self.distanceTravelled = self.distanceTravelled + 1 if self.direcion == 1 else self.distanceTravelled - 1
        if self.distanceTravelled >= globals.DISTANCE_TO_RUN:
            self.spritesDict["victory_menu"][0].toggle_menu()
            return

        newRect = self.rect.move(self.curSpeedX, self.curSpeedY)
        if newRect.collidelist(self.spritesDict["walls"]) == -1:
            self.rect = newRect
        else:
            if self.jumpInProg: 
                self.rect = self.rect.move(0, self.curSpeedY) # fixes bug where player gets stuck on wall while mid-jump


        if self.jumpInProg: self.manage_jump()

        # not a good placement but 1 player vs loop 5 enemies each
        # makes it so that when the player is going forward and all enemies are behind him one of them respawns in front for balancing sake
        # additionally, calculates the enemies on each side of the player for the HUD
        allEnemiesBehind = True
        self.numEnemiesToEachSide = [0, 0]

        for enemySprite in self.spritesDict["enemies"]:
            if self.direcion == 1 and enemySprite.rect.left > self.rect.right:
                allEnemiesBehind = False
            if enemySprite.rect.right < self.rect.right:
                self.numEnemiesToEachSide[0] += 1
            else:
                self.numEnemiesToEachSide[1] += 1

        if self.direcion == 1 and allEnemiesBehind:
            for i in range(2):
                self.spritesDict["enemies"][i].respawn(True)


    
    def blit(self):
        self.screen.blit(self.image, self.rect)


    ######################################################################
    # SPECIAL

    def init_jump(self):
        if self.jumpInProg: return
        self.jumpInProg = True
        self.curSpeedY = self.speedY * -1 # needs to go up at first
        self.nextImageTimer.cancel() # no good way to pause/resume the timer, so I just quit it

    def manage_jump(self):
        if self.rect.top <= self.jumpMaxHeight: # jump has reached max height, time to go down
            self.curSpeedY = self.curSpeedY * -1
        elif self.rect.bottom >= globals.DISPLAY_HEIGHT - globals.DIST_FROM_BOTTOM: # has landed
            self.jumpInProg = False
            self.curSpeedY = 0
            self.nextImageTimer = repeattimer.RepeatTimer(self.nextImageTimerDfDelay, self.set_image)
            self.nextImageTimer.daemon = True
            self.nextImageTimer.start()

    def toggle_direction(self):
        self.direcion *= -1
        self.spritesDict["background"][0].speedX *= -1
        self.spritesDict["cross"][0].speedX *= -1

        
    ######################################################################
    # OTHER

    def set_image(self):
        while True:
            try:
                self.image = pygame.image.load(f"./media/images/player/{self.nextImgNum}.gif")
                if self.direcion == -1: self.image = pygame.transform.flip(self.image, True, False)
                break
            except:
                self.nextImgNum = 0

        self.nextImgNum += 1
