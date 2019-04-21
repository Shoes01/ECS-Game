import esper

from components.actor.equipment import EquipmentComponent
from components.actor.inventory import InventoryComponent
from components.actor.remove import RemoveComponent
from components.actor.wear import WearComponent
from components.item.slot import SlotComponent
from components.item.wearable import WearableComponent
from components.game.message_log import MessageLogComponent
from components.name import NameComponent
from game import PopupMenu, PopupChoice

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
                
                self.world.popup_menus.append(menu)
                self.world.remove_component(ent, WearComponent)

            else:
                # Wear the item.
                item = self.world.component_for_entity(ent, WearComponent).item_id
                name_component = self.world.component_for_entity(item, NameComponent)
                turn = self.world.turn
                slot_filled_item = None
                

                # Check to see that the entity is not already wearing an item in the slot.
                slot_filled = False
                for worn_item in eqp.equipment:
                    if self.world.component_for_entity(worn_item, SlotComponent).slot == self.world.component_for_entity(item, SlotComponent).slot:
                        slot_filled = True
                        slot_filled_item = worn_item
                        break

                if item in eqp.equipment:
                    # Already worn, so remove it.
                    self.world.remove_component(ent, WearComponent)
                    self.world.add_component(ent, RemoveComponent(item_id=item))
                elif slot_filled:
                    # An item is already in the slot we want; swap the two items.
                    slot = self.world.component_for_entity(item, SlotComponent).slot
                    success = 'slot_filled'
                    self.world.component_for_entity(1, MessageLogComponent).messages.append({'wear': (name_component.name, slot, success, turn)})
                    eqp.equipment.append(item)
                    name_component.name += ' (worn)'
                    self.world.remove_component(ent, WearComponent)
                    self.world.add_component(ent, RemoveComponent(item_id=slot_filled_item))
                elif self.world.has_component(item, WearableComponent):
                    # Wear the item!
                    slot = self.world.component_for_entity(item, SlotComponent).slot
                    success = True
                    self.world.component_for_entity(1, MessageLogComponent).messages.append({'wear': (name_component.name, slot, success, turn)})
                    eqp.equipment.append(item)
                    name_component.name += ' (worn)'
                else:
                    # This is not a wearable item.
                    success = False
                    self.world.component_for_entity(1, MessageLogComponent).messages.append({'wear': (name_component.name, None, success, turn)})
                    self.world.remove_component(ent, WearComponent)