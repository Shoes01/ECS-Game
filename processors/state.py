import esper

from components.actor.player import PlayerComponent
from components.game.state import StateComponent
from components.game.dijgen import DijgenComponent
from components.game.end_game import EndGameComponent
from components.game.mapgen import MapgenComponent
from components.game.popup import PopupComponent

class StateProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        state_component = self.world.component_for_entity(1, StateComponent)
        
        if state_component.state == 'Exit':
            # This state signals the engine to turn off. There is no coming back.
            pass

        if state_component.state == 'Game':
            if self.world.has_component(1, EndGameComponent):
                # self.world.remove_component(1, EndGameComponent)
                state_component.state = 'MainMenu'
            if self.world.component_for_entity(2, PlayerComponent).killed:
                self.world.remove_component(2, PlayerComponent)
                state_component.state = 'GameOver'
            if self.world.component_for_entity(1, PopupComponent).menus:
                state_component.state = 'PopupMenu'
        
        elif state_component.state == 'GameOver':
            if self.world.has_component(1, EndGameComponent):
                # self.world.remove_component(1, EndGameComponent)
                state_component.state = 'MainMenu'

        elif state_component.state == 'MainMenu':
            if self.world.has_component(1, MapgenComponent):
                self.world.remove_component(1, MapgenComponent)
                state_component.state = 'Game'
            if self.world.has_component(1, EndGameComponent):
                self.world.remove_component(1, EndGameComponent)
                state_component.state = 'Exit'
            
        elif state_component.state == 'PopupMenu':
            if not self.world.component_for_entity(1, PopupComponent).menus:
                state_component.state = 'Game'