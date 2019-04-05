import esper

from _helper_functions import tile_occupied
from components.actor.actor import ActorComponent
from components.actor.combat import CombatComponent
from components.actor.player import PlayerComponent
from components.actor.player_input import PlayerInputComponent
from components.actor.velocity import VelocityComponent
from components.position import PositionComponent
from components.tile import TileComponent

class MovementProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (actor, vel, pos) in self.world.get_components(ActorComponent, VelocityComponent, PositionComponent):
            
            occupying_entity = tile_occupied(self.world, pos.x + vel.dx, pos.y + vel.dy)
            if occupying_entity:
                self.world.remove_component(ent, VelocityComponent)
                self.world.add_component(ent, CombatComponent(defender_ID=occupying_entity))
            
            if self.world.has_component(ent, PlayerComponent):
                # Player may run into walls, whereas AI uses the dijkstra map to navigate.
                for ent_tile, (pos_tile, tile) in self.world.get_components(PositionComponent, TileComponent):
                    if pos_tile.x == pos.x + vel.dx and pos_tile.y == pos.y + vel.dy and tile.blocks_path:
                        self.world.remove_component(ent, VelocityComponent)

            if self.world.has_component(ent, VelocityComponent):
                pos.x += vel.dx
                pos.y += vel.dy