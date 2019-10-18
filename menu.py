from _data import map

class PopupChoiceCondition():
    ' This is a single condition to a popup menu choice. '
    def __init__(self, description, valid=True):
        self.description = description
        self.valid = valid

class PopupChoice():
    ' This is a single entry into the popup menu. '
    def __init__(self, name, key, result, processor, valid=True, description="", upkeep=None, conditions=[]):
        self.conditions = conditions # type: list of PopupChoiceConditions
        self.description = description
        self.name = name     # The name of the choice.
        self.key = key       # The key to select this choice.
        self.processor = processor # The processor that the results will be fed into.
        self.result = result # type: dict
        self._valid = valid   # If this is False, then the option is greyed out (at the moment, it can still be selected).

    @property
    def valid(self):
        if len(self.conditions) == 0:
            return True if self._valid else False
        else:
            for condition in self.conditions:
                if condition.valid is False:
                    return False
            else:
                return True
        
class PopupMenu():
    ' This contains the input and render information for a popup menu. '
    def __init__(self, title, contents=None, include_esc=True, x=10, y=5, w=map.w-20, h=map.h-10, auto_close=True):
        self.title = title
        self.contents = [] # type: list of PopupChoices
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.auto_close = auto_close # If True, all menus will be closed upon selecting a choice.
        self.include_esc = include_esc # If True, a choice to close the menu will be printed at the bottom of the menu.

        ### Additional information that could be added later:
        # Subtitle
        # Definition panel (in the case of items)
        # Category bool: if set to true, the renderer will sort items by their type. (items don't have a type yet)
        # Equipped bool: if set to true, the equipped items will be listed on the side?