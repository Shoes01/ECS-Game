import esper

from components.position import Position
from components.velocity import Velocity

class MovementProcessor(esper.Processor):
    def __init__(self, tiles):
        super().__init__()
        self.tiles = tiles
    
    def process(self):
        for ent, (vel, pos) in self.world.get_components(Velocity, Position):
            if not self.tiles['blocks_path'][pos.x + vel.dx, pos.y + vel.dy]:
                pos.x += vel.dx
                pos.y += vel.dy

            vel.dx = 0
            vel.dy = 0