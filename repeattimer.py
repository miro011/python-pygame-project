from threading import Timer

# https://stackoverflow.com/a/48741004
# Used to regulate the speed of motion images. 
# This timer works in the background (thread) and calls the approriate function every x seconds
# timer = RepeatTimer(intSecs, funcNameToRun)
# timer.start() | timer.cancel()
# ALTERNATIVE: pygame.time.get_ticks
class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)