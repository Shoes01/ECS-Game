import attr
import esper

from _data import map
from typing import Any, Dict, List

@attr.s(slots=True, auto_attribs=True)
class PopupChoiceCondition:
    ' This is a single condition to a popup menu choice. '
    description: str = ""
    valid: bool = True

@attr.s(slots=True, auto_attribs=True, kw_only=True)
class PopupChoiceResult():
    ' This is the result of making a menu choice. '
    result: Dict[str, int] = attr.Factory(dict) # entity name, entity ID.
    processor: esper.Processor # Could also put Any here if this doesn't work.

@attr.s(slots=True, auto_attribs=True, kw_only=True)
class PopupChoice():
    ' This is a single entry into the popup menu. '
    conditions: List[PopupChoiceCondition] = attr.Factory(list)
    description: str = ""
    key: str # The key to select this choice.
    name: str
    results: List[PopupChoiceResult] = attr.Factory(list)

    @property
    def valid(self):
        for condition in self.conditions:
            if condition.valid is False:
                return False
        else:
            return True

@attr.s(slots=True, auto_attribs=True, kw_only=True)
class PopupMenu():
    ' This contains the input and render information for a popup menu. '
    title: str
    contents: List[PopupChoice] = attr.Factory(list)
    x: int = 10
    y: int = 5
    w: int = map.w - 20
    h: int = map.h - 10
    auto_close: bool = True # If True, all menus will be closed upon selecting a choice.
    include_description: Any = None # What is this? "Is it dict = Dict[str, int] # entity name, entity ID?
    include_esc: bool = True # If True, a choice to close the menu will be printed at the bottom of the menu.
    reveal_all: bool = True # If this is False, then invalid options are shown as ???s.
    
    ### Additional information that could be added later:
    # Subtitle
    # Category bool: if set to true, the renderer will sort items by their type. (items don't have a type yet)
    # Equipped bool: if set to true, the equipped items will be listed on the side?