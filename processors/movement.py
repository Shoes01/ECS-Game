import esper

from components.actor.actor import ActorComponent
from components.actor.player import PlayerComponent
from components.item.item import ItemComponent
from components.name import NameComponent
from components.position import PositionComponent
from components.tile import TileComponent
from processors.combat import CombatProcessor
from processors.dijkstra import DijkstraProcessor
from processors.discovery import DiscoveryProcessor
from processors.energy import EnergyProcessor
from processors.render import RenderProcessor
from queue import Queue

class MovementProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']
            move = event['move']
            skill = event.get('skill')
            
            if move is False:
                self.world.get_processor(EnergyProcessor).queue.put({'ent': ent, 'wait': True})
                continue
            
            dx, dy = move
            pos = self.world.component_for_entity(ent, PositionComponent)
            occupying_entity = self.world.get_entities_at(pos.x + dx, pos.y + dy, ActorComponent)
            success = True

            if len(occupying_entity) == 1:
                success = False
                # TODO: Bump attacks are always physical at the moment.
                self.world.get_processor(CombatProcessor).queue.put({'ent': ent, 'defender_IDs': occupying_entity})
            
            if self.world.has_component(ent, PlayerComponent):
                self.world.get_processor(RenderProcessor).queue.put({'recompute_fov': True, 'redraw': True})
                self.world.get_processor(DijkstraProcessor).queue.put({'update_dijkstra': True})

                # Player may run into walls, whereas AI uses the dijkstra map to navigate.
                for ent_tile, (pos_tile, tile) in self.world.get_components(PositionComponent, TileComponent):
                    if pos_tile.x == pos.x + dx and pos_tile.y == pos.y + dy and tile.blocks_path:
                        success = False

                # Custom messages for the player too.
                items = self.world.get_entities_at(pos.x + dx, pos.y + dy, ItemComponent)
                if items:
                    if len(items) == 1:
                        name = self.world.component_for_entity(items.pop(), NameComponent).name
                        self.world.get_processor(DiscoveryProcessor).queue.put({'message': ('move_items', (self.world.turn+1, name, 0))})
                    else:
                        self.world.get_processor(DiscoveryProcessor).queue.put({'message': ('move_items', (self.world.turn+1, None, len(items)))})

            if success:
                pos.x += dx
                pos.y += dy
                
                if not skill:
                    self.world.get_processor(EnergyProcessor).queue.put({'ent': ent, 'move': True})
