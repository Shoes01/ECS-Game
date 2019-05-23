import esper

from components.actor.equipment import EquipmentComponent
from components.actor.inventory import InventoryComponent
from components.name import NameComponent
from components.persist import PersistComponent
from components.position import PositionComponent
from menu import PopupMenu, PopupChoice
from processors.energy import EnergyProcessor
from processors.state import StateProcessor
from processors.wearable import WearableProcessor
from queue import Queue

class DropProcessor(esper.Processor):
    def __init__(self):
        super().__init__()
        self.queue = Queue()
    
    def process(self):
        while not self.queue.empty():
            event = self.queue.get()

            ent = event['ent']
            item = event['item']

            eqp = self.world.component_for_entity(ent, EquipmentComponent)
            inv = self.world.component_for_entity(ent, InventoryComponent)
            pos = self.world.component_for_entity(ent, PositionComponent)
            
            if item is True:
                # Create popup menu for player to choose from.
                menu = PopupMenu(title='Which item would you like to drop?')
                
                n = 97
                for item in inv.inventory:
                    _name = self.world.component_for_entity(item, NameComponent).name
                    _key = chr(n)
                    _result = {'item': item}
                    _processor = None
                    if item in eqp.equipment:
                        _processor = WearableProcessor
                    else:
                        _processor = DropProcessor
                    menu.contents.append(PopupChoice(name=_name, key=_key, result=_result, processor=_processor))
                    n += 1
                
                self.world.get_processor(StateProcessor).queue.put({'popup': menu})
            
            else:
                # Remove the item from the player.
                inv.inventory.remove(item)
                self.world.remove_component(item, PersistComponent)
                
                # Return the item to the map.
                item_pos = self.world.add_component(item, PositionComponent(x=pos.x, y=pos.y))

                self.world.get_processor(EnergyProcessor).queue.put({'ent': ent, 'drop': True})
                self.world.messages.append({'drop': (self.world.component_for_entity(item, NameComponent).name, self.world.turn)})