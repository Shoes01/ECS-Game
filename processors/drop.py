import esper

from components.actor.drop import DropComponent
from components.actor.equipment import EquipmentComponent
from components.actor.inventory import InventoryComponent
from components.item.pickedup import PickedupComponent
from components.game.message_log import MessageLogComponent
from components.game.popup import PopupComponent, PopupMenu, PopupChoice
from components.game.turn_count import TurnCountComponent
from components.name import NameComponent
from components.persist import PersistComponent
from components.position import PositionComponent

class DropProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (drop, eqp, inv, pos) in self.world.get_components(DropComponent, EquipmentComponent, InventoryComponent, PositionComponent):
            
            if drop.item_id is None:
                # Create popup menu for player to choose from.
                menu = PopupMenu(title='Which item would you like to drop?')
                
                n = 97
                for item in inv.inventory:
                    _name = self.world.component_for_entity(item, NameComponent).name
                    _key = chr(n)
                    _result = None
                    if item in eqp.equipment:
                        _result = {'action': {'wear': item}}
                    else:
                        _result = {'action': {'drop': item}}
                    menu.contents.append(PopupChoice(name=_name, key=_key, result=_result))
                    n += 1
                
                self.world.component_for_entity(1, PopupComponent).menus.append(menu)
                self.world.remove_component(ent, DropComponent)
            
            else:
                item = drop.item_id

                # Remove the item from the player.
                inv.inventory.remove(item)
                self.world.remove_component(item, PersistComponent)
                
                # Return the item to the map.
                self.world.remove_component(item, PickedupComponent)
                item_pos = self.world.component_for_entity(item, PositionComponent)
                item_pos.x, item_pos.y = pos.x, pos.y

                self.world.component_for_entity(1, MessageLogComponent).messages.append({'drop': (self.world.component_for_entity(item, NameComponent).name, self.world.component_for_entity(1, TurnCountComponent).turn_count)})