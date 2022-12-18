DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 640

REFRESH_DELAY_S = 0.016666667 # 60FPS

WHITE_COLOR=(255, 255, 255)
YELLOW_COLOR=(255, 255, 0)
GREEN_COLOR=(0, 255, 255)
ORANGE_COLOR=(255, 100, 0)
BLUE_COLOR = (0, 0, 128)

DIST_FROM_BOTTOM = 40 # used so that I can put a HUD on the bottom (player, enemies etc.)

ENEMY_SPLIT_CHANCE = 50 # 50% chance that when an enemy is killed, 2 additional once will be spawned
# if ENEMY_SPLIT_CHANCE = 70%
#randomint(0,100)
#if 0-70 => spawn