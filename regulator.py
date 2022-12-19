import pygame
import random

import globals
import repeattimer
import enemy

# this is a class designated to do things and hold variables that don't logically belong to sprite classes
# declare before everything else in spritesDict

class Regulator():

    ######################################################################
    # CONSTRUCTOR

    def __init__(self, screen, spritesDict):
        self.screen = screen
        self.spritesDict = spritesDict

    ######################################################################
    # BACKGROUND RELATED

    # return the x coordinates for both backgrounds in a sorted array
    def get_backgrounds_sorted_x_coords(self):
        arr = []
        for rect in self.spritesDict["background"][0].rectsArr:
            arr.append(rect.left)
            arr.append(rect.right)
        arr.sort()
        return arr

    ######################################################################
    # ENEMY RELATED

    def kill_all_enemies(self):
        for enemySprite in self.spritesDict["enemies"]:
            enemySprite.nextImageTimer.cancel()
            enemySprite.shouldDelete = True

    def spawn_df_num_enemies(self):
        for i in range(globals.ENEMY_DF_NUMBER):
            self.spritesDict["enemies"].append(enemy.Enemy(self.screen, self, self.spritesDict))

    # makes it so that when the player is going forward and has managed to get all enemies behind him though acrobatic, TWO of them respawn in front for balancing sake
    # this test is ran in the player instance for performance sake (1 player vs however many enemies, each doing this loop)
    def all_enemies_behind_fixer(self):
        if self.spritesDict["player"][0].direction != 1: return

        allEnemiesBehind = True

        for enemySprite in self.spritesDict["enemies"]:
            if enemySprite.rect.left > self.spritesDict["player"][0].rect.right:
                allEnemiesBehind = False
                break

        if allEnemiesBehind:
            for i in range(2):
                self.spritesDict["enemies"][i].respawn(True)


    ######################################################################
    # GENERAL

    def get_new_repeat_timer(self, delay, funcToRun):
        rt = repeattimer.RepeatTimer(delay, funcToRun)
        rt.daemon = True # will be terminated abruptly by the Python process once all other non-daemon threads are finished (in this case none). Otherwise it hangs.
        rt.start()
        return rt

    # returns true or false - it relates to the name of whatever variable is plugged into "percentValue"
    # for example: chanceToDie = 70 . If this function retruns true it means "yes, you will die"
    def calculate_chancery(self, percentValue):
        # have to do this because it seems it will generate more small numbers when it is 1,100
        percentValue = int(percentValue/10)
        result = random.randint(0, 10)
        return True if 0 <= result <= percentValue else False

    def cancel_all_timers(self):
        self.spritesDict["player"][0].nextImageTimer.cancel()
        self.spritesDict["drone"][0].nextImageTimer.cancel()
        for enemySprite in self.spritesDict["enemies"]: enemySprite.nextImageTimer.cancel()

    # no need to worry about canceling timers or deleting anything - it's done automatically
    def quit_the_game(self):
        pygame.quit()
        raise SystemExit(0)