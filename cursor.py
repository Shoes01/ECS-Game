from _data import UI_COLORS

class Cursor():
    def __init__(self):
        self.active = False
        self.char = 'X'
        self.color = UI_COLORS['cursor']
        self.x = 0
        self.y = 0