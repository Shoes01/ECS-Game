import esper

from components.position import Position
from components.velocity import Velocity

class MovementProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (vel, pos) in self.world.get_components(Velocity, Position):
            pos.x += vel.dx
            pos.y += vel.dy

            vel.dx = 0
            vel.dy = 0