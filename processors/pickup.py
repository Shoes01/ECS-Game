import esper

from components.actor.inventory import InventoryComponent
from components.actor.pickup import PickupComponent
from components.game.popup import PopupComponent, PopupMenu, PopupChoice
from components.item.item import ItemComponent
from components.item.pickedup import PickedupComponent
from components.name import NameComponent
from components.position import PositionComponent

class PickupProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (inv, pick, pos) in self.world.get_components(InventoryComponent, PickupComponent, PositionComponent):

            if pick.item_id is None:
                matched_items = []

                for item_ent, (item, item_pos) in self.world.get_components(ItemComponent, PositionComponent):
                    if pos.x == item_pos.x and pos.y == item_pos.y:
                        matched_items.append(item_ent)
                
                if len(matched_items) == 0:
                    self.world.remove_component(ent, PickupComponent)

                elif len(matched_items) == 1:
                    item_id = matched_items.pop()
                    inv.inventory.append(item_id)
                    self.world.add_component(item_id, PickedupComponent())
                    item_pos = self.world.component_for_entity(item_id, PositionComponent)
                    item_pos.x, item_pos.y = -1, -1
                
                elif len(matched_items) > 1:
                    # Create popup menu for player to choose from.
                    menu = PopupMenu(title='Which item do you want to pick up?')
                    
                    n = 97
                    for item in matched_items:
                        _name = self.world.component_for_entity(item, NameComponent).name
                        _keu = chr(n)
                        _result = {'pick_up': item}
                        menu.contents.append(PopupChoice(name=_name, key=_key, result=_result)
                        n += 1

                    self.world.component_for_entity(1, PopupComponent).menus.append(menu)
                    self.world.remove_component(ent, PickupComponent)

            else:
                inv.inventory.append(pick.item_id)
                self.world.add_component(pick.item_id, PickedupComponent())
                item_pos = self.world.component_for_entity(pick.item_id, PositionComponent)
                item_pos.x, item_pos.y = -1, -1

            
