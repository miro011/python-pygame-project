import pygame
import globals

# must be declared after "drone"

class Player():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen, regulator, spritesDict):
        self.screen = screen
        self.regulator = regulator
        self.spritesDict = spritesDict
        
        self.image = pygame.image.load(f"./media/images/player/0.gif")
        self.rect = self.image.get_rect()
        self.rect.center = (globals.DISPLAY_WIDTH/2, globals.DISPLAY_HEIGHT - (self.image.get_height()/2) - globals.DIST_FROM_BOTTOM)

        self.nextImgNum = 0
        self.nextImageTimerDfDelay = 0.05
        self.nextImageTimer = self.regulator.get_new_repeat_timer(self.nextImageTimerDfDelay, self.set_image)

        self.speedX = 8
        self.speedY = 15 # jump duration

        self.curSpeedX = 0
        self.curSpeedY = 0

        self.jumpInProg = False
        self.jumpMaxHeight = self.spritesDict["drone"][0].rect.bottom

        self.direction = 1 # 1 = forward / -1 = backward


    ######################################################################
    # OPTIONAL
        
    def user_input(self, eventsQueueArr):
        for event in eventsQueueArr:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.curSpeedX = self.speedX
                if event.key == pygame.K_LEFT:
                    self.curSpeedX = self.speedX * -1
                if event.key == pygame.K_UP:
                    self.init_jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    self.curSpeedX = 0
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3: # 1-left 2-middle, 3-right, 4-scrollup, 5-scrolldown
                    self.toggle_direction()

        # make the animation faster/slower
        if self.curSpeedX == 0:
            self.nextImageTimer.interval = self.nextImageTimerDfDelay
        else:
            if (self.direction == 1 and self.curSpeedX > 0) or (self.direction == -1 and self.curSpeedX < 0):
                self.nextImageTimer.interval = self.nextImageTimerDfDelay / 1.5 # the lower the delay, the faster the animation
            elif (self.direction == 1 and self.curSpeedX < 0) or (self.direction == -1 and self.curSpeedX > 0):
                self.nextImageTimer.interval = self.nextImageTimerDfDelay * 1.5



    def update_location(self):
        newRect = self.rect.move(self.curSpeedX, self.curSpeedY)
        if newRect.collidelist(self.spritesDict["walls"]) == -1:
            self.rect = newRect
        else:
            if self.jumpInProg: 
                self.rect = self.rect.move(0, self.curSpeedY) # fixes bug where player gets stuck on a wall while mid-jump


        if self.jumpInProg: self.manage_jump()

        self.regulator.all_enemies_behind_fixer()


    
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
            self.nextImageTimer = self.regulator.get_new_repeat_timer(self.nextImageTimerDfDelay, self.set_image)

    def toggle_direction(self):
        self.direction *= -1
        self.spritesDict["background"][0].speedX *= -1

        
    ######################################################################
    # OTHER

    def set_image(self):
        while True:
            try:
                self.image = pygame.image.load(f"./media/images/player/{self.nextImgNum}.gif")
                if self.direction == -1: self.image = pygame.transform.flip(self.image, True, False)
                break
            except:
                self.nextImgNum = 0

        self.nextImgNum += 1
