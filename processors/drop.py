import esper

from components.actor.drop import DropComponent
from components.actor.equipment import EquipmentComponent
from components.actor.inventory import InventoryComponent
from components.item.pickedup import PickedupComponent
from components.game.popup import PopupComponent
from components.name import NameComponent
from components.position import PositionComponent

class DropProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (drop, eqp, inv, pos) in self.world.get_components(DropComponent, EquipmentComponent, InventoryComponent, PositionComponent):
            
            if drop.item_id is None:
                # Create popup menu for player to choose from.
                title = 'Which item would you like to drop?'
                choices = []
                # Present the player with a list of items.
                n = 97
                for item in self.world.component_for_entity(ent, InventoryComponent).inventory:
                    choices.append(self.generate_choices(chr(n), eqp, item))
                    n += 1
                
                choices.append(('Close menu', 'ESC', {'event': {'pop_popup_menu': True}}))
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
    
    def generate_choices(self, char, eqp, item):
        name = self.world.component_for_entity(item, NameComponent).name
        result = None
        if item in eqp.equipment:
            name += ' (worn)'
            result = {'action': {'wear': item}}
        else:
            result = {'action': {'drop': item}}

        return (name, char, result)