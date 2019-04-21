import esper

from _helper_functions import load_game, save_game
from components.actor.player import PlayerComponent
from processors.initial import InitialProcessor
from processors.final import FinalProcessor

class EventProcessor(esper.Processor):
    ' The EventProcessor adds and removes Components based on the event. '
    ' This, in turn, will cause the StateProcessor to change the game state. '
    ' It is like the ActionProcessor, but for the user and not the character. '
    def __init__(self):
        super().__init__()
    
    def process(self):
        while self.world.events:
            event = self.world.events.pop()

            _boss_killed = event.get('boss_killed')
            _close_popup_menu = event.get('close_popup_menu')
            _exit = event.get('exit')
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
            _view_log = event.get('view_log')

            if _boss_killed:
                self.world.victory = True

            if _close_popup_menu:
                menus = self.world.popup_menus
                while len(menus):
                    menus.pop()

            if _exit:
                self.world.pop_state = True

            if _key_stroke:
                key = _key_stroke
                self.world.key = key
                self.world.mouse_pos = None

            if _load_game:
                load_game(self.world)
                self.world.events.append({'close_popup_menu': True})
                self.world.messages.append({'game_loaded': True})
            
            if _look:
                x, y = _look
                self.world.cursor.active = True
                self.world.cursor.x = x
                self.world.cursor.y = y

            if _mouse_pos:
                x, y = _mouse_pos
                self.world.mouse_pos = (x, y)
            
            if _move_cursor:
                dx, dy = _move_cursor
                self.world.cursor.x += dx
                self.world.cursor.y += dy

            if _new_map:
                self.world.generate_map = True
                self.world.create_dijkstra_map = True

            if _player_killed:
                self.world.component_for_entity(2, PlayerComponent).killed = True

            if _pop_popup_menu:
                self.world.popup_menus.pop()

            if _popup:
                self.world.popup_menus.append(_popup)
            
            if _save_game:
                self.world.messages.append({'game_saved': True})
                save_game(self.world._next_entity_id, self.world._components, self.world._entities)

            if _scroll:
                self.world.messages_offset += _scroll

            if _toggle_debug:
                if self.world.debug_mode:
                    self.world.debug_mode = False
                else:
                    self.world.debug_mode = True
            
            if _view_log:
                self.world.view_log = True