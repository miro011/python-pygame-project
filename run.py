import pygame
import globals
import sprites
import time

#################################################################

pygame.init()
screen = pygame.display.set_mode((globals.DISPLAY_WIDTH, globals.DISPLAY_HEIGHT)) 
pygame.display.set_caption("THE CURSED FOREST")
pygame.mouse.set_visible(False)

pygame.mixer.music.load("./media/sounds/background.ogg")
pygame.mixer.music.play(loops=-1)

sprites = sprites.Sprites(screen)

while 1==1:
    sprites.animate()
    time.sleep(globals.REFRESH_DELAY_S)