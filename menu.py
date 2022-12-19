import pygame
import globals

class Menu():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, spritesInst, menuType):
        self.spritesInst = spritesInst
        self.screen = self.spritesInst.screen
        self.regulator = self.spritesInst.regulator

        self.status = -1 # -1 is off, 1 is on
        self.menuType = menuType

        self.bgImage = pygame.image.load(f"./media/images/{self.get_menu_img_name()}.jpg")
        self.bgRect = self.bgImage.get_rect()

        self.textStr = None
        self.textColor = None
        self.textBgColor = None
        self.set_per_menu_attrs()

        self.font = pygame.font.Font('freesansbold.ttf', 32)

        self.textLineObjsArr = self.generate_multiline_text_elems()

    ######################################################################
    # OPTIONAL

    def user_input(self, eventsQueueArr):
        for event in eventsQueueArr:
            if event.type == pygame.KEYUP:
                if self.menuType == "welcome":
                    if self.status == 1 and event.key == pygame.K_1:
                        self.toggle_menu()
                elif self.menuType == "pause":
                    if event.key == pygame.K_ESCAPE or (self.status == 1 and event.key == pygame.K_1):
                        self.toggle_menu()
                    elif self.status == 1 and event.key == pygame.K_2:
                        self.regulator.quit_the_game()
                elif self.menuType == "over" or self.menuType == "victory":
                    if self.status == 1 and event.key == pygame.K_1:
                        self.status = -1
                        del self.spritesInst.dict[f"{self.menuType}_menu"]
                        self.spritesInst.load_dict()
                    elif self.status == 1 and event.key == pygame.K_2:
                        self.regulator.quit_the_game()

    def blit(self):
        if self.status != 1: return
        self.screen.blit(self.bgImage, self.bgRect)
        for textLineObj in self.textLineObjsArr: self.screen.blit(textLineObj["text"], textLineObj["rect"])

    
    ######################################################################
    # SPECIAL

    # change the status and change the keys (aka pause) everything in spritesDict, except the menu "this" instance represents, and the regulator
    def toggle_menu(self):
        self.status *= -1

        keysArr = list(self.spritesInst.dict.keys()) # for some odd reason python keeps updating it when I change keys, and I need this to be static

        if self.menuType in ["over", "victory"]:
            self.regulator.cancel_all_timers()
            for key in keysArr:
                if key != f"{self.menuType}_menu":
                    del self.spritesInst.dict[key]
        else:
            for key in keysArr:
                if key == f"{self.menuType}_menu": continue
                newKey = f"{key}.paused" if self.status == 1 else key[:-7]
                self.spritesInst.dict[newKey] = self.spritesInst.dict[key]
                del self.spritesInst.dict[key]


    ######################################################################
    # OTHER

    def get_menu_img_name(self):
        return "menu-background-welcome" if self.menuType == "welcome" else "menu-background"

    def set_per_menu_attrs(self):
        if self.menuType == "welcome":
            self.textStr = "[1] PLAY"
            self.textColor = globals.RED_COLOR
            self.textBgColor = globals.BLACK_COLOR
        elif self.menuType == "pause":
            self.textStr = "PAUSED\n\n\n[1] resume\n\n[2] quit"
            self.textColor = globals.WHITE_COLOR
        elif self.menuType == "over":
            self.textStr = "GAME OVER\n\n\n[1] try again\n\n[2] quit"
            self.textColor = globals.RED_COLOR
        elif self.menuType == "victory":
            self.textStr = "CONGRATULATIONS, YOU MANAGED TO ESCAPE!!!\n\n\n[1] play again\n\n[2] quit"
            self.textColor = globals.GREEN_COLOR

    # returns an array dicts, representing a text and rect elements for each line: [{text:textElem, rect:rectElem}...]
    def generate_multiline_text_elems(self):
        output = []
        textLinesArr = self.textStr.split("\n")
        lineHeight = overallHeight = curElemYCenter = None

        for i in range(len(textLinesArr)):
            textElem = self.font.render(textLinesArr[i], True, self.textColor, self.textBgColor)
            textRect = textElem.get_rect()

            if not lineHeight:
                lineHeight = textRect.height
                overallHeight = lineHeight * len(textLinesArr)
                curElemYCenter = (((globals.DISPLAY_HEIGHT - overallHeight) / 2) + (lineHeight / 2)) # starting with the ones on the top

            textRect.center = (globals.DISPLAY_WIDTH / 2, curElemYCenter) # set the center of the rectangular object
            output.append({"text":textElem, "rect":textRect})
            curElemYCenter += lineHeight

        return output