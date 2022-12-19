import pygame
import globals
import random
import enemy

# must be declared after "player" and "background" in spritesDict

class Cross():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen, regulator, spritesDict):
        self.screen = screen
        self.regulator = regulator
        self.spritesDict = spritesDict
        
        self.image = pygame.image.load("./media/images/cross.png")
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.get_starting_xy_coords())
        
        self.speedX = self.spritesDict["background"][0].speedX
        self.speedY = 0

        self.shouldDelete = False

        self.heavenSound = pygame.mixer.Sound("./media/sounds/heaven.ogg")

    ######################################################################
    # OPTIONAL

    def update_location(self):
        self.speedX = self.spritesDict["background"][0].speedX

        self.rect = self.rect.move(self.speedX, self.speedY)

        stillOnBackground = True if self.rect.collidelist(self.spritesDict["background"][0].rectsArr) >= 0 else False
        collidedWithPlayer = True if self.rect.collidelist(self.spritesDict["player"]) >= 0 else False

        if collidedWithPlayer:
            pygame.mixer.Sound.play(self.heavenSound)
            pygame.mixer.Sound.play(self.spritesDict["enemies"][0].teleportSound)
            self.regulator.kill_all_enemies()
            self.regulator.spawn_df_num_enemies()
            self.respawn()
        if not stillOnBackground:
            self.respawn()
            

    def blit(self):
        self.screen.blit(self.image, self.rect)

    ######################################################################
    # OTHER

    # returns the leftXCoord and topYCoord in an array
    def get_starting_xy_coords(self):
        bgSortedXCoords = self.regulator.get_backgrounds_sorted_x_coords()
        leftXCoord = bgSortedXCoords[0] if self.spritesDict["background"][0].speedX > 0 else bgSortedXCoords[-1] - self.image.get_width()
        topYCoord = random.randint(
            self.spritesDict["player"][0].jumpMaxHeight, 
            globals.DISPLAY_HEIGHT - globals.DIST_FROM_BOTTOM - self.image.get_height()
        )
        return [leftXCoord, topYCoord]

    def respawn(self):
        self.shouldDelete = True
        self.spritesDict["cross"].append(Cross(self.screen, self.regulator, self.spritesDict))