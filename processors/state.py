import esper

from components.game.level import LevelComponent
from components.game.state import StateComponent
from processors.render import RenderProcessor

class StateProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        game_state_component = self.world.component_for_entity(1, StateComponent)

        if self.world.has_component(1, LevelComponent):
            game_state_component.state = 'Game'
            self.world.remove_component(1, LevelComponent)