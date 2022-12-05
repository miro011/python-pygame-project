import pygame
import globals

class Menu():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, screen, spritesDict, status):
        self.screen = screen
        self.spritesDict = spritesDict
        self.status = status # -1 = off, 1 = on

        # Menu image
        self.image = pygame.image.load("./media/images/menu-background.png")
        self.x = 0
        self.y = 0

        # Menu text
        '''
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = "1.Resume\n2.Quit"
        self.text = font.render('1.Resume\n2.Quit', True, globals.GREEN_COLOR, globals.BLUE_COLOR)
        self.textRect = self.text.get_rect() # create a rectangular object for the text
        self.textRect.center = (globals.DISPLAY_WIDTH / 2, globals.DISPLAY_HEIGHT / 2) # set the center of the rectangular object
        '''
        self.textLineElemsArr = self.generate_multiline_text_elems("1.Resume\n2.Quit")

    ######################################################################
    # OPTIONAL

    def user_input(self, eventsQueueArr):
        for event in eventsQueueArr:
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE: self.toggle_menu()
                elif event.key == pygame.K_1: self.toggle_menu()
                elif event.key == pygame.K_2: pygame.quit()

    def blit(self):
        self.screen.blit(self.image, (self.x, self.y))
        #self.screen.blit(self.text, self.textRect) # have to blit the text after the image for it be on top
        for textElem in self.textLineElemsArr: self.screen.blit(textElem[0], textElem[1])

    ######################################################################
    # SPECIAL

    # return an array of text lines: [[textElem1, textRect1], [textElem2, textRect2]...]
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
            output.append([textElem, textRect])
            curElemYCenter += lineHeight

        return output

    def toggle_menu(self):
        self.status = self.status * -1

        for key in self.spritesDict.keys():
            if key == "menu": continue
            newKey = ""
            if self.status == 1: newKey = f"{key}.paused"
            elif key.endswith(".paused"): newKey = key[:-7]
            self.spritesDict[newKey] = self.spritesDict[key]
            del self.spritesDict[key]