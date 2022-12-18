import pygame
import globals

class Menu():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, spritesInst, menuType):
        self.spritesInst = spritesInst
        self.screen = self.spritesInst.screen

        self.status = -1 # -1 is off, 1 is on
        self.menuType = menuType

        menuImgName = "menu-background-welcome" if self.menuType == "welcome" else "menu-background"
        self.image = pygame.image.load(f"./media/images/{menuImgName}.jpg")
        self.rect = self.image.get_rect()

        textStr = None
        if self.menuType == "welcome": textStr = "[1] PLAY"
        elif self.menuType == "pause": textStr = "PAUSED\n\n\n[1] resume\n\n[2] quit"
        elif self.menuType == "over": textStr = "GAME OVER\n\n\n[1] try again\n\n[2] quit"
        elif self.menuType == "victory": textStr = "CONGRATULATIONS, YOU MANAGED TO ESCAPE!!!\n\n\n[1] play again\n\n[2] quit"
        self.textLineObjsArr = self.generate_multiline_text_elems(textStr)

    ######################################################################
    # OPTIONAL

    def user_input(self, eventsQueueArr):
        for event in eventsQueueArr:
            if event.type == pygame.KEYUP:
                if self.menuType == "welcome":
                    if self.status == 1 and event.key == pygame.K_1:
                        self.status = -1
                        self.spritesInst.load_dict()
                elif self.menuType == "pause":
                    if event.key == pygame.K_ESCAPE or (self.status == 1 and event.key == pygame.K_1):
                        self.toggle_menu()
                    elif self.status == 1 and event.key == pygame.K_2:
                        self.quit_the_game()
                elif self.menuType == "over" or self.menuType == "victory":
                    if self.status == 1 and event.key == pygame.K_1:
                        self.status = -1
                        self.spritesInst.load_dict()
                    elif self.status == 1 and event.key == pygame.K_2:
                        self.quit_the_game()

    def blit(self):
        if self.status != 1: return
        self.screen.blit(self.image, self.rect)
        for textLineObj in self.textLineObjsArr: self.screen.blit(textLineObj["text"], textLineObj["rect"])

    
    ######################################################################
    # SPECIAL

    def toggle_menu(self):
        self.status *= -1

        keysArr = list(self.spritesInst.dict.keys()) # for some odd reason python keeps updating it when I change keys, and I need this to be static
        for key in keysArr:
            if key == f"{self.menuType}_menu": continue
            newKey = f"{key}.paused" if self.status == 1 else key[:-7]
            self.spritesInst.dict[newKey] = self.spritesInst.dict[key]
            del self.spritesInst.dict[key]


    ######################################################################
    # OTHER

    # return an array of text lines: [{text:textElem, rect:rectElem}...]
    def generate_multiline_text_elems(self, textStr):
        output = []

        font = pygame.font.Font('freesansbold.ttf', 32)
        textLinesArr = textStr.split("\n")

        # used to get the height, so we can calculate and center mutliple lines
        sampleTextElem = font.render(textLinesArr[0], True, globals.RED_COLOR)
        sampleTextRect = sampleTextElem.get_rect()
        
        lineHeight = sampleTextRect.height
        overallHeight = lineHeight * len(textLinesArr)

        curElemYCenter = (((globals.DISPLAY_HEIGHT - overallHeight) / 2) + (lineHeight / 2)) # starting with the ones on the top

        for i in range(len(textLinesArr)):
            textElem = font.render(textLinesArr[i], True, globals.RED_COLOR)
            textRect = textElem.get_rect()
            textRect.center = (globals.DISPLAY_WIDTH / 2, curElemYCenter) # set the center of the rectangular object
            output.append({"text":textElem, "rect":textRect})
            curElemYCenter += lineHeight

        return output

    def quit_the_game(self):
        pygame.quit()
        raise SystemExit(0)