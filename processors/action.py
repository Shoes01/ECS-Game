import esper

from components.action import Action
from components.player import Player
from components.turn import Turn
from components.velocity import Velocity

class ActionProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (action, turn) in self.world.get_components(Action, Turn):
            _move = action.value.get('move')

            if _move:
                dx, dy = _move
                self.world.add_component(ent, Velocity(dx=dx, dy=dy))

            self.world.remove_component(ent, Action)
