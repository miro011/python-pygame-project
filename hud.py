import globals
import pygame

class Hud():
    ######################################################################
    # CONSTRUCTOR

    def __init__(self, screen, spritesDict):
        self.screen = screen
        self.spritesDict = spritesDict
        self.text = None
        self.rect = None

    ######################################################################
    # OPTIONAL

    def blit(self):
        font = pygame.font.Font('freesansbold.ttf', 16)
        self.text = font.render(self.get_msg(), True, globals.WHITE_COLOR, globals.BLACK_COLOR)
        self.rect = self.text.get_rect()
        self.rect.center = (globals.DISPLAY_WIDTH/2, globals.DISPLAY_HEIGHT - (globals.DIST_FROM_BOTTOM/2))

        self.screen.blit(self.text, self.rect)

    ######################################################################
    # OTHER

    def get_msg(self):
        playerInst = self.spritesDict["player"][0]
        milesLeft = round(globals.DISTANCE_TO_RUN_MILES - (globals.DISTANCE_TO_RUN_MILES * (playerInst.distanceTravelled / globals.DISTANCE_TO_RUN)))
        return f"   REMAINING: {milesLeft} miles          ENEMY DISTRIBUTION: {playerInst.numEnemiesToEachSide[0]}|{playerInst.numEnemiesToEachSide[1]}          ENEMIES KILLED: {playerInst.kills}   "