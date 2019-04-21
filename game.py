import world

from _data import map, UI_COLORS

class GameWorld(world.CustomWorld):
    def __init__(self):
        super().__init__()
        self.create_dijkstra_map = False
        self.debug_mode = False
        self.events = []
        self.generate_map = False
        self.key = None
        self.messages = []
        self.messages_offset = 0
        self.mouse_pos = None
        self.pop_state = False
        self.popup_menus = []
        self.redraw = False
        self.reset_game = False
        self.state_stack = ['Exit', 'MainMenu']
        self.ticker = 0
        self.victory = False
        self.view_log = False
        
        self.cursor = Cursor()
        self.map = Map()

    @property
    def state(self):
        return self.state_stack[-1]
    
    @property
    def turn(self):
        return self.ticker // 10

class Cursor():
    def __init__(self):
        self.active = False
        self.char = 'X'
        self.color = UI_COLORS['cursor']
        self.x = 0
        self.y = 0

class Map():
    def __init__(self):
        self.height = map.h
        self.dijkstra_map = None
        self.directory = None
        self.fov_map = None
        self.tiles = None
        self.width = map.w
        self.floor = 0
        
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