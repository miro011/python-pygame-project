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

        self.font = pygame.font.Font('freesansbold.ttf', 16)

        self.distanceTravelled = 0 # +60/s (going forward) || Ex: | Target: 120x60=7200 = 10 miles | Calc Remaining: 10 - (10 * (x/7200))
        self.numEnemiesToEachSide = [0, 0] # enemies left of play , enemies right of player
        self.kills = 0

        self.victorySound = pygame.mixer.Sound("./media/sounds/victory.ogg")
        
    ######################################################################
    # OPTIONAL

    def blit(self):
        if (self.distance_update_and_result() == "max reached"): return
        self.update_num_enemies_on_each_side()

        self.update_text_and_rect()
        self.screen.blit(self.text, self.rect)

    ######################################################################
    # SPECIAL

    # returns a value so that the rest of the blit() method, calling this function can be stopped
    def distance_update_and_result(self):
        playerDir = self.spritesDict["player"][0].direction
        self.distanceTravelled = self.distanceTravelled + 1 if playerDir == 1 else self.distanceTravelled - 1

        if self.distanceTravelled >= globals.DISTANCE_TO_RUN:
            pygame.mixer.Sound.play(self.victorySound)
            self.spritesDict["victory_menu"][0].toggle_menu()
            return "max reached"
        
        return ""

    def update_num_enemies_on_each_side(self):
        self.numEnemiesToEachSide = [0, 0]
        playerRect = self.spritesDict["player"][0].rect
        for enemySprite in self.spritesDict["enemies"]:
            if enemySprite.rect.right < playerRect.right:
                self.numEnemiesToEachSide[0] += 1
            else:
                self.numEnemiesToEachSide[1] += 1

    def update_text_and_rect(self):
        self.text = self.font.render(self.get_msg(), True, globals.ORANGE_COLOR, globals.BLACK_COLOR)
        self.rect = self.text.get_rect()
        self.rect.center = (globals.DISPLAY_WIDTH/2, globals.DISPLAY_HEIGHT - (globals.DIST_FROM_BOTTOM/2))

    ######################################################################
    # OTHER

    def get_msg(self):
        milesLeft = round(globals.DISTANCE_TO_RUN_MILES - (globals.DISTANCE_TO_RUN_MILES * (self.distanceTravelled / globals.DISTANCE_TO_RUN)))
        return f"   REMAINING: {milesLeft} miles          ENEMY DISTRIBUTION: {self.numEnemiesToEachSide[0]}|{self.numEnemiesToEachSide[1]}          ENEMIES KILLED: {self.kills}   "