import esper

from components.game.mapgen import MapgenComponent
from components.game.state import StateComponent
from processors.render import RenderProcessor

class StateProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        game_state_component = self.world.component_for_entity(1, StateComponent)

        if self.world.has_component(1, MapgenComponent):
            game_state_component.state = 'Game'