from _data import UI_COLORS

class CursorComponent:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.char = 'X'
        self.color = UI_COLORS['cursor']