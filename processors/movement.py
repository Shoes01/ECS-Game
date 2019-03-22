import esper

from components.actor.actor import ActorComponent
from components.player import PlayerComponent
from components.position import PositionComponent
from components.tile import TileComponent
from components.velocity import VelocityComponent

class MovementProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (actor, vel, pos) in self.world.get_components(ActorComponent, VelocityComponent, PositionComponent):
            
            for ent_blocker, (actor, pos_blocker) in self.world.get_components(ActorComponent, PositionComponent):
                if pos_blocker.x == pos.x + vel.dx and pos_blocker.y == pos.y + vel.dy:
                    return
        
            if self.world.has_component(ent, PlayerComponent):
                # Player may run into walls, whereas AI uses the dijkstra map to navigate.
                for ent_tile, (pos_tile, tile) in self.world.get_components(PositionComponent, TileComponent):
                    if pos_tile.x == pos.x + vel.dx and pos_tile.y == pos.y + vel.dy and tile.blocks_path:
                        return

            pos.x += vel.dx
            pos.y += vel.dy

            self.world.remove_component(ent, VelocityComponent)