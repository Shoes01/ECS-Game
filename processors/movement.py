import esper

from components.actor.actor import ActorComponent
from components.position import PositionComponent
from components.tile import TileComponent
from components.velocity import VelocityComponent

class MovementProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (actor, vel, pos) in self.world.get_components(ActorComponent, VelocityComponent, PositionComponent):
            
            for ent_blocker, (pos_blocker) in self.world.get_component(PositionComponent):
                if pos_blocker.x == pos.x + vel.dx and pos_blocker.y == pos.y + vel.dy:
                    if self.world.has_component(ent_blocker, ActorComponent) or (self.world.has_component(ent_blocker, TileComponent) and self.world.component_for_entity(ent_blocker, TileComponent).blocks_path):
                        break
            else:
                pos.x += vel.dx
                pos.y += vel.dy

            self.world.remove_component(ent, VelocityComponent)