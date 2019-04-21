import esper

from components.actor.inventory import InventoryComponent
from components.actor.pickup import PickupComponent
from components.game.message_log import MessageLogComponent
from components.item.item import ItemComponent
from components.item.pickedup import PickedupComponent
from components.name import NameComponent
from components.persist import PersistComponent
from components.position import PositionComponent
from game import PopupMenu, PopupChoice

class PickupProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (inv, pick, pos) in self.world.get_components(InventoryComponent, PickupComponent, PositionComponent):
            turn = self.world.turn

            if pick.item_id is None:
                matched_items = []

                for item_ent, (item, item_pos) in self.world.get_components(ItemComponent, PositionComponent):
                    if pos.x == item_pos.x and pos.y == item_pos.y:
                        matched_items.append(item_ent)
                
                if len(matched_items) == 0:
                    self.world.component_for_entity(1, MessageLogComponent).messages.append({'pickup': (None, False, turn)})
                    self.world.remove_component(ent, PickupComponent)

                elif len(matched_items) == 1:
                    self.pick_up(matched_items.pop(), inv, turn)
                
                elif len(matched_items) > 1:
                    # Create popup menu for player to choose from.
                    menu = PopupMenu(title='Which item do you want to pick up?')
                    
                    n = 97
                    for item in matched_items:
                        _name = self.world.component_for_entity(item, NameComponent).name
                        _key = chr(n)
                        _result = {'pick_up': item}
                        menu.contents.append(PopupChoice(name=_name, key=_key, result=_result))
                        n += 1

                    self.world.popup_menus.append(menu)
                    self.world.remove_component(ent, PickupComponent)

            else:
                self.pick_up(pick.item_id, inv, turn)
    
    def pick_up(self, item, inv_component, turn):
        # Attach item to player.
        inv_component.inventory.append(item)
        self.world.add_component(item, PersistComponent())

        # Remove the item from the map.
        self.world.add_component(item, PickedupComponent())
        item_pos = self.world.component_for_entity(item, PositionComponent)
        item_pos.x, item_pos.y = -1, -1

        self.world.component_for_entity(1, MessageLogComponent).messages.append({'pickup': (self.world.component_for_entity(item, NameComponent).name, True, turn)})
