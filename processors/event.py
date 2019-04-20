import esper

from _helper_functions import load_game, save_game
from components.actor.player import PlayerComponent
from components.game.cursor import CursorComponent
from components.game.end_game import EndGameComponent
from components.game.events import EventsComponent
from components.game.input import InputComponent
from components.game.map import MapComponent
from components.game.message_log import MessageLogComponent
from components.game.popup import PopupComponent
from components.game.state import StateComponent
from components.game.victory import VictoryComponent
from processors.initial import InitialProcessor
from processors.final import FinalProcessor

class EventProcessor(esper.Processor):
    ' The EventProcessor adds and removes Components based on the event. '
    ' This, in turn, will cause the StateProcessor to change the game state. '
    ' It is like the ActionProcessor, but for the user and not the character. '
    def __init__(self):
        super().__init__()
    
    def process(self):
        events_component = self.world.component_for_entity(1, EventsComponent)
        
        while events_component.events:
            event = events_component.events.pop()

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
                self.world.add_component(1, VictoryComponent())

            if _close_popup_menu:
                menus = self.world.component_for_entity(1, PopupComponent).menus
                while len(menus):
                    menus.pop()

            if _exit:
                self.world.add_component(1, EndGameComponent())

            if _key_stroke:
                key = _key_stroke
                self.world.component_for_entity(1, InputComponent).key = key
                self.world.component_for_entity(1, InputComponent).mouse_pos = None

            if _load_game:
                load_game(self.world)
                events_component.events.append({'close_popup_menu': True})
                self.world.component_for_entity(1, MessageLogComponent).messages.append({'game_loaded': True})
            
            if _look:
                x, y = _look
                self.world.add_component(1, CursorComponent(x=x, y=y))

            if _mouse_pos:
                x, y = _mouse_pos
                self.world.component_for_entity(1, InputComponent).mouse_pos = (x, y)
            
            if _move_cursor:
                dx, dy = _move_cursor
                cursor_component = self.world.component_for_entity(1, CursorComponent)
                cursor_component.x += dx
                cursor_component.y += dy

            if _new_map:
                self.world.generate_map = True
                self.world.create_dijkstra_map = True

            if _player_killed:
                self.world.component_for_entity(2, PlayerComponent).killed = True

            if _pop_popup_menu:
                self.world.component_for_entity(1, PopupComponent).menus.pop()

            if _popup:
                self.world.component_for_entity(1, PopupComponent).menus.append(_popup)
            
            if _save_game:
                self.world.component_for_entity(1, MessageLogComponent).messages.append({'game_saved': True})
                save_game(self.world._next_entity_id, self.world._components, self.world._entities)

            if _scroll:
                self.world.component_for_entity(1, MessageLogComponent).offset += _scroll

            if _toggle_debug:
                if self.world.debug_mode:
                    self.world.debug_mode = False
                else:
                    self.world.debug_mode = True
            
            if _view_log:
                self.world.view_log = True