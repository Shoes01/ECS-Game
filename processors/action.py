import esper

from components.turn import Turn
from components.velocity import Velocity

class ActionProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.action = None
    
    def process(self):
        # Look for the entity whose turn it is.
        # Then assign the appropriate component.
        # For example, of action == {'move': (0, -1)}, set the vel.dx and vel.dy.
        _move = self.action.get('move')

        for ent, (turn, vel) in self.world.get_components(Turn, Velocity):
            if _move:
                dx, dy = _move
                vel.dx = dx
                vel.dy = dy
