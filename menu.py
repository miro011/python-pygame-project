import pygame
import globals

class Menu():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen, spritesDict, status):
        self.screen = screen
        self.spritesDict = spritesDict
        self.status = status # -1 is off, 1 is on

        # Menu image
        self.image = pygame.image.load("./media/images/menu-background.jpg")
        self.rect = self.image.get_rect()

        # Menu text
        self.textLineObjsArr = self.generate_multiline_text_elems("[1] Resume\n\n[2] Quit")

    ######################################################################
    # OPTIONAL

    def user_input(self, eventsQueueArr):
        for event in eventsQueueArr:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE: self.toggle_menu()
                elif self.status == 1 and event.key == pygame.K_1: self.toggle_menu()
                elif self.status == 1 and event.key == pygame.K_2: pygame.quit()

    def blit(self):
        self.screen.blit(self.image, self.rect)
        for textLineObj in self.textLineObjsArr: self.screen.blit(textLineObj["text"], textLineObj["rect"])

    ######################################################################
    # SPECIAL

    # return an array of text lines: [{text:textElem, rect:rectElem}...]
    def generate_multiline_text_elems(self, textStr):
        output = []

        font = pygame.font.Font('freesansbold.ttf', 32)
        textLinesArr = textStr.split("\n")

        # used to get the height, so we can calculate and center mutliple lines
        sampleTextElem = font.render(textLinesArr[0], True, globals.GREEN_COLOR, globals.BLUE_COLOR)
        sampleTextRect = sampleTextElem.get_rect()
        
        lineHeight = sampleTextRect.height
        overallHeight = lineHeight * len(textLinesArr)

        curElemYCenter = (((globals.DISPLAY_HEIGHT - overallHeight) / 2) + (lineHeight / 2)) # starting with the ones on the top

        for i in range(len(textLinesArr)):
            textElem = font.render(textLinesArr[i], True, globals.GREEN_COLOR, globals.BLUE_COLOR)
            textRect = textElem.get_rect()
            textRect.center = (globals.DISPLAY_WIDTH / 2, curElemYCenter) # set the center of the rectangular object
            output.append({"text":textElem, "rect":textRect})
            curElemYCenter += lineHeight

        return output

    def toggle_menu(self):
        self.status *= -1

        keysArr = list(self.spritesDict.keys()) # for some odd reason python keeps updating it when I change keys, and I need this to be static
        for key in keysArr:
            if key == "menu": continue
            newKey = f"{key}.paused" if self.status == 1 else key[:-7]
            self.spritesDict[newKey] = self.spritesDict[key]
            del self.spritesDict[key]