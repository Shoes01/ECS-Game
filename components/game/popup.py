from _data import map

class PopupComponent():
    def __init__(self):
        self.menus = [] # type: a list containing (title, choices)
        # title: string
        # choices: name, key, result

        """
        Example of how a 'choice' should look:
        choices=[
            (
                'Yes',
                'y',
                {'event': 'Exit'}
            )]
        """