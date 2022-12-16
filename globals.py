from threading import Timer

######################################################################
# VARIABLES

DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 640

REFRESH_DELAY_S = 0.01667 # 60FPS = 16.67ms

WHITE_COLOR=(255, 255, 255)
YELLOW_COLOR=(255, 255, 0)
GREEN_COLOR=(0, 255, 255)
ORANGE_COLOR=(255, 100, 0)
BLUE_COLOR = (0, 0, 128)

# https://stackoverflow.com/a/48741004
# Used to regulate the speed of motion images. 
# This timer works in the background (thread) and calls the approriate function every x seconds
# timer = RepeatTimer(intSecs, funcNameToRun)
# timer.start() | timer.cancel()
# timer.cancel()
# ALTERNATIVE: pygame.time.get_ticks
class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)