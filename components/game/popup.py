from _data import map

class PopupComponent():
    def __init__(self):
        self.menus = [] # type: a list containing (title, choices)

        """
        Example of how a 'choice' should look:
        choices=[
            (
                'Yes',
                'y',
                {'event': 'Exit'}
            )]
        """