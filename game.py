import os
import shelve
import world

from _data import map, UI_COLORS

class GameWorld(world.CustomWorld):
    def __init__(self):
        super().__init__()
        ' Flags. ' 
        self.create_dijkstra_map = False
        self.generate_map = False
        self.pop_state = False
        self.reset_game = False
        self.victory = False
        self.view_log = False
        
        ' Data. '
        self.debug_mode = False # This one is a toggle
        self.events = []
        self.key = None
        self.messages = []
        self.messages_offset = 0
        self.mouse_pos = None
        self.popup_menus = []
        self.redraw = False # This information needs to communicate cross-tick
        self.state_stack = ['Exit', 'MainMenu']
        self.ticker = 0

        ' Objects. '
        self.consoles = None
        self.cursor = Cursor()
        self.map = Map()

    @property
    def state(self):
        return self.state_stack[-1]
    
    @property
    def turn(self):
        return self.ticker // 10
        
    def load_game(self):
        if not os.path.isfile('savegame.dat'):
            state = self.state

            if state is not 'MainMenu':
                message = 'There is no save file to load.'
                self.messages.append({'error': message})
            return 0

        with shelve.open('savegame', 'r') as data_file:
            self.consoles = data_file['consoles']
            self.map = data_file['map']
            self.messages = data_file['log']
            self.state_stack = data_file['state']
            self.ticker = data_file['ticker']
            self._components = data_file['components']
            self._entities = data_file['entities']
            self._next_entity_id = data_file['next_entity_id']
            
    def save_game(self):
        with shelve.open('savegame', 'n') as data_file:
            data_file['consoles'] = self.consoles
            data_file['map'] = self.map
            data_file['log'] = self.messages
            data_file['state'] = self.state_stack
            data_file['ticker'] = self.ticker
            data_file['components'] = self._components
            data_file['entities'] = self._entities
            data_file['next_entity_id'] = self._next_entity_id
            
    def reset_flags(self):
        self.create_dijkstra_map = False
        self.generate_map = False
        self.pop_state = False
        self.reset_game = False
        self.victory = False
        self.view_log = False

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