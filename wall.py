class Wall():

    ######################################################################
    # CONSTRUCTOR
    
    def __init__(self, x, y, width, height, description):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.description = description

    ######################################################################
    # GETTERS

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height