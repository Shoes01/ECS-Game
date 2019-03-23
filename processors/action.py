import esper

from components.actor.has_turn import HasTurnComponent
from components.action import ActionComponent
from components.player import PlayerComponent
from components.velocity import VelocityComponent
from processors.ai_input import AiInputProcessor

class ActionProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (action, turn) in self.world.get_components(ActionComponent, HasTurnComponent):
            _move = action.action.get('move')
            _wait = action.action.get('wait')

            if _move:
                dx, dy = _move
                self.world.add_component(ent, VelocityComponent(dx=dx, dy=dy))
            
            if _wait:
                pass

            self.world.remove_component(ent, ActionComponent)
            self.world.remove_component(ent, HasTurnComponent)
            
            if self.world.has_component(ent, PlayerComponent):
                self.world.add_processor(AiInputProcessor(), 35)