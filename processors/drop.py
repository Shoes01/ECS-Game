import esper

from components.actor.drop import DropComponent
from components.actor.inventory import InventoryComponent
from components.item.pickedup import PickedupComponent
from components.game.popup import PopupComponent
from components.name import NameComponent
from components.position import PositionComponent

class DropProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (drop, inv, pos) in self.world.get_components(DropComponent, InventoryComponent, PositionComponent):
            
            if drop.item_id is None:
                # Create popup menu for player to choose from.
                title = 'Which item would you like to drop?'
                choices = []
                # Present the player with a list of items.
                n = 97
                for item in self.world.component_for_entity(ent, InventoryComponent).inventory:
                    name = self.world.component_for_entity(item, NameComponent).name
                    char = chr(n)
                    result = {'action': {'drop': item}}
                    choices.append((name, char, result))
                    n += 1
                
                choices.append(('Nevermind', 'ESC', {'event': {'cancel': True}}))
                popup_component = self.world.component_for_entity(1, PopupComponent).menus.append( (title, choices) )
                self.world.add_component(1, popup_component)
                self.world.remove_component(ent, DropComponent)
            
            else:
                item = drop.item_id

                # Remove the item from the player.
                self.world.component_for_entity(ent, InventoryComponent).inventory.remove(item)
                
                # Remove the player from the item.
                self.world.remove_component(item, PickedupComponent)
                item_pos = self.world.component_for_entity(item, PositionComponent)
                item_pos.x, item_pos.y = pos.x, pos.y