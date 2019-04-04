from _data import con

class PopupComponent():
    def __init__(self, title, choices, x=5, y=5, w=con.w-5, h=con.h-5):
        self.title = title
        self.choices = choices
        self.x = x
        self.y = y
        self.w = w
        self.h = h