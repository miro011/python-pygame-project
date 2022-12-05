######################################################################
# VARIABLES

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

WHITE_COLOR=(255, 255, 255)
YELLOW_COLOR=(255, 255, 0)
GREEN_COLOR=(0, 255, 255)
ORANGE_COLOR=(255, 100, 0)
BLUE_COLOR = (0, 0, 128)

######################################################################
# FUNCTIONS

# spritesToTestAgainstArr can either be a single sprite or an array of similar sprites (ex. enemies, walls etc.)
# returns an array of sprites, spriteToTest collided with
def collision(spriteToTest, spritesToTestAgainstArr):
    
    def outside_range_fixer(num, max): # adjust values to be within the range of the window (so calculations work)
        if num < 0: num = 0
        elif num > max: num = max
        return num

    def generate_xy_dict(sprite): # returns: [xMin:num, xMax:num, yMin:num, yMax:num]
        return {
            "xMin": outside_range_fixer(sprite.x, DISPLAY_WIDTH),
            "xMax": outside_range_fixer(sprite.x + sprite.get_width(), DISPLAY_WIDTH),
            "yMin": outside_range_fixer(sprite.y, DISPLAY_HEIGHT),
            "yMax": outside_range_fixer(sprite.y + sprite.get_height(), DISPLAY_HEIGHT)
        }

    collidedWithArr = [] # output
    if type(spritesToTestAgainstArr) != list: spritesToTestAgainstArr = [spritesToTestAgainstArr]
    xy = generate_xy_dict(spriteToTest)

    for spriteToTestAgainst in spritesToTestAgainstArr:
        tXy = generate_xy_dict(spriteToTestAgainst)
        xMatch = yMatch = False

        for x in [xy["xMin"], xy["xMax"]]:
            if x >= tXy["xMin"] and x <= tXy["xMax"]:
                xMatch = True
        for y in [xy["yMin"], xy["yMax"]]:
            if y >= tXy["yMin"] and y <= tXy["yMax"]:
                yMatch = True

        if xMatch and yMatch:
            collidedWithArr.append(spriteToTestAgainst)
    
    return collidedWithArr