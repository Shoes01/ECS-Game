import esper

from components.actor.actor import ActorComponent
from components.actor.combat import CombatComponent
from components.actor.player import PlayerComponent
from components.actor.velocity import VelocityComponent
from components.item.item import ItemComponent
from components.name import NameComponent
from components.position import PositionComponent
from components.tile import TileComponent

class MovementProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (actor, vel, pos) in self.world.get_components(ActorComponent, VelocityComponent, PositionComponent):
            
            occupying_entity = self.world.get_entities_at(pos.x + vel.dx, pos.y + vel.dy, ActorComponent)
            if len(occupying_entity) == 1:
                self.world.remove_component(ent, VelocityComponent)
                self.world.add_component(ent, CombatComponent(defender_ID=occupying_entity.pop()))
            
            if self.world.has_component(ent, PlayerComponent):
                # Player may run into walls, whereas AI uses the dijkstra map to navigate.
                for ent_tile, (pos_tile, tile) in self.world.get_components(PositionComponent, TileComponent):
                    if pos_tile.x == pos.x + vel.dx and pos_tile.y == pos.y + vel.dy and tile.blocks_path:
                        self.world.remove_component(ent, VelocityComponent)
                # Custom messages for the player too.
                items = self.world.get_entities_at(pos.x + vel.dx, pos.y + vel.dy, ItemComponent)
                if items:
                    if len(items) == 1:
                        name = self.world.component_for_entity(items.pop(), NameComponent).name
                        self.world.messages.append({'move_items': (self.world.turn, name, 0)})
                    else:
                        self.world.messages.append({'move_items': (self.world.turn, None, len(items))})

                    

            if self.world.has_component(ent, VelocityComponent):
                pos.x += vel.dx
                pos.y += vel.dy