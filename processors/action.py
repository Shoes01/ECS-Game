import esper

from components.action import Action
from components.player import Player
from components.turn import Turn
from components.velocity import Velocity

class ActionProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (action, turn, vel) in self.world.get_components(Action, Turn, Velocity):
            _move = action.value.get('move')

            if _move:
                dx, dy = _move
                vel.dx = dx
                vel.dy = dy

            self.world.remove_component(ent, Action)
