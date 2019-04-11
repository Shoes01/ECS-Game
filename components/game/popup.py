from _data import map

"""
The PopupComponent is always attached to the game entity.
When it is not empty, the popup menu rendering subprocessor displays it, and the input processor accepts input for it.

The PopupComponent contains a list of PopupMenus. 
The PopupMenu contains basic information, as well as a list of PopupChoices.
"""

class PopupChoice():
    ' This is a single entry into the popup menu. '
    def __init__(self, name, key, result, action=True, valid=True):
        self.name = name     # The name of the choice.
        self.key = key       # The key to select this choice.
        self.action = action # If it is False, then this choice is an event.
        self.result = result # type: dict
        self.valid = valid   # If this is False, then the option is greyed out (at the moment, it can still be selected).
        
class PopupMenu():
    ' This contains the input and render information for a popup menu. '
    def __init__(self, title, contents=[], include_esc=True, x=10, y=5, w=map.w-20, h=map.h-10):
        self.title = title
        self.contents = contents # type: list of PopupChoices
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.include_esc = include_esc # If True, a choice to close the menu will be printed at the bottom of the menu.

        ### Additional information that could be added later:
        # Subtitle
        # Definition panel (in the case of items)
        # Category bool: if set to true, the renderer will sort items by their type. (items don't have a type yet)
        # Equipped bool: if set to true, the equipped items will be listed on the side?

class PopupComponent():
    def __init__(self):
        self.menus = [] # type: list of PopupMenus
