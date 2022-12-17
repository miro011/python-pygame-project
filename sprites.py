import pygame
import psutil

import menu
import wall
import background
import player
import enemy
import pointer
import helicopter

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
        self.dict["walls"].append(wall.Wall("top"))
        self.dict["walls"].append(wall.Wall("bottom"))
        self.dict["walls"].append(wall.Wall("left"))
        self.dict["walls"].append(wall.Wall("right"))

        self.dict["background"] = []
        self.dict["background"].append(background.Background(self.screen))

        self.dict["helicopter"] = []
        self.dict["helicopter"].append(helicopter.Helicopter(self.screen, self.dict))

        self.dict["player"] = []
        self.dict["player"].append(player.Player(self.screen, self.dict))

        '''self.dict["enemies"] = []
        for i in range(6):
            self.dict["enemies"].append(enemy.Enemy(self.screen, self.dict))'''

        self.dict["bullets"] = []

        self.dict["pointer"] = []
        self.dict["pointer"].append(pointer.Pointer(self.screen, self.dict))


    def animate(self):
        #print(f"RAM memory % used: {psutil.virtual_memory()[2]}")
        #print(f"RAM Used (GB): {psutil.virtual_memory()[3]/1000000000}")
        
        eventsQueueArr = pygame.event.get()

        keysArr = list(self.dict.keys())
        for key in keysArr:
            if key.endswith(".paused"): continue
            if key not in self.dict: break # key no longer there, meaning that menu was toggled and all the other keys were changed as well

            for sprite in self.dict[key][:]: # itterate over array and remove items simuntaniously
                if hasattr(sprite, 'user_input'):
                    sprite.user_input(eventsQueueArr)
                if hasattr(sprite, 'update_location'):
                    sprite.update_location()
                if hasattr(sprite, 'shouldDelete') and sprite.shouldDelete:
                    self.dict[key].remove(sprite) # this removes its reference in self.dict
                    del sprite # this removes the sprite instance itself
                    continue
                if hasattr(sprite, 'blit'):
                    sprite.blit()
                
        pygame.display.update()
