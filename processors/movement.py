import esper

from components.actor import Actor
from components.position import Position
from components.tile import Tile
from components.velocity import Velocity

class MovementProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (actor, vel, pos) in self.world.get_components(Actor, Velocity, Position):
            
            for ent_tile, (pos_tile, tile) in self.world.get_components(Position, Tile):
                if pos_tile.x == pos.x + vel.dx and pos_tile.y == pos.y + vel.dy and tile.blocks_path:
                    break
            else:
                pos.x += vel.dx
                pos.y += vel.dy

            self.world.remove_component(ent, Velocity)