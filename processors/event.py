import esper

from components.actor.player import PlayerComponent
from processors.initial import InitialProcessor
from processors.final import FinalProcessor
from processors.mapgen import MapgenProcessor
from processors.state import StateProcessor
from menu import PopupMenu, PopupChoice, PopupChoiceResult
from queue import Queue

class EventProcessor(esper.Processor):
    ' The EventProcessor adds and removes Components based on the event. '
    ' This, in turn, will cause the StateProcessor to change the game state. '
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            _close_popup_menu = event.get('close_popup_menu')
            _key_stroke = event.get('key_stroke')
            _load_game = event.get('load_game')
            _look = event.get('look')
            _mouse_pos = event.get('mouse_pos')
            _move_cursor = event.get('move')
            _open_main_menu = event.get('open_main_menu')
            _pop_popup_menu = event.get('pop_popup_menu')
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
                self.world.get_processor(StateProcessor).queue.put({'pop': True})
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

            elif _open_main_menu:
                menu = PopupMenu(title='What would you like to do?')
                menu.contents.append(PopupChoice(
                    name='Load game', 
                    key='l', 
                    results=(PopupChoiceResult(
                        result={'load_game': True}, processor=EventProcessor),)))
                menu.contents.append(PopupChoice(
                    name='Quit', 
                    key='q', 
                    results=(PopupChoiceResult(
                        result={'exit': True}, processor=StateProcessor),)))
                menu.contents.append(PopupChoice(
                    name='Save game', 
                    key='s', 
                    results=(PopupChoiceResult(
                        result={'save_game': True}, processor=EventProcessor),)))
                self.world.get_processor(StateProcessor).queue.put({'popup': menu})

            elif _pop_popup_menu:
                self.world.popup_menus.pop()
            
            elif _save_game:
                self.world.messages.append({'game_saved': True})
                self.world.save_game()

            elif _scroll:
                self.world.messages_offset += _scroll

            elif _toggle_debug:
                self.world.toggle_debug_mode = not self.world.toggle_debug_mode
                