from _data import map

class PopupChoiceCondition():
    ' This is a single condition to a popup menu choice. '
    def __init__(self, description, valid=True):
        self.description = description
        self.valid = valid

class PopupChoiceResult():
    ' This is the result of making a menu choice. '
    def __init__(self, result, processor):
        self.result = result
        self.processor = processor

class PopupChoice():
    ' This is a single entry into the popup menu. '
    def __init__(self, name, key, results, valid=True, description=None, conditions=None):
        self.conditions = [] if conditions is None else conditions # type: list of PopupChoiceConditions
        self.description = "" if description is None else description
        self.name = name     # The name of the choice.
        self.key = key       # The key to select this choice.
        self.results = results # type: list of PopupMenuResults
        self._valid = valid   # If this is False, then the option is greyed out (at the moment, it can still be selected).

    @property
    def valid(self):
        if len(self.conditions) == 0:
            return self._valid
        else:
            for condition in self.conditions:
                if condition.valid is False:
                    return False
            else:
                return True
        
class PopupMenu():
    ' This contains the input and render information for a popup menu. '
    def __init__(self, title, contents=None, include_esc=True, x=10, y=5, w=map.w-20, h=map.h-10, auto_close=True, include_description=None, reveal_all=True):
        self.title = title
        self.contents = [] # type: list of PopupChoices
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        
        self.auto_close = auto_close # If True, all menus will be closed upon selecting a choice.
        self.include_description = include_description # If not None, it will include all the ingredients necessary to form a description.
        self.include_esc = include_esc # If True, a choice to close the menu will be printed at the bottom of the menu.
        self.reveal_all = reveal_all # If this is False, then invalid options are shown as ???s.
        
        ### Additional information that could be added later:
        # Subtitle
        # Category bool: if set to true, the renderer will sort items by their type. (items don't have a type yet)
        # Equipped bool: if set to true, the equipped items will be listed on the side?