import esper

from components.game.level import LevelComponent
from components.game.state import StateComponent
from processors.render import RenderProcessor

class StateProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        game_state = self.world.component_for_entity(1, StateComponent).state

        if self.world.try_component(1, LevelComponent()):
            game_state = 'Game'