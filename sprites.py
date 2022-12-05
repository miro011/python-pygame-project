import pygame
import psutil

import globals
import menu
import wall
import background
import player
import enemy

class Sprites():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen):
        self.screen = screen
        self.dict = {}
        self.populate_dict_always()


    # this is run despite of level
    def populate_dict_always(self):

        self.dict["menu"] = []
        self.dict["menu"].append(menu.Menu(self.screen, self.dict, -1))

        self.dict["walls"] = []
        self.dict["walls"].append(wall.Wall(0, 0, 0, globals.DISPLAY_HEIGHT, "vertical left"))
        self.dict["walls"].append(wall.Wall(0, 0, globals.DISPLAY_WIDTH, 0, "horizontal top"))
        self.dict["walls"].append(wall.Wall(globals.DISPLAY_WIDTH, 0, 0, globals.DISPLAY_HEIGHT, "vertical right"))
        self.dict["walls"].append(wall.Wall(0, globals.DISPLAY_HEIGHT, globals.DISPLAY_WIDTH, 0, "horizontal bottom"))

        self.dict["background"] = []
        self.dict["background"].append(background.Background(self.screen))

        self.dict["player"] = []
        self.dict["player"].append(player.Player(self.screen, self.dict))

        self.dict["enemies"] = []
        for i in range(6):
            self.dict["enemies"].append(enemy.Enemy(self.screen, self.dict))

        self.dict["bullets"] = []


    def animate(self):
        #print(f"RAM memory % used: {psutil.virtual_memory()[2]}")
        #print(f"RAM Used (GB): {psutil.virtual_memory()[3]/1000000000}")
        
        eventsQueueArr = pygame.event.get()

        try: # keys are subject to change
            for key in self.dict.keys():
                if key.endswith(".paused"): continue

                for sprite in self.dict[key][:]: # itterate over array and remove items simuntaniously
                    if hasattr(sprite, 'shouldDelete') and sprite.shouldDelete:
                        self.dict[key].remove(sprite) # this removes its reference in self.dict
                        del sprite # this removes the sprite instance itself
                        continue
                    if hasattr(sprite, 'user_input'):
                        sprite.user_input(eventsQueueArr)
                    if hasattr(sprite, 'update_location'):
                        sprite.update_location()
                    if hasattr(sprite, 'blit'):
                        sprite.blit()
        except:
            pass
                
        pygame.display.update()
