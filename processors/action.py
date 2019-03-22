import esper

from components.action import ActionComponent
from components.player import PlayerComponent
from components.turn import TurnComponent
from components.velocity import VelocityComponent

class ActionProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (action, turn) in self.world.get_components(ActionComponent, TurnComponent):
            _move = action.value.get('move')

            if _move:
                dx, dy = _move
                self.world.add_component(ent, VelocityComponent(dx=dx, dy=dy))

            self.world.remove_component(ent, ActionComponent)
