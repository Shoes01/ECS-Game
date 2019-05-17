import esper

from components.actor.player import PlayerComponent
from processors.initial import InitialProcessor
from processors.final import FinalProcessor
from processors.mapgen import MapgenProcessor
from processors.state import StateProcessor
from queue import Queue

class EventProcessor(esper.Processor):
    ' The EventProcessor adds and removes Components based on the event. '
    ' This, in turn, will cause the StateProcessor to change the game state. '
    ' It is like the ActionProcessor, but for the user and not the character. '
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()


        while self.world.events:
            event = self.world.events.pop()

            _close_popup_menu = event.get('close_popup_menu')
            _key_stroke = event.get('key_stroke')
            _load_game = event.get('load_game')
            _look = event.get('look')
            _mouse_pos = event.get('mouse_pos')
            _move_cursor = event.get('move')
            _new_map = event.get('new_map')
            _player_killed = event.get('player_killed')
            _pop_popup_menu = event.get('pop_popup_menu')
            _popup = event.get('popup')
            _save_game = event.get('save_game')
            _scroll = event.get('scroll')
            _toggle_debug = event.get('toggle_debug')        

            if _close_popup_menu:
                menus = self.world.popup_menus
                while len(menus):
                    menus.pop()

            elif _key_stroke:
                key = _key_stroke
                self.world.key = key
                self.world.mouse_pos = None

            elif _load_game:
                self.world.load_game()
                self.world.events.append({'close_popup_menu': True})
                self.world.messages.append({'game_loaded': True})
            
            elif _look:
                x, y = _look
                self.world.cursor.x = x
                self.world.cursor.y = y
                self.world.get_processor(StateProcessor).queue.put({'look': True})

            elif _mouse_pos:
                x, y = _mouse_pos
                self.world.mouse_pos = (x, y)
            
            elif _move_cursor:
                dx, dy = _move_cursor
                self.world.cursor.x += dx
                self.world.cursor.y += dy

            elif _new_map:
                self.world.get_processor(MapgenProcessor).queue.put({'generate_map': True})
                self.world.get_processor(StateProcessor).queue.put({'generate_map': True})

            elif _player_killed:
                self.world.component_for_entity(1, PlayerComponent).killed = True

            elif _pop_popup_menu:
                self.world.popup_menus.pop()

            elif _popup:
                self.world.popup_menus.append(_popup)
            
            elif _save_game:
                self.world.messages.append({'game_saved': True})
                self.world.save_game()

            elif _scroll:
                self.world.messages_offset += _scroll

            elif _toggle_debug:
                self.world.toggle_debug_mode = not self.world.toggle_debug_mode
                