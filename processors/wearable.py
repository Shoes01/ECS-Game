import esper

from components.actor.equipment import EquipmentComponent
from components.actor.inventory import InventoryComponent
from components.actor.wear import WearComponent
from components.item.wearable import WearableComponent
from components.game.message_log import MessageLogComponent
from components.game.popup import PopupComponent, PopupMenu, PopupChoice
from components.game.turn_count import TurnCountComponent
from components.name import NameComponent

class WearableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
    
    def process(self):
        for ent, (eqp, wear) in self.world.get_components(EquipmentComponent, WearComponent):

            if wear.item_id is None:
                # Create popup menu for player to choose from.
                menu = PopupMenu(title='Which item would you like to wear or remove?')
                
                n = 97
                for item in self.world.component_for_entity(ent, InventoryComponent).inventory:
                    if not self.world.has_component(item, WearableComponent):
                        continue
                    _name = self.world.component_for_entity(item, NameComponent).name
                    _key = chr(n)
                    _result = {'wear': item}
                    menu.contents.append(PopupChoice(name=_name, key=_key, result=_result))
                    n += 1
                
                self.world.component_for_entity(1, PopupComponent).menus.append(menu)
                self.world.remove_component(ent, WearComponent)

            else:
                # Wear the item.
                item = self.world.component_for_entity(ent, WearComponent).item_id
                if item in eqp.equipment:
                    self.world.component_for_entity(item, NameComponent).name = self.world.component_for_entity(item, NameComponent)._name
                    self.world.component_for_entity(1, MessageLogComponent).messages.append({'wear_already': (self.world.component_for_entity(item, NameComponent).name, self.world.component_for_entity(1, TurnCountComponent).turn_count)})
                    eqp.equipment.remove(item)
                    
                elif self.world.has_component(item, WearableComponent):
                    self.world.component_for_entity(1, MessageLogComponent).messages.append({'wear': (self.world.component_for_entity(item, NameComponent).name, self.world.component_for_entity(1, TurnCountComponent).turn_count)})
                    eqp.equipment.append(item)
                    self.world.component_for_entity(item, NameComponent).name += ' (worn)'
                else:
                    self.world.component_for_entity(1, MessageLogComponent).messages.append({'wear_fail': (self.world.component_for_entity(item, NameComponent).name, self.world.component_for_entity(1, TurnCountComponent).turn_count)})
                    self.world.remove_component(ent, WearComponent)