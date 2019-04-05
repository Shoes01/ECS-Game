import esper

from components.actor.player import PlayerComponent
from components.game.debug import DebugComponent
from components.game.dijgen import DijgenComponent
from components.game.event import EventComponent
from components.game.exit import ExitGameComponent
from components.game.map import MapComponent
from components.game.mapgen import MapgenComponent
from components.game.popup import PopupComponent
from components.game.end_game import EndGameComponent
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
        if self.world.has_component(1, EventComponent):
            event = self.world.component_for_entity(1, EventComponent).event
            state = self.world.component_for_entity(1, StateComponent).state

            _cancel = event.get('cancel')
            _exit = event.get('exit')
            _new_map = event.get('new_map')
            _player_killed = event.get('player_killed')
            _popup_menu = event.get('popup_menu')
            _toggle_debug = event.get('toggle_debug')

            if _toggle_debug:
                if self.world.has_component(1, DebugComponent):
                    self.world.remove_component(1, DebugComponent)
                else:
                    self.world.add_component(1, DebugComponent())
            
            if _cancel and self.world.has_component(1, PopupComponent):
                self.world.remove_component(1, PopupComponent)

            if state == 'MainMenu':                
                if _exit:
                    self.world.add_component(1, ExitGameComponent())
                if _new_map:
                    self.world.add_component(1, MapgenComponent())
                    self.world.add_component(1, DijgenComponent())
            
            if state == 'Game':
                if _exit:
                    self.world.add_component(1, EndGameComponent())
                if _player_killed:
                    self.world.component_for_entity(2, PlayerComponent).killed = True
                if _popup_menu:
                    self.world.add_component(1, _popup_menu)

            if state == 'GameOver':
                if _exit:
                    self.world.add_component(1, EndGameComponent())
            
            self.world.remove_component(1, EventComponent)