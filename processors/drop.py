import esper

from components.actor.drop import DropComponent
from components.actor.inventory import InventoryComponent
from components.position import PositionComponent
from components.item.pickedup import PickedupComponent

class DropProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (drop, inv, pos) in self.world.get_components(DropComponent, InventoryComponent, PositionComponent):
            item = drop.item_id

            # Remove the item from the player.
            self.world.component_for_entity(ent, InventoryComponent).inventory.remove(item)
            
            # Remove the player from the item.
            self.world.remove_component(item, PickedupComponent)
            item_pos = self.world.component_for_entity(item, PositionComponent)
            item_pos.x, item_pos.y = pos.x, pos.y
