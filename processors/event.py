import esper

from _helper_functions import load_game, save_game
from components.actor.player import PlayerComponent
from components.game.debug import DebugComponent
from components.game.dijgen import DijgenComponent
from components.game.end_game import EndGameComponent
from components.game.events import EventsComponent
from components.game.map import MapComponent
from components.game.mapgen import MapgenComponent
from components.game.popup import PopupComponent
from components.game.state import StateComponent
from processors.initial import InitialProcessor
from processors.final import FinalProcessor

class EventProcessor(esper.Processor):
    ' The EventProcessor adds and removes Components based on the event. '
    ' This, in turn, will cause the StateProcessor to change the game state. '
    ' It is like the ActionProcessor, but for the user and not the character. '
    def __init__(self):
        super().__init__()
    
    def process(self):
        if self.world.has_component(1, EventsComponent):
            events = self.world.component_for_entity(1, EventsComponent).events
            state = self.world.component_for_entity(1, StateComponent).state

            for event in events:
                _close_popup_menu = event.get('close_popup_menu')
                _exit = event.get('exit')
                _load_game = event.get('load_game')
                _new_map = event.get('new_map')
                _player_killed = event.get('player_killed')
                _popup = event.get('popup')
                _save_game = event.get('save_game')
                _toggle_debug = event.get('toggle_debug')


                if _close_popup_menu:
                    self.world.component_for_entity(1, PopupComponent).menus.pop()

                if _exit:
                    self.world.add_component(1, EndGameComponent())

                if _load_game:
                    load_game(self.world)

                if _new_map:
                    self.world.add_component(1, MapgenComponent())
                    self.world.add_component(1, DijgenComponent())

                if _player_killed:
                    self.world.component_for_entity(2, PlayerComponent).killed = True

                if _popup:
                    self.world.component_for_entity(1, PopupComponent).menus.append(_popup)
                
                if _save_game:
                    save_game(self.world._next_entity_id, self.world._components, self.world._entities)

                if _toggle_debug:
                    if self.world.has_component(1, DebugComponent):
                        self.world.remove_component(1, DebugComponent)
                    else:
                        self.world.add_component(1, DebugComponent())
            
            self.world.remove_component(1, EventsComponent)