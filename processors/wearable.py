import esper

from components.actor.equipment import EquipmentComponent
from components.actor.inventory import InventoryComponent
from components.item.slot import SlotComponent
from components.item.wearable import WearableComponent
from components.name import NameComponent
from menu import PopupMenu, PopupChoice
from processors.energy import EnergyProcessor
from processors.removable import RemovableProcessor
from processors.state import StateProcessor
from queue import Queue

class WearableProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']
            item = event.get('item')

            eqp = self.world.component_for_entity(ent, EquipmentComponent)

            if not item:
                # Create popup menu for player to choose from.
                menu = PopupMenu(title='Which item would you like to wear or remove?')
                
                n = 97
                for item in self.world.component_for_entity(ent, InventoryComponent).inventory:
                    if not self.world.has_component(item, WearableComponent):
                        continue
                    _name = self.world.component_for_entity(item, NameComponent).name
                    _key = chr(n)
                    _result = {'ent': ent, 'item': item}
                    menu.contents.append(PopupChoice(name=_name, key=_key, result=_result, processor=WearableProcessor))
                    n += 1
                
                self.world.get_processor(StateProcessor).queue.put({'popup': menu})

            else:
                # Wear the item.
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
                    self.world.get_processor(RemovableProcessor).queue.put({'ent': ent, 'item': item})
                elif slot_filled:
                    # An item is already in the slot we want; swap the two items.
                    slot = self.world.component_for_entity(item, SlotComponent).slot
                    success = 'slot_filled'
                    self.world.messages.append({'wear': (name_component.name, slot, success, turn)})
                    eqp.equipment.append(item)
                    name_component.name += ' (worn)'
                    self.world.get_processor(RemovableProcessor).queue.put({'ent': ent, 'item': slot_filled_item})
                elif self.world.has_component(item, WearableComponent):
                    # Wear the item!
                    slot = self.world.component_for_entity(item, SlotComponent).slot
                    success = True
                    self.world.messages.append({'wear': (name_component.name, slot, success, turn)})
                    eqp.equipment.append(item)
                    name_component.name += ' (worn)'
                    self.world.get_processor(EnergyProcessor).queue.put({'ent': ent, 'item': True})
                else:
                    # This is not a wearable item.
                    success = False
                    self.world.messages.append({'wear': (name_component.name, None, success, turn)})