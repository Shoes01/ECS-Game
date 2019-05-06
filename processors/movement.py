import esper

from components.actor.actor import ActorComponent
from components.actor.combat import CombatComponent
from components.actor.player import PlayerComponent
from components.item.item import ItemComponent
from components.name import NameComponent
from components.position import PositionComponent
from components.tile import TileComponent
from processors.energy import EnergyProcessor
from queue import Queue

class MovementProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']
            dx, dy = event['move']
            
            pos = self.world.component_for_entity(ent, PositionComponent)
            success = True

            occupying_entity = self.world.get_entities_at(pos.x + dx, pos.y + dy, ActorComponent)
            if len(occupying_entity) == 1:
                success = False
                self.world.add_component(ent, CombatComponent(defender_IDs=occupying_entity))
            
            if self.world.has_component(ent, PlayerComponent):
                # Player may run into walls, whereas AI uses the dijkstra map to navigate.
                for ent_tile, (pos_tile, tile) in self.world.get_components(PositionComponent, TileComponent):
                    if pos_tile.x == pos.x + dx and pos_tile.y == pos.y + dy and tile.blocks_path:
                        success = False
                # Custom messages for the player too.
                items = self.world.get_entities_at(pos.x + dx, pos.y + dy, ItemComponent)
                if items:
                    if len(items) == 1:
                        name = self.world.component_for_entity(items.pop(), NameComponent).name
                        self.world.messages.append({'move_items': (self.world.turn, name, 0)})
                    else:
                        self.world.messages.append({'move_items': (self.world.turn, None, len(items))})

            if success:
                pos.x += dx
                pos.y += dy
                self.world.get_processor(EnergyProcessor).queue.put({'ent': ent, 'move': True})
