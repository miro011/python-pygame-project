import pygame
import globals

class Player():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen, spritesDict):
        self.screen = screen
        self.spritesDict = spritesDict
        
        self.image = None
        self.rect = None

        self.nextImgNum = 0
        self.set_image()

        self.nextImageTimer = globals.RepeatTimer(0.05, self.set_image)
        self.nextImageTimer.start()


    ######################################################################
    # OPTIONAL
        
    def user_input(self, eventsQueueArr):
        for event in eventsQueueArr:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == "RIGHT":
                self.jump()


    def update_location(self):
        return
    
    def blit(self):
        self.screen.blit(self.image, self.rect)


    ######################################################################
    # SPECIAL

    def set_image(self):
        while True:
            try:
                self.image = pygame.image.load(f"./media/images/player/{self.nextImgNum}.gif")
                break
            except:
                self.nextImgNum = 0

        self.nextImgNum += 1

        self.rect = self.image.get_rect()
        self.rect.move_ip(100, (globals.DISPLAY_HEIGHT-self.image.get_height())-40)


    def jump(self):
        return