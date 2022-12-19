import pygame
import repeattimer
import bullet

class Drone():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen, regulator, spritesDict):
        self.screen = screen
        self.regulator = regulator
        self.spritesDict = spritesDict

        self.nextImgNum = 0
        self.image = pygame.image.load(f"./media/images/drone/{self.nextImgNum}.gif")
        self.rect = self.image.get_rect()

        self.nextImageTimer = self.regulator.get_new_repeat_timer(0.07, self.set_image)

        self.isShooting = False

        self.shootSound = pygame.mixer.Sound("./media/sounds/shoot.ogg")
        self.droneSound = pygame.mixer.Sound("./media/sounds/drone.ogg")
        self.droneSoundChannel = None

    ######################################################################
    # OPTIONAL

    def user_input(self, eventsQueueArr):
        for event in eventsQueueArr:
            if event.type == pygame.MOUSEBUTTONUP:
                if not self.isShooting and event.button == 1: # 1-left 2-middle, 3-right, 4-scrollup, 5-scrolldown
                    self.shoot()

    def update_location(self):
        self.drone_sound_handler()
        newRect = self.rect.copy()
        newRect.center = (self.spritesDict["player"][0].rect.center[0], self.image.get_height()/2)
        if newRect.collidelist(self.spritesDict["walls"]) == -1:
            self.rect = newRect

    def blit(self):
        self.screen.blit(self.image, self.rect)

    
    ######################################################################
    # SPECIAL

    def shoot(self):
        pygame.mixer.Sound.play(self.shootSound)
        self.isShooting = True
        self.spritesDict["bullets"].append(bullet.Bullet(self.screen, self.spritesDict))

    ######################################################################
    # OTHER

    def set_image(self):
        while True:
            try:
                self.image = pygame.image.load(f"./media/images/drone/{self.nextImgNum}.gif")
                break
            except:
                self.nextImgNum = 0

        self.nextImgNum += 1

    def drone_sound_handler(self):
        if not self.droneSoundChannel or not self.droneSoundChannel.get_busy():
            self.droneSoundChannel = self.droneSound.play()