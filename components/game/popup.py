from _data import map

class PopupComponent():
    def __init__(self, title, choices, x=10, y=5, w=map.w-20, h=map.h-10):
        self.title = title
        self.choices = choices
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        """
        Example of how a 'choice' should look:
        choices=[
            (
                'Yes',
                'y',
                {'event': 'Exit'}
            )]
        """